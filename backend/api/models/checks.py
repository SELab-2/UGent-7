from django.db import models
from api.models.project import Project
from api.models.extension import FileExtension


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

    # Run script
    # TODO set upload_to
    run_script = models.FileField(
        blank=False,
        null=False
    )
