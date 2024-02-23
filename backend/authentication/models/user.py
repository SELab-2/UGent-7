import datetime

from django.db.models import CharField, EmailField, IntegerField, DateTimeField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """This model represents a single authenticatable user.
    It extends the built-in Django user model with CAS-specific attributes.
    """
    id = CharField(
        primary_key=True
    )

    first_name = CharField(
        blank=False,
        null=False
    )

    last_name = CharField(
        blank=False,
        null=False
    )

    email = EmailField(
        blank=False,
        null=False,
        unique=True
    )

    faculty = CharField(
        blank=True
    )

    last_enrolled = IntegerField(
        default = datetime.MINYEAR,
        blank = True,
        null = True
    )

    last_login_at = DateTimeField(
        null=True,
        blank=True
    )

    created_at = DateTimeField(
        auto_now_add=True
    )

    @property
    def full_name(self) -> str:
        """The full name of the user."""
        return f"{self.first_name} {self.last_name}"