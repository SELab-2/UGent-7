from rest_framework import viewsets, status
from ..models.course import Course
from ..serializers.course_serializer import CourseSerializer
from ..serializers.teacher_serializer import TeacherSerializer
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseTeachersViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
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
