from authentication.models import User
from django.db import models


class Assistant(User):
    """This model represents a single assistant.
    It extends the User model from the authentication app with
    assistant-specific attributes.
    """

    # All the courses the assistant is assisting in
    courses = models.ManyToManyField(
        'Course',
        related_name='assistants',  # Allows us to access the assistants from the course
        blank=True
    )
