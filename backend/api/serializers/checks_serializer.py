from rest_framework import serializers

from ..models.checks import ExtraCheck, StructureCheck
from ..models.extension import FileExtension


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


class ExtraCheckSerializer(serializers.ModelSerializer):

    project = serializers.HyperlinkedRelatedField(
        view_name="project-detail",
        read_only=True
    )

    class Meta:
        model = ExtraCheck
        fields = [
            "id",
            "project"
        ]
