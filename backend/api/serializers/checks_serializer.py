from rest_framework import serializers
from ..models.extension import FileExtension
from ..models.checks import StructureCheck, ExtraCheck


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
        fields = [
            "id",
            "name",
            "project",
            "obligated_extensions",
            "blocked_extensions"
        ]


class ExtraCheckSerializer(serializers.ModelSerializer):

    project = serializers.HyperlinkedRelatedField(
        view_name="project-detail",
        read_only=True
    )

    class Meta:
        model = ExtraCheck
        fields = [
            "id",
            "project",
            "run_script"
        ]
