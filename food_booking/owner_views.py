from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
import logging
from datetime import datetime, timedelta
from .models import FoodItem, Order, OrderItem
from .forms import FoodItemForm
import json



# Set up logging for security events
logger = logging.getLogger(__name__)


def is_owner(user):
    """Check if user is an owner/admin - enhanced security"""
    # Must be authenticated, active, and staff
    return (user.is_authenticated and
            user.is_active and
            user.is_staff and
            user.is_superuser)  # Only superusers can access owner features


def owner_access_denied(request):
    """Custom 403 handler for owner access denied"""
    # Log unauthorized access attempts
    if request.user.is_authenticated:
        logger.warning(f'Unauthorized access attempt to owner area by user: {request.user.username} (ID: {request.user.id})')
    else:
        logger.warning('Unauthorized access attempt to owner area by anonymous user')

    return HttpResponseForbidden(
        '<h1>Access Denied</h1>'
        '<p>You do not have permission to access this area.</p>'
        '<p><a href="/">Return to Menu</a></p>'
    )


@login_required
@user_passes_test(is_owner)
def owner_dashboard(request):
    """Owner dashboard with overview statistics"""

    # Additional security check
    if not is_owner(request.user):
        messages.error(request, 'Access denied. You do not have permission to view this area.')
        return redirect('food_booking:menu')

    # Get date range for filtering
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Today's statistics
    today_orders = Order.objects.filter(created_at__date=today)
    today_revenue = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    today_count = today_orders.count()

    # This week's statistics
    week_orders = Order.objects.filter(created_at__date__gte=week_ago)
    week_revenue = week_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    week_count = week_orders.count()

    # This month's statistics
    month_orders = Order.objects.filter(created_at__date__gte=month_ago)
    month_revenue = month_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    month_count = month_orders.count()

    # Payment method breakdown
    payment_stats = Order.objects.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('total_amount')
    ).order_by('-total')

    # Recent orders
    recent_orders = Order.objects.select_related().order_by('-created_at')[:10]

    # Popular food items
    popular_items = OrderItem.objects.values('food_item__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')[:5]

    # Pending orders count
    pending_orders = Order.objects.filter(payment_status='PENDING').count()

    context = {
        'today_revenue': today_revenue,
        'today_count': today_count,
        'week_revenue': week_revenue,
        'week_count': week_count,
        'month_revenue': month_revenue,
        'month_count': month_count,
        'payment_stats': payment_stats,
        'recent_orders': recent_orders,
        'popular_items': popular_items,
        'pending_orders': pending_orders,
    }

    return render(request, 'food_booking/owner/dashboard.html', context)


@login_required
@user_passes_test(is_owner)
def owner_orders(request):
    """Manage all orders"""

    # Get filter parameters
    status_filter = request.GET.get('status', '')
    payment_filter = request.GET.get('payment', '')
    date_filter = request.GET.get('date', '')
    search_query = request.GET.get('search', '')

    # Base queryset
    orders = Order.objects.select_related().prefetch_related('orderitem_set__food_item')

    # Apply filters
    if status_filter:
        orders = orders.filter(payment_status=status_filter)

    if payment_filter:
        orders = orders.filter(payment_method=payment_filter)

    if date_filter:
        if date_filter == 'today':
            orders = orders.filter(created_at__date=timezone.now().date())
        elif date_filter == 'week':
            week_ago = timezone.now().date() - timedelta(days=7)
            orders = orders.filter(created_at__date__gte=week_ago)
        elif date_filter == 'month':
            month_ago = timezone.now().date() - timedelta(days=30)
            orders = orders.filter(created_at__date__gte=month_ago)

    if search_query:
        orders = orders.filter(
            Q(customer_name__icontains=search_query) |
            Q(seat_number__icontains=search_query) |
            Q(mobile_number__icontains=search_query)
        )

    # Order by creation date
    orders = orders.order_by('-created_at')

    # Pagination (simple version)
    page_size = 20
    page = int(request.GET.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size

    total_orders = orders.count()
    total_pages = (total_orders + page_size - 1) // page_size

    orders_page = orders[start:end]

    context = {
        'orders': orders_page,
        'total_orders': total_orders,
        'current_page': page,
        'total_pages': total_pages,
        'status_filter': status_filter,
        'payment_filter': payment_filter,
        'date_filter': date_filter,
        'search_query': search_query,
        'payment_methods': Order.PAYMENT_METHOD_CHOICES,
        'payment_statuses': Order.PAYMENT_STATUS_CHOICES,
    }

    return render(request, 'food_booking/owner/orders.html', context)


@login_required
@user_passes_test(is_owner)
def owner_order_detail(request, order_id):
    """View detailed order information"""

    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.select_related('food_item').all()

    if request.method == 'POST':
        # Update payment status
        new_status = request.POST.get('payment_status')
        if new_status in dict(Order.PAYMENT_STATUS_CHOICES):
            order.payment_status = new_status
            order.save()
            messages.success(request, f'Payment status updated to {order.get_payment_status_display()}')
            return redirect('food_booking:owner_order_detail', order_id=order.id)

    context = {
        'order': order,
        'order_items': order_items,
        'payment_statuses': Order.PAYMENT_STATUS_CHOICES,
    }

    return render(request, 'food_booking/owner/order_detail.html', context)


@login_required
@user_passes_test(is_owner)
def owner_food_items(request):
    """Manage food items"""

    food_items = FoodItem.objects.all().order_by('name')

    if request.method == 'POST':
        # Handle food item updates
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        if item_id and action:
            try:
                item = FoodItem.objects.get(id=item_id)

                if action == 'toggle_availability':
                    item.available = not item.available
                    item.save()
                    status = 'available' if item.available else 'unavailable'
                    messages.success(request, f'{item.name} is now {status}')

                elif action == 'delete':
                    item_name = item.name
                    item.delete()
                    messages.success(request, f'{item_name} has been deleted')

            except FoodItem.DoesNotExist:
                messages.error(request, 'Food item not found')

    context = {
        'food_items': food_items,
    }

    return render(request, 'food_booking/owner/food_items.html', context)


@login_required
@user_passes_test(is_owner)
def owner_add_food_item(request):
    """Add new food item"""

    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item added successfully!')
            return redirect('food_booking:owner_food_items')
    else:
        form = FoodItemForm()

    context = {
        'form': form,
        'action': 'Add',
    }

    return render(request, 'food_booking/owner/food_item_form.html', context)


@login_required
@user_passes_test(is_owner)
def owner_edit_food_item(request, item_id):
    """Edit existing food item"""

    food_item = get_object_or_404(FoodItem, id=item_id)

    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item updated successfully!')
            return redirect('food_booking:owner_food_items')
    else:
        form = FoodItemForm(instance=food_item)

    context = {
        'form': form,
        'action': 'Edit',
        'food_item': food_item,
    }

    return render(request, 'food_booking/owner/food_item_form.html', context)


@login_required
@user_passes_test(is_owner)
def owner_analytics(request):
    """Detailed analytics and reports"""

    # Date range for analytics
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    # Daily revenue for the last 30 days
    daily_revenue = []
    daily_orders = []

    for i in range(30):
        date = end_date - timedelta(days=i)
        day_orders = Order.objects.filter(created_at__date=date)
        revenue = day_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        count = day_orders.count()

        daily_revenue.append({
            'date': date.strftime('%Y-%m-%d'),
            'revenue': float(revenue)
        })
        daily_orders.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })

    # Payment method analysis
    payment_analysis = Order.objects.filter(
        created_at__date__gte=start_date
    ).values('payment_method').annotate(
        count=Count('id'),
        total_revenue=Sum('total_amount'),
        avg_order_value=Sum('total_amount') / Count('id')
    ).order_by('-total_revenue')

    # Top selling items
    top_items = OrderItem.objects.filter(
        order__created_at__date__gte=start_date
    ).values('food_item__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price'),
        order_count=Count('order', distinct=True)
    ).order_by('-total_quantity')[:10]

    # Seat usage analysis
    seat_analysis = Order.objects.filter(
        created_at__date__gte=start_date
    ).values('seat_number').annotate(
        order_count=Count('id'),
        total_revenue=Sum('total_amount')
    ).order_by('-order_count')[:20]

    context = {
        'daily_revenue': json.dumps(list(reversed(daily_revenue))),
        'daily_orders': json.dumps(list(reversed(daily_orders))),
        'payment_analysis': payment_analysis,
        'top_items': top_items,
        'seat_analysis': seat_analysis,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'food_booking/owner/analytics.html', context)


@login_required
@user_passes_test(is_owner)
def owner_settings(request):
    """Owner settings and configuration"""

    if request.method == 'POST':
        # Handle settings updates
        messages.success(request, 'Settings updated successfully!')
        return redirect('food_booking:owner_settings')

    context = {
        'theatre_name': 'MovieSnacks Theatre',
        'contact_email': 'owner@moviesnacks.com',
        'contact_phone': '+91 98765 43210',
        'business_hours': '10:00 AM - 11:00 PM',
        'delivery_time': '15-20 minutes',
    }

    return render(request, 'food_booking/owner/settings.html', context)

'''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import HttpResponseForbidden
import logging
from datetime import timedelta
from .models import FoodItem, Order, OrderItem
from .forms import FoodItemForm
import json

# Set up logging for security events
logger = logging.getLogger(__name__)

# --- ACCESS CONTROL SETUP ---

def is_owner(user):
    """Check if user is an owner/admin with full superuser access."""
    return (
        user.is_authenticated and
        user.is_active and
        user.is_staff and
        user.is_superuser
    )

def owner_access_denied(request):
    """Custom 403 handler for owner access denied with logging."""
    if request.user.is_authenticated:
        logger.warning(f'Unauthorized access attempt to owner area by user: {request.user.username} (ID: {request.user.id})')
    else:
        logger.warning('Unauthorized access attempt to owner area by anonymous user')

    return HttpResponseForbidden(
        '<h1>Access Denied</h1>'
        '<p>You do not have permission to access this area.</p>'
        '<p><a href="/">Return to Menu</a></p>'
    )


# Helper decorator to redirect unauthorized users to a custom page or login
def owner_required(view_func):
    decorated_view_func = login_required(
        user_passes_test(
            is_owner,
            login_url='/login/',  # Change this to your login URL
            redirect_field_name=None
        )(view_func)
    )
    return decorated_view_func


# --- OWNER VIEWS WITH ACCESS CONTROL ---

@owner_required
def owner_dashboard(request):
    """Owner dashboard with overview statistics."""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    today_orders = Order.objects.filter(created_at__date=today)
    today_revenue = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    today_count = today_orders.count()

    week_orders = Order.objects.filter(created_at__date__gte=week_ago)
    week_revenue = week_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    week_count = week_orders.count()

    month_orders = Order.objects.filter(created_at__date__gte=month_ago)
    month_revenue = month_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    month_count = month_orders.count()

    payment_stats = Order.objects.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('total_amount')
    ).order_by('-total')

    recent_orders = Order.objects.select_related().order_by('-created_at')[:10]

    popular_items = OrderItem.objects.values('food_item__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')[:5]

    pending_orders = Order.objects.filter(payment_status='PENDING').count()

    context = {
        'today_revenue': today_revenue,
        'today_count': today_count,
        'week_revenue': week_revenue,
        'week_count': week_count,
        'month_revenue': month_revenue,
        'month_count': month_count,
        'payment_stats': payment_stats,
        'recent_orders': recent_orders,
        'popular_items': popular_items,
        'pending_orders': pending_orders,
    }

    return render(request, 'food_booking/owner/dashboard.html', context)

# Similarly replace @login_required @user_passes_test(is_owner) with @owner_required
# for all owner views below:

@owner_required
def owner_orders(request):
    # ... keep existing logic unchanged ...
    pass

@owner_required
def owner_order_detail(request, order_id):
    # ... keep existing logic unchanged ...
    pass

@owner_required
def owner_food_items(request):
    # ... keep existing logic unchanged ...
    pass

@owner_required
def owner_add_food_item(request):
    # ... keep existing logic unchanged ...
    pass

@owner_required
def owner_edit_food_item(request, item_id):
    # ... keep existing logic unchanged ...
    pass

@owner_required
def owner_analytics(request):
    # ... keep existing logic unchanged ...
    pass

@owner_required
def owner_settings(request):
    # ... keep existing logic unchanged ...
    pass


# --- OPTIONAL: Public view example accessible by everyone ---
def menu(request):
    """Public menu accessible by anyone without login."""
    food_items = FoodItem.objects.filter(available=True).order_by('name')
    context = {'food_items': food_items}
    return render(request, 'food_booking/menu.html', context)


# --- OPTIONAL: Utility to check access inside any view ---
def check_if_superuser(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return True
    return False'''

