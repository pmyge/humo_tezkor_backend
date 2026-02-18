import os
import django
import sys

# Add the backend directory to sys.path
backend_dir = r"c:\Users\User\.gemini\antigravity\scratch\punyo_market\backend"
sys.path.append(backend_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.admin import site
from orders.models import Order
from products.models import Product, Category
from django.test import RequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()

def test_admin_list(model_class):
    print(f"\nTesting Admin for {model_class.__name__}...")
    try:
        ma = site._registry[model_class]
    except KeyError:
        print(f"Error: {model_class.__name__} not registered in admin.")
        return

    # Create a mock request
    rf = RequestFactory()
    request = rf.get('/')
    request.user = User.objects.filter(is_superuser=True).first()
    
    if not request.user:
        print("Warning: No superuser found, skipping user-dependent checks.")
        # Create a dummy superuser for testing if needed
    
    cl = ma.get_changelist_instance(request)
    queryset = cl.get_queryset(request)
    
    print(f"Queryset count: {queryset.count()}")
    
    for obj in queryset[:10]:
        print(f"Checking object ID {obj.id}...", end=" ")
        row = []
        for field_name in ma.list_display:
            try:
                if hasattr(ma, field_name):
                    val = getattr(ma, field_name)(obj)
                else:
                    val = getattr(obj, field_name)
                row.append(str(val))
            except Exception as e:
                print(f"\nERROR in field '{field_name}' for ID {obj.id}: {e}")
                import traceback
                traceback.print_exc()
                return False
        print("OK")
    return True

if __name__ == "__main__":
    success = True
    success &= test_admin_list(Order)
    success &= test_admin_list(Product)
    success &= test_admin_list(Category)
    
    if success:
        print("\nAll tested admin lists are rendering correctly for the first 10 items.")
    else:
        print("\nDiagnosis finished with errors.")
