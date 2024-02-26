from rest_framework import viewsets
from ..models.admin import Admin
from ..serializers.admin_serializer import AdminSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
