from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, SupplierListView
from .views import add_supplier_to_product
from . import views


urlpatterns = [
    path('', ProductListView.as_view(), name='ms18-home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:cart_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path('add-supplier-to-product/<int:product_id>/', add_supplier_to_product, name='add-supplier-to-product'),
   #path('clear-cart/', views.clear_cart, name='clear-cart'),
   #path('about/cart/', views.cart_view, name='about-cart'),  # Add a URL pattern for the about/cart page
    path('about/', views.about, name='ms18-about'),
]
