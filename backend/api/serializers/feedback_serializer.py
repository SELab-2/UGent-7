from rest_framework import serializers
from api.serializers.submission_serializer import SubmissionSerializer
from api.serializers.teacher_serializer import TeacherSerializer


class FeedbackSerializer(serializers.Serializer):
    """Serializer for the feedback message"""
    message = serializers.CharField(required=True)
    author = TeacherSerializer(read_only=True)
    submission = SubmissionSerializer(read_only=True)

    def to_internal_value(self, data):
        data["author"] = self.context["request"].user.teacher
        return super().to_internal_value(data)

