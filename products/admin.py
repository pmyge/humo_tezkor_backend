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
    list_per_page = 15
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
    list_display = ('id', 'name', 'category', 'price', 'order', 'is_active')
    list_select_related = ('category',)
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_per_page = 10
