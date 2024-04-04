from api.models.docker import DockerImage
from api.serializers.docker_serializer import DockerImageSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


class DockerImageViewSet(APIView):

    def get_object(self, pk):
        try:
            return DockerImage.objects.get(pk=pk)
        except DockerImage.DoesNotExist:
            return Response(status=404)

    def get(self, request):
        images = DockerImage.objects.all().filter(Q(public=True) | Q(owner=request.user))
        serializer = DockerImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DockerImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response({
            "message": serializer.errors
        })

    def put(self, request, pk):
        image = self.get_object(pk)
        if request.user.is_staff or image.owner == request.user:
            serializer = DockerImageSerializer(image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({
                "message": serializer.errors
            })

    def delete(self, request, pk):
        image = self.get_object(pk=pk)
        # Staff can wlasy delete
        # Owner can delete if image is not public. Can happen that it becomes public is user was staff before
        if request.user.is_staff or (image.owner == request.user and not image.public):
            image.delete()
            return Response(status=204)
        return Response(status=403)
