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
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'name_ru', 'image')
        }),
        ('Sozlamalar', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ru', 'category', 'price', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'name_ru', 'description')
    list_editable = ('price', 'order', 'is_active')
    ordering = ('category', 'order', 'name')
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('category', 'name', 'name_ru', 'image', 'price')
        }),
        ('Tavsif', {
            'fields': ('description', 'description_ru'),
            'classes': ('collapse',)
        }),
        ('Sozlamalar', {
            'fields': ('order', 'is_active')
        }),
    )
