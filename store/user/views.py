from django.shortcuts import HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from urllib.parse import unquote

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
    

class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение почты'
    template_name = 'user/email_verification.html'

    def get(self, request, *args, **kwargs):
        email = unquote(kwargs['email'])
        code = kwargs['code']
        user = models.User.objects.get(email=email)
        email_verification = models.EmailVerification.objects.filter(user=user, code=code)
        print(f"email_verification: {email_verification}. email_verification: {email_verification.first().is_expired()}")
        if email_verification.exists() and email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))