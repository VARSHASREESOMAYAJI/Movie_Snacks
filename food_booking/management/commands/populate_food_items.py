from django.core.management.base import BaseCommand
from food_booking.models import FoodItem


class Command(BaseCommand):
    help = 'Populate database with sample food items for movie theatre'

    def handle(self, *args, **options):
        food_items = [
            {
                'name': 'Popcorn (Large)',
                'description': 'Fresh, hot popcorn with butter and salt. Perfect movie snack!',
                'price': 120.00,
                'available': True
            },
            {
                'name': 'Popcorn (Medium)',
                'description': 'Fresh, hot popcorn with butter and salt. Great size for sharing.',
                'price': 90.00,
                'available': True
            },
            {
                'name': 'Nachos with Cheese',
                'description': 'Crispy nachos served with melted cheese sauce and jalapeños.',
                'price': 150.00,
                'available': True
            },
            {
                'name': 'Hot Dog',
                'description': 'Classic hot dog with mustard, ketchup, and onions.',
                'price': 180.00,
                'available': True
            },
            {
                'name': 'Pizza Slice',
                'description': 'Fresh pizza slice with cheese and tomato sauce.',
                'price': 200.00,
                'available': True
            },
            {
                'name': 'Chicken Wings',
                'description': 'Crispy fried chicken wings with your choice of sauce.',
                'price': 250.00,
                'available': True
            },
            {
                'name': 'French Fries',
                'description': 'Golden crispy french fries with ketchup.',
                'price': 100.00,
                'available': True
            },
            {
                'name': 'Ice Cream Cone',
                'description': 'Vanilla ice cream cone. Perfect dessert!',
                'price': 80.00,
                'available': True
            },
            {
                'name': 'Chocolate Bar',
                'description': 'Premium chocolate bar. Various flavors available.',
                'price': 60.00,
                'available': True
            },
            {
                'name': 'Chips & Dip',
                'description': 'Assorted chips with salsa and guacamole.',
                'price': 120.00,
                'available': True
            },
            {
                'name': 'Soft Drink (Large)',
                'description': 'Refreshing soft drink. Coke, Pepsi, Sprite available.',
                'price': 80.00,
                'available': True
            },
            {
                'name': 'Soft Drink (Medium)',
                'description': 'Refreshing soft drink. Coke, Pepsi, Sprite available.',
                'price': 60.00,
                'available': True
            },
            {
                'name': 'Mineral Water',
                'description': 'Pure mineral water. Stay hydrated during the movie.',
                'price': 40.00,
                'available': True
            },
            {
                'name': 'Coffee (Hot)',
                'description': 'Fresh brewed coffee. Perfect for evening shows.',
                'price': 70.00,
                'available': True
            },
            {
                'name': 'Tea (Hot)',
                'description': 'Hot tea with milk and sugar. Soothing beverage.',
                'price': 50.00,
                'available': True
            },
            {
                'name': 'Milk Shake',
                'description': 'Creamy milk shake. Chocolate, vanilla, strawberry flavors.',
                'price': 120.00,
                'available': True
            },
            {
                'name': 'Sandwich',
                'description': 'Fresh sandwich with cheese, lettuce, and tomato.',
                'price': 160.00,
                'available': True
            },
            {
                'name': 'Burger',
                'description': 'Juicy burger with cheese, lettuce, tomato, and special sauce.',
                'price': 220.00,
                'available': True
            },
            {
                'name': 'Candy Pack',
                'description': 'Assorted candies. Sweet treats for the movie.',
                'price': 45.00,
                'available': True
            },
            {
                'name': 'Nuts Mix',
                'description': 'Premium mixed nuts. Healthy snack option.',
                'price': 90.00,
                'available': True
            }
        ]

        created_count = 0
        updated_count = 0

        for item_data in food_items:
            food_item, created = FoodItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {food_item.name}')
                )
            else:
                # Update existing item
                for key, value in item_data.items():
                    setattr(food_item, key, value)
                food_item.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated: {food_item.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully populated food items!\n'
                f'Created: {created_count}\n'
                f'Updated: {updated_count}\n'
                f'Total: {FoodItem.objects.count()}'
            )
        )
