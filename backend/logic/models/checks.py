from django.db import models


class FileExtension(models.Model):
    """Model that represents a file extension."""

    extension = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return str(self.extension)


class Checks(models.Model):
    """Model that represents checks for a project."""

    # ID check should be generated automatically

    dockerfile = models.FileField(
        blank=True,
        null=True
    )

    # Link to the file extensions that are allowed
    allowed_file_extensions = models.ManyToManyField(
        FileExtension,
        related_name='checks_allowed',
        blank=True
    )

    # Link to the file extensions that are forbidden
    forbidden_file_extensions = models.ManyToManyField(
        FileExtension,
        related_name='checks_forbidden',
        blank=True
    )
