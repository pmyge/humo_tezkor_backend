import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import Customer

try:
    # Try to find a non-staff user to test deletion
    user_to_delete = Customer.objects.filter(is_staff=False).first()
    if user_to_delete:
        print(f"DEBUG: Attempting to delete user {user_to_delete.id} ({user_to_delete.username})")
        user_to_delete.delete()
        print("DEBUG: Deletion successful!")
    else:
        print("DEBUG: No test user found to delete.")
except Exception as e:
    import traceback
    print("DEBUG: Deletion failed!")
    traceback.print_exc()
