from django.urls import path
from notifications.views import NotificationView

urlpatterns = [
    path("tmp/<str:user_id>/", NotificationView.as_view(), name="notification-detail"),
]
