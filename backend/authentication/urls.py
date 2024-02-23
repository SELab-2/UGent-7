from django.urls import path
from authentication.views import auth

urlpatterns = [
    path('login', auth.login),
    path('logout', auth.logout)
]