from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.course import Course
from ..serializers.course_serializer import CourseSerializer
from ..serializers.teacher_serializer import TeacherSerializer
from ..serializers.assistant_serializer import AssistantSerializer
from ..serializers.student_serializer import StudentSerializer
from ..serializers.project_serializer import ProjectSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=["get"])
    def teachers(self, request, pk=None):
        """Returns a list of teachers for the given course"""

        try:
            queryset = Course.objects.get(id=pk)
            teachers = queryset.teachers.all()

            # Serialize the teacher objects
            serializer = TeacherSerializer(
                teachers, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Course.DoesNotExist:
            # Invalid course ID
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message": "Course not found"}
            )

    @action(detail=True, methods=["get"])
    def assistants(self, request, pk=None):
        """Returns a list of assistants for the given course"""

        try:
            queryset = Course.objects.get(id=pk)
            assistants = queryset.assistants.all()

            # Serialize the assistant objects
            serializer = AssistantSerializer(
                assistants, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Course.DoesNotExist:
            # Invalid course ID
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message": "Course not found"}
            )

    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        """Returns a list of students for the given course"""

        try:
            queryset = Course.objects.get(id=pk)
            students = queryset.students.all()

            # Serialize the student objects
            serializer = StudentSerializer(
                students, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Course.DoesNotExist:
            # Invalid course ID
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message": "Course not found"}
            )

    @action(detail=True, methods=["get"])
    def projects(self, request, pk=None):
        """Returns a list of projects for the given course"""

        try:
            queryset = Course.objects.get(id=pk)
            projects = queryset.projects.all()

            # Serialize the project objects
            serializer = ProjectSerializer(
                projects, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Course.DoesNotExist:
            # Invalid course ID
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message": "Course not found"}
            )
