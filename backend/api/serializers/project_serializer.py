from django.utils.translation import gettext
from rest_framework import serializers
from api.models.project import Project
from api.models.group import Group
from rest_framework.exceptions import ValidationError
from ..models.submission import Submission, SubmissionFile
from api.serializers.submission_serializer import SubmissionSerializer


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
        """
        # The validator needs the project context.
        if "project" not in self.context:
            raise ValidationError(gettext("project.error.context"))
        """

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
