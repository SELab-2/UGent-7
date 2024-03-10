from django.utils.translation import gettext
from rest_framework import serializers
from ..models.project import Project
from rest_framework.exceptions import ValidationError
from ..models.submission import Submission, SubmissionFile


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


class SubmissionAddSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # The validator needs the project context.
        if "project" not in self.context:
            raise ValidationError(gettext("project.error.context"))

        project: Project = self.context["project"]

        data["submission_number"] = 156
        # Check if the project's deadline is not passed.
        if project.deadline_passed():
            raise ValidationError(gettext("project.error.submission.past_project"))

        return data
