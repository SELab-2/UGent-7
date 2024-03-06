from django.db import models


class BlockedExtension(models.Model):
    """Model that represents a file extension that is blocked."""

    # ID should be generated automatically

    extension = models.CharField(
        max_length=10,
        unique=True
    )


class ObligatedExtension(models.Model):
    """Model that represents a file extension that is obligated."""

    # ID should be generated automatically

    extension = models.CharField(
        max_length=10,
        unique=True
    )
