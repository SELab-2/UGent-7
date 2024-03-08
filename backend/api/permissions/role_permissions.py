from rest_framework.permissions import IsAuthenticated
from api.models.student import Student
from api.models.assistant import Assistant
from api.models.teacher import Teacher

class IsStudent(IsAuthenticated):
    def has_permission(self, request, view):
        """Returns true if the request contains a user,
        with said user being a student"""
        return super().has_permission(request, view) and \
            Student.objects.filter(id=request.user.id).exists()

class IsTeacher(IsAuthenticated):
    def has_permission(self, request, view):
        """Returns true if the request contains a user,
        with said user being a student"""
        return super().has_permission(request, view) and \
            Teacher.objects.filter(id=request.user.id).exists()

class IsAssistant(IsAuthenticated):
    def has_permission(self, request, view):
        """Returns true if the request contains a user,
        with said user being a student"""
        return super().has_permission(request, view) and \
            Assistant.objects.filter(id=request.user.id).exists()