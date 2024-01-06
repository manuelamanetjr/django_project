from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Product(models.Model):
    title = models.CharField(max_length=100)
    content = models. TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='product_pics')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})
    

class PurchaseOrder(models.Model):
    employee = models.CharField(max_length=100)
    date_posted = models.DateField()
    title = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    content = models.TextField()

    def __str__(self):
        return self.title  # Return a string representation of the object
