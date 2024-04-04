from rest_framework import viewsets

from ..models.checks import ExtraCheck, StructureCheck
from ..models.extension import FileExtension
from ..serializers.checks_serializer import (ExtraCheckSerializer,
                                             FileExtensionSerializer,
                                             StructureCheckSerializer)


class StructureCheckViewSet(viewsets.ModelViewSet):
    queryset = StructureCheck.objects.all()
    serializer_class = StructureCheckSerializer


class ExtraCheckViewSet(viewsets.ModelViewSet):
    queryset = ExtraCheck.objects.all()
    serializer_class = ExtraCheckSerializer


class FileExtensionViewSet(viewsets.ModelViewSet):
    queryset = FileExtension.objects.all()
    serializer_class = FileExtensionSerializer
