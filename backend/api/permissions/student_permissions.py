from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.permissions.role_permissions import is_teacher
from authentication.models import User

class StudentPermission(BasePermission):

    # Dit is garbage omdat altijd de has_permission eerst moet slagen.

    # IsAdminUser is already defined but because of DRF has_permissions must be present
    # https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
    def has_permission(self, request, view):
        """Check if user has permission to view a general student endpoint."""
        user: User = request.user
        if view.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
            return user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        """Check if user has permission to view a detailed group endpoint"""
        user: User = request.user
        return request.method in SAFE_METHODS and (user.id == request.user.id or is_teacher(user))
