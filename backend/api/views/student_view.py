from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.student import Student
from ..serializers.student_serializer import StudentSerializer
from ..serializers.course_serializer import CourseSerializer
from ..serializers.group_serializer import GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Returns a list of courses for the given student"""

        try:
            queryset = Student.objects.get(id=pk)
            courses = queryset.courses.all()

            # Serialize the course objects
            serializer = CourseSerializer(
                courses, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Student.DoesNotExist:
            # Invalid student ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Student not found"})

    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        """Returns a list of groups for the given student"""

        try:
            queryset = Student.objects.get(id=pk)
            groups = queryset.groups.all()

            # Serialize the group objects
            serializer = GroupSerializer(
                groups, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Student.DoesNotExist:
            # Invalid student ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Student not found"})
