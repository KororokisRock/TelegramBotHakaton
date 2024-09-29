from django.contrib.auth import views
from django.urls import path
from . import views as v

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', v.profile, name='profile'),
    path('registr/', v.reg, name='reg'),
]