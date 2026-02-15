from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ru', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'name_ru')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('General', {
            'fields': ('name', 'name_ru', 'image')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    class Media:
        js = ('products/admin_translate.js',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ru', 'category', 'price', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'name_ru', 'description')
    list_editable = ('price', 'order', 'is_active')
    ordering = ('category', 'order', 'name')
    
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
