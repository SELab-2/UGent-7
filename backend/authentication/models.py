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

    username = CharField(
        max_length=12,
        unique=True
    )

    email = EmailField(
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

    faculty = models.ManyToManyField(
        'Faculty',
        related_name='faculties',
        blank=True
    )

    last_enrolled = IntegerField(
        default = datetime.MINYEAR,
        null = True
    )

    create_time = DateTimeField(
        auto_now=True
    )

    """Model settings"""
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Faculty(models.Model):
    """This model represents a faculty."""

    """Model fields"""
    name = CharField(
        max_length=50,
        primary_key=True
    )

    user = models.ManyToManyField(
        'User',
        related_name='users',
        blank=True
    )
