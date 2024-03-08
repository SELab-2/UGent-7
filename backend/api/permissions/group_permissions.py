from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from authentication.models import User
from api.models.teacher import Teacher
from api.models.assistant import Assistant
from api.models.student import Student


class GroupPermission(BasePermission):

    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general group endpoint."""
        user: User = request.user

        # The general group endpoint is not accessible for any role.
        if request.method in SAFE_METHODS:
            return False

        # We only allow teachers and assistants to create new groups.
        return user.teacher.exists() or user.assistant.exists()

    def has_object_permission(self, request: Request, view: ViewSet, group) -> bool:
        """Check if user has permission to view a detailed group endpoint"""
        user: User = request.user
        course = group.course
        role: Teacher | Assistant | Student = user.teacher or user.assistant or user.student

        if request.method in SAFE_METHODS:
            # Users linked to the course linked to the group can fetch group details.
            return role is not None and \
                role.courses.filter(id=course.id).exists()

        # We only allow teachers and assistants to modify specified groups.
        teacher_assistant_role: Teacher | Assistant = user.teacher or user.assistant

        return teacher_assistant_role is not None and \
            teacher_assistant_role.courses.filter(id=course.id).exists()
