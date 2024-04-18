from api.models.submission import (CheckResult, ExtraCheckResult,
                                   StructureCheckResult, Submission,
                                   SubmissionFile)
from django.db.models import Max
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ["file"]


class CheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckResult
        fields = "__all__"


class StructureCheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StructureCheckResult
        exclude = ["polymorphic_ctype"]


class ExtraCheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraCheckResult
        exclude = ["polymorphic_ctype"]


class CheckResultPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        CheckResult: CheckResultSerializer,
        StructureCheckResult: StructureCheckResultSerializer,
        ExtraCheckResult: ExtraCheckResultSerializer,
    }


class SubmissionSerializer(serializers.ModelSerializer):

    group = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="group-detail"
    )

    files = SubmissionFileSerializer(many=True, read_only=True)

    results = CheckResultPolymorphicSerializer(many=True, read_only=True)

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

        # Required otherwise the default value isn't used
        validated_data["is_valid"] = True

        # Create the Submission instance without the files
        submission = Submission.objects.create(**validated_data)

        # Create SubmissionFile instances for each file and check if none fail structure checks
        for file in files_data:
            SubmissionFile.objects.create(submission=submission, file=file)
            # TODO: Run checks as a background task
            # status, _ = check_zip_file(submission.group.project, submissionFile.file.path)
            # if not status:
            #     passed = False

        submission.save()

        return submission
