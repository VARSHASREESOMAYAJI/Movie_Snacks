from django.core.management.base import BaseCommand
from food_booking.forms import OrderForm


class Command(BaseCommand):
    help = 'Test the two-step seat selection form'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Testing Two-Step Seat Selection Form')
        )
        self.stdout.write('=' * 50)
        
        # Test form initialization
        form = OrderForm()
        
        self.stdout.write('\n1. Form Fields:')
        self.stdout.write(f'   Row Letter: {form.fields["row_letter"].choices[:5]}...')
        self.stdout.write(f'   Seat Number: {form.fields["seat_number"].choices[:5]}...')
        
        # Test validation
        self.stdout.write('\n2. Validation Tests:')
        
        # Test empty form
        form_data = {}
        form = OrderForm(data=form_data)
        self.stdout.write(f'   Empty form valid: {form.is_valid()}')
        if not form.is_valid():
            self.stdout.write(f'   Errors: {form.errors}')
        
        # Test with only row selected
        form_data = {'row_letter': 'B'}
        form = OrderForm(data=form_data)
        self.stdout.write(f'   Only row selected valid: {form.is_valid()}')
        if not form.is_valid():
            self.stdout.write(f'   Errors: {form.errors}')
        
        # Test with both selected
        form_data = {'row_letter': 'B', 'seat_number': '15'}
        form = OrderForm(data=form_data)
        self.stdout.write(f'   Both selected valid: {form.is_valid()}')
        if form.is_valid():
            self.stdout.write(f'   Combined seat: {form.cleaned_data["row_letter"] + form.cleaned_data["seat_number"]}')
        
        self.stdout.write(
            self.style.SUCCESS('\nTwo-step seat selection test completed!')
        )
