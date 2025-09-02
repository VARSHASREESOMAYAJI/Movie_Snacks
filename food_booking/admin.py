from django.contrib import admin
from django.utils.html import format_html
from .models import FoodItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price', 'subtotal']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created_at']
    list_filter = ['available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['available', 'price']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price')
        }),
        ('Status', {
            'fields': ('available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'seat_number', 'payment_method', 
        'payment_status', 'total_amount', 'created_at'
    ]
    list_filter = ['payment_method', 'payment_status', 'created_at']
    search_fields = ['customer_name', 'seat_number', 'mobile_number']
    list_editable = ['payment_status']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'seat_number', 'mobile_number')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('orderitem_set')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'food_item', 'quantity', 'price', 'subtotal']
    list_filter = ['food_item', 'order__payment_status']
    search_fields = ['order__customer_name', 'food_item__name']
    readonly_fields = ['subtotal']
    
    def subtotal(self, obj):
        return f"₹{obj.subtotal}"
    subtotal.short_description = 'Subtotal'
