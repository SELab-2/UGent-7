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

        if "owner" in data and data["owner"] != self.context["request"].user and not self.context["request"].user.is_staff:
            # Only allow staff to set the owner of an image to someone else
            raise ValidationError(_("docker.errors.no_staff"))

        if "owner" not in data:
            # Add the owner data if not present
            if not self.partial:
                # If it's created assign the user who made the request
                data["owner"] = self.context["request"].user
            else:
                # Else use the pre exisiting owner
                data["owner"] = self.instance.owner

        if "public" in data and data["public"] and not data["owner"].is_staff:
            # Only allow staff to have public images
            raise ValidationError(_("docker.errors.custom"))

        return data
