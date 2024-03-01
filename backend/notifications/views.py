from __future__ import annotations

from typing import List

from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


# TODO: Give admin access to everything
class NotificationPermission(BasePermission):
    # The user can only access their own notifications
    # An admin can access all notifications
    def has_permission(self, request: Request, view: NotificationView) -> bool:
        return view.kwargs.get("user_id") == request.user.id


class NotificationView(APIView):
    permission_classes: List[BasePermission] = [IsAuthenticated, NotificationPermission]

    def get(self, request: Request, user_id: str) -> Response:
        notifications = Notification.objects.filter(user=user_id)
        serializer = NotificationSerializer(
            notifications, many=True, context={"request": request}
        )

        return Response(serializer.data)

    # Mark all notifications as read for the user
    def post(self, request: Request, user_id: str) -> Response:
        notifications = Notification.objects.filter(user=user_id)
        notifications.update(is_read=True)

        return Response(status=HTTP_200_OK)
