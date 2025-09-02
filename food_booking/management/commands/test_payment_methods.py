from django.core.management.base import BaseCommand
from food_booking.forms import OrderForm


class Command(BaseCommand):
    help = 'Test the new payment methods and validation'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Testing New Payment Methods')
        )
        self.stdout.write('=' * 50)
        
        # Test form initialization
        form = OrderForm()
        
        self.stdout.write('\n1. Available Payment Methods:')
        for choice in form.fields['payment_method'].choices:
            self.stdout.write(f'   {choice[0]}: {choice[1]}')
        
        # Test validation for different payment methods
        self.stdout.write('\n2. Validation Tests:')
        
        # Test UPI payment with mobile
        form_data = {
            'row_letter': 'A',
            'seat_number': '1',
            'customer_name': 'Test User',
            'payment_method': 'UPI',
            'mobile_number': '9876543210'
        }
        form = OrderForm(data=form_data)
        self.stdout.write(f'   UPI with mobile valid: {form.is_valid()}')
        
        # Test UPI payment without mobile (should fail)
        form_data['mobile_number'] = ''
        form = OrderForm(data=form_data)
        self.stdout.write(f'   UPI without mobile valid: {form.is_valid()}')
        if not form.is_valid():
            self.stdout.write(f'   Errors: {form.errors.get("mobile_number", [])}')
        
        # Test PhonePe payment with mobile
        form_data['payment_method'] = 'PHONEPE'
        form_data['mobile_number'] = '9876543210'
        form = OrderForm(data=form_data)
        self.stdout.write(f'   PhonePe with mobile valid: {form.is_valid()}')
        
        # Test Card payment with mobile
        form_data['payment_method'] = 'CARD'
        form_data['mobile_number'] = '9876543210'
        form = OrderForm(data=form_data)
        self.stdout.write(f'   Card with mobile valid: {form.is_valid()}')
        
        # Test Cash payment without mobile (should work)
        form_data['payment_method'] = 'CASH'
        form_data['mobile_number'] = ''
        form = OrderForm(data=form_data)
        self.stdout.write(f'   Cash without mobile valid: {form.is_valid()}')
        
        self.stdout.write(
            self.style.SUCCESS('\nPayment methods test completed!')
        )
