from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from  django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, PurchaseOrder, Cart, Supplier, RequestedProduct, Requisition
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def home(request):
    context = {
        'products': Product.objects.all(),
        'suppliers': Supplier.objects.all()
    }
    return render(request, 'ms18/home.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'ms18/home.html'
    context_object_name = 'products'
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'ms18/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Check if the product has a supplier before accessing its attributes
            if self.object.supplier:
                context['supplier_name'] = self.object.supplier.SUPPLIER_NAME
            else:
                context['supplier_name'] = None
        except Supplier.DoesNotExist:
            # Handle the case where the supplier does not exist
            raise Http404("Supplier does not exist for this product.")

        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['PROD_NAME', 'PROD_DESCRIPTION', 'PROD_IMAGE', 'PROD_QUANTITY', 'PROD_PRICE', 'supplier']

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    
class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    fields = ['SUPPLIER_NAME', 'SUPPLIER_ADDRESS', 'SUPPLIER_PHONE']
    success_url = '/'

    def form_valid(self, form):
        # You can add any additional logic here before saving the form
        return super().form_valid(form)
    
    def clean_PROD_PRICE(self):
        prod_price = self.cleaned_data.get('PROD_PRICE')

        # Check if the price is a positive floating-point number
        if prod_price is not None and prod_price <= 0:
            raise ValidationError('Price must be a positive number.')

        return prod_price
    
    
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['PROD_NAME', 'PROD_DESCRIPTION', 'PROD_PRICE', 'PROD_IMAGE']
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        product = self.get_object()
        return True
    
    def clean_PROD_PRICE(self):
        prod_price = self.cleaned_data['PROD_PRICE']

        # Check if the price is a positive floating-point number
        if prod_price <= 0:
            raise ValidationError('Price must be a positive number.')

        return prod_price
        

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.employee:
            return True
        return False

@login_required
def about(request):
     # Retrieve products ordered by date_posted in descending order (newest first)
    products = Product.objects.all()
    return render(request, 'ms18/about.html', {'products': products})
    
    
from .models import Cart

def add_to_cart(request):
    if request.user.is_authenticated and request.method == 'POST':
        selected_products = []
        for key, value in request.POST.items():
            if key.startswith('quantity_') and int(value) > 0:
                product_id = key.split('_')[1]
                try:
                    product = Product.objects.get(pk=product_id)

                    # Calculate the order price based on the associated product's price
                    order_price = product.PROD_PRICE

                    selected_products.append(product)

                    # Create a PurchaseOrder for the selected product with a pending status
                    order = PurchaseOrder.objects.create(
                        ORD_EMPLOYEE=request.user.username,
                        ORD_DATE_POSTED=timezone.now(),
                        ORD_NAME=product.PROD_NAME,
                        ORD_QUANTITY=int(value),
                        ORD_DESCRIPTION=product.PROD_DESCRIPTION,
                        ORD_PRICE=order_price,  # Set the order price based on the product's price
                        status=PurchaseOrder.PENDING  # Set the initial status to pending
                    )

                    # Create a Cart entry for the selected product and purchase order
                    Cart.objects.create(
                        CART_QUANTITY=int(value),
                        CART_DATE_ADDED=timezone.now(),
                        user=request.user,
                        product=product,
                        PurchaseOrder=order
                    )

                except Product.DoesNotExist:
                    messages.error(request, f"Product with ID {product_id} does not exist.")
                except Exception as e:
                    messages.error(request, f"An error occurred while adding product with ID {product_id}: {e}")

        if selected_products:
            messages.success(request, 'Items added to orders successfully! Pending admin approval.')

        return redirect('cart')  # Redirect to a 'cart' view or another appropriate view
    else:
        messages.error(request, 'Please log in to add items to the orders.')
        return redirect('login')  # Redirect to the login page if the user is not authenticated


def cart(request):
    user = request.user
    cart_items = PurchaseOrder.objects.filter(ORD_EMPLOYEE=user.username)

    overall_total = 0

    for order in cart_items:
        order.total_price = order.ORD_QUANTITY * order.ORD_PRICE
        overall_total += order.total_price

    context = {
        'cart_items': cart_items,
        'overall_total': overall_total,
    }
    return render(request, 'ms18/cart.html', context)

    
class SupplierListView(ListView):
    model = Supplier
    template_name = 'ms18/supplier_list.html'
    context_object_name = 'suppliers'
    
def add_supplier_to_product(request, product_id):
    if request.method == 'POST':
        supplier_name = request.POST.get('supplier_name')

        # Assuming you have a 'supplier' field in your Product model
        product = Product.objects.get(pk=product_id)
        product.supplier = supplier_name
        product.save()

        messages.success(request, f'Supplier "{supplier_name}" added to {product.PROD_NAME}.')
        return redirect(reverse('product-detail', args=[product_id]))


def add_product(request):
    if request.method == 'POST':
        form = ProductUpdateView(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page or another view
    else:
        form = ProductUpdateView()

    return render(request, 'your_template.html', {'form': form})

def admin_review_orders(request):
    # Retrieve pending orders for admin review
    pending_orders = PurchaseOrder.objects.filter(status=PurchaseOrder.PENDING)

    context = {
        'pending_orders': pending_orders
    }
    return render(request, 'ms18/admin_review_orders.html', context)


@transaction.atomic
def admin_approve_order(request, order_id):
    order = get_object_or_404(PurchaseOrder, id=order_id)

    # Update the status to Approved
    order.status = PurchaseOrder.APPROVED
    order.save()

    try:
        product = Product.objects.get(PROD_NAME=order.ORD_NAME)
        original_quantity = product.PROD_QUANTITY
        product.PROD_QUANTITY += order.ORD_QUANTITY
        product.save()

        # Print statements for debugging
        print(f"Order {order.id} approved. Inventory updated: {original_quantity} -> {product.PROD_QUANTITY}")
        print(f"Product details: {product.PROD_NAME}, Quantity: {product.PROD_QUANTITY}")
        messages.success(request, f'Order {order.id} approved. Inventory updated.')
    except Product.DoesNotExist:
        messages.error(request, f"Product {order.ORD_NAME} does not exist.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")

    return redirect('admin_review_orders')


@user_passes_test(lambda u: u.is_staff)
def admin_reject_order(request, order_id):
    order = get_object_or_404(PurchaseOrder, id=order_id)
    order.status = PurchaseOrder.REJECTED
    order.save()
    messages.success(request, f'Order {order.id} rejected.')
    return redirect('admin_review_orders')


def inventory(request):
    products = Product.objects.all()

    for product in products:
        print(f"Product: {product.PROD_NAME}, Quantity: {product.PROD_QUANTITY}")

    return render(request, 'ms18/home.html', {'products': products})


def generate_receipt(request):
    user = request.user
    cart_items = PurchaseOrder.objects.filter(ORD_EMPLOYEE=user.username)

    # Customize the receipt content based on your requirements
    receipt_content = f"Orders from {user.username}\n\n"
    overall_total = 0
    
    for order in cart_items:
        total_price = order.ORD_QUANTITY * order.ORD_PRICE
        overall_total += total_price

        receipt_content += f"Order {order.id}:\n"
        receipt_content += f"Product: {order.ORD_NAME}\n"
        receipt_content += f"Quantity: {order.ORD_QUANTITY}\n"
        receipt_content += f"Unit Price: ₱{order.ORD_PRICE}\n"
        receipt_content += f"Status: {order.status}\n\n"
        receipt_content += f"Overall Total: ₱{overall_total}"

    response = HttpResponse(receipt_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="order.txt"'

    return response













@login_required
def about(request):
     # Retrieve products ordered by date_posted in descending order (newest first)
    products = Product.objects.all()
    return render(request, 'ms18/about.html', {'products': products})

    

def add_requisitions(request):
    context = {
        'products': Product.objects.all(),
        'suppliers': Supplier.objects.all()
    }
    return render(request, 'ms18/add_requisition.html', context)

def add_to_req(request):
    if request.method == 'POST':
        selected_supplier_id = request.POST.get('hidden_supplier_id')
        search_supplier_name = request.POST.get('search_supplier_name', '')  # Example: retrieving from POST data
        if not selected_supplier_id:
            messages.error(request, "No supplier selected.")
            return redirect('view-requisitions')

        user_instance, created = User.objects.get_or_create(username=request.user.username)

        try:
            supplier = Supplier.objects.get(pk=selected_supplier_id)
        except Supplier.DoesNotExist:
            messages.error(request, f"Supplier with ID {selected_supplier_id} does not exist.")
            return redirect('view-requisitions')

        requisition = Requisition.objects.create(
            REQ_EMPLOYEE=user_instance,
            supplier=supplier,
        )

        products_added = []

        for key, value in request.POST.items():
            if key.startswith('quantity_') and int(value) > 0:
                product_id = key.split('_')[1]
                try:
                    product = Product.objects.get(pk=product_id)
                    quantity = request.POST.get(f'quantity_{product.id}', 0)
                    products_added.append(product.PROD_NAME)

                    # Create RequestedProduct without assigning Requisition
                    requested_product = RequestedProduct.objects.create(
                        REQUESTED_PRODUCT_NAME=product.PROD_NAME,
                        REQUESTED_PRODUCT_QUANTITY=quantity,
                        Product=product,
                    )

                    # Assign the Requisition to the RequestedProduct
                    requested_product.Requisition = requisition
                    requested_product.save()

                except Product.DoesNotExist:
                    messages.error(request, f"Product with ID {product_id} does not exist.")
                except Exception as e:
                    messages.error(request, f"An error occurred while adding product with ID {product_id}: {e}")

        if products_added:
            requisition.save()
            messages.success(request, f'Products ({", ".join(products_added)}) added to Requisition successfully!')

        else:
            messages.warning(request, 'No products were added to the Requisition.')

    return redirect('view-requisitions')


def view_requisitions(request):
    requisitions = Requisition.objects.order_by('-REQ_ID')
    context = {
        'Requisition': requisitions,
    }
    return render(request, 'ms18/requisition_view.html', context)

def approve_requisition(request, req_id):
    requisition = Requisition.objects.get(pk=req_id)
    requisition.approve()  # Implement a method in your Requisition model to handle approval

    # Update product quantities
    for requested_product in requisition.requestedproduct_set.all():
        requested_product.Product.PROD_QUANTITY -= requested_product.REQUESTED_PRODUCT_QUANTITY
        requested_product.Product.save()

    messages.success(request, f'Requisition {req_id} approved successfully!')
    return redirect('view-requisitions')


def reject_requisition(request, req_id):
    requisition = Requisition.objects.get(pk=req_id)
    requisition.reject()  # Implement a method in your Requisition model to handle rejection
    messages.success(request, f'Requisition {req_id} rejected successfully!')
    return redirect('view-requisitions')


def RequestedProdView(request, pk):
    requisition = get_object_or_404(Requisition, REQ_ID=pk)
    requested_prods = RequestedProduct.objects.filter(Requisition=requisition)
    
    context = {
        'requested_prods': requested_prods,
    }
    return render(request, 'ms18/requested_prod_view.html', context)
