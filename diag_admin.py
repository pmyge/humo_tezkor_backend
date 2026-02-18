import os
import django
import sys

# Add the backend directory to sys.path
backend_dir = r"c:\Users\User\.gemini\antigravity\scratch\punyo_market\backend"
sys.path.append(backend_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.admin import site
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from orders.models import Order
from products.models import Product, Category
from users.models import UserProfile, Customer
import traceback

User = get_user_model()

def test_admin_list(model_class):
    print(f"\n--- Testing Admin for {model_class.__name__} ---")
    try:
        ma = site._registry[model_class]
    except KeyError:
        print(f"Error: {model_class.__name__} not registered in admin.")
        return True

    rf = RequestFactory()
    request = rf.get('/')
    request.user = User.objects.filter(is_superuser=True).first()
    
    if not request.user:
        print("Warning: No superuser found. Using mock superuser.")
        request.user = User(is_superuser=True, is_staff=True, username='mock_admin')
    
    try:
        # Check changelist instantiation
        cl = ma.get_changelist_instance(request)
        queryset = cl.get_queryset(request)
        print(f"Queryset count: {queryset.count()}")
        
        # Check list_display rendering
        for obj in queryset[:3]:
            print(f"Checking object ID {obj.id}...", end=" ")
            for field_name in ma.list_display:
                try:
                    if hasattr(ma, field_name):
                        val = getattr(ma, field_name)(obj)
                    else:
                        val = getattr(obj, field_name)
                    str(val)
                except Exception as e:
                    print(f"\nERROR in field-rendering '{field_name}' for ID {obj.id}: {e}")
                    traceback.print_exc()
                    return False
            print("OK")
    except Exception as e:
        print(f"CRITICAL ERROR in {model_class.__name__} changelist: {e}")
        traceback.print_exc()
        return False
        
    return True

if __name__ == "__main__":
    success = True
    models_to_test = [Order, Product, Category, Group, UserProfile, Customer]
    
    try:
        from chat.models import ChatMessage
        models_to_test.append(ChatMessage)
    except ImportError:
        pass

    for m in models_to_test:
        success &= test_admin_list(m)
    
    if success:
        print("\nAll tested admin lists are rendering correctly.")
    else:
        print("\nDiagnosis finished with errors.")
