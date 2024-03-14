from rest_framework import serializers
from ..models.assistant import Assistant


class AssistantSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
        view_name="assistant-courses",
        read_only=True,
    )

    faculties = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="faculty-detail"
    )

    class Meta:
        model = Assistant
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "faculties",
            "last_enrolled",
            "create_time",
            "courses",
        ]


class AssistantIDSerializer(serializers.Serializer):
    assistant = serializers.PrimaryKeyRelatedField(
        queryset=Assistant.objects.all()
    )
