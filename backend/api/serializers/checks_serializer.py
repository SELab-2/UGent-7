from api.models.checks import ExtraCheck, StructureCheck
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


# TODO: Check if docker image is public and / or his
class ExtraCheckSerializer(serializers.ModelSerializer):

    project = serializers.HyperlinkedRelatedField(
        view_name="project-detail",
        read_only=True
    )

    # docker_image = serializers.HyperlinkedRelatedField(
    #     view_name="docker-image-detail",
    #     read_only=True
    # )

    class Meta:
        model = ExtraCheck
        fields = "__all__"
