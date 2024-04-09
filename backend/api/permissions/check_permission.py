from api.models.checks import ExtraCheck
from api.models.course import Course
from api.permissions.role_permissions import is_assistant, is_teacher
from authentication.models import User
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class ExtraCheckPermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet):
        user: User = request.user

        return user.is_staff or is_teacher(user) or is_assistant(user)

    def has_object_permission(self, request: Request, view: ViewSet, obj: ExtraCheck):
        user: User = request.user
        course: Course = obj.project.course

        if not is_assistant(user) and not is_teacher(user):
            return user.is_staff

        return user.is_staff or course.teachers.filter(id=user.id).exists() or course.assistants.filter(id=user.id).exists()
