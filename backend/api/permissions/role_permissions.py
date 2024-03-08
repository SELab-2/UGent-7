from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from authentication.models import User
from api.models.student import Student
from api.models.assistant import Assistant
from api.models.teacher import Teacher


def is_student(user: User):
    return Student.objects.filter(id=user.id).exists()


def is_assistant(user: User):
    return Assistant.objects.filter(id=user.id).exists()


def is_teacher(user: User):
    return Teacher.objects.filter(id=user.id).exists()


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
