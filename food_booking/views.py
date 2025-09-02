from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import FoodItem, Order, OrderItem
from .forms import OrderForm, CartItemForm, UpdateCartForm
import json


def menu_view(request):
    """Display the food menu"""
    food_items = FoodItem.objects.filter(available=True).order_by('name')
    
    # Initialize cart in session if not exists
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    context = {
        'food_items': food_items,
        'cart': request.session['cart'],
        'cart_total': sum(item['price'] * item['quantity'] for item in request.session['cart'].values()),
        'cart_count': sum(item['quantity'] for item in request.session['cart'].values())
    }
    return render(request, 'food_booking/menu.html', context)


@require_POST
def add_to_cart(request):
    """Add item to cart"""
    form = CartItemForm(request.POST)
    if form.is_valid():
        food_item_id = form.cleaned_data['food_item_id']
        quantity = form.cleaned_data['quantity']
        
        try:
            food_item = FoodItem.objects.get(id=food_item_id, available=True)
            
            # Initialize cart if not exists
            if 'cart' not in request.session:
                request.session['cart'] = {}
            
            cart = request.session['cart']
            
            # Add or update item in cart
            if str(food_item_id) in cart:
                cart[str(food_item_id)]['quantity'] += quantity
            else:
                cart[str(food_item_id)] = {
                    'id': food_item_id,
                    'name': food_item.name,
                    'price': float(food_item.price),
                    'quantity': quantity
                }
            
            request.session.modified = True
            messages.success(request, f'{food_item.name} added to cart!')
            
        except FoodItem.DoesNotExist:
            messages.error(request, 'Item not found or not available.')
    
    return redirect('food_booking:menu')


@require_POST
def update_cart(request):
    """Update cart item quantity"""
    form = UpdateCartForm(request.POST)
    if form.is_valid():
        item_id = form.cleaned_data['item_id']
        quantity = form.cleaned_data['quantity']
        
        cart = request.session.get('cart', {})
        
        if str(item_id) in cart:
            if quantity <= 0:
                del cart[str(item_id)]
                messages.success(request, 'Item removed from cart.')
            else:
                cart[str(item_id)]['quantity'] = quantity
                messages.success(request, 'Cart updated successfully.')
            
            request.session.modified = True
    
    return redirect('food_booking:menu')


@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = request.session.get('cart', {})
    
    if str(item_id) in cart:
        item_name = cart[str(item_id)]['name']
        del cart[str(item_id)]
        request.session.modified = True
        messages.success(request, f'{item_name} removed from cart.')
    
    return redirect('food_booking:menu')


def order_form(request):
    """Display order form and handle submission"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty. Please add some items first.')
        return redirect('food_booking:menu')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order()
            # Combine row and seat number
            row_letter = form.cleaned_data['row_letter']
            seat_num = form.cleaned_data['seat_number']
            if row_letter and seat_num:
                order.seat_number = f"{row_letter}{seat_num}"
            else:
                messages.error(request, 'Please select both row and seat number.')
                return render(request, 'food_booking/order_form.html', {
                    'form': form,
                    'cart': cart,
                    'cart_total': cart_total,
                    'cart_count': sum(item['quantity'] for item in cart.values())
                })
            
            order.customer_name = form.cleaned_data['customer_name']
            order.mobile_number = form.cleaned_data['mobile_number']
            order.payment_method = form.cleaned_data['payment_method']
            order.total_amount = sum(item['price'] * item['quantity'] for item in cart.values())
            order.save()
            
            # Create order items
            for item_id, item_data in cart.items():
                try:
                    food_item = FoodItem.objects.get(id=item_data['id'])
                    OrderItem.objects.create(
                        order=order,
                        food_item=food_item,
                        quantity=item_data['quantity'],
                        price=food_item.price
                    )
                except FoodItem.DoesNotExist:
                    continue
            
            # Clear cart
            del request.session['cart']
            request.session.modified = True
            
            messages.success(request, 'Order placed successfully!')
            return redirect('food_booking:order_confirmation', order_id=order.id)
    else:
        form = OrderForm()
    
    cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
    
    context = {
        'form': form,
        'cart': cart,
        'cart_total': cart_total,
        'cart_count': sum(item['quantity'] for item in cart.values())
    }
    return render(request, 'food_booking/order_form.html', context)


def order_confirmation(request, order_id):
    """Display order confirmation"""
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'cart_count': 0  # No cart items on confirmation page
    }
    return render(request, 'food_booking/order_confirmation.html', context)


def clear_cart(request):
    """Clear the entire cart"""
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
        messages.success(request, 'Cart cleared successfully.')
    
    return redirect('food_booking:menu')


# API endpoints for AJAX requests
@csrf_exempt
@require_POST
def api_add_to_cart(request):
    """API endpoint for adding items to cart via AJAX"""
    try:
        data = json.loads(request.body)
        food_item_id = data.get('food_item_id')
        quantity = int(data.get('quantity', 1))
        
        if not food_item_id or quantity < 1:
            return JsonResponse({'success': False, 'message': 'Invalid data'})
        
        food_item = FoodItem.objects.get(id=food_item_id, available=True)
        
        # Initialize cart if not exists
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        cart = request.session['cart']
        
        # Add or update item in cart
        if str(food_item_id) in cart:
            cart[str(food_item_id)]['quantity'] += quantity
        else:
            cart[str(food_item_id)] = {
                'id': food_item_id,
                'name': food_item.name,
                'price': float(food_item.price),
                'quantity': quantity
            }
        
        request.session.modified = True
        
        cart_total = sum(item['price'] * item['quantity'] for item in cart.values())
        cart_count = sum(item['quantity'] for item in cart.values())
        
        return JsonResponse({
            'success': True,
            'message': f'{food_item.name} added to cart!',
            'cart_total': cart_total,
            'cart_count': cart_count
        })
        
    except (json.JSONDecodeError, FoodItem.DoesNotExist, ValueError):
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
