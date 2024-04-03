from api.models.extension import FileExtension
from api.models.project import Project
from django.db import models
from ypovoli.settings import FILE_PATHS


class StructureCheck(models.Model):
    """Model that represents a structure check for a project.
       This means that the structure of a submission is checked.
       These checks are obligated to pass."""

    # ID should be generated automatically

    # Name of the structure check
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    # Link to the project
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="structure_checks"
    )

    # Obligated extensions
    obligated_extensions = models.ManyToManyField(
        FileExtension,
        related_name="obligated_extensions",
        blank=True
    )

    # Blocked extensions
    blocked_extensions = models.ManyToManyField(
        FileExtension,
        related_name="blocked_extensions",
        blank=True
    )

    # ID check should be generated automatically


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
    file_path = models.FileField(
        upload_to=FILE_PATHS["docker_images"],
        max_length=256,
        blank=False,
        null=False
    )

    # Whether the image is custom uploaded by a prof.
    custom = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )


class ExtraCheck(models.Model):
    """Model that represents an extra check for a project.
       These checks are not obligated to pass."""

    # ID should be generated automatically

    # Link to the project
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="extra_checks"
    )

    docker_image = models.ForeignKey(
        DockerImage,
        on_delete=models.CASCADE,
        related_name="extra_checks"
    )

    # File path of the script that runs the checks
    file_path = models.CharField(
        max_length=256,
        blank=False,
        null=False
    )

    # Maximum time the script can run for
    # TODO: Set a max of 1000 seconds
    timeout = models.SmallIntegerField(
        default=300,
        blank=False,
        null=False
    )

    # Whether the log files should be kept and made available to the user
    show_log = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )
