from django.utils.translation import gettext
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from api.models.course import Course
from api.models.assistant import Assistant
from api.permissions.course_permissions import CoursePermission, CourseTeacherPermission
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

    @action(detail=True, methods=["get", "post", "delete"], permission_classes=[IsAdminUser | CourseTeacherPermission])
    def assistants(self, request: Request, **_) -> Response:
        """Action for managing assistants associated to a course"""
        # This automatically fetches the course from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        course = self.get_object()

        if request.method == "GET":
            # Return assistants of a course.
            assistants = course.assistants.all()

            serializer = AssistantSerializer(
                assistants, many=True, context={"request": request}
            )

            return Response(serializer.data)

        try:
            assistant = Assistant.objects.get(
                id=request.query_params.get("id")
            )

            if request.method == "POST":
                # Add a new assistant to the course.
                course.assistants.add(assistant)

                return Response({
                    "message": gettext("courses.success.assistants.add")
                })
            elif request.method == "DELETE":
                # Remove an assistant from the course.
                course.assistants.remove(assistant)

                return Response({
                    "message": gettext("courses.success.assistants.remove")
                })
        except Assistant.DoesNotExist:
            # Not found
            raise NotFound(gettext("assistants.error.404"))


    @action(detail=True, methods=["get"])
    def students(self, request, **_):
        """Returns a list of students for the given course"""
        course = self.get_object()
        students = course.students.all()

        # Serialize the student objects
        serializer = StudentSerializer(
            students, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def projects(self, request, **_):
        """Returns a list of projects for the given course"""
        course = self.get_object()
        projects = course.projects.all()

        # Serialize the project objects
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsStudent])
    def join(self, request, **_):
        """Enrolls the authenticated student in the project"""
        # Add the course to the student's enrollment list.
        self.get_object().students.add(
            request.user.student
        )

        return Response({
            "message": gettext("courses.success.join")
        })