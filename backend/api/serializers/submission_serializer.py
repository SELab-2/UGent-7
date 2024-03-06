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

    extra_checks_results = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="extra_checks-detail"
    )

    class Meta:
        model = Submission
        fields = [
            "id",
            "group",
            "submission_number",
            "submission_time",
            "files",
            "structure_checks_passed",
            "extra_checks_results"
        ]
