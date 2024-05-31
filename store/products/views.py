from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView 

from products import models



class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = 'Store'
        return context


class ProductListView(ListView):
    template_name = 'products/products.html'
    model = models.Product
    queryset = models.Product.objects.all()
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Store - Каталог'
        context['categories'] = models.ProductCategory.objects.annotate(product_count=Count('product')).all()
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = self.queryset.select_related('category').all()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


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