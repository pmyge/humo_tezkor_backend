from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Minimal list_display to ensure stability
    list_display = ('id', 'user', 'phone_number', 'status', 'total_amount', 'delivery_address', 'created_at')
    list_select_related = ('user',)
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
