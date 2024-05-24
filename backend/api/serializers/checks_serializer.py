from api.models.checks import ExtraCheck, FileExtension, StructureCheck
from api.models.docker import DockerImage
from api.models.project import Project
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound


class FileExtensionSerializer(serializers.ModelSerializer):
    extension = serializers.CharField(
        required=True,
        max_length=10
    )

    class Meta:
        model = FileExtension
        fields = ["id", "extension"]


class StructureCheckSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="project-detail"
    )

    obligated_extensions = FileExtensionSerializer(
        many=True
    )

    blocked_extensions = FileExtensionSerializer(
        many=True
    )

    def validate(self, attrs):
        """Validate the structure check"""
        project: Project = self.context["project"]

        # The structure check path should not exist already
        if project.structure_checks.filter(path=attrs["path"]).exists():
            raise ValidationError(_("project.error.structure_checks.already_existing"))

        # The same extension should not be in both blocked and obligated
        blocked = set([ext["extension"] for ext in attrs["blocked_extensions"]])
        obligated = set([ext["extension"] for ext in attrs["obligated_extensions"]])

        if blocked.intersection(obligated):
            raise ValidationError(_("project.error.structure_checks.extension_blocked_and_obligated"))

        return attrs

    def create(self, validated_data: dict) -> StructureCheck:
        """Create a new structure check"""
        blocked = validated_data.pop("blocked_extensions")
        obligated = validated_data.pop("obligated_extensions")

        check: StructureCheck = StructureCheck.objects.create(
            path=validated_data.pop("path"),
            **validated_data
        )

        for ext in obligated:
            ext, _ = FileExtension.objects.get_or_create(
                extension=ext["extension"]
            )
            check.obligated_extensions.add(ext)

        # Add blocked extensions
        for ext in blocked:
            ext, _ = FileExtension.objects.get_or_create(
                extension=ext["extension"]
            )
            check.blocked_extensions.add(ext)

        return check

    class Meta:
        model = StructureCheck
        fields = "__all__"


class ExtraCheckSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="project-detail"
    )

    docker_image = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="docker-image-detail"
    )

    class Meta:
        model = ExtraCheck
        fields = "__all__"

    def validate(self, attrs: dict) -> dict:
        """Validate the extra check"""
        data = super().validate(attrs)

        # Check if the docker image is provided
        if "docker_image" not in self.initial_data:
            raise serializers.ValidationError(_("extra_check.error.docker_image"))

        # Check if the docker image exists
        image = DockerImage.objects.get(
            id=self.initial_data["docker_image"]
        )

        if image is None:
            raise NotFound(_("extra_check.error.docker_image"))

        data["docker_image"] = image

        # Check if the time limit and memory limit are in the correct range
        if "time_limit" in data and not 10 <= data["time_limit"] <= 1000:
            raise serializers.ValidationError(_("extra_check.error.time_limit"))

        if "memory_limit" in data and not 50 <= data["memory_limit"] <= 1024:
            raise serializers.ValidationError(_("extra_check.error.memory_limit"))

        return data
