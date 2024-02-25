from rest_framework import viewsets
from ..models.admin import Admin
from ..serializers import AdminSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer