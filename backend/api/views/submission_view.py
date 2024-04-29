from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from ..models.submission import Submission, SubmissionFile
from ..serializers.feedback_serializer import FeedbackSerializer
from ..serializers.submission_serializer import (SubmissionFileSerializer,
                                                 SubmissionSerializer)


class SubmissionFileViewSet(viewsets.ModelViewSet):
    queryset = SubmissionFile.objects.all()
    serializer_class = SubmissionFileSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    @action(detail=True, methods=["get"])
    def feedback(self, request, **_)  -> Response:
        """Returns all the feedback for the given submission"""
        submission = self.get_object()
        feedback = submission.feedback.all()

        # Serialize the feedback object
        serializer = FeedbackSerializer(
            feedback, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @feedback.mapping.post
    @feedback.mappint.put
    @swagger_auto_schema(request_body=)
