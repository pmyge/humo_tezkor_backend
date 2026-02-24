import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product
from django.db.models import Max

def test_auto_order():
    print("--- Diagnostic Start ---")
    
    # Check Categories
    cats = Category.objects.all().order_by('order')
    print(f"Current Categories: {cats.count()}")
    for c in cats:
        print(f" - {c.name}: order={c.order}")
    
    max_cat = Category.objects.aggregate(Max('order'))['order__max']
    print(f"Calculated Max Category Order: {max_cat}")
    
    # Try to simulate a save
    new_cat = Category(name="Test Auto Order")
    print(f"New Category (before save) order: {new_cat.order}")
    
    # Manual check of the logic in save()
    if not new_cat.pk and new_cat.order == 0:
        new_cat.order = (max_cat or 0) + 1
    
    print(f"New Category (calculated) order: {new_cat.order}")
    
    print("--- Diagnostic End ---")

if __name__ == "__main__":
    test_auto_order()
