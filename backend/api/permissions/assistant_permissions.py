from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from authentication.models import User
from api.permissions.role_permissions import is_student, is_assistant, is_teacher
from api.models.course import Course


class AssistantPermission(BasePermission):
    """Permission class used as default policy for assistant endpoint."""
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general assistant endpoint."""
        user: User = request.user
        # Only admins and teachers can fetch all assistants.
        return request.method in SAFE_METHODS and is_teacher(user) 


    def has_object_permission(self, request: Request, view: ViewSet, course: Course) -> bool:
        """Check if user has permission to view a detailed assistant endpoint"""
        user: User = request.user

        # Logged-in users can fetch assistant details.
        return request.method in SAFE_METHODS and user.is_authenticated