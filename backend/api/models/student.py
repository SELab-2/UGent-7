from authentication.models import User
from django.db import models


class Student(User):
    """This model represents a single student.
    It extends the User model from the authentication app with
    student-specific attributes.
    """

    # All the courses the student is enrolled in
    courses = models.ManyToManyField(
        'Course',
        related_name='students',  # Allows us to access the students from the course
        blank=True
    )
