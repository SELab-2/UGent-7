from rest_framework import serializers

from api.models.feedback import Feedback
from api.serializers.submission_serializer import SubmissionSerializer
from api.serializers.teacher_serializer import TeacherSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for the feedback message"""
    def to_internal_value(self, data):
        data["author"] = self.context["request"].user.teacher
        return super().to_internal_value(data)

    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ["author", "submission"]
