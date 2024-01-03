from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from . import views

urlpatterns = [
    path('', ProductListView.as_view(), name='ms18-home'),
    path('post/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('post/new/', ProductCreateView.as_view(), name='product-create'),
    path('post/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('post/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('about/', views.about, name='ms18-about'),
]
