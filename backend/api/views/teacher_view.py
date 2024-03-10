from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from ..models.teacher import Teacher
from ..serializers.teacher_serializer import TeacherSerializer
from ..serializers.course_serializer import CourseSerializer


class TeacherViewSet(ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = []

    @action(detail=True, methods=["get"])
    def courses(self, request, pk=None):
        """Returns a list of courses for the given teacher"""
        teacher = self.get_object()
        courses = teacher.courses.all()

        # Serialize the course objects
        serializer = CourseSerializer(
            courses, many=True, context={"request": request}
        )
        return Response(serializer.data)