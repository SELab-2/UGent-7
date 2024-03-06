from rest_framework import viewsets
from ..models.checks import Checks, FileExtension
from ..serializers.checks_serializer import ChecksSerializer, FileExtensionSerializer


class ChecksViewSet(viewsets.ModelViewSet):
    queryset = Checks.objects.all()
    serializer_class = ChecksSerializer


class FileExtensionViewSet(viewsets.ModelViewSet):
    queryset = FileExtension.objects.all()
    serializer_class = FileExtensionSerializer
