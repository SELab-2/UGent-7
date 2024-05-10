from typing import TYPE_CHECKING

from api.models.course import Course
from api.models.mixins.role import RoleMixin
from authentication.models import User
from django.db import models

if TYPE_CHECKING:
    from api.models.group import Group
    from django.db.models.manager import RelatedManager


class Student(RoleMixin, User):
    """This model represents a single student.
    It extends the User model from the authentication app with
    student-specific attributes.
    """

    # The student's Ghent University ID
    student_id = models.CharField(max_length=8, null=True, unique=True)

    # All the courses the student is enrolled in
    courses = models.ManyToManyField(
        Course,
        # Allows us to access the students from the course
        related_name="students",
        blank=True,
    )

    def is_enrolled_in_group(self, project):
        """Check if the student is enrolled in a group for the given project."""
        return self.groups.filter(project=project).exists()

    if TYPE_CHECKING:
        groups: RelatedManager['Group']
