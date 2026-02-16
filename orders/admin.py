from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total',)
    fields = ('product', 'quantity', 'price', 'get_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__phone_number', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'phone_number')
        }),
        ('Order Details', {
            'fields': ('status', 'total_amount', 'delivery_address', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_total')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__id')
