from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a superuser for the movie theatre admin interface'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for the superuser'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@movietheatre.com',
            help='Email for the superuser'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password for the superuser'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            return

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser!\n'
                    f'Username: {username}\n'
                    f'Email: {email}\n'
                    f'Password: {password}\n\n'
                    f'You can now login to /admin/ with these credentials.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
