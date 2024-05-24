from typing import cast

from api.models.submission import (ExtraCheckResult, StructureCheckResult,
                                   Submission)
from api.permissions.role_permissions import (is_assistant, is_student,
                                              is_teacher)
from authentication.models import User
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class SubmissionPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        submission_id = view.kwargs.get("pk")

        if request.method not in SAFE_METHODS or submission_id is None:
            return False

        user: User = cast(User, request.user)
        # check if user is in group of submission
        group = Submission.objects.get(id=submission_id).group
        return user.is_staff or is_teacher(user) or is_assistant(user) or group.students.filter(id=user.id).exists()

    def has_object_permission(self, request: Request, view: APIView, obj: Submission) -> bool:
        if request.method not in SAFE_METHODS:
            return False

        user: User = cast(User, request.user)

        if user.is_staff:
            return True

        if is_teacher(user) or is_assistant(user):
            return True

        return obj.group.students.filter(id=user.id).exists()


class SubmissionFeedbackPermission(SubmissionPermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return True

    def has_object_permission(self, request: Request, view: APIView, submission: Submission) -> bool:
        if is_student(request.user) and submission.group.students.filter(id=request.user.id):
            return True

        if is_teacher(request.user) or is_assistant(request.user):
            return True

        return False


class StructureCheckResultPermission(SubmissionPermission):
    def has_object_permission(self, request: Request, view: APIView, obj: StructureCheckResult) -> bool:
        return super().has_object_permission(request, view, obj.submission)


class ExtraCheckResultPermission(SubmissionPermission):
    def has_object_permission(self, request: Request, view: APIView, obj: ExtraCheckResult) -> bool:
        return super().has_object_permission(request, view, obj.submission)


class ExtraCheckResultLogPermission(ExtraCheckResultPermission):
    def has_object_permission(self, request: Request, view: APIView, obj: ExtraCheckResult) -> bool:
        result = super().has_object_permission(request, view, obj)

        if not result:
            return False

        user: User = cast(User, request.user)

        if is_student(user):
            return obj.extra_check.show_log

        return True


class ExtraCheckResultArtifactPermission(ExtraCheckResultPermission):
    def has_object_permission(self, request: Request, view: APIView, obj: ExtraCheckResult) -> bool:
        result = super().has_object_permission(request, view, obj)

        if not result:
            return False

        user: User = cast(User, request.user)

        if is_student(user):
            return obj.extra_check.show_artifact

        return True
