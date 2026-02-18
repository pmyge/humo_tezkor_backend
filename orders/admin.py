from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Enhanced list_display to include products and categories
    list_display = (
        'id', 'user', 'phone_number', 'status', 
        'total_amount', 'get_products', 'get_categories', 
        'delivery_address', 'created_at'
    )
    list_select_related = ('user',)
    
    def get_queryset(self, request):
        # Optimization: Prefetch items and their related products and categories
        return super().get_queryset(request).prefetch_related('items__product__category')

    @admin.display(description='Mahsulotlar')
    def get_products(self, obj):
        return ", ".join([item.product.name for item in obj.items.all()])

    @admin.display(description='Kategoriya ID')
    def get_categories(self, obj):
        # Unique list of category IDs from items
        cat_ids = {str(item.product.category_id) for item in obj.items.all() if item.product and item.product.category_id}
        return ", ".join(sorted(cat_ids))

    list_filter = ('status', 'created_at')
    # Removed potential problematic search fields
    search_fields = ('phone_number', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at', 'total_amount')
    inlines = [OrderItemInline]
    actions = ['confirm_orders', 'mark_delivered']

    @admin.action(description='Buyurtmani tasdiqlash')
    def confirm_orders(self, request, queryset):
        rows_updated = queryset.update(status='active')
        self.message_user(request, f"{rows_updated} ta buyurtma tasdiqlandi.")

    @admin.action(description='Berdim (O\'chirish)')
    def mark_delivered(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} ta buyurtma o'chirildi (Berildi).")
    
    fieldsets = (
        ('Asosiy malumotlar', {
            'fields': ('user', 'phone_number', 'status', 'total_amount')
        }),
        ('Manzil va Eslatma', {
            'fields': ('delivery_address', 'latitude', 'longitude', 'notes')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

# We are NOT registering OrderItem here to keep the sidebar clean as requested.
# It is still visible as an inline within OrderAdmin.
