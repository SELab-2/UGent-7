import io
import zipfile

from rest_framework.reverse import reverse

from api.models.group import Group
from api.models.project import Project
from api.models.submission import (CheckResult, ExtraCheckResult,
                                   StructureCheckResult, Submission)
from django.core.files import File
from django.db.models import Max
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_polymorphic.serializers import PolymorphicSerializer


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

    results = CheckResultPolymorphicSerializer(many=True, read_only=True)
    zip = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = "__all__"
        extra_kwargs = {
            "submission_number": {
                "required": False,
                "default": 0,
            }
        }

    def get_zip(self, obj):
        if obj.zip:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(reverse('submission-download', args=[obj.pk]))
        return None

    def validate(self, attrs):

        group: Group = self.context["group"]
        project: Project = group.project

        # Check if the project's deadline is not passed.
        if project.deadline_passed():
            raise ValidationError(_("project.error.submissions.past_project"))

        if not project.is_visible():
            raise ValidationError(_("project.error.submissions.non_visible_project"))

        if project.is_archived():
            raise ValidationError(_("project.error.submissions.archived_project"))

        if "files" not in self.context["request"].FILES or len(self.context["request"].FILES.getlist("files")) == 0:
            raise ValidationError(_("project.error.submissions.no_files"))

        return attrs

    def create(self, validated_data):
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

        # Zip all the files into a single file
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, 'w') as zip:
            for file in self.context["request"].FILES.getlist("files"):
                zip.writestr(file.name, file.read())
        memory_zip.seek(0)

        validated_data["zip"] = File(memory_zip, name="submission.zip")

        # Create the Submission instance without the files
        submission = Submission.objects.create(**validated_data)

        return submission
