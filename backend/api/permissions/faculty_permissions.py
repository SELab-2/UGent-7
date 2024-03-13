from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class FacultyPermission(BasePermission):
    """Permission class for faculty related endpoints"""

    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general faculty endpoint."""

        # The general faculty endpoint that lists all faculties is accessible for any role.
        if request.method in SAFE_METHODS:
            return True

        # We only allow admins to create, update, and delete faculties.
        return False
