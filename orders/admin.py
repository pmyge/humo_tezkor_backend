from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total',)
    fields = ('product', 'quantity', 'price', 'get_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_user', 'phone_number', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__first_name', 'user__username', 'phone_number', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    actions = ['confirm_orders', 'mark_delivered']
    
    def display_user(self, obj):
        try:
            return str(obj.user)
        except:
            return "No User"
    display_user.short_description = 'User'

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
        ('Info', {
            'fields': ('user', 'phone_number', 'status')
        }),
        ('Details', {
            'fields': ('total_amount', 'delivery_address', 'latitude', 'longitude', 'notes')
        }),
        ('Time', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_total')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__id')
