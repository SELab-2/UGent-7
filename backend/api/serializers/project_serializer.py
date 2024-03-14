from django.utils.translation import gettext
from rest_framework import serializers
from api.models.project import Project
from api.models.group import Group
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from api.models.checks import FileExtension
from api.serializers.submission_serializer import SubmissionSerializer
from api.serializers.checks_serializer import StructureCheckSerializer


class ProjectSerializer(serializers.ModelSerializer):
    course = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="course-detail",
        read_only=True
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

    submissions = serializers.HyperlinkedIdentityField(
        view_name="project-submissions",
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
            "score_visible",
            "group_size",
            "structure_checks",
            "extra_checks",
            "course",
            "groups",
            "submissions"
        ]

    def validate(self, data):
        if "course" in self.context:
            data["course_id"] = self.context["course"].id
        else:
            raise ValidationError(gettext("project.errors.context"))

        # Check if start date of the project is not in the past
        if data["start_date"] < timezone.now().replace(hour=0, minute=0, second=0):
            raise ValidationError(gettext("project.errors.start_date_in_past"))

        # Check if deadline of the project is before the start date
        if data["deadline"] < data["start_date"]:
            raise ValidationError(gettext("project.errors.deadline_before_start_date"))

        return data


class TeacherCreateGroupSerializer(serializers.Serializer):
    number_groups = serializers.IntegerField(min_value=1)

    def validate(self, data):
        return data


class SubmissionStatusSerializer(serializers.Serializer):
    non_empty_groups = serializers.IntegerField(read_only=True)
    groups_submitted = serializers.IntegerField(read_only=True)
    submissions_passed = serializers.IntegerField(read_only=True)


class SubmissionAddSerializer(SubmissionSerializer):
    def validate(self, data):

        group: Group = self.context["group"]
        project: Project = group.project

        # Check if the project's deadline is not passed.
        if project.deadline_passed():
            raise ValidationError(gettext("project.error.submissions.past_project"))

        if not project.is_visible():
            raise ValidationError(gettext("project.error.submissions.non_visible_project"))

        if project.is_archived():
            raise ValidationError(gettext("project.error.submissions.archived_project"))

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
