from django import forms

from orders.models import Order


class OrderForms(forms.ModelForm)
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'email',
            'address',
        )