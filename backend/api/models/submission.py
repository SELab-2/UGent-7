from django.db import models
from api.models.group import Group

class Submission(models.Model):
    """Model for submission of a project by a group of students."""

    # Submission ID should be generated automatically

    group = models.ForeignKey(
        Group,
        # If the group is deleted, the submission should be deleted as well
        on_delete=models.CASCADE,
        related_name='submissions',
        blank=False,
        null=False
    )

    # Multiple submissions can be made by a group
    submission_number = models.PositiveIntegerField(
        blank=False,
        null=False
    )

    # Automatically set the submission time to the current time
    submission_time = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        # A group can only have one submission with a specific number
        unique_together = ('group', 'submission_number')


class SubmissionFile(models.Model):
    """Model for a file that is part of a submission."""

    # File ID should be generated automatically

    submission = models.ForeignKey(
        Submission,
        # If the submission is deleted, the file should be deleted as well
        on_delete=models.CASCADE,
        related_name='files',
        blank=False,
        null=False
    )

    # TODO - Set the right place to save the file
    file = models.FileField(
        blank=False,
        null=False
    )