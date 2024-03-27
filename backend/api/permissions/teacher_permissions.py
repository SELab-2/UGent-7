from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from authentication.models import User


# (Almost) same as StudentPermission
class TeacherPermission(IsAuthenticated):

    def has_permission(self, request, view):
        """Check if user has permission to view a general Teacher endpoint."""
        if view.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """Check if user has permission to view a detailed group endpoint"""
        user: User = request.user
        return request.method in SAFE_METHODS and user.id == request.user.id
