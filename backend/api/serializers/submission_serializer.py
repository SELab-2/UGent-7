from rest_framework import serializers
from ..models.submission import Submission, SubmissionFile, ExtraChecksResult
from api.helpers.check_folder_structure import check_zip_file # , parse_zip_file


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ["file"]


class ExtraChecksResultSerializer(serializers.ModelSerializer):

    extra_check = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name="extra-check-detail"
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

    def create(self, validated_data):
        # Extract files from the request
        request = self.context.get('request')
        files_data = request.FILES.getlist('files')

        # Create the Submission instance without the files
        submission = Submission.objects.create(**validated_data)

        pas: bool = True
        # Create SubmissionFile instances for each file and check if none fail structure checks
        for file in files_data:
            SubmissionFile.objects.create(submission=submission, file=file)
            status, _ = check_zip_file(submission.group.project, file.name)
            if not status:
                pas = False

        # Set structure_checks_passed to True
        submission.structure_checks_passed = pas
        submission.save()
        return submission
