from django.contrib import admin
from .models import Product, PurchaseOrder

admin.site.register(Product)
admin.site.register(PurchaseOrder)