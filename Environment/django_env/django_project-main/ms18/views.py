from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, PurchaseOrder, Cart
from django.contrib import messages
from django.utils import timezone



def home(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'ms18/home.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'ms18/home.html'
    context_object_name = 'products'
    ordering = ['-PROD_DATE_POSTED']
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    
    
class ProductDetailView(DetailView):
    model = Product
    
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['PROD_NAME', 'PROD_DESCRIPTION', 'PROD_IMAGE', 'PROD_QUANTITY', 'PROD_PRICE']
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    

    
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['PROD_NAME', 'PROD_DESCRIPTION', 'PROD_IMAGE']
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.employee:
            return True
        return False


def about(request):
     # Retrieve products ordered by date_posted in descending order (newest first)
    products = Product.objects.order_by('-PROD_DATE_POSTED')
    return render(request, 'ms18/about.html', {'products': products})
    
    
def add_to_cart(request):
    if request.user.is_authenticated and request.method == 'POST':
        selected_products = []
        for key, value in request.POST.items():
            if key.startswith('quantity_') and int(value) > 0:
                product_id = key.split('_')[1]
                try:
                    product = Product.objects.get(pk=product_id)
                    selected_products.append(product)
                    # Create a PurchaseOrder for the selected product
                    PurchaseOrder.objects.create(
                        ORD_EMPLOYEE=request.user.username,
                        ORD_DATE_POSTED=timezone.now(),
                        ORD_NAME=product.PROD_NAME,
                        ORD_QUANTITY=int(value),
                        ORD_DESCRIPTION=product.PROD_DESCRIPTION
                    )
                except Product.DoesNotExist:
                    messages.error(request, f"Product with ID {product_id} does not exist.")
                except Exception as e:
                    messages.error(request, f"An error occurred while adding product with ID {product_id}: {e}")
        
        if selected_products:
            messages.success(request, 'Items added to cart successfully!')
        
        return redirect('cart')  # Redirect to a 'cart' view or another appropriate view
    else:
        messages.error(request, 'Please log in to add items to the cart.')
        return redirect('login')  # Redirect to the login page if the user is not authenticated
 
    
def cart(request):
    # Retrieve items in the cart based on the logged-in user
    user = request.user
    cart_items = PurchaseOrder.objects.filter(ORD_EMPLOYEE=user.username)

    # Print out cart_items for inspection
    print(cart_items)

    context = {
        'cart_items': cart_items
    }
    return render(request, 'ms18/cart.html', context)

def remove_from_cart(request, cart_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(PurchaseOrder, pk=cart_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart!")
        return redirect('cart')
    else:
        return HttpResponseBadRequest("Invalid request method")