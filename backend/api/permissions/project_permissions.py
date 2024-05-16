from api.permissions.role_permissions import (is_assistant, is_student,
                                              is_teacher)
from authentication.models import User
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class ProjectPermission(BasePermission):
    """Permission class for project related endpoints"""

    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general project endpoint."""
        user: User = request.user

        # We only allow teachers and assistants to create new projects.
        return is_teacher(user) or is_assistant(user)

    def has_object_permission(self, request: Request, view: ViewSet, project) -> bool:
        """Check if user has permission to view a detailed project endpoint"""
        user: User = request.user
        course = project.course
        teacher_or_assistant = is_teacher(user) and user.teacher.courses.filter(id=course.id).exists() or \
            is_assistant(user) and user.assistant.courses.filter(id=course.id).exists()

        if request.method in SAFE_METHODS:
            # Users that are linked to the course can view the project.
            return teacher_or_assistant or (is_student(user) and user.student.courses.filter(id=course.id).exists())

        # We only allow teachers and assistants to modify specified projects.
        return teacher_or_assistant


class ProjectGroupPermission(BasePermission):
    """Permission class for project related group endpoints"""

    def has_object_permission(self, request: Request, view: ViewSet, project) -> bool:
        user: User = request.user
        course = project.course
        teacher_or_assistant = is_teacher(user) and user.teacher.courses.filter(id=course.id).exists() or \
            is_assistant(user) and user.assistant.courses.filter(id=course.id).exists()

        if request.method in SAFE_METHODS:
            # Users that are linked to the course can view the group.
            return teacher_or_assistant or (is_student(user) and user.student.courses.filter(id=course.id).exists())

        # We only allow teachers and assistants to create new groups.
        return teacher_or_assistant
