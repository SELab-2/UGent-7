from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.student import Student
from ..serializers.student_serializer import StudentSerializer
from ..serializers.course_serializer import CourseSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCoursesViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        """Returns a list of courses for the given student"""
        student_id = kwargs.get('student_id')

        try:
            queryset = Student.objects.get(id=student_id)
            courses = queryset.courses.all()

            # Serialize the course objects
            serializer = CourseSerializer(
                courses, many=True, context={'request': request}
            )
            return Response(serializer.data)

        except Student.DoesNotExist:
            # Invalid student ID
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Student not found"})
