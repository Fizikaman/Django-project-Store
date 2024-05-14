from django.contrib import admin

from products import models
# Register your models here.

admin.site.register(models.Product)
admin.site.register(models.ProductCategory)

class BasketAdmin(admin.TabularInline):
    model = models.Basket
    fields = [
        'product',
        'quantity',
        'created',
    ]
    extra = 0
    readonly_fields = ['created']