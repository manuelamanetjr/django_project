from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product



def home(request):
    context = {
        'posts': Product.objects.all()
    }
    return render(request, 'ms18/home.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'ms18/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
class ProductDetailView(DetailView):
    model = Product
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False

def about(request):
    return render(request, 'ms18/about.html', {'title': 'About'})