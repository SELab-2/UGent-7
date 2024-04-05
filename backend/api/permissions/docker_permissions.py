from api.models.docker import DockerImage
from api.permissions.role_permissions import is_assistant, is_teacher
from authentication.models import User
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


# TODO: Types
class DockerPermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        user: User = request.user

        return user.is_staff or is_teacher(user) or is_assistant(user)

    def has_object_permission(self, request: Request, view: ViewSet, obj: DockerImage):
        user: User = request.user

        # GET
        # Public -> everyone (after has_permission)
        # Private -> admin and owner
        if request.method in SAFE_METHODS:
            return user.is_staff or obj.public or obj.owner == user

        # Public -> Staff
        # Private -> Staff and Owner
        return user.is_staff or (obj.owner == user and not obj.public)
