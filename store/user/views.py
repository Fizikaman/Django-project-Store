from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm

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


def registration(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем с успешной регистрацией!')
            return HttpResponseRedirect(reverse('user:login'))

    context = {'form': form}
    return render(request, 'user/registration.html', context)


def profile(request):
    form = UserProfileForm(instance=request.user)

    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))

    context = {'title':'Store - Профиль', 'form':form}
    return render(request, 'user/profile.html', context)


def logout(requset):
    auth.logout(requset)
    return HttpResponseRedirect(reverse('index'))