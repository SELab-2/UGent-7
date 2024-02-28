import datetime

from django.db import models
from django.db.models import CharField, EmailField, IntegerField, DateTimeField
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    """This model represents a single authenticatable user.
    It extends the built-in Django user model with CAS-specific attributes.
    """

    """Model fields"""
    password = None # We don't use passwords for our user model.

    id = CharField(
        max_length=12,
        primary_key=True
    )

    first_name = CharField(
        max_length=50,
        null=False
    )

    last_name = CharField(
        max_length=50,
        null=False
    )

    email = EmailField(
        null=False,
        unique=True
    )

    faculty = CharField(
        max_length=50,
        null = True
    )

    last_enrolled = IntegerField(
        default = datetime.MINYEAR,
        null = True
    )

    create_time = DateTimeField(
        auto_created=True
    )

    """Model settings"""
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

class Faculty(models.Model):
    """This model represents a faculty."""

    """Model fields"""
    name = CharField(
        max_length=50,
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        # This is how we can access groups from a project
        related_name='faculties',
        null=True
    )
