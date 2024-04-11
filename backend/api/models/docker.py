from api.logic.get_file_path import get_docker_image_file_path
from authentication.models import User
from django.db import models


# TODO: registry
# TODO: Build als we binnenkrijgen
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
        upload_to=get_docker_image_file_path,
        max_length=256,
        blank=False,
        null=False
    )

    # User who added the image
    # TODO: Periodically remove images with user = null and public = false
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="docker_images",
        blank=False,
        null=True,
    )

    # Whether the image can be used by everyone
    public = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )
