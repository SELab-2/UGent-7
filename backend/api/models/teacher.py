from authentication.models import User
from django.db import models


class Teacher(User):
    """This model represents a single teacher.
    It extends the User model from the authentication app with
    teacher-specific attributes.
    """

    # All the courses the teacher is teaching
    courses = models.ManyToManyField(
        'Course',
        related_name='teachers',  # Allows us to access the teachers from the course
        blank=True
    )
