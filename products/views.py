from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product


# Create your views here.

class DetailProduct(DetailView):
    context_object_name = "product"
    model = Product
    template_name = "products/detail_product.html"
