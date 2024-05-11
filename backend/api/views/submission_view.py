from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin

from ..models.submission import Submission
from ..serializers.submission_serializer import SubmissionSerializer


# TODO: Permission to ask for logs
class SubmissionViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    @action(detail=True)
    def zip(self, request, **_):
        submission: Submission = self.get_object()

        return FileResponse(open(submission.zip.path, "rb"), as_attachment=True)
