from rest_framework import serializers
from ..models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="project-detail"
    )

    students = serializers.HyperlinkedIdentityField(
        view_name="group-students",
        read_only=True,
    )

    class Meta:
        model = Group
        fields = ["id", "project", "students", "score"]
