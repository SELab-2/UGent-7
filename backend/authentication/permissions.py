from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class CASPermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet):
        """Check whether a user has permission in the CAS flow context."""
        return request.user.is_authenticated or view.action not in [
            'logout', 'whoami'
        ]