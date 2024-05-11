from rest_framework import viewsets
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin

from ..models.submission import Submission
from ..serializers.submission_serializer import SubmissionSerializer


# TODO: Permission to ask for logs
class SubmissionViewSet(RetrieveModelMixin, viewsets.GenericViewSet, DestroyModelMixin):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
