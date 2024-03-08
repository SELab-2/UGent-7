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

        # The general group endpoint that lists all groups is not accessible for any role.
        if view.action == "list":
            return False
        elif request.method in SAFE_METHODS:
            return True

        # We only allow teachers and assistants to create new groups.
        return hasattr(user, "teacher") and user.teacher.exists() or hasattr(user, "assistant") and user.assistant.exists()

    def has_object_permission(self, request: Request, view: ViewSet, group) -> bool:
        """Check if user has permission to view a detailed group endpoint"""
        user: User = request.user
        course = group.project.course
        teacher_assistant_role: Teacher | Assistant = hasattr(user, "teacher") and user.teacher or \
             hasattr(user, "assistant") and user.assistant

        if request.method in SAFE_METHODS:
            role: Teacher | Assistant | Student = teacher_assistant_role or hasattr(user, "student") and user.student

            # Users linked to the course linked to the group can fetch group details.
            return role is not None and \
                role.courses.filter(id=course.id).exists()

        # We only allow teachers and assistants to modify specified groups.
        return teacher_assistant_role is not None and \
            teacher_assistant_role.courses.filter(id=course.id).exists()


class GroupStudentPermission(BasePermission):
    """Permission class for student-only group endpoints"""

    def has_object_permission(self, request: Request, view: ViewSet, group) -> bool:
        user: User = request.user
        course = group.project.course
        student: Student = user.student

        # We only allow students to join groups.
        return student is not None and \
            student.courses.filter(id=course.id).exists()
