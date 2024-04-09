from api.logic.check_folder_structure import check_zip_file  # , parse_zip_file
from api.models.submission import (ErrorTemplate, ExtraChecksResult,
                                   Submission, SubmissionFile)
from django.db.models import Max
from rest_framework import serializers


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ["file"]


class ErrorTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorTemplate
        fields = "__all__"


class ExtraChecksResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtraChecksResult
        exclude = ["log_file"]


class SubmissionSerializer(serializers.ModelSerializer):

    group = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="group-detail"
    )

    files = SubmissionFileSerializer(many=True, read_only=True)

    extra_checks_results = ExtraChecksResultSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = "__all__"
        extra_kwargs = {
            "submission_number": {
                "required": False,
                "default": 0,
            }
        }

    def create(self, validated_data):
        # Extract files from the request
        request = self.context.get('request')
        files_data = request.FILES.getlist('files')

        # Get the group for the submission
        group = validated_data['group']

        # Get the project associated with the group
        project = group.project

        # Get the maximum submission number for the group's project
        max_submission_number = Submission.objects.filter(
            group__project=project
        ).aggregate(Max('submission_number'))['submission_number__max'] or 0

        # Set the new submission number to the maximum value plus 1
        validated_data['submission_number'] = max_submission_number + 1

        # Create the Submission instance without the files
        submission = Submission.objects.create(**validated_data)

        pas: bool = True
        # Create SubmissionFile instances for each file and check if none fail structure checks
        for file in files_data:
            SubmissionFile.objects.create(submission=submission, file=file)
            status, _ = check_zip_file(submission.group.project, file.name)
            if not status:
                pas = False

        # Set structure_checks_passed
        submission.structure_checks_passed = pas
        submission.save()
        return submission
