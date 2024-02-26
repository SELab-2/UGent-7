from rest_framework import viewsets
from ..models.teacher import Teacher
from ..serializers.teacher_serializer import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
