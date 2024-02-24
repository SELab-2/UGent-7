from django.db import models


class Group(models.Model):
    """Model for group of students that work together on a project."""

    # ID should be generated automatically

    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,  # If the project is deleted, the group should be deleted as well
        related_name='groups',     # This is how we can access groups from a project
        blank=False,
        null=False
    )

    # Students that are part of the group
    students = models.ManyToManyField(
        'Student',
        related_name='groups',  # This is how we can access groups from a student
        blank=False,
        null=False
    )
