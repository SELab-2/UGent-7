from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


# TODO: Give admin access to everything
class NotificationPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return view.kwargs.get("user_id") == request.user.id


class NotificationView(APIView):
    permission_classes = [IsAuthenticated, NotificationPermission]

    def get(self, request, user_id):
        notifications = Notification.objects.filter(user=user_id)
        serializer = NotificationSerializer(
            notifications, many=True, context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request, user_id):
        notifications = Notification.objects.filter(user=user_id)
        notifications.update(is_read=True)

        return Response(status=HTTP_200_OK)
