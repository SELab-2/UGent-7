from django.urls import path
from authentication import views

urlpatterns = [
    path('hello', views.hello)
]
