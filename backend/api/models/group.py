from typing import TYPE_CHECKING

from api.models.project import Project
from api.models.student import Student
from django.db import models

if TYPE_CHECKING:
    from api.models.submission import Submission
    from django.db.models.manager import RelatedManager


class Group(models.Model):
    """Model for group of students that work together on a project."""

    id = models.AutoField(auto_created=True, primary_key=True)

    project = models.ForeignKey(
        Project,
        # If the project is deleted, the group should be deleted as well
        on_delete=models.CASCADE,
        # This is how we can access groups from a project
        related_name="groups",
        blank=False,
        null=False,
    )

    # Students that are part of the group
    students = models.ManyToManyField(
        Student,
        # This is how we can access groups from a student
        related_name="groups",
        blank=False,
    )

    # Score of the group
    score = models.FloatField(blank=True, null=True)

    def is_full(self) -> bool:
        """Check if the group is full."""
        return self.students.count() >= self.project.group_size

    if TYPE_CHECKING:
        submissions: RelatedManager['Submission']
