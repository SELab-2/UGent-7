from django.utils.translation import gettext
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from api.models.project import Project
from api.permissions.student_permissions import StudentPermission
from api.models.student import Student
from api.serializers.project_serializer import ProjectSerializer
from api.serializers.student_serializer import StudentSerializer, CreateStudentSerializer, StudentIDSerializer
from api.serializers.course_serializer import CourseSerializer
from api.serializers.group_serializer import GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser | StudentPermission]

    @swagger_auto_schema(request_body=CreateStudentSerializer)
    def create(self, request: Request, *args, **kwargs) -> Response:
        """Add the student role to the user"""
        try:
            student: Student = Student.objects.get(pk=request.data.get('user'))

            student.activate()
        except Student.DoesNotExist:
            serializer = CreateStudentSerializer(
                data=request.data
            )

            if serializer.is_valid(raise_exception=True):
                Student.create(serializer.validated_data.get('user'),
                               student_id=serializer.validated_data.get('student_id')
                               )

        finally:
            return Response({
                "message": gettext("students.success.add")
            })

    @swagger_auto_schema(request_body=StudentIDSerializer)
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Delete the student role from the user"""
        self.get_object().deactivate()

        return Response({
            "message": gettext("students.success.destroy")
        })

    @action(detail=True)
    def courses(self, request, **_):
        """Returns a list of courses for the given student"""
        student = self.get_object()
        courses = student.courses.all()

        # Serialize the course objects
        serializer = CourseSerializer(
            courses, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True)
    def groups(self, request, **_):
        """Returns a list of groups for the given student"""
        student = self.get_object()
        groups = student.groups.all()

        # Serialize the group objects
        serializer = GroupSerializer(
            groups, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True)
    def projects(self, request: Request, **_) -> Response:
        """Returns a list of projects for the given student"""
        student = self.get_object()
        projects = Project.objects.filter(course__in=student.courses.all()).select_related('course')

        # Serialize the project objects
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request}
        )

        return Response(serializer.data)
