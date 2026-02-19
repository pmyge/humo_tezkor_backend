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
if not User.objects.filter(username='punyo').exists():
    User.objects.create_superuser(
        username='punyo',
        password='punyo33',
        telegram_user_id=None,
        first_name='Punyo',
        last_name='Admin'
    )
    print("✅ Superuser 'punyo' created with password 'punyo33'")
else:
    # Ensure punyo exists and has no telegram_user_id
    existing_punyo = User.objects.get(username='punyo')
    if existing_punyo.telegram_user_id is not None:
        existing_punyo.telegram_user_id = None
        existing_punyo.save()
    print("ℹ️ Superuser 'punyo' already exists")

# Optional: Disable or delete old 'admin' if requested, but for now just focus on punyo
