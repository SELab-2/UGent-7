from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.response import Response

from ..models.checks import ExtraCheck, StructureCheck
from ..models.extension import FileExtension
from ..serializers.checks_serializer import (ExtraCheckSerializer,
                                             FileExtensionSerializer,
                                             StructureCheckSerializer)


class StructureCheckViewSet(viewsets.ModelViewSet):
    queryset = StructureCheck.objects.all()
    serializer_class = StructureCheckSerializer


# TODO: Run all checks again and send message to submissions guys if not success (just in general send mail when project checks failed). Both update and delete
# TODO: Set result to invalid for all submission but the newest
class ExtraCheckView(UpdateModelMixin, DestroyModelMixin):

    def update(self, request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        return super().destroy(request, *args, **kwargs)


class ExtraCheckViewSet(viewsets.ModelViewSet):
    queryset = ExtraCheck.objects.all()
    serializer_class = ExtraCheckSerializer


class FileExtensionViewSet(viewsets.ModelViewSet):
    queryset = FileExtension.objects.all()
    serializer_class = FileExtensionSerializer
