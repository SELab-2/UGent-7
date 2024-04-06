from api.models.checks import ExtraCheck, StructureCheck
from api.models.docker import DockerImage
from api.models.extension import FileExtension
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

        # TODO: Doesn't allow PATCH
        if "docker_image" not in data:
            # TODO: translation
            raise serializers.ValidationError("docker_image is required")

        return data
