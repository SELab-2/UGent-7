from django.utils.translation import gettext
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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
    """Actions for general course logic"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser | CoursePermission]

    @action(detail=True, permission_classes=[IsAdminUser | CourseTeacherPermission])
    def assistants(self, request: Request, **_):
        """Returns a list of assistants for the given course"""
        course = self.get_object()
        assistants = course.assistants.all()

        # Serialize assistants
        serializer = AssistantSerializer(
            assistants, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @assistants.mapping.post
    @assistants.mapping.put
    def _add_assistant(self, request: Request, **_):
        """Add an assistant to the course"""
        course = self.get_object()

        try:
            # Add assistant to course
            assistant = Assistant.objects.get(
                id=request.data.get("id")
            )

            course.assistants.add(assistant)

            return Response({
                "message": gettext("courses.success.assistants.add")
            })
        except Assistant.DoesNotExist:
            # Not found
            raise NotFound(gettext("assistants.error.404"))

    @assistants.mapping.delete
    def _remove_assistant(self, request: Request, **_):
        """Remove an assistant from the course"""
        course = self.get_object()

        try:
            # Add assistant to course
            assistant = Assistant.objects.get(
                id=request.data.get("id")
            )

            course.assistants.remove(assistant)

            return Response({
                "message": gettext("courses.success.assistants.delete")
            })
        except Assistant.DoesNotExist:
            # Not found
            raise NotFound(gettext("assistants.error.404"))

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

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser | CourseTeacherPermission])
    def clone(self, request: Request, **__):
        """Copy the course to a new course with the same fields"""
        course: Course = self.get_object()

        try:
            course_serializer = CourseSerializer(
                course.child_course, context={"request": request}
            )
        except Course.DoesNotExist:
            course_serializer = CourseSerializer(
                course.clone(
                    year=request.data.get("academic_startyear")
                ),
                context={"request": request}
            )

            course_serializer.save()

        return Response(course_serializer.data)