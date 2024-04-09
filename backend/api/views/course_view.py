from api.models.course import Course
from api.permissions.course_permissions import (CourseAssistantPermission,
                                                CoursePermission,
                                                CourseStudentPermission,
                                                CourseTeacherPermission)
from api.permissions.role_permissions import IsTeacher, is_teacher
from api.serializers.assistant_serializer import (AssistantIDSerializer,
                                                  AssistantSerializer)
from api.serializers.course_serializer import (CourseCloneSerializer,
                                               CourseSerializer,
                                               StudentJoinSerializer,
                                               StudentLeaveSerializer,
                                               TeacherJoinSerializer,
                                               TeacherLeaveSerializer,
                                               CreateCourseSerializer)
from api.serializers.project_serializer import (CreateProjectSerializer,
                                                ProjectSerializer)
from api.serializers.student_serializer import StudentSerializer
from api.serializers.teacher_serializer import TeacherSerializer
from api.views.pagination.basic_pagination import BasicPagination
from django.utils.translation import gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    """Actions for general course logic"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser | CoursePermission]

    # TODO: Creating should return the info of the new object and not a message "created" (General TODO)
    def create(self, request: Request, *_):
        """Override the create method to add the teacher to the course"""
        serializer = CreateCourseSerializer(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            course = serializer.save()

            # If it was a teacher who created the course, add them as a teacher
            if is_teacher(request.user):
                course.teachers.add(request.user.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False)
    def search(self, request: Request) -> Response:
        self.pagination_class = BasicPagination

        # Extract filter params
        search = request.query_params.get("search", "")
        years = request.query_params.getlist("years[]")
        faculties = request.query_params.getlist("faculties[]")

        # Filter the queryset based on the search term
        queryset = self.get_queryset().filter(
            name__icontains=search
        )

        # Filter the queryset based on selected years
        if years:
            queryset = queryset.filter(academic_startyear__in=years)

        # Filter the queryset based on selected faculties
        if faculties:
            queryset = queryset.filter(faculty__in=faculties)

        # Serialize the resulting queryset
        serializer = self.serializer_class(self.paginate_queryset(queryset), many=True, context={
            "request": request
        })

        return self.get_paginated_response(serializer.data)

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
    @swagger_auto_schema(request_body=AssistantIDSerializer)
    def _add_assistant(self, request: Request, **_):
        """Add an assistant to the course"""
        course = self.get_object()

        # Add assistant to course
        serializer = AssistantIDSerializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            course.assistants.add(
                serializer.validated_data["assistant"]
            )

        return Response({
            "message": gettext("courses.success.assistants.add")
        })

    @assistants.mapping.delete
    @swagger_auto_schema(request_body=AssistantIDSerializer)
    def _remove_assistant(self, request: Request, **_):
        """Remove an assistant from the course"""
        course = self.get_object()

        # Remove assistant from course
        serializer = AssistantIDSerializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            course.assistants.remove(
                serializer.validated_data["assistant"]
            )

        return Response({
            "message": gettext("courses.success.assistants.remove")
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
    @swagger_auto_schema(request_body=StudentJoinSerializer)
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
                serializer.validated_data["student"]
            )

        return Response({
            "message": gettext("courses.success.students.add")
        })

    @students.mapping.delete
    @swagger_auto_schema(request_body=StudentLeaveSerializer)
    def _remove_student(self, request: Request, **_):
        """Remove a student from the course"""
        # Get the course
        course = self.get_object()

        # Remove the student from the course
        serializer = StudentLeaveSerializer(data=request.data, context={
            "course": course
        })

        if serializer.is_valid(raise_exception=True):
            course.students.remove(
                serializer.validated_data["student"]
            )

        return Response({
            "message": gettext("courses.success.students.remove")
        })

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | CourseTeacherPermission])
    def teachers(self, request, **_):
        """Returns a list of teachers for the given course"""
        course = self.get_object()
        teachers = course.teachers.all()

        # Serialize the teacher objects
        serializer = TeacherSerializer(
            teachers, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @teachers.mapping.post
    @teachers.mapping.put
    @swagger_auto_schema(request_body=TeacherJoinSerializer)
    def _add_teacher(self, request, **_):
        """Add a teacher to the course"""
        # Get the course
        course = self.get_object()

        # Add teacher to course
        serializer = TeacherJoinSerializer(data=request.data, context={
            "course": course
        })

        if serializer.is_valid(raise_exception=True):
            course.teachers.add(
                serializer.validated_data["teacher"]
            )

        return Response({
            "message": gettext("courses.success.teachers.add")
        })

    @teachers.mapping.delete
    @swagger_auto_schema(request_body=TeacherLeaveSerializer)
    def _remove_teacher(self, request, **_):
        """Remove a teacher from the course"""
        # Get the course
        course = self.get_object()

        # Remove the teacher from the course
        serializer = TeacherLeaveSerializer(data=request.data, context={
            "course": course
        })

        if serializer.is_valid(raise_exception=True):
            course.teachers.remove(
                serializer.validated_data["teacher"]
            )

        return Response({
            "message": gettext("courses.success.teachers.remove")
        })

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
    @swagger_auto_schema(request_body=CreateProjectSerializer)
    def _add_project(self, request, **_):
        """Add a project to the course"""
        course = self.get_object()

        serializer = CreateProjectSerializer(
            data=request.data, context={
                "request": request,
                "course": course
            }
        )

        # Validate the serializer
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            course.projects.add(project)

        return Response({
            "message": gettext("course.success.project.add"),
        })

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser | IsTeacher])
    @swagger_auto_schema(request_body=CourseCloneSerializer)
    def clone(self, request: Request, **__):
        """Copy the course to a new course with the same fields"""
        course: Course = self.get_object()

        serializer = CourseCloneSerializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            try:
                # We should return the already cloned course, if present
                course = course.child_course

            except Course.DoesNotExist:
                # Else, we clone the course
                course = course.clone(
                    clone_teachers=serializer.validated_data["clone_teachers"],
                    clone_assistants=serializer.validated_data["clone_assistants"]
                )

        # Return serialized cloned course
        course_serializer = CourseSerializer(course, context={"request": request})

        return Response(course_serializer.data)
