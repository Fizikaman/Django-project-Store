from django.shortcuts import render
from products import models

# Create your views here.

def index(request):
    return render(request, 'products/index.html')


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': models.Product.objects.all(),
        'categories': models.ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)


