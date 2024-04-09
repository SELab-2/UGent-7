from api.models.checks import ExtraCheck, StructureCheck
from api.models.docker import DockerImage
from api.models.extension import FileExtension
from django.utils.translation import gettext as _
from rest_framework import serializers


class FileExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileExtension
        fields = ["extension"]


class StructureCheckSerializer(serializers.ModelSerializer):

    project = serializers.HyperlinkedRelatedField(
        view_name="project-detail",
        read_only=True
    )

    obligated_extensions = FileExtensionSerializer(many=True, required=False, default=[])

    blocked_extensions = FileExtensionSerializer(many=True, required=False, default=[])

    class Meta:
        model = StructureCheck
        fields = "__all__"


class DockerImagerHyperLinkedRelatedField(serializers.HyperlinkedRelatedField):
    view_name = "docker-image-detail"
    queryset = DockerImage.objects.all()

    def to_internal_value(self, data):
        try:
            return self.queryset.get(pk=data)
        except DockerImage.DoesNotExist:
            return self.fail("no_match")


class ExtraCheckSerializer(serializers.ModelSerializer):

    project = serializers.HyperlinkedRelatedField(
        view_name="project-detail",
        read_only=True
    )

    docker_image = DockerImagerHyperLinkedRelatedField()

    class Meta:
        model = ExtraCheck
        fields = "__all__"

    def validate(self, attrs):
        data = super().validate(attrs)

        # Only check if docker image is present when it is not a partial update
        if not self.partial:
            if "docker_image" not in data:
                raise serializers.ValidationError(_("extra_check.error.docker_image"))

        if "timeout" in data and data["timeout"] > 1000:
            raise serializers.ValidationError(_("extra_check.error.timeout"))

        return data
