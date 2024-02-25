from rest_framework import viewsets
from ..models.teacher import Teacher
from ..serializers import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer