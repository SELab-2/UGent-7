from authentication.models import User
from django.db import models
from ypovoli.settings import FILE_PATHS


class DockerImage(models.Model):
    """
    Models that represents the different docker environments to run tests in
    """

    # ID should be generated automatically

    # Name of the docker image
    name = models.CharField(
        max_length=256,
        blank=False,
        null=False
    )

    # File path of the docker image
    file = models.FileField(
        upload_to=FILE_PATHS["docker_images"],
        max_length=256,
        blank=False,
        null=False
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="docker_images",
        blank=False,
        null=True,
    )

    # Whether the image can be used by everyone
    public = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )