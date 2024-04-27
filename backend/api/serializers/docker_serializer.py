from api.models.docker import DockerImage
from api.signals import run_docker_image_build
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class DockerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockerImage
        fields: str = "__all__"

    def validate(self, attrs):
        data = super().validate(attrs=attrs)

        data["owner"] = self.context["request"].user

        if "public" in data and data["public"] and not data["owner"].is_staff:
            raise ValidationError(_("docker.errors.custom"))

        return data

    def create(self, validated_data):
        docker_image = super().create(validated_data)
        run_docker_image_build.send(sender=DockerImage, docker_image=docker_image)
        return docker_image

    def update(self, instance, validated_data):
        docker_image = super().update(instance, validated_data)
        run_docker_image_build.send(sender=DockerImage, docker_image=docker_image)
        return docker_image
