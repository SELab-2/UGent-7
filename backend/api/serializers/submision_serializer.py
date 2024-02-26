from rest_framework import serializers
from ..models.submission import Submission, SubmissionFile


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ['id', 'submission', 'file']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'group', 'submission_number', 'submission_time']
