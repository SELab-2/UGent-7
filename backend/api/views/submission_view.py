from rest_framework import viewsets

from ..models.submission import Submission
from ..serializers.submission_serializer import SubmissionSerializer


# TODO: Permission to ask for logs
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
