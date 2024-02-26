from rest_framework import viewsets
from ..models.student import Student
from ..serializers.student_serializer import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
