from django.contrib import admin
from .models import Category, Product

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('id', 'name', 'price', 'order', 'is_active')
    readonly_fields = ('id',)
    show_change_link = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_ru', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'name_ru')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    inlines = [ProductInline]
    
    fieldsets = (
        ('General', {
            'fields': ('name', 'name_ru', 'image', 'image_base64')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    readonly_fields = ('image_base64',)

    class Media:
        js = ('products/admin_translate.js',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_ru', 'category', 'price', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'name_ru', 'description')
    list_editable = ('price', 'order', 'is_active')
    ordering = ('category', 'order', 'name')
    readonly_fields = ('id',)
    
    fieldsets = (
        ('General', {
            'fields': ('category', 'name', 'name_ru', 'image', 'price')
        }),
        ('Description', {
            'fields': ('description', 'description_ru'),
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    class Media:
        js = ('products/admin_translate.js',)
