from rest_framework import viewsets
from authentication.models import Faculty
from ..serializers.faculty_serializer import facultySerializer


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = facultySerializer
