from django.urls import path
from api.views import logic_view

urlpatterns = [
    path('hello', logic_view.hello)
]
