from datetime import datetime
from django.db import models
from api.models.checks import Checks
from api.models.course import Course


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
        # The default value is the current date and time
        default=datetime.now,
        blank=True,
    )

    deadline = models.DateTimeField(
        blank=False,
        null=False
    )

    # Check entity that is linked to the project
    checks = models.ForeignKey(
        Checks,
        # If the checks are deleted, the project should remain
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    # Course that the project belongs to
    course = models.ForeignKey(
        Course,
        # If the course is deleted, the project should be deleted as well
        on_delete=models.CASCADE,
        related_name='projects',
        blank=False,
        null=False
    )
