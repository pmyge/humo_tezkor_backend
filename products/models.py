import base64
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models


class Category(models.Model):
    """Product category model"""
    name = models.CharField(max_length=100, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=100, verbose_name="Nomi (RU)")
    image = models.ImageField(upload_to='categories/', verbose_name="Rasm")
    image_base64 = models.TextField(blank=True, null=True, verbose_name="Rasm (Base64)")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)
                # Optimize image for DB storage (max 400px width/height for categories)
                img.thumbnail((400, 400))
                
                buffer = BytesIO()
                # Save as JPEG with 70% quality to reduce size
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(buffer, format="JPEG", quality=70)
                
                img_str = base64.b64encode(buffer.getvalue()).decode()
                self.image_base64 = f"data:image/jpeg;base64,{img_str}"
            except Exception as e:
                print(f"Error processing category image: {e}")
        
        super().save(*args, **kwargs)


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
    image_base64 = models.TextField(blank=True, null=True, verbose_name="Rasm (Base64)")
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

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)
                # Optimize image for DB storage (max 800px width/height for products)
                img.thumbnail((800, 800))
                
                buffer = BytesIO()
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(buffer, format="JPEG", quality=75)
                
                img_str = base64.b64encode(buffer.getvalue()).decode()
                self.image_base64 = f"data:image/jpeg;base64,{img_str}"
            except Exception as e:
                print(f"Error processing product image: {e}")
        
        super().save(*args, **kwargs)
