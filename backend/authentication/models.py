import datetime

from django.db import models
from django.db.models import CharField, EmailField, IntegerField, DateTimeField, BooleanField
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


class User(AbstractBaseUser):
    """This model represents a single authenticatable user.
    It extends the built-in Django user model with CAS-specific attributes.
    """

    """Model fields"""
    password = None  # We don't use passwords for our user model.

    id = CharField(max_length=12, primary_key=True)

    username = CharField(max_length=12, unique=True)

    is_staff = BooleanField(default=False, null=False)

    email = EmailField(null=False, unique=True)

    first_name = CharField(max_length=50, null=False)

    last_name = CharField(max_length=50, null=False)

    faculties = models.ManyToManyField("Faculty", related_name="users", blank=True)

    last_enrolled = IntegerField(default=datetime.MINYEAR, null=True)

    create_time = DateTimeField(auto_now_add=True)

    """Model settings"""
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"


class Faculty(models.Model):
    """This model represents a faculty."""

    """Model fields"""
    name = CharField(max_length=50, primary_key=True)
