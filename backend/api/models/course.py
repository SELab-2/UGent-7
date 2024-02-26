from django.db import models


class Course(models.Model):
    """This model represents a single course.
    It contains all the information about a course."""

    # ID of the course should automatically be generated

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    # Begin year of the academic year
    academic_startyear = models.IntegerField(
        blank=False,
        null=False
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    # OneToOneField is used to represent a one-to-one relationship
    # with the course of the previous academic year
    parent_course = models.OneToOneField(
        'self',
        on_delete=models.SET_NULL,  # If the old course is deleted, the child course should remain
        related_name='child_course',  # Allows us to access the child course from the parent course
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        """The string representation of the course."""
        return str(self.name)

    @property
    def academic_year(self) -> str:
        """The academic year of the course."""
        return f"{self.academic_startyear}-{self.academic_startyear + 1}"
