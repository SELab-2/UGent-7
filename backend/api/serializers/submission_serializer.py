from rest_framework import serializers
from ..models.submission import Submission, SubmissionFile, ExtraChecksResult


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ["file"]


class ExtraChecksResultSerializer(serializers.ModelSerializer):

    extra_check = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name="extra_check-detail"
    )

    class Meta:
        model = ExtraChecksResult
        fields = [
            "extra_check",
            "passed"
        ]


class SubmissionSerializer(serializers.ModelSerializer):

    group = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="group-detail"
    )

    files = SubmissionFileSerializer(many=True, read_only=True)

    extra_checks_results = ExtraChecksResultSerializer(many=True, read_only=True)

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
