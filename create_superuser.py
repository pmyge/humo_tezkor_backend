import os
import django
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        password='admin',
        telegram_user_id=12345678,  # Dummy ID for admin
        first_name='Admin',
        last_name='User'
    )
    print("✅ Superuser 'admin' created with password 'admin'")
else:
    print("ℹ️ Superuser 'admin' already exists")
