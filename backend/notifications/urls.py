from notifications.views import NotificationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"", NotificationViewSet, basename="notification")

urlpatterns = router.urls
