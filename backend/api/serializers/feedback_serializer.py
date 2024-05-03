from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.models.feedback import Feedback
from api.permissions.role_permissions import is_teacher
from api.serializers.submission_serializer import SubmissionSerializer
from api.serializers.teacher_serializer import TeacherSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for the feedback message"""
    def to_internal_value(self, data):
        if "user" in self.context:
            if not is_teacher(self.context["user"]):
                raise ValidationError(gettext("feedback.error.no_teacher"))
        return super().to_internal_value(data)

    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ["author", "submission"]
