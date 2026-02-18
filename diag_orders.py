import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from orders.models import Order, OrderItem
from users.models import UserProfile

def check_orders():
    print("Checking Orders...")
    orders = Order.objects.all()
    for order in orders:
        try:
            print(f"Order #{order.id}: User={order.user}, Status={order.status}, Total={order.total_amount}")
            str(order)
            for item in order.items.all():
                print(f"  Item: {item.product.name} x{item.quantity}")
                str(item)
        except Exception as e:
            print(f"!!! Error in Order #{order.id}: {e}")

if __name__ == "__main__":
    check_orders()
