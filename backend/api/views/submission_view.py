from django.http import FileResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.models.submission import Submission, StructureCheckResult, ExtraCheckResult
from api.permissions.submission_permissions import SubmissionPermission, StructureCheckResultPermission, \
    ExtraCheckResultPermission, ExtraCheckResultArtifactPermission, ExtraCheckResultLogPermission, \
    SubmissionFeedbackPermission
from api.serializers.feedback_serializer import FeedbackSerializer
from api.serializers.submission_serializer import (
    ExtraCheckResultSerializer, StructureCheckResultSerializer,
    SubmissionSerializer)


class SubmissionViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [SubmissionPermission]

    @action(detail=True)
    def zip(self, request, **__):
        submission: Submission = self.get_object()

        if not submission.zip:
            return Response({"message": _("submission.download.zip")}, status=404)

        return FileResponse(open(submission.zip.path, "rb"), as_attachment=True)

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | SubmissionFeedbackPermission])
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
            serializer.save(submission=submission, author=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class StructureCheckResultViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = StructureCheckResult.objects.all()
    serializer_class = StructureCheckResultSerializer
    permission_classes = [StructureCheckResultPermission]


class ExtraCheckResultViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = ExtraCheckResult.objects.all()
    serializer_class = ExtraCheckResultSerializer
    permission_classes = [ExtraCheckResultPermission]

    @action(detail=True, permission_classes=[IsAdminUser | ExtraCheckResultArtifactPermission])
    def log(self, request, **__):
        extra_check_result: ExtraCheckResult = self.get_object()

        if not extra_check_result.log_file:
            return Response({"message": _("extra_check_result.download.log")}, status=404)

        return FileResponse(open(extra_check_result.log_file.path, "rb"), as_attachment=True, filename="log.txt")

    @action(detail=True, permission_classes=[IsAdminUser | ExtraCheckResultLogPermission])
    def artifact(self, request, **__):
        extra_check_result: ExtraCheckResult = self.get_object()

        if not extra_check_result.artifact:
            return Response({"message": _("extra_check_result.download.artifact")}, status=404)

        return FileResponse(open(extra_check_result.artifact.path, "rb"), as_attachment=True, filename="artifact.zip")
