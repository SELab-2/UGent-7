from django.db import models
from authentication.models import User
from api.models.course import Course
from api.models.mixins.role import RoleMixin


class Assistant(RoleMixin, User):
    """This model represents a single assistant.
    It extends the User model from the authentication app with
    assistant-specific attributes.
    """

    # All the courses the assistant is assisting in
    courses = models.ManyToManyField(
        Course,
        # Allows us to access the assistants from the course
        related_name="assistants",
        blank=True,
    )
