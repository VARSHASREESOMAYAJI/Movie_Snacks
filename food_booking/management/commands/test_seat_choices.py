from django.core.management.base import BaseCommand
from food_booking.forms import OrderForm


class Command(BaseCommand):
    help = 'Test the seat choices generation for the order form'

    def handle(self, *args, **options):
        form = OrderForm()
        
        self.stdout.write(
            self.style.SUCCESS('Testing Seat Choices Generation')
        )
        self.stdout.write('=' * 50)
        
        # Show first few choices
        self.stdout.write('First 10 seat choices:')
        for i, choice in enumerate(form.fields['seat_number'].choices[:10]):
            self.stdout.write(f'  {choice[0]} = {choice[1]}')
        
        self.stdout.write('...')
        
        # Show last few choices
        self.stdout.write('Last 10 seat choices:')
        for choice in form.fields['seat_number'].choices[-10:]:
            self.stdout.write(f'  {choice[0]} = {choice[1]}')
        
        # Show total count
        total_choices = len(form.fields['seat_number'].choices)
        self.stdout.write(f'\nTotal seat choices: {total_choices}')
        self.stdout.write(f'Expected: 26 rows × 20 seats = 520 choices')
        
        # Show initial value
        initial = form.fields['seat_number'].initial
        self.stdout.write(f'Initial value: {initial}')
        
        self.stdout.write(
            self.style.SUCCESS('\nSeat choices generation test completed!')
        )
