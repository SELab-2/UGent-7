from datetime import datetime
from typing import Self
from django.db import models


class Course(models.Model):
    """This model represents a single course.
    It contains all the information about a course."""

    # ID of the course should automatically be generated

    name = models.CharField(max_length=100, blank=False, null=False)

    # Begin year of the academic year
    academic_startyear = models.IntegerField(blank=False, null=False)

    description = models.TextField(blank=True, null=True)

    # OneToOneField is used to represent a one-to-one relationship
    # with the course of the previous academic year
    parent_course = models.OneToOneField(
        "self",
        # If the old course is deleted, the child course should remain
        on_delete=models.SET_NULL,
        # Allows us to access the child course from the parent course
        related_name="child_course",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        """The string representation of the course."""
        return str(self.name)

    def is_past(self) -> bool:
        """Returns whether the course is from a past academic year"""
        return datetime(self.academic_startyear + 1, 10, 1) < datetime.now()

    def clone(self, clone_assistants=True) -> Self:
        """Clone the course to the next academic start year"""
        course = Course.objects.create(
            name=self.name,
            description=self.description,
            academic_startyear=self.academic_startyear + 1,
            parent_course=self
        )

        if clone_assistants:
            # Add all the assistants of the current course to the follow up course
            for assistant in self.assistants.all():
                course.assistants.add(assistant)

        return course

    @property
    def academic_year(self) -> str:
        """The academic year of the course."""
        return f"{self.academic_startyear}-{self.academic_startyear + 1}"
