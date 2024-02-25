from django.urls import path
from authentication.views import login, logout, validate, whoami

urlpatterns = [
    path('login', login, name='auth.login'),
    path('validate', validate, name='auth.validate'),
    path('whoami', whoami, name='auth.whoami'),
    path('logout', logout, name='auth.logout')
]