from django.core.files import File
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import RetrieveModelMixin

from ..models.submission import Submission
from ..serializers.feedback_serializer import FeedbackSerializer
from ..serializers.submission_serializer import SubmissionSerializer


# TODO: Permission to ask for logs
class SubmissionViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    @action(detail=True, methods=["get"])
    def feedback(self, request, **_) -> Response:
        """Returns all the feedback for the given submission"""
        submission = self.get_object()
        feedback = submission.feedback.all()

        # Serialize the feedback object
        serializer = FeedbackSerializer(
            feedback, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @feedback.mapping.post
    @feedback.mapping.put
    def _add_feedback(self, request, **_) -> Response:
        """Adds feedback to the given submission"""
        submission = self.get_object()
        context = {"request": request, "user": request.user, "submission": submission}
        serializer = FeedbackSerializer(data=request.data, context=context)

        if serializer.is_valid():
            serializer.save(submission=submission)
            return Response({
                "message": "Success",
                "feedback": serializer.data
            })

        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["get"])
    def download(self, request: Request, **_) -> FileResponse:
        """Downloads the submission"""
        submission = self.get_object()
        file: File = submission.zip

        response = FileResponse(file.file.open(), filename="submission_" + str(submission.pk) + ".zip")
        response["Conent-Length"] = file.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % f'submission_{str(submission.pk)}.zip'
        return response
