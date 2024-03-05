from rest_framework import serializers
from ..models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    course = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="course-detail"
    )

    checks = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="check-detail"
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
            "checks",
            "course",
        ]
