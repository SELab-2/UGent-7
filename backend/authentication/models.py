from datetime import MINYEAR
from django.db import models
from django.apps import apps
from django.utils.functional import cached_property
from django.db.models import CharField, EmailField, IntegerField, DateTimeField, BooleanField, Model
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin


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

    last_enrolled = IntegerField(default=MINYEAR, null=True)

    create_time = DateTimeField(auto_now_add=True)

    """Model settings"""
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    def make_admin(self):
        self.is_staff = True
        self.save()

    @cached_property
    def roles(self):
        """Return all roles associated with this user"""
        return [
            # Use the class' name in lower case...
            model.__name__.lower()
            # ...for each installed app that could define a role model...
            for app_config in apps.get_app_configs()
            # ...for each model in the app's models...
            for model in app_config.get_models()
            # ...that inherit the User class.
            if model is not self.__class__
            if issubclass(model, self.__class__)
            if model.objects.filter(id=self.id).exists()
        ]

    @staticmethod
    def get_dummy_admin():
        return User(
            id="admin",
            first_name="Nikkus",
            last_name="Derdinus",
            username="nderdinus",
            email="nikkus@ypovoli.be",
            is_staff=True
        )


class Faculty(models.Model):
    """This model represents a faculty."""

    """Model fields"""
    id = CharField(max_length=50, primary_key=True)

    name = CharField(
        max_length=50,
        default="faculty",
        null=False
    )
