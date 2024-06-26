from django.db import models
from api.models.submission import Submission
from authentication.models import User


class Feedback(models.Model):
    """Model that represents a feedback message."""

    # ID should be generated automatically

    # Feedback message
    message = models.TextField(null=False)

    # Feedback message author
    author = models.ForeignKey(
        User,
        # If the author is deleted, the feedback message should be deleted as well
        on_delete=models.CASCADE,
        related_name="feedback_messages",
        blank=False,
        null=False,
    )

    # Feedback message creation date
    creation_date = models.DateTimeField(
        # The default value is the current date and time
        auto_now_add=True,
        blank=False,
        null=False
    )

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="feedback",
        blank=False,
        null=False
    )
