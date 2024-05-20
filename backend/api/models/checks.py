from api.logic.get_file_path import get_extra_check_file_path
from api.models.docker import DockerImage
from api.models.project import Project
from django.db import models


class FileExtension(models.Model):
    """Model that represents a file extension."""

    id = models.AutoField(auto_created=True, primary_key=True)

    extension = models.CharField(
        max_length=10,
        unique=True
    )


class StructureCheck(models.Model):
    """Model that represents a structure check for a project.
       This means that the structure of a submission is checked.
       These checks are obligated to pass."""

    id = models.AutoField(auto_created=True, primary_key=True)

    # Path from the root of the project to the location where the structure check is run
    path = models.CharField(
        max_length=255,
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


class ExtraCheck(models.Model):
    """Model that represents an extra check for a project.
       These checks are not obligated to pass."""

    id = models.AutoField(auto_created=True, primary_key=True)

    # Name of the extra check
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    # Link to the project
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="extra_checks",
        blank=False,
        null=False
    )

    # Link to the docker image that runs the checks
    docker_image = models.ForeignKey(
        DockerImage,
        on_delete=models.CASCADE,
        related_name="extra_checks",
        blank=False,
        null=False
    )

    # File path of the script that runs the checks
    file = models.FileField(
        upload_to=get_extra_check_file_path,
        max_length=256,
        blank=False,
        null=False
    )

    # Maximum time the container runs for in seconds
    time_limit = models.PositiveSmallIntegerField(
        default=30,
        blank=False,
        null=False
    )

    # Maximum memory the container uses in MB
    memory_limit = models.PositiveSmallIntegerField(
        default=128,
        blank=False,
        null=False
    )

    # Whether the log files should made available to the student
    show_log = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )

    # Whether the artifacts should made available to the student
    show_artifact = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )
