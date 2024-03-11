from api.permissions.notification_permissions import NotificationPermission
from authentication.models import User
from authentication.serializers import UserSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"], permission_classes=[NotificationPermission])
    def notifications(self, request: Request, pk: str):
        notifications = Notification.objects.filter(user=pk)
        serializer = NotificationSerializer(
            notifications, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[NotificationPermission],
        url_path="notifications/read",
    )
    def read(self, request: Request, pk: str):
        notifications = Notification.objects.filter(user=pk)
        notifications.update(is_read=True)

        return Response(status=HTTP_200_OK)
