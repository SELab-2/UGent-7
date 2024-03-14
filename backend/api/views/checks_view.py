from rest_framework import viewsets
from ..models.extension import FileExtension
from ..models.checks import StructureCheck, ExtraCheck
from ..serializers.checks_serializer import (
    StructureCheckSerializer, ExtraCheckSerializer, FileExtensionSerializer
)


class StructureCheckViewSet(viewsets.ModelViewSet):
    queryset = StructureCheck.objects.all()
    serializer_class = StructureCheckSerializer


class ExtraCheckViewSet(viewsets.ModelViewSet):
    queryset = ExtraCheck.objects.all()
    serializer_class = ExtraCheckSerializer


class FileExtensionViewSet(viewsets.ModelViewSet):
    queryset = FileExtension.objects.all()
    serializer_class = FileExtensionSerializer
