from datetime import timedelta
from typing import TYPE_CHECKING

from api.models.course import Course
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from api.models.checks import ExtraCheck, StructureCheck
    from api.models.group import Group
    from django.db.models.manager import RelatedManager


# TODO max submission size
class Project(models.Model):
    """Model that represents a project."""

    id = models.AutoField(auto_created=True, primary_key=True)

    name = models.CharField(max_length=100, blank=False, null=False)

    description = models.TextField(blank=True, null=True)

    # Project already visible to students
    visible = models.BooleanField(default=True)

    # Project archived
    archived = models.BooleanField(default=False)

    # Locked groups
    locked_groups = models.BooleanField(default=False)

    start_date = models.DateTimeField(
        # The default value is the current date and time
        default=timezone.now,
        blank=True,
    )

    deadline = models.DateTimeField(blank=False, null=False)

    # Max score that can be achieved in the project
    max_score = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        default=20
    )

    # Score already visible to students
    score_visible = models.BooleanField(default=False)

    # Size of the groups than can be formed
    group_size = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        default=1
    )

    # Course that the project belongs to
    course = models.ForeignKey(
        Course,
        # If the course is deleted, the project should be deleted as well
        on_delete=models.CASCADE,
        related_name="projects",
        blank=False,
        null=False,
    )

    def deadline_approaching_in(self, days=7):
        """Returns True if the deadline is approaching in the next days."""
        now = timezone.now()
        approaching_date = now + timezone.timedelta(days=days)
        return now <= self.deadline <= approaching_date

    def deadline_passed(self):
        """Returns True if the deadline has passed."""
        now = timezone.now()
        return now > self.deadline

    def has_started(self):
        """Returns True if the project has started."""
        now = timezone.now()
        return now >= self.start_date

    def is_archived(self):
        """Returns True if a project is archived."""
        return self.archived

    def is_visible(self):
        """Returns True if a project is visible."""
        return self.visible

    def toggle_visible(self):
        """Toggles the visibility of the project."""
        self.visible = not self.visible
        self.save()

    def toggle_archived(self):
        """Toggles the archived status of the project."""
        self.archived = not self.archived
        self.save()

    def is_groups_locked(self):
        """Returns True if participating groups are locked."""
        return self.locked_groups

    def toggle_groups_locked(self):
        """Toggles the locked state of the groups related to the project."""
        self.locked_groups = not self.locked_groups
        self.save()

    def increase_deadline(self, days):
        self.deadline = self.deadline + timedelta(days=days)
        self.save()

    if TYPE_CHECKING:
        groups: RelatedManager[Group]
        structure_checks: RelatedManager[StructureCheck]
        extra_checks: RelatedManager[ExtraCheck]
