from urllib.parse import unquote

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from user import models
from user.forms import UserLoginForm, UserProfileForm, UserRegistrationForm


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
    

class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение почты'
    template_name = 'user/email_verification.html'

    def get(self, request, *args, **kwargs):
        email = unquote(kwargs['email'])
        code = kwargs['code']
        user = models.User.objects.get(email=email)
        email_verification = models.EmailVerification.objects.filter(user=user, code=code)

        if email_verification.exists() and email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
        

def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))