from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from api.permissions.role_permissions import is_teacher
from authentication.models import User


class StudentPermission(IsAuthenticated):

    def has_permission(self, request, view):
        """Check if user has permission to view a general student endpoint."""
        return view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        """Check if user has permission to view a detailed group endpoint"""
        user: User = request.user
        return request.method in SAFE_METHODS and (user.id == request.user.id or is_teacher(user))
