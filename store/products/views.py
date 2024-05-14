from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products import models

# Create your views here.

def index(request):
    return render(request, 'products/index.html')


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': models.Product.objects.select_related('category').all(),
        'categories': models.ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = models.Product.objects.get(id=product_id)
    baskets = models.Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        models.Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = models.Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])