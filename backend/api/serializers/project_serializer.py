from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext
from django.utils import timezone
from rest_framework import serializers
from ..models.project import Project
from api.models.course import Course


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

        # Check if start data of the project is not in the past
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
