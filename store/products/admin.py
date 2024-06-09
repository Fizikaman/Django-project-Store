from django.contrib import admin

from products import models

# Register your models here.

admin.site.register(models.ProductCategory)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'quantity',
        'category',
    ]
    fields = [
        'image',
        'name',
        'description',
        ('price', 'quantity'),
        'stripe_product_price_id',
        'category',
    ]
    readonly_fields = ['description']
    search_fields = ['name']
    ordering = ['-name']


class BasketAdmin(admin.TabularInline):
    model = models.Basket
    fields = [
        'product',
        'quantity',
        'created',
    ]
    extra = 0
    readonly_fields = ['created']
