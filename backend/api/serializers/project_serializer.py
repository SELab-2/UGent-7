from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext
from django.utils import timezone
from rest_framework import serializers
from ..models.project import Project
from api.models.group import Group
from api.models.course import Course
from django.utils.translation import gettext
from rest_framework import serializers
from api.models.submission import Submission, SubmissionFile
from api.serializers.submission_serializer import SubmissionSerializer


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

    def validate(self, data):
        if "course" in self.context:
            data["course_id"] = self.context["course"].id
        else:
            raise ValidationError(gettext("project.errors.context"))

        # Check if start date of the project is not in the past
        if data["start_date"] < timezone.now():
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
            raise ValidationError(gettext("project.error.submission.past_project"))

        if not project.is_visible():
            raise ValidationError(gettext("project.error.submission.non_visible_project"))

        if project.is_archived():
            raise ValidationError(gettext("project.error.submission.archived_project"))

