from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.assistant import Assistant
from ..serializers.assistant_serializer import AssistantSerializer
from ..serializers.course_serializer import CourseSerializer


class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer


class AssistantCoursesViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        """Returns a list of courses for the given assistant"""
        assistant_id = kwargs.get('assistant_id')

        try:
            queryset = Assistant.objects.get(id=assistant_id)
            courses = queryset.courses.all()

            # Serialize the course objects
            serializer = CourseSerializer(
                courses, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Assistant.DoesNotExist:
            # Invalid assistant ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Assistant not found"})
