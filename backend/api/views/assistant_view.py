from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser
from api.permissions.role_permissions import IsTeacher
from api.permissions.assistant_permissions import AssistantPermission
from api.models.assistant import Assistant
from ..models.assistant import Assistant
from ..serializers.assistant_serializer import AssistantSerializer
from ..serializers.course_serializer import CourseSerializer

### TODO :  - courses kan enkel door assistenten en admins opgevraagd worden (teachers?)
###         - Enkel Teachers en admins kunnen assistenten maken
class AssistantViewSet(ReadOnlyModelViewSet):

    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsAdminUser, AssistantPermission]

    @action(detail=True, methods=["get"])
    def courses(self, request, **_):
        """Returns a list of courses for the given assistant"""
        assistant = self.get_object()
        courses = assistant.courses()

        # Serialize the course objects
        serializer = CourseSerializer(
            courses, many=True, context={"request": request}
        )

        return Response(serializer.data)