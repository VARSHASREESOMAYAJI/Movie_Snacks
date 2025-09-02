from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


class Command(BaseCommand):
    help = 'Test security of owner views - ensure regular users cannot access them'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Testing Owner View Security')
        )
        self.stdout.write('=' * 50)
        
        # Create test users
        try:
            # Create a regular user
            regular_user, created = User.objects.get_or_create(
                username='testuser',
                defaults={
                    'email': 'testuser@example.com',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            if created:
                regular_user.set_password('testpass123')
                regular_user.save()
                self.stdout.write('✓ Created regular user: testuser')
            else:
                self.stdout.write('✓ Regular user already exists: testuser')
            
            # Create a staff user (but not superuser)
            staff_user, created = User.objects.get_or_create(
                username='staffuser',
                defaults={
                    'email': 'staff@example.com',
                    'first_name': 'Staff',
                    'last_name': 'User'
                }
            )
            if created:
                staff_user.set_password('staffpass123')
                staff_user.save()
                self.stdout.write('✓ Created staff user: staffuser')
            else:
                self.stdout.write('✓ Staff user already exists: staffuser')
            
            staff_user.is_staff = True
            staff_user.save()
            
            # Create a superuser
            superuser, created = User.objects.get_or_create(
                username='superuser',
                defaults={
                    'email': 'super@example.com',
                    'first_name': 'Super',
                    'last_name': 'User'
                }
            )
            if created:
                superuser.set_password('superpass123')
                superuser.save()
                self.stdout.write('✓ Created superuser: superuser')
            else:
                self.stdout.write('✓ Superuser already exists: superuser')
            
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating test users: {e}')
            )
            return
        
        # Test access to owner views
        owner_urls = [
            'food_booking:owner_dashboard',
            'food_booking:owner_orders',
            'food_booking:owner_food_items',
            'food_booking:owner_analytics',
            'food_booking:owner_settings',
        ]
        
        self.stdout.write('\nTesting Access Control:')
        self.stdout.write('-' * 30)
        
        for url_name in owner_urls:
            try:
                url = reverse(url_name)
                
                # Test 1: Anonymous user (should redirect to login)
                client = Client()
                response = client.get(url)
                self.stdout.write(f'{url_name}: Anonymous → {response.status_code} (should be 302/redirect)')
                
                # Test 2: Regular user (should redirect to login or get access denied)
                client.force_login(regular_user)
                response = client.get(url)
                self.stdout.write(f'{url_name}: Regular User → {response.status_code} (should be 302/redirect or 403)')
                
                # Test 3: Staff user (should redirect to login or get access denied)
                client.force_login(staff_user)
                response = client.get(url)
                self.stdout.write(f'{url_name}: Staff User → {response.status_code} (should be 302/redirect or 403)')
                
                # Test 4: Superuser (should work)
                client.force_login(superuser)
                response = client.get(url)
                self.stdout.write(f'{url_name}: Superuser → {response.status_code} (should be 200)')
                
                self.stdout.write('')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error testing {url_name}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\nSecurity test completed!')
        )
        self.stdout.write('\nTest Users Created:')
        self.stdout.write('Regular User: testuser / testpass123')
        self.stdout.write('Staff User: staffuser / staffpass123')
        self.stdout.write('Superuser: superuser / superpass123')
        self.stdout.write('\nNote: Only superuser should be able to access owner views!')
