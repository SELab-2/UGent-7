from django.urls import path
from notifications.views import NotificationView, TestingView

# TODO: Remove test
urlpatterns = [
    path("tmp/<str:user_id>/", NotificationView.as_view(), name="notification-detail"),
    path("test/", TestingView.as_view(), name="notification-test"),
]
