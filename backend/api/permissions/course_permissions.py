from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from authentication.models import User
from api.models.teacher import Teacher
from api.models.assistant import Assistant
from api.models.course import Course


class CoursePermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general course endpoint."""
        user: User = request.user

        if request.method in SAFE_METHODS:
            # Logged-in users can fetch course lists.
            return request.user.is_authenticated

        # We only allow teachers to create new courses.
        return user.teacher.exists()

    def has_object_permission(self, request: Request, view: ViewSet, course: Course) -> bool:
        """Check if user has permission to view a detailed course endpoint"""
        user: User = request.user

        if request.method in SAFE_METHODS:
            # Logged-in users can fetch course details.
            return request.user.is_authenticated

        # We only allow teachers and assistants to modify specified courses.
        role: Teacher|Assistant = user.teacher or user.assistant

        return role is not None and \
            role.courses.filter(id=course.id).exists()