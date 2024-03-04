from rest_framework.permissions import BasePermission, DjangoModelPermissions


class CASPermission(BasePermission):
    def has_permission(self, request, view):
        pass