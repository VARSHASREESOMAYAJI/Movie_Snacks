from django import forms
from .models import Order, OrderItem, FoodItem


class FoodItemForm(forms.ModelForm):
    """Form for managing food items"""
    
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'available']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter food item name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Enter food item description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }


class OrderForm(forms.ModelForm):
    """Form for customer order details"""
    
    # Row choices: A-Z
    ROW_CHOICES = [('', 'Select Row')] + [(row, row) for row in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    
    # Seat choices: 1-30 (will be populated dynamically)
    SEAT_CHOICES = [('', 'Select Seat')] + [(str(i), str(i)) for i in range(1, 31)]
    
    row_letter = forms.ChoiceField(
        choices=ROW_CHOICES,
        initial='',
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-lg font-medium',
            'id': 'row-select'
        })
    )
    
    seat_number = forms.ChoiceField(
        choices=SEAT_CHOICES,
        initial='',
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-lg font-medium opacity-50',
            'id': 'seat-select',
            'disabled': True
        })
    )
    
    class Meta:
        model = Order
        fields = ['customer_name', 'mobile_number', 'payment_method']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your name'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your mobile number (optional)'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg'
            })
        }



    def clean_customer_name(self):
        customer_name = self.cleaned_data['customer_name']
        if not customer_name.strip():
            raise forms.ValidationError("Customer name is required.")
        return customer_name.strip()

    def clean(self):
        cleaned_data = super().clean()
        row_letter = cleaned_data.get('row_letter')
        seat_number = cleaned_data.get('seat_number')
        payment_method = cleaned_data.get('payment_method')
        mobile_number = cleaned_data.get('mobile_number')
        
        if not row_letter:
            raise forms.ValidationError("Please select a row.")
        
        if not seat_number:
            raise forms.ValidationError("Please select a seat number.")
        
        # Mobile number is required for all digital payment methods
        if payment_method in ['UPI', 'PHONEPE', 'GPAY', 'PAYTM', 'CARD']:
            if not mobile_number:
                raise forms.ValidationError("Mobile number is required for digital payments.")
        
        # Validate mobile number format if provided
        if mobile_number:
            mobile_number = mobile_number.strip()
            if not mobile_number.isdigit() or len(mobile_number) < 10:
                raise forms.ValidationError("Please enter a valid mobile number.")
            cleaned_data['mobile_number'] = mobile_number
        
        return cleaned_data
    



class CartItemForm(forms.Form):
    """Form for adding items to cart"""
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-16 px-2 py-1 border border-gray-300 rounded-md text-center',
            'min': '1',
            'max': '10'
        })
    )
    food_item_id = forms.IntegerField(widget=forms.HiddenInput())


class UpdateCartForm(forms.Form):
    """Form for updating cart item quantities"""
    quantity = forms.IntegerField(
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'w-16 px-2 py-1 border border-gray-300 rounded-md text-center',
            'min': '0',
            'max': '10'
        })
    )
    item_id = forms.IntegerField(widget=forms.HiddenInput())
