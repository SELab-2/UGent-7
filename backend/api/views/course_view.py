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

    @action(detail=True)
    def teachers(self, request, *args, **kwargs):
        """Returns a list of teachers for the given course"""
        course_id = kwargs.get('course_id')

        try:
            queryset = Course.objects.get(id=course_id)
            teachers = queryset.teachers.all()

            # Serialize the teacher objects
            serializer = TeacherSerializer(
                teachers, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Course.DoesNotExist:
            # Invalid course ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Course not found"})

    @action(detail=True, methods=['get'])
    def assistants(self, request, *args, **kwargs):
        """Returns a list of assistants for the given course"""
        course_id = kwargs.get('course_id')

        try:
            queryset = Course.objects.get(id=course_id)
            assistants = queryset.assistants.all()

            # Serialize the assistant objects
            serializer = AssistantSerializer(
                assistants, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Course.DoesNotExist:
            # Invalid course ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Course not found"})

    @action(detail=True, methods=['get'])
    def students(self, request, *args, **kwargs):
        """Returns a list of students for the given course"""
        course_id = kwargs.get('course_id')

        try:
            queryset = Course.objects.get(id=course_id)
            students = queryset.students.all()

            # Serialize the student objects
            serializer = StudentSerializer(
                students, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Course.DoesNotExist:
            # Invalid course ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Course not found"})

    @action(detail=True, methods=['get'])
    def projects(self, request, *args, **kwargs):
        """Returns a list of projects for the given course"""
        course_id = kwargs.get('course_id')

        try:
            queryset = Course.objects.get(id=course_id)
            projects = queryset.projects.all()

            # Serialize the project objects
            serializer = ProjectSerializer(
                projects, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Course.DoesNotExist:
            # Invalid course ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Course not found"})


# class CourseTeachersViewSet(viewsets.ModelViewSet):

#     def list(self, request, *args, **kwargs):
#         """Returns a list of teachers for the given course"""
#         course_id = kwargs.get('course_id')

#         try:
#             queryset = Course.objects.get(id=course_id)
#             teachers = queryset.teachers.all()

#             # Serialize the teacher objects
#             serializer = TeacherSerializer(
#                 teachers, many=True, context={'request': request}
#             )
#             return Response(serializer.data)

#         except Course.DoesNotExist:
#             # Invalid course ID
#             return Response(status=status.HTTP_404_NOT_FOUND,
#                             data={"message": "Course not found"})


# class CourseAssistantsViewSet(viewsets.ModelViewSet):

#     def list(self, request, *args, **kwargs):
#         """Returns a list of assistants for the given course"""
#         course_id = kwargs.get('course_id')

#         try:
#             queryset = Course.objects.get(id=course_id)
#             assistants = queryset.assistants.all()

#             # Serialize the assistant objects
#             serializer = AssistantSerializer(
#                 assistants, many=True, context={'request': request}
#             )
#             return Response(serializer.data)

#         except Course.DoesNotExist:
#             # Invalid course ID
#             return Response(status=status.HTTP_404_NOT_FOUND,
#                             data={"message": "Course not found"})


# class CourseStudentsViewSet(viewsets.ModelViewSet):

#     def list(self, request, *args, **kwargs):
#         """Returns a list of students for the given course"""
#         course_id = kwargs.get('course_id')

#         try:
#             queryset = Course.objects.get(id=course_id)
#             students = queryset.students.all()

#             # Serialize the student objects
#             serializer = StudentSerializer(
#                 students, many=True, context={'request': request}
#             )
#             return Response(serializer.data)

#         except Course.DoesNotExist:
#             # Invalid course ID
#             return Response(status=status.HTTP_404_NOT_FOUND,
#                             data={"message": "Course not found"})


# class CourseProjectsViewSet(viewsets.ModelViewSet):

#     def list(self, request, *args, **kwargs):
#         """Returns a list of projects for the given course"""
#         course_id = kwargs.get('course_id')

#         try:
#             queryset = Course.objects.get(id=course_id)
#             projects = queryset.projects.all()

#             # Serialize the project objects
#             serializer = ProjectSerializer(
#                 projects, many=True, context={'request': request}
#             )
#             return Response(serializer.data)

#         except Course.DoesNotExist:
#             # Invalid course ID
#             return Response(status=status.HTTP_404_NOT_FOUND,
#                             data={"message": "Course not found"})
