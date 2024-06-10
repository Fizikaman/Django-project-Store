from typing import Iterable

import stripe
from django.db import models

from store.settings import STRIPE_SECRET_KEY
from user.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert, force_update, using, update_fields)
    
    def create_stripe_product_price(self):
         stripe_product = stripe.Product.create(name=self.name)
         stripe_product_price = stripe.Price.create(
             product=stripe_product['id'],
             unit_amount=round(self.price * 100),
             currency='rub',
         )
         return stripe_product_price


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)
    
    def total_quantity(self):
        return sum(basket.quantity for basket in self)
    
    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                    'price': basket.product.stripe_product_price_id,
                    'quantity': basket.quantity,
                }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self) -> str:
        return f"Корзина для {self.user.username} | Продукт: {self.product}" 
    
    def sum(self):
        return self.product.price * self.quantity
    
    def to_json(self):
         basket_item = {
             'product_name': self.product.name,
             'quantity': self.quantity,
             'price': float(self.product.price),
             'sum': float(self.sum())
         }
         return basket_item