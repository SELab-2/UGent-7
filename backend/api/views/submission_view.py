from rest_framework import viewsets

from ..models.submission import Submission, SubmissionFile
from ..serializers.submission_serializer import (SubmissionFileSerializer,
                                                 SubmissionSerializer)


class SubmissionFileViewSet(viewsets.ModelViewSet):
    queryset = SubmissionFile.objects.all()
    serializer_class = SubmissionFileSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
