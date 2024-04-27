from api.models.checks import ExtraCheck, StructureCheck
from api.models.docker import DockerImage
from api.models.extension import FileExtension
from api.models.project import Project
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FileExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileExtension
        fields = ["extension"]


class FileExtensionHyperLinkedRelatedField(serializers.HyperlinkedRelatedField):
    view_name = "file-extensions-detail"
    queryset = FileExtension.objects.all()

    def to_internal_value(self, data):
        try:
            return self.queryset.get(pk=data)
        except FileExtension.DoesNotExist:
            return self.fail("no_match")


# TODO: Support partial updates
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


# TODO: Simplify
class StructureCheckAddSerializer(StructureCheckSerializer):

    def validate(self, attrs):
        project: Project = self.context["project"]
        if project.structure_checks.filter(name=attrs["name"]).count():
            raise ValidationError(_("project.error.structure_checks.already_existing"))

        obl_ext = set()
        for ext in self.context["obligated"]:
            extension, result = FileExtension.objects.get_or_create(
                extension=ext
            )
            obl_ext.add(extension)
        attrs["obligated_extensions"] = obl_ext

        block_ext = set()
        for ext in self.context["blocked"]:
            extension, result = FileExtension.objects.get_or_create(
                extension=ext
            )
            if extension in obl_ext:
                raise ValidationError(_("project.error.structure_checks.extension_blocked_and_obligated"))
            block_ext.add(extension)
        attrs["blocked_extensions"] = block_ext

        return attrs


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
