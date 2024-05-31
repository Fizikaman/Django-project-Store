from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from user import models

# Create your views here.

def login(request):
    form = UserLoginForm()

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))

    context = {'form': form}
    return render(request, 'user/login.html', context)



class UserRegistrationView(CreateView):
    model = models.User
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context['title'] = 'Store - Регистрация'
        return context


class UserProfileView(UpdateView):
    model = models.User
    template_name = 'user/profile.html'
    form_class = UserProfileForm
    

    def get_success_url(self):
        return reverse_lazy('user:profile', args=(self.object.id,))


    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.select_related('user', 'product').filter(user=self.object)
        return context


def logout(requset):
    auth.logout(requset)
    return HttpResponseRedirect(reverse('index'))