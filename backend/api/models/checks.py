from api.logic.get_file_path import get_extra_check_file_path
from api.models.docker import DockerImage
from api.models.extension import FileExtension
from api.models.project import Project
from django.db import models


# TODO: Remove zip.* translations
# TODO: How it the zip structure checked?
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

# TODO: Add state, queued, running, done


class ExtraCheck(models.Model):
    """Model that represents an extra check for a project.
       These checks are not obligated to pass."""

    # ID should be generated automatically

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

    # Maximum time the script can run for
    timeout = models.PositiveSmallIntegerField(
        default=60,
        blank=False,
        null=False
    )

    # Whether the log files should be kept and made available to the user
    show_log = models.BooleanField(
        default=True,
        blank=False,
        null=False
    )
