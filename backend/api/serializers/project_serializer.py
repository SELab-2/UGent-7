from rest_framework import serializers
from ..models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    course = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="course-detail"
    )

    structure_checks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="structure_check-detail"
    )

    extra_checks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="extra_check-detail"
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
