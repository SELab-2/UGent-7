from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from api.models.student import Student
from api.permissions.role_permissions import is_teacher
from authentication.models import User


class StudentPermission(IsAuthenticated):

    def has_permission(self, request, view):
        """Check if user has permission to view a general student endpoint."""
        return True

    def has_object_permission(self, request, view, student: Student) -> bool:
        """Check if user has permission to view a detailed group endpoint"""
        user: User = request.user

        return request.method in SAFE_METHODS and (user.id == student.id or is_teacher(user))
