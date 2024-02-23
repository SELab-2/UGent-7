from django.urls import path
from logic.views import logic_view

urlpatterns = [
    path('hello', logic_view.hello)
]
