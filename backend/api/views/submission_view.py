from api.models.submission import (ExtraCheckResult, StructureCheckResult,
                                   Submission)
from api.permissions.submission_permissions import (
    ExtraCheckResultArtifactPermission, ExtraCheckResultLogPermission,
    ExtraCheckResultPermission, StructureCheckResultPermission,
    SubmissionPermission)
from api.serializers.submission_serializer import (
    ExtraCheckResultSerializer, StructureCheckResultSerializer,
    SubmissionSerializer)
from django.http import FileResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


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
