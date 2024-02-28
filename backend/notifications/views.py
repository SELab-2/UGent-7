from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework.viewsets import ModelViewSet


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
