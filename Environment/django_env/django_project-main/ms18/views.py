from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, PurchaseOrder



def home(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'ms18/home.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'ms18/home.html'
    context_object_name = 'products'
    ordering = ['-date_posted']
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    
    
class ProductDetailView(DetailView):
    model = Product
    
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'content', 'image']
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.employee:
            return True
        return False

    
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'content', 'image']
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.employee:
            return True
        return False

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
    products = Product.objects.order_by('-date_posted')

    return render(request, 'ms18/about.html', {'products': products})


def purchase_order(request):
   if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1] 
                quantity = value
                product = get_object_or_404(Product, pk=product_id)  # Fetch the product

                PurchaseOrder.objects.create(
                    employee=request.user.username,
                    quantity=quantity,
                    title=product.title,  # Assuming 'title' is a field in PurchaseOrder
                    date_posted=product.date_posted,  # Assuming 'date_posted' is a field in PurchaseOrder
                    # Assign other relevant fields from the product to PurchaseOrder
                    # content=product.content,
                )
                return HttpResponseRedirect('/success/')
        return render(request, 'ms18/about.html')
    
def add_to_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})  # Get the cart from the session or create a new empty cart
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)
                if quantity > 0:
                    product = get_object_or_404(Product, id=product_id)
                    cart_item = {
                        'title': product.title,
                        'quantity': quantity,
                        # Add other product details to the cart if needed
                    }
                    cart[product_id] = cart_item
        request.session['cart'] = cart  # Update the cart in the session
        return HttpResponseRedirect('/cart/')  # Redirect to the cart page
    return render(request, 'ms18/about.html')  # Render the same page if not a POST request

def cart_view(request):
    cart = request.session.get('cart', {})  # Retrieve cart information from the session
    return render(request, 'ms18/cart.html', {'cart': cart})