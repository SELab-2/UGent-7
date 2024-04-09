from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from authentication.models import User
from api.permissions.role_permissions import is_student, is_assistant, is_teacher


class GroupPermission(BasePermission):

    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general group endpoint."""
        user: User = request.user

        # The general group endpoint that lists all groups is not accessible for any role.
        if request.method in SAFE_METHODS:
            return True

        # We only allow teachers and assistants to create new groups.
        return is_teacher(user) or is_assistant(user)

    def has_object_permission(self, request: Request, view: ViewSet, group) -> bool:
        """Check if user has permission to view a detailed group endpoint"""
        user: User = request.user
        course = group.project.course
        teacher_or_assitant = is_teacher(user) and user.teacher.courses.filter(
            id=course.id).exists() or is_assistant(user) and user.assistant.courses.filter(id=course.id).exists()

        if request.method in SAFE_METHODS:
            # Users that are linked to the course can view the group.
            return teacher_or_assitant or (is_student(user) and user.student.courses.filter(id=course.id).exists())

        # We only allow teachers and assistants to modify specified groups.
        return teacher_or_assitant


class GroupStudentPermission(BasePermission):
    """Permission class for student related group endpoints"""

    def has_object_permission(self, request: Request, view: ViewSet, group) -> bool:
        user: User = request.user
        course = group.project.course
        teacher_or_assistant = is_teacher(user) and user.teacher.courses.filter(
            id=course.id).exists() or is_assistant(user) and user.assistant.courses.filter(id=course.id).exists()

        if request.method in SAFE_METHODS:
            # Users related to the course can view the students of the group.
            return teacher_or_assistant or (is_student(user) and user.student.courses.filter(id=course.id).exists())

        # Students can only add and remove themselves from a group.
        if is_student(user) and request.data.get("student") == user.id:
            # Make sure the student is actually part of the course.
            return user.student.courses.filter(id=course.id).exists()

        # Teachers and assistants can add and remove any student from a group
        return teacher_or_assistant


class GroupSubmissionPermission(BasePermission):
    """Permission class for submission related group endpoints"""

    def had_object_permission(self, request: Request, view: ViewSet, group) -> bool:
        user: User = request.user
        course = group.project.course
        teacher_or_assitant = is_teacher(user) and user.teacher.courses.filter(
            id=course.id).exists() or is_assistant(user) and user.assistant.courses.filter(id=course.id).exists()
        if request.method in SAFE_METHODS:
            # Users related to the group can view the submissions of the group
            return teacher_or_assitant or (is_student(user) and user.student.groups.filter(id=group.id).exists())

        # Student can only add submissions to their own group
        if is_student(user) and request.data.get("student") == user.id and view.action == "create":
            return user.student.course.filter(id=course.id).exists()

        # Removing a Submissions is not possible for teachers and assistants
