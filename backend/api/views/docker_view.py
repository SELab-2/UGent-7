from api.models.docker import DockerImage
from api.serializers.docker_serializer import DockerImageSerializer
from django.db.models import Q
from django.db.models.manager import BaseManager
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


# TODO: Add to urls.py
# TODO: Simplify -> GenericAPIView https://python.plainenglish.io/all-about-views-in-django-rest-framework-drf-genericapiview-and-mixins-fe37d7db7582
class DockerImageView(APIView):

    def get_object(self, pk: int) -> DockerImage | None:
        try:
            return DockerImage.objects.get(pk=pk)
        except DockerImage.DoesNotExist:
            return None

    def get(self, request: Request) -> Response:
        images: BaseManager[DockerImage] = DockerImage.objects.all().filter(Q(public=True) | Q(owner=request.user))
        serializer = DockerImageSerializer(images, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request: Request) -> Response:
        serializer = DockerImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)

        return Response(data=serializer.errors, status=400)

    def put(self, request: Request, pk: int) -> Response:
        image: DockerImage | None = self.get_object(pk=pk)
        if image:
            if request.user.is_staff or image.owner == request.user:
                serializer = DockerImageSerializer(image, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
        return Response(status=404)

    def delete(self, request: Request, pk: int) -> Response:
        image: DockerImage | None = self.get_object(pk=pk)
        # Staff can always delete
        # Owner can delete if image is not public. Can happen that it becomes public is user was staff before
        if image:
            if request.user.is_staff or (image.owner == request.user and not image.public):
                image.delete()
                return Response(status=204)
        return Response(status=403)
