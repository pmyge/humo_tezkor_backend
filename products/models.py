from django.db import models


class Category(models.Model):
    """Product category model"""
    name = models.CharField(max_length=100, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=100, verbose_name="Nomi (RU)")
    image = models.ImageField(upload_to='categories/', verbose_name="Rasm")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model"""
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name="Kategoriya"
    )
    name = models.CharField(max_length=200, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=200, verbose_name="Nomi (RU)")
    image = models.ImageField(upload_to='products/', verbose_name="Rasm")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (UZS)")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    description = models.TextField(blank=True, verbose_name="Tavsif (UZ)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (RU)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.price} UZS"
