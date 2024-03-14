from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser
from api.permissions.assistant_permissions import AssistantPermission
from ..models.assistant import Assistant
from ..serializers.assistant_serializer import AssistantSerializer
from ..serializers.course_serializer import CourseSerializer


class AssistantViewSet(ReadOnlyModelViewSet):

    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsAdminUser | AssistantPermission]

    @action(detail=True, methods=["get"])
    def courses(self, request, **_):
        """Returns a list of courses for the given assistant"""
        assistant = self.get_object()
        courses = assistant.courses

        # Serialize the course objects
        serializer = CourseSerializer(
            courses, many=True, context={"request": request}
        )

        return Response(serializer.data)
