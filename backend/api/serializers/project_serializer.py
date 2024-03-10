from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext
from rest_framework import serializers
from ..models.project import Project
from api.models.course import Course


class ProjectSerializer(serializers.ModelSerializer):
    course = serializers.HyperlinkedRelatedField(
        many=False, view_name="course-detail", queryset=Course.objects.all()
    )

    structure_checks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="structure-check-detail"
    )

    extra_checks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="extra-check-detail"
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
        print("*** Project validation goes here ***")
        return data


class TeacherCreateGroupSerializer(serializers.Serializer):
    number_groups = serializers.IntegerField(min_value=1)

    def validate(self, data):
        return data
