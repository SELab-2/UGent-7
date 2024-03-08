from django.utils.translation import gettext
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.models.student import Student
from api.models.course import Course
from api.permissions.course_permissions import CoursePermission
from api.permissions.role_permissions import IsStudent
from api.serializers.course_serializer import CourseSerializer
from api.serializers.teacher_serializer import TeacherSerializer
from api.serializers.assistant_serializer import AssistantSerializer
from api.serializers.student_serializer import StudentSerializer
from api.serializers.project_serializer import ProjectSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser | CoursePermission]

    @action(detail=True, methods=["get"])
    def teachers(self, request, **_):
        """Returns a list of teachers for the given course"""
        # This automatically fetches the course from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        course = self.get_object()
        teachers = course.teachers.all()

        # Serialize the teacher objects
        serializer = TeacherSerializer(
            teachers, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def assistants(self, request, **_):
        """Returns a list of assistants for the given course"""
        # This automatically fetches the course from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        course = self.get_object()
        assistants = course.assistants.all()

        if request.method == "GET":
            # Serialize the assistant objects
            serializer = AssistantSerializer(
                assistants, many=True, context={"request": request}
            )

            return Response(serializer.data)

        # Add a new assistant to the course, assistant ID in request.get("assistant_id")




    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        """Returns a list of students for the given course"""
        course = self.get_object()

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
            raise NotFound(gettext("courses.errors.not_found"))

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
            raise NotFound(gettext("courses.errors.not_found"))

    @action(detail=True, methods=["post"], permission_classes=[IsStudent])
    def join(self, request, pk=None):
        """Enrolls the authenticated student in the project"""

        try:
            # Add the course to the student's enrollment list.
            Student.objects.get(id=request.user.id).courses.add(
                Course.objects.get(id=pk)
            )

            return Response({
                "message": gettext("courses.messages.successful_join")
            })

        except Course.DoesNotExist:
            # Invalid course ID
            raise NotFound(gettext("courses.errors.not_found"))
        except Student.DoesNotExist:
            # Invalid student user, this should not happen,
            # since the IsStudent permission class already checks this.
            raise NotFound(gettext("students.errors.not_found"))