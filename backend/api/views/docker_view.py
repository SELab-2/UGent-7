from api.models.docker import DockerImage
from api.permissions.docker_permissions import DockerPermission
from api.permissions.role_permissions import IsAssistant, IsTeacher
from api.serializers.docker_serializer import DockerImageSerializer
from django.db.models import Q
from django.db.models.manager import BaseManager
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


# TODO: Add to urls.py
class DockerImageViewSet(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):

    queryset = DockerImage.objects.all()
    serializer_class = DockerImageSerializer
    permission_classes = [DockerPermission]

    # TODO: Maybe not necessary
    # https://www.django-rest-framework.org/api-guide/permissions/#overview-of-access-restriction-methods
    def list(self, request: Request) -> Response:
        images: BaseManager[DockerImage] = DockerImage.objects.all()
        if not request.user.is_staff:
            images = images.filter(Q(public=True) | Q(owner=request.user))
        serializer = DockerImageSerializer(images, many=True)
        return Response(data=serializer.data, status=200)
