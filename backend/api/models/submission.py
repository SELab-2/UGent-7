from api.logic.get_file_path import (get_extra_check_result_file_path,
                                     get_submission_file_path)
from api.models.checks import ExtraCheck
from api.models.group import Group
from api.signals import run_extra_checks
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    # True if submission passed the structure checks
    structure_checks_passed = models.BooleanField(
        blank=False,
        null=False,
        default=False
    )

    # TODO: Does this matter? Submission number should be assigned in the backend
    class Meta:
        # A group can only have one submission with a specific number
        unique_together = ("group", "submission_number")


@receiver(post_save, sender=Submission)
def run_checks(sender, instance: Submission, **kwargs):
    run_extra_checks.send(sender=Submission, submission=instance)


# TODO: Why a different class?
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


class ErrorTemplate(models.Model):
    """
        Model possible error templates for a submission checks result.
    """

    # ID should be generated automatically

    # Key of the error template message
    message_key = models.CharField(
        max_length=256,
        blank=False,
        null=False
    )


class ExtraChecksResult(models.Model):
    """Model for the result of extra checks on a submission."""

    # Result ID should be generated automatically

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="extra_checks_results",
        blank=False,
        null=False
    )

    # Link to the extra checks that were performed
    extra_check = models.ForeignKey(
        ExtraCheck,
        on_delete=models.CASCADE,
        related_name="results",
        blank=False,
        null=False
    )

    # True if the submission passed the extra checks
    passed = models.BooleanField(
        blank=False,
        null=False,
        default=False
    )

    # Error message if the submission failed the extra checks
    error_message = models.ForeignKey(
        ErrorTemplate,
        on_delete=models.CASCADE,
        related_name="extra_checks_results",
        blank=True,
        null=True
    )

    # File path for the log file of the extra checks
    log_file = models.FileField(
        upload_to=get_extra_check_result_file_path,
        max_length=256,
        blank=False,
        null=True
    )

    # Whether the pass result is still valid
    # Becomes invalid after changing / adding a check
    is_valid = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )
