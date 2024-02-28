from __future__ import annotations
from django.db.models import CharField, EmailField, DateTimeField
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

    username = CharField(
        max_length=10,
        null=False,
        unique=True
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
        null = True,
        blank = True
    )

    last_enrolled = CharField(
        max_length=11,
        null = True,
        blank = True
    )

    create_time = DateTimeField(
        auto_now_add=True
    )

    """Model settings"""
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []