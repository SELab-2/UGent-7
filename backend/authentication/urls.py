from django.urls import path
from authentication.views import login, logout, validate

urlpatterns = [
    path('login', login, name='auth.login'),
    path('validate', validate, name='auth.validate'),
    path('logout', logout, name='auth.logout')
]