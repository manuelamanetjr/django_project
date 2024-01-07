from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Product(models.Model):
    PROD_NAME = models.CharField(max_length=100)
    PROD_DESCRIPTION = models. TextField()
    PROD_DATE_POSTED = models.DateTimeField(default = timezone.now)
    PROD_IMAGE = models.ImageField(default='default.png', upload_to='product_pics')
    PROD_QUANTITY = models.IntegerField(default=0)
    PROD_PRICE = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def __str__(self):
        return self.PROD_NAME
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.PROD_IMAGE.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.PROD_IMAGE.path)
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})
    
class PurchaseOrder(models.Model):
    ORD_EMPLOYEE = models.CharField(max_length=100)
    ORD_DATE_POSTED = models.DateTimeField(default=timezone.now)
    ORD_NAME = models.CharField(max_length=200)
    ORD_QUANTITY = models.IntegerField(default=0)
    ORD_PRICE = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    ORD_DESCRIPTION = models.TextField()

    def __str__(self):
        return self.ORD_NAME 
    
class Cart(models.Model):
    CART_ID = models.AutoField(primary_key=True)
    CART_QUANTITY = models.IntegerField(default=0)
    CART_DATE_ADDED = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart ID: {self.cart_id} - Product: {self.product.PROD_NAME}"
