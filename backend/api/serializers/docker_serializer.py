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

        if not self.partial:
            data["owner"] = self.context["request"].user
        else:
            data["owner"] = self.instance.owner

        if "public" in data and data["public"] and not data["owner"].is_staff:
            raise ValidationError(_("docker.errors.custom"))

        return data
