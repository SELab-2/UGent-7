from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.assistant import Assistant
from ..serializers.assistant_serializer import AssistantSerializer
from ..serializers.course_serializer import CourseSerializer


class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer

    @action(detail=True, methods=["get"])
    def courses(self, request, pk=None):
        """Returns a list of courses for the given assistant"""

        try:
            queryset = Assistant.objects.get(id=pk)
            courses = queryset.courses.all()

            # Serialize the course objects
            serializer = CourseSerializer(
                courses, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Assistant.DoesNotExist:
            # Invalid assistant ID
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Assistant not found"},
            )
