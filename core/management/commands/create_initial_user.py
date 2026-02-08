from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates initial user jayati with password jayati2026'

    def handle(self, *args, **options):
        if User.objects.filter(username='jayati').exists():
            self.stdout.write(self.style.WARNING('User "jayati" already exists'))
            return

        user = User.objects.create_user(
            username='jayati',
            password='jayati2026',
            first_name='Jayti',
            last_name='Pargal'
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))
