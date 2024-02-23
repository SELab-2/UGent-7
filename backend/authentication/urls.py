from django.urls import path
from authentication.views import auth_view

urlpatterns = [
    path('hello', auth_view.hello)
]