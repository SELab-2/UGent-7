from api.models.assistant import Assistant
from api.models.student import Student
from api.models.teacher import Teacher
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
        return is_teacher(request.user) or is_assistant(request.user) or request.method in SAFE_METHODS

    def has_object_permission(self, request: Request, view: ViewSet, project) -> bool:
        """Check if user has permission to view a detailed project endpoint"""
        user = request.user

        # Check if the user is a teacher that has the course linked to the project.
        teacher = Teacher.objects.filter(id=user.id).first()
        assistant = Assistant.objects.filter(id=user.id).first()
        student = Student.objects.filter(id=user.id).first()

        # Get the individual permission clauses.
        teacher_permission = teacher is not None and teacher.courses.filter(id=project.course.id).exists()
        assistant_permission = assistant is not None and assistant.courses.filter(id=project.course.id).exists()
        student_permission = student is not None and student.courses.filter(id=project.course.id).exists()

        if request.method in SAFE_METHODS:
            return teacher_permission or assistant_permission or student_permission

        return teacher_permission or assistant_permission


class ProjectGroupPermission(BasePermission):
    """Permission class for project related group endpoints"""
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general project group endpoint."""
        return is_teacher(request.user) or is_assistant(request.user) or request.method in SAFE_METHODS

    def has_object_permission(self, request: Request, view: ViewSet, project) -> bool:
        """Check if user has permission to view a detailed project group endpoint"""
        user = request.user

        # Check if the user is a teacher that has the course linked to the project.
        teacher = Teacher.objects.filter(id=user.id).first()
        assistant = Assistant.objects.filter(id=user.id).first()
        student = Student.objects.filter(id=user.id).first()

        # Get the individual permission clauses.
        teacher_permission = teacher is not None and teacher.courses.filter(id=project.course.id).exists()
        assistant_permission = assistant is not None and assistant.courses.filter(id=project.course.id).exists()
        student_permission = student is not None and student.courses.filter(id=project.course.id).exists()

        return teacher_permission or assistant_permission or student_permission
