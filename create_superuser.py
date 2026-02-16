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
        telegram_user_id=None,  # Do not assign Telegram ID to admin to avoid overlap
        first_name='Admin',
        last_name='User'
    )
    print("✅ Superuser 'admin' created with password 'admin'")
else:
    # Ensure existing admin doesn't have a telegram_user_id to avoid Mini App overlap
    existing_admin = User.objects.get(username='admin')
    if existing_admin.telegram_user_id is not None:
        existing_admin.telegram_user_id = None
        existing_admin.save()
        print("🧹 Existing admin's telegram_user_id cleared to avoid overlap")
    print("ℹ️ Superuser 'admin' already exists")
