import datetime
from django.db import models


class Project(models.Model):
    """Model that represents a project."""

    # ID should be generated automatically

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    # Project already visible to students
    visible = models.BooleanField(
        default=True
    )

    # Project archived
    archived = models.BooleanField(
        default=False
    )

    start_date = models.DateTimeField(
        default=datetime.datetime.now,  # The default value is the current date and time
        blank=True,
    )

    deadline = models.DateTimeField(
        blank=False,
        null=False
    )

    # Check entity that is linked to the project
    checks = models.ForeignKey(
        'Checks',
        on_delete=models.SET_NULL,  # If the checks are deleted, the project should remain
        blank=True,
        null=True
    )

    # Course that the project belongs to
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,  # If the course is deleted, the project should be deleted as well
        blank=False,
        null=False
    )
