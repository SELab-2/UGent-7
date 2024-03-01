from django.urls import path
from notifications.views import NotificationView

urlpatterns = [path("<str:user_id>/", NotificationView.as_view())]
