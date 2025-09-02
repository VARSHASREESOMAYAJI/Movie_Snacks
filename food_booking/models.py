from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class FoodItem(models.Model):
    """Model for food items available for ordering"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    """Model for customer orders"""
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI (Any UPI App)'),
        ('PHONEPE', 'PhonePe'),
        ('GPAY', 'Google Pay'),
        ('PAYTM', 'Paytm'),
        ('CARD', 'Credit/Debit Card'),
        ('CASH', 'Cash'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    seat_number = models.CharField(max_length=10)
    customer_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    payment_method = models.CharField(
        max_length=10, 
        choices=PAYMENT_METHOD_CHOICES,
        default='UPI'
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} (Seat {self.seat_number})"

    def calculate_total(self):
        """Calculate total amount from order items"""
        total = sum(item.subtotal for item in self.orderitem_set.all())
        self.total_amount = total
        self.save()
        return total


class OrderItem(models.Model):
    """Model for individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ['order', 'food_item']

    def __str__(self):
        return f"{self.quantity}x {self.food_item.name}"

    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        """Set price from food item if not set"""
        if not self.price:
            self.price = self.food_item.price
        super().save(*args, **kwargs)
        # Update order total
        self.order.calculate_total()
