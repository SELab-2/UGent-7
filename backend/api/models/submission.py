from api.logic.get_file_path import (get_extra_check_result_file_path,
                                     get_submission_file_path)
from api.models.checks import ExtraCheck, StructureCheck
from api.models.group import Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel


class Submission(models.Model):
    """Model for submission of a project by a group of students."""

    # Submission ID should be generated automatically

    group = models.ForeignKey(
        Group,
        # If the group is deleted, the submission should be deleted as well
        on_delete=models.CASCADE,
        related_name="submissions",
        blank=False,
        null=False,
    )

    # Multiple submissions can be made by a group
    submission_number = models.PositiveIntegerField(blank=True, null=True)

    # Automatically set the submission time to the current time
    submission_time = models.DateTimeField(auto_now_add=True)

    # Whether the checks results are still valid
    # Becomes invalid after changing / adding a check
    is_valid = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )

    class Meta:
        # A group can only have one submission with a specific number
        unique_together = ("group", "submission_number")


class SubmissionFile(models.Model):
    """Model for a file that is part of a submission."""

    # File ID should be generated automatically

    submission = models.ForeignKey(
        Submission,
        # If the submission is deleted, the file should be deleted as well
        on_delete=models.CASCADE,
        related_name="files",
        blank=False,
        null=False,
    )

    file = models.FileField(
        upload_to=get_submission_file_path,
        max_length=265,
        blank=False,
        null=False
    )


class StateEnum(models.TextChoices):
    QUEUED = "QUEUED", _("submission.state.queued")
    RUNNING = "RUNNING", _("submission.state.running")
    SUCCESS = "SUCCESS", _("submission.state.success")
    FAILED = "FAILED", _("submission.state.failed")


class ErrorMessageEnum(models.TextChoices):
    # Structure checks errors
    BLOCKED_EXTENSION = "BLOCKED_EXTENSION", _("submission.error.blockedextension")
    OBLIGATED_EXTENSION_NOT_FOUND = "OBLIGATED_EXTENSION_NOT_FOUND", _("submission.error.obligatedextensionnotfound")
    OBLIGATED_DIRECTORY_NOT_FOUND = "OBLIGATED_DIRECTORY_NOT_FOUND", _("submission.error.obligateddirectorynotfound")
    UNASKED_DIRECTORY = "UNASKED_DIRECTORY", _("submission.error.unaskeddirectory")

    # Extra checks errors
    DOCKER_IMAGE_ERROR = "DOCKER_IMAGE_ERROR", _("submission.error.dockerimageerror")
    TIMELIMIT = "TIMELIMIT", _("submission.error.timelimit")
    MEMORYLIMIT = "MEMORYLIMIT", _("submission.error.memorylimit")
    RUNTIMEERROR = "RUNTIMEERROR", _("submission.error.runtimeerror")
    UNKNOWN = "UNKNOWN", _("submission.error.unknown")


class CheckResult(PolymorphicModel):

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="results",
        blank=False,
        null=False
    )

    result = models.CharField(
        max_length=256,
        choices=StateEnum.choices,
        default=StateEnum.QUEUED,
        blank=False,
        null=False
    )

    error_message = models.CharField(
        max_length=256,
        choices=ErrorMessageEnum.choices,
        blank=True,
        null=True
    )


class StructureCheckResult(CheckResult):

    structure_check = models.ForeignKey(
        StructureCheck,
        on_delete=models.CASCADE,
        related_name="structure_check",
        blank=False,
        null=False
    )


class ExtraCheckResult(CheckResult):

    # Link to the extra checks that were performed
    extra_check = models.ForeignKey(
        ExtraCheck,
        on_delete=models.CASCADE,
        related_name="extra_check",
        blank=False,
        null=False
    )

    # File path for the log file of the extra checks
    log_file = models.FileField(
        upload_to=get_extra_check_result_file_path,
        max_length=256,
        blank=False,
        null=True
    )
