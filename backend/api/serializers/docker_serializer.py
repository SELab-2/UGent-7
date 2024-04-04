from api.models.docker import DockerImage
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class DockerImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DockerImage
        fields: str = "__all__"

    # TODO: Test if valid docker image (or not and trust the user)
    def validate(self, attrs):
        data = super().validate(attrs=attrs)

        if "user" not in self.context:
            raise ValidationError(_("docker.errors.context"))

        if data["public"] and not self.context["user"].is_staff:
            raise ValidationError(_("docker.errors.custom"))

        return data
