from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from authentication.models import User
from api.models.student import Student
from api.models.assistant import Assistant
from api.models.teacher import Teacher


def is_student(user: User) -> bool:
    """Check whether the user is a student"""
    return Student.objects.filter(id=user.id, is_active=True).exists()


def is_assistant(user: User) -> bool:
    """Check whether the user is an assistant"""
    return Assistant.objects.filter(id=user.id, is_active=True).exists()


def is_teacher(user: User) -> bool:
    """Check whether the user is a teacher"""
    return Teacher.objects.filter(id=user.id, is_active=True).exists()


class IsStudent(IsAuthenticated):
    def has_permission(self, request: Request, view):
        """Returns true if the request contains a user,
        with said user being a student"""
        return super().has_permission(request, view) and is_student(request.user)


class IsTeacher(IsAuthenticated):
    def has_permission(self, request: Request, view):
        """Returns true if the request contains a user,
        with said user being a student"""
        return super().has_permission(request, view) and is_teacher(request.user)


class IsAssistant(IsAuthenticated):
    def has_permission(self, request, view):
        """Returns true if the request contains a user,
        with said user being a student"""
        return super().has_permission(request, view) and is_assistant(request.user)


class IsSameUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request: Request, view: ViewSet, user: User):
        """Returns true if the request's user is the same as the given user"""
        return super().has_permission(request, view) and user.id == request.user.id
