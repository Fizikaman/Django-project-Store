from django.urls import path
from django.contrib.auth.decorators import login_required

from user import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', login_required(views.UserProfileView.as_view()), name='profile'),
    path('logout/', views.logout, name='logout'),
]