from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from authentication.models import User
from api.permissions.role_permissions import is_student, is_assistant, is_teacher
from api.models.course import Course


class CoursePermission(BasePermission):
    """Permission class used as default policy for course endpoints."""
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general course endpoint."""
        user: User = request.user

        # Logged-in users can fetch course information.
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # Only teachers can create courses.
        return is_teacher(user)

    def has_object_permission(self, request: Request, view: ViewSet, course: Course) -> bool:
        """Check if user has permission to view a detailed course endpoint"""
        user: User = request.user

        # Logged-in users can fetch course details.
        if request.method in SAFE_METHODS:
            return user.is_authenticated

        # We only allow teachers and assistants to modify their own courses.
        return is_teacher(user) and user.teacher.courses.contains(course) or \
            is_assistant(user) and user.assistant.courses.contains(course)


class CourseAssistantPermission(CoursePermission):
    """Permission class for assistant related endpoints."""
    def has_object_permission(self, request: Request, view: ViewSet, course: Course) -> bool:
        user: User = request.user

        # Logged-in users can fetch course assistants.
        if request.method in SAFE_METHODS:
            return user.is_authenticated

        # Only teachers can modify assistants of their own courses.
        return is_teacher(user) and user.teacher.courses.contains(course)


class CourseStudentPermission(CoursePermission):
    """Permission class for student related endpoints."""
    def has_object_permission(self, request: Request, view: ViewSet, course: Course):
        user: User = request.user

        # Logged-in users can fetch course students.
        if request.method in SAFE_METHODS:
            return user.is_authenticated

        # Only students can add or remove themselves from a course.
        if is_student(user) and request.data.get("id") == user.id:
            return True

        # Teachers and assistants can add and remove any student.
        return super().has_object_permission(request, view, course)


class CourseProjectPermission(CoursePermission):
    """Permission class for project related endpoints."""
    def has_object_permission(self, request: Request, view: ViewSet, course: Course):
        user: User = request.user

        # Logged-in users can fetch course projects.
        if request.method in SAFE_METHODS:
            return user.is_authenticated

        # Teachers and assistants can modify projects.
        return super().has_object_permission(request, view, course)
