from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from user import models
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = models.User
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')
    title = 'Store - Регистрация'
    success_message = 'Вы успешно зарегистрированы!'


class UserProfileView(TitleMixin, UpdateView):
    model = models.User
    template_name = 'user/profile.html'
    form_class = UserProfileForm
    title = 'Store - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('user:profile', args=(self.object.id,))


    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.select_related('user', 'product').filter(user=self.object)
        return context