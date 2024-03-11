from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class NotificationPermission(BasePermission):
    # The user can only access their own notifications
    # An admin can access all notifications
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        return view.kwargs.get("pk") == request.user.id or request.user.is_staff
