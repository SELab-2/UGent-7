from api.models.checks import ExtraCheck, FileExtension, StructureCheck
from api.permissions.check_permission import CheckPermission
from api.serializers.checks_serializer import (ExtraCheckSerializer,
                                               FileExtensionSerializer,
                                               StructureCheckSerializer)
from rest_framework import viewsets
from rest_framework.mixins import (DestroyModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)


class StructureCheckViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = StructureCheck.objects.all()
    serializer_class = StructureCheckSerializer
    permission_classes = [CheckPermission]


class ExtraCheckViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ExtraCheck.objects.all()
    serializer_class = ExtraCheckSerializer
    permission_classes = [CheckPermission]


class FileExtensionViewSet(viewsets.ModelViewSet):
    queryset = FileExtension.objects.all()
    serializer_class = FileExtensionSerializer
