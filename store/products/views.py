from typing import Any

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count
from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products import models


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductListView(TitleMixin, ListView):
    template_name = 'products/products.html'
    model = models.Product
    queryset = models.Product.objects.all()
    paginate_by = 3
    title = 'Store - Каталог'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ProductListView, self).get_context_data(**kwargs)
        categories = cache.get('categories')
        if not categories:
            context['categories'] = models.ProductCategory.objects.annotate(product_count=Count('product')).all()
            cache.set('categories', context['categories'], 60)
        else:
            context['categories'] = categories
        return context
    
    def get_cache_key(self) -> str:
        category_id = self.kwargs.get('category_id')
        return f'queryset_cache_{self.__class__.__name__}_{category_id}'

    def get_queryset(self) -> QuerySet[Any]:
        cache_key = self.get_cache_key()
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = self.queryset.select_related('category').all()
            category_id = self.kwargs.get('category_id')
            if category_id:
                queryset = queryset.filter(category_id=category_id)
            cache.set(cache_key, queryset, timeout=300)  # Cache timeout in seconds

        return queryset


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