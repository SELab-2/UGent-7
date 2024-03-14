from django.utils.translation import gettext
from rest_framework import serializers
from api.models.project import Project
from api.models.group import Group
from rest_framework.exceptions import ValidationError
from api.models.submission import Submission, SubmissionFile
from api.models.checks import FileExtension, StructureCheck
from api.serializers.submission_serializer import SubmissionSerializer
from api.serializers.checks_serializer import StructureCheckSerializer
from rest_framework.request import Request


class ProjectSerializer(serializers.ModelSerializer):
    course = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="course-detail"
    )

    structure_checks = serializers.HyperlinkedIdentityField(
        view_name="project-structure-checks",
        read_only=True
    )

    extra_checks = serializers.HyperlinkedIdentityField(
        view_name="project-extra-checks",
        read_only=True
    )

    groups = serializers.HyperlinkedIdentityField(
        view_name="project-groups",
        read_only=True
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "visible",
            "archived",
            "start_date",
            "deadline",
            "max_score",
            "group_size",
            "structure_checks",
            "extra_checks",
            "course",
            "groups"
        ]


class TeacherCreateGroupSerializer(serializers.Serializer):
    number_groups = serializers.IntegerField(min_value=1)


class SubmissionAddSerializer(SubmissionSerializer):
    def validate(self, data):

        group: Group = self.context["group"]
        project: Project = group.project

        # Check if the project's deadline is not passed.
        if project.deadline_passed():
            raise ValidationError(gettext("project.error.submission.past_project"))

        if not project.is_visible():
            raise ValidationError(gettext("project.error.submission.non_visible_project"))

        if project.is_archived():
            raise ValidationError(gettext("project.error.submission.archived_project"))

        return data


class StructureCheckAddSerializer(StructureCheckSerializer):
    def validate(self, data):
        project: Project = self.context["project"]
        if project.structure_checks.filter(name=data["name"]).count():
            raise ValidationError(gettext("project.error.structure_checks.already_existing"))

        obl_ext = set()
        for ext in self.context["obligated"]:
            extensie, _ = FileExtension.objects.get_or_create(
                extension=ext
            )
            obl_ext.add(extensie)
        data["obligated_extensions"] = obl_ext

        block_ext = set()
        for ext in self.context["blocked"]:
            extensie, _ = FileExtension.objects.get_or_create(
                extension=ext
            )
            if extensie in obl_ext:
                raise ValidationError(gettext("project.error.structure_checks.extension_blocked_and_obligated"))
            block_ext.add(extensie)
        data["blocked_extensions"] = block_ext

        return data


class StructureCheckDeleteSerializer(StructureCheckSerializer):
    def validate(self, data):
        if "project" not in self.context:
            raise ValidationError(gettext("project.error.context"))

        project: Project = self.context["project"]

        # Get the struture_check
        structureCheck: StructureCheck = data["structure_check_id"]

        # Make sure the struture_check was in the project
        if True or not project.structure_checks.filter(id=structureCheck.id).exists():
            raise ValidationError(gettext("struture_check.errors.not_present"))

        return data
