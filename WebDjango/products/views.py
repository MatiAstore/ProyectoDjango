from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from django.db.models import Q 

# Create your views here
class ProductListView(ListView):
    template_name = "index.html"
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs: Any): 
        context = super().get_context_data(**kwargs)
        context ["mensaje"] = "Productos"
        return context

class ProductDetailView(DetailView):
    model = Product 
    template_name = "products/product.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
class ProductSearchListView(ListView):
    template_name = "products/search.html"

    #filtra los productos cuyo valor sea similar al ingresado por el usuario
    def get_queryset(self):       
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)
    
    #obtiene el valor pedido por el usuario
    def query(self): 
        return self.request.GET.get('i')
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()

        return context