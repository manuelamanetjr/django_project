from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from . import views

urlpatterns = [
    path('', ProductListView.as_view(), name='ms18-home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('purchase-order/', views.purchase_order, name='purchase-order'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_view, name='cart'),
    path('about/', views.about, name='ms18-about'),
]
