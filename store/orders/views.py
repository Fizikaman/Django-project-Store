from django.views.generic.edit import CreateView

from orders.forms import OrderForms

class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForms