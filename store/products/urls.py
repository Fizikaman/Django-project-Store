from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.products, name='index'),
    path('category/<int:category_id>/', views.products, name='category'),
    path('baskets/add/<int:product_id>', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>', views.basket_remove, name='basket_remove'),
]
