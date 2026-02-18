from django.db import models
from products.models import Product
from users.models import UserProfile


class Order(models.Model):
    """Order model for user purchases"""
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('active', 'Faol'),
        ('completed', 'Yakunlandi'),
        ('canceled', 'Bekor qilindi'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_address = models.TextField(blank=True, default='')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone_number = models.CharField(max_length=20, default='')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
    
    def __str__(self):
        user_name = "Unknown"
        if self.user:
            user_name = f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
        return f"Order #{self.id or 'New'} - {user_name} ({self.status})"


class OrderItem(models.Model):
    """Order item model for products in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Snapshot of product price
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return f"{self.product.name if self.product else 'Item'} x{self.quantity}"
    
    def get_total(self):
        return self.price * self.quantity
