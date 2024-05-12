from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from user import models


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите имя пользователя',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите пароль',
    }))

    class Meta:
        model = models.User
        fields = [
            'username',
            'password',
        ]


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите фамилию',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите имя пользователя',
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите электронную почту',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control py-4', 'placeholder':'Введите пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control py-4', 'placeholder':'Подтвердите пароль',
    }))


    class Meta:
        model = models.User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4'}))
    username= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4', 'readonly':True}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'custom-file-label'}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4', 'readonly':True}))

    class Meta:
        model = models.User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'image',
        ]