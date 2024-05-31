from typing import Any
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from products import models



class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = 'Store'
        return context


def products(request, category_id=None, page_number=1):
    products = models.Product.objects.select_related('category').all()

    if category_id:
        products = models.Product.objects.select_related('category').filter(category_id=category_id)

    categories = models.ProductCategory.objects.annotate(product_count=Count('product')).all()

    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Store - Каталог',
        'products': products_paginator,
        'categories': categories,
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