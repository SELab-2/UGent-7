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

from api.views.pagination.basic_pagination import BasicPagination


class DockerImageViewSet(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):

    queryset = DockerImage.objects.all()
    serializer_class = DockerImageSerializer
    permission_classes = [DockerPermission]

    @action(detail=False)
    def search(self, request: Request) -> Response:
        self.pagination_class = BasicPagination

        search = request.query_params.get("search", "")
        identifier = request.query_params.get("id", "")
        name = request.query_params.get("name", "")
        owner = request.query_params.get("owner", "")

        queryset1 = self.get_queryset().filter(
            id__icontains=search
        )
        queryset2 = self.get_queryset().filter(
            name__icontains=search
        )
        # queryset3 = self.get_queryset().filter(
        #     owner__icontains=search
        # )
        queryset1 = queryset1.union(queryset2)
        queryset = self.get_queryset().filter(
            id__icontains=identifier,
            name__icontains=name,
        )
        queryset = queryset.union(queryset1)

        serializer = self.serializer_class(self.paginate_queryset(queryset), many=True, context={
            "request": request
        })

        return self.get_paginated_response(serializer.data)

    # TODO: Maybe not necessary
    # https://www.django-rest-framework.org/api-guide/permissions/#overview-of-access-restriction-methods
    def list(self, request: Request) -> Response:
        images: BaseManager[DockerImage] = DockerImage.objects.all()
        if not request.user.is_staff:
            images = images.filter(Q(public=True) | Q(owner=request.user))
        serializer = DockerImageSerializer(images, many=True)
        return Response(data=serializer.data, status=200)
