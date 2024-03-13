from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from authentication.models import Faculty
from api.permissions.faculty_permissions import FacultyPermission
from ..serializers.faculty_serializer import facultySerializer


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = facultySerializer
    permission_classes = [IsAdminUser | FacultyPermission]
