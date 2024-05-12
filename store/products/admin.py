from django.contrib import admin

from products import models
# Register your models here.

admin.site.register(models.Product)
admin.site.register(models.ProductCategory)