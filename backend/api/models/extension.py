from django.db import models


class FileExtension(models.Model):
    """Model that represents a file extension."""

    # ID should be generated automatically

    extension = models.CharField(
        max_length=10,
        unique=True
    )
