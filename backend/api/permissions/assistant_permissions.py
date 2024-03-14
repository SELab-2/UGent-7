from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from api.permissions.role_permissions import is_teacher, is_assistant
from api.models.assistant import Assistant


class AssistantPermission(BasePermission):
    """Permission class used as default policy for assistant endpoint."""
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Check if user has permission to view a general assistant endpoint."""
        user = request.user

        if view.action == "list":
            # Only teachers can query the assistant list.
            return user.is_authenticated and is_teacher(user)

        return is_teacher(user) or is_assistant(user)

    def has_object_permission(self, request: Request, view: ViewSet, assistant: Assistant) -> bool:
        # Teachers can view the details of all assistants.
        # Users can view their own assistant object.
        return is_teacher(request.user) or request.user.id == assistant.id
