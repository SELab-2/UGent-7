from rest_framework import permissions

from api.permissions.role_permissions import is_teacher


class IsAdminOrTeacherForPatch(permissions.BasePermission):
    """
    Custom permission to only allow admins to access objects in general,
    but teachers can only make PATCH requests.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        elif request.method == 'PATCH' and is_teacher(request.user):
            return True
        return False
