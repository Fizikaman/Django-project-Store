import stripe
from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from orders.forms import OrderForms
from common.views import TitleMixin
from store.settings import STRIPE_SECRET_KEY, DOMAIN_NAME

stripe.api_key = STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForms
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1PP23tP4xKVB7vS2OZgbTUxa',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(DOMAIN_NAME, reverse('orders:order_canceled')),
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)