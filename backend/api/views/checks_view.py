import re

from api.models.checks import ExtraCheck, StructureCheck
from api.models.extension import FileExtension
from api.permissions.check_permission import ExtraCheckPermission
from api.serializers.checks_serializer import (ExtraCheckSerializer,
                                               FileExtensionSerializer,
                                               StructureCheckSerializer)
from rest_framework import viewsets
from rest_framework.mixins import (DestroyModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)


class StructureCheckViewSet(viewsets.ModelViewSet):
    queryset = StructureCheck.objects.all()
    serializer_class = StructureCheckSerializer


class ExtraCheckViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ExtraCheck.objects.all()
    serializer_class = ExtraCheckSerializer
    permission_classes = [ExtraCheckPermission]


class FileExtensionViewSet(viewsets.ModelViewSet):
    queryset = FileExtension.objects.all()
    serializer_class = FileExtensionSerializer
