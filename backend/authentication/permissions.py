from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from ypovoli import settings


class IsDebug(BasePermission):
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        return settings.DEBUG
