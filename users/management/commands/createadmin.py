from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create admin superuser'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin',
                telegram_id='admin_user',
                first_name='Admin',
                last_name='User',
                email='admin@punyomarket.com'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser "admin" created successfully!'))
            self.stdout.write(self.style.SUCCESS('Username: admin'))
            self.stdout.write(self.style.SUCCESS('Password: admin'))
        else:
            self.stdout.write(self.style.WARNING('ℹ️ Superuser "admin" already exists'))
