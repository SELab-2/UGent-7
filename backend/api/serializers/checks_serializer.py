from api.models.checks import ExtraCheck, FileExtension, StructureCheck
from api.models.docker import DockerImage
from api.models.project import Project
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FileExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileExtension
        fields = ["extension"]


class StructureCheckSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedIdentityField(
        view_name="project-detail"
    )

    obligated_extensions = FileExtensionSerializer(
        many=True,
        required=False,
        default=[]
    )

    blocked_extensions = FileExtensionSerializer(
        many=True,
        required=False,
        default=[]
    )

    def validate(self, attrs):
        """Validate the structure check"""
        project: Project = self.context["project"]

        if project.structure_checks.filter(path=attrs["path"]).exists():
            raise ValidationError(_("project.error.structure_checks.already_existing"))

        return attrs

    def create(self, validated_data):
        """Create a new structure check"""
        blocked = validated_data.pop("blocked_extensions")
        obligated = validated_data.pop("obligated_extensions")
        check: StructureCheck = StructureCheck.objects.create(**validated_data)

        for ext in obligated:
            check.obligated_extensions.create(**ext)

        # Add blocked extensions

        for ext in blocked:
            check.blocked_extensions.create(**ext)

        return check

    class Meta:
        model = StructureCheck
        fields = "__all__"


class ExtraCheckSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedIdentityField(
        view_name="project-detail",
        read_only=True
    )

    docker_image = serializers.HyperlinkedIdentityField(
        view_name="docker-image-detail"
    )

    class Meta:
        model = ExtraCheck
        fields = "__all__"

    def validate(self, attrs):
        data = super().validate(attrs)

        if "time_limit" in data and not 10 <= data["time_limit"] <= 1000:
            raise serializers.ValidationError(_("extra_check.error.time_limit"))

        if "memory_limit" in data and not 50 <= data["memory_limit"] <= 1024:
            raise serializers.ValidationError(_("extra_check.error.memory_limit"))

        return data
