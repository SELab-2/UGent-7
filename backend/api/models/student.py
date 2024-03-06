from django.db import models
from authentication.models import User
from api.models.course import Course


class Student(User):
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
