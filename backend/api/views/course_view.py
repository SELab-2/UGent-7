from django.utils.translation import gettext
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from api.models.course import Course
from api.models.group import Group
from api.permissions.course_permissions import (
    CoursePermission,
    CourseAssistantPermission,
    CourseStudentPermission
)
from api.permissions.role_permissions import IsTeacher
from api.serializers.course_serializer import CourseSerializer, StudentJoinSerializer, StudentLeaveSerializer
from api.serializers.teacher_serializer import TeacherSerializer
from api.serializers.assistant_serializer import AssistantSerializer, AssistantIDSerializer
from api.serializers.student_serializer import StudentSerializer
from api.serializers.project_serializer import ProjectSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Actions for general course logic"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser | CoursePermission]

    @action(detail=True, permission_classes=[IsAdminUser | CourseAssistantPermission])
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

        # Add assistant to course
        serializer = AssistantIDSerializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            course.assistants.add(
                serializer.validated_data["assistant_id"]
            )

        return Response({
            "message": gettext("courses.success.assistants.add")
        })

    @assistants.mapping.delete
    def _remove_assistant(self, request: Request, **_):
        """Remove an assistant from the course"""
        course = self.get_object()

        # Remove assistant from course
        serializer = AssistantIDSerializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            course.assistants.remove(
                serializer.validated_data["assistant_id"]
            )

        return Response({
            "message": gettext("courses.success.assistants.add")
        })

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | CourseStudentPermission])
    def students(self, request, **_):
        """Returns a list of students for the given course"""
        course = self.get_object()
        students = course.students.all()

        # Serialize the student objects
        serializer = StudentSerializer(
            students, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @students.mapping.post
    @students.mapping.put
    def _add_student(self, request: Request, **_):
        """Add a student to the course"""
        # Get the course
        course = self.get_object()

        # Add student to course
        serializer = StudentJoinSerializer(data=request.data, context={
            "course": course
        })

        if serializer.is_valid(raise_exception=True):
            course.students.add(
                serializer.validated_data["student_id"]
            )

        return Response({
            "message": gettext("courses.success.students.add")
        })

    @students.mapping.delete
    def _remove_student(self, request: Request, **_):
        """Remove a student from the course"""
        # Get the course
        course = self.get_object()

        # Add student to course
        serializer = StudentLeaveSerializer(data=request.data, context={
            "course": course
        })

        if serializer.is_valid(raise_exception=True):
            course.students.remove(
                serializer.validated_data["student_id"]
            )

        return Response({
            "message": gettext("courses.success.students.add")
        })

    @action(detail=True, methods=["get"])
    def teachers(self, request, **_):
        """Returns a list of teachers for the given course"""
        course = self.get_object()
        teachers = course.teachers.all()

        # Serialize the teacher objects
        serializer = TeacherSerializer(
            teachers, many=True, context={"request": request}
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

    @projects.mapping.post
    @projects.mapping.put
    def _add_project(self, request, **_):
        """Add a project to the course"""
        course = self.get_object()

        serializer = ProjectSerializer(
            data=request.data, context={
                "request": request,
                "course": course
            }
        )

        project = None

        # Validate the serializer
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            course.projects.add(project)

        # Create groups for the project
        students_count = course.students.count()
        for _ in range(students_count):
            Group.objects.create(project=project)

        return Response({
            "message": gettext("course.success.project.add"),
        })

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser | IsTeacher])
    def clone(self, request: Request, **__):
        """Copy the course to a new course with the same fields"""
        course: Course = self.get_object()

        try:
            # We should return the already cloned course, if present
            course = course.child_course

        except Course.DoesNotExist:
            # Else, we clone the course
            course = course.clone(
                clone_assistants=request.data.get("clone_assistants")
            )

            course.save()

        # Return serialized cloned course
        course_serializer = CourseSerializer(course, context={"request": request})

        return Response(course_serializer.data)
