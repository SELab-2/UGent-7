from rest_framework import serializers
from ..models.submission import Submission, SubmissionFile


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ["file"]


class SubmissionSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="group-detail"
    )

    files = SubmissionFileSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = ["id", "group", "submission_number", "submission_time", "files"]
