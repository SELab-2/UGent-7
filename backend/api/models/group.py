from django.db import models
from api.models.project import Project
from api.models.student import Student


class Group(models.Model):
    """Model for group of students that work together on a project."""

    # ID should be generated automatically

    project = models.ForeignKey(
        Project,
        # If the project is deleted, the group should be deleted as well
        on_delete=models.CASCADE,
        # This is how we can access groups from a project
        related_name='groups',
        blank=False,
        null=False
    )

    # Students that are part of the group
    students = models.ManyToManyField(
        Student,
        # This is how we can access groups from a student
        related_name='groups',
        blank=False,
    )

    # Score of the group
    score = models.FloatField(
        blank=True,
        null=True
    )
