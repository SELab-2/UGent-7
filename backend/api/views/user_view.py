from api.permissions.notification_permissions import NotificationPermission
from api.permissions.role_permissions import IsSameUser
from api.views.pagination.basic_pagination import BasicPagination
from authentication.models import User
from authentication.serializers import UserSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsSameUser]

    @action(detail=False)
    def search(self, request: Request) -> Response:
        self.pagination_class = BasicPagination

        search = request.query_params.get("search", "")
        username = request.query_params.get("username", "")
        email = request.query_params.get("email", "")

        queryset = self.get_queryset().filter(
            id__icontains=search,
            username__icontains=username,
            email__icontains=email
        )

        serializer = self.serializer_class(self.paginate_queryset(queryset), many=True, context={
            "request": request
        })

        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[NotificationPermission])
    def notifications(self, request: Request, pk: str):
        """Returns a list of notifications for the given user"""
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
        """Marks all notifications as read for the given user"""
        notifications = Notification.objects.filter(user=pk)
        notifications.update(is_read=True)

        return Response(status=HTTP_200_OK)
