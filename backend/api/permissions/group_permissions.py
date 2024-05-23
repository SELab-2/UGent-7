from api.models.assistant import Assistant
from api.models.group import Group
from api.models.project import Project
from api.models.student import Student
from api.models.teacher import Teacher
from api.permissions.role_permissions import (is_assistant, is_student,
                                              is_teacher)
from authentication.models import User
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet


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
        if is_student(user) and request.data.get("student") == user.id:  # type: ignore
            # Make sure the student is actually part of the course.
            return user.student.courses.filter(id=course.id).exists()

        # Teachers and assistants can add and remove any student from a group
        return teacher_or_assistant


class GroupSubmissionPermission(BasePermission):
    """Permission class for submission related group endpoints"""

    def had_object_permission(self, request: Request, _: ViewSet, group: Group) -> bool:
        """Check if user has permission to view a detailed group submission endpoint"""
        user = request.user
        course = group.project.course

        # Check if the user is a teacher that has the course linked to the project.
        teacher = Teacher.objects.filter(id=user.id).first()
        assistant = Assistant.objects.filter(id=user.id).first()
        student = Student.objects.filter(id=user.id).first()

        # Get the individual permission clauses.
        teacher_permission = teacher is not None and teacher.courses.filter(id=course.id).exists()
        assistant_permission = assistant is not None and assistant.courses.filter(id=course.id).exists()
        student_permission = student is not None and student.groups.filter(id=group.id).exists()

        return teacher_permission or assistant_permission or student_permission
