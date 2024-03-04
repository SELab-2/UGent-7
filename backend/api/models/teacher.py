from django.db import models
from api.models.course import Course
from authentication.models import User


class Teacher(User):
    """This model represents a single teacher.
    It extends the User model from the authentication app with
    teacher-specific attributes.
    """

    # All the courses the teacher is teaching
    courses = models.ManyToManyField(
        Course,
        # Allows us to access the teachers from the course
        related_name="teachers",
        blank=True,
    )
