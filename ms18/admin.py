from django.contrib import admin
from .models import Product, PurchaseOrder, Requisition, RequestedProduct
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('ORD_EMPLOYEE', 'ORD_DATE_POSTED', 'ORD_NAME', 'ORD_QUANTITY', 'status')

    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model to ensure the model is saved
        super().save_model(request, obj, form, change)

        # Check if the order is approved
        if obj.status == PurchaseOrder.APPROVED:
            try:
                # Retrieve the corresponding product and update the inventory
                product = Product.objects.get(PROD_NAME=obj.ORD_NAME)
                original_quantity = product.PROD_QUANTITY
                product.PROD_QUANTITY += obj.ORD_QUANTITY
                print(f"Before update - Original Quantity: {original_quantity}, Order Quantity: {obj.ORD_QUANTITY}, Updated Quantity: {product.PROD_QUANTITY}")
                product.save()

                # Print statements for debugging
                print(f"Order {obj.id} approved. Inventory updated: {original_quantity} -> {product.PROD_QUANTITY}")
                print(f"Product details: {product.PROD_NAME}, Quantity: {product.PROD_QUANTITY}")

            except Product.DoesNotExist:
                print(f"Product {obj.ORD_NAME} does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}")

class RequisitionAdmin(admin.ModelAdmin):
    list_display = ('REQ_NAME', 'REQ_QUANTITY', 'REQ_STATUS')
    
    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model to ensure the model is saved
        super().save_model(request, obj, form, change)

        # Check if the order is approved
        if obj.status == PurchaseOrder.APPROVED:
            try:
                # Retrieve the corresponding product and update the inventory
                product = Product.objects.get(PROD_NAME=obj.REQ_PROD_NAME)
                original_quantity = product.PROD_QUANTITY
                product.PROD_QUANTITY -= obj.REQ_QUANTITY
                product.save()

                # Print statements for debugging
                print(f"Order {obj.id} approved. Inventory updated: {original_quantity} -> {product.PROD_QUANTITY}")
                print(f"Product details: {product.PROD_NAME}, Quantity: {product.PROD_QUANTITY}")

            except RequestedProduct.DoesNotExist:
                print(f"RequestedProduct for Requisition {obj.id} does not exist.")
            except Product.DoesNotExist:
                print(f"Product {obj.ORD_NAME} does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}")

class ProductAdmin(admin.ModelAdmin):
    # Customize the admin behavior for the Product model if needed
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(Requisition, RequisitionAdmin)
admin.site.register(RequestedProduct)