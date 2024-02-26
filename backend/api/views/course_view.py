from rest_framework import viewsets
from ..models.course import Course
from ..serializers.course_serializer import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
