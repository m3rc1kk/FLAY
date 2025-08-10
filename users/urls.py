from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', LoginView.as_view(), name='auth'),
    path('login/', telegram_auth, name='login'),
]
