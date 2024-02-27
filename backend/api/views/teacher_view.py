from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.teacher import Teacher
from ..serializers.teacher_serializer import TeacherSerializer
from ..serializers.course_serializer import CourseSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherCoursesViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        """Returns a list of courses for the given teacher"""
        teacher_id = kwargs.get('teacher_id')

        try:
            queryset = Teacher.objects.get(id=teacher_id)
            courses = queryset.courses.all()

            # Serialize the course objects
            serializer = CourseSerializer(
                courses, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Teacher.DoesNotExist:
            # Invalid teacher ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Teacher not found"})
