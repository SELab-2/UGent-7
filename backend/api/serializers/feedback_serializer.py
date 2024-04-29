from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FeedbackSerializer(serializers.Serializer):
    """Serializer for the feedback message"""
    message = serializers.CharField()
    author = serializers.HyperlinkedIdentityField(
        view_name="user-detail",
        read_only=True
    )

    def validate(self, data):
        """Validate the serializer data"""
        if "message" not in data:
            raise ValidationError("message is required")

        return data