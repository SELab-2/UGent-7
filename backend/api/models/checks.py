from api.logic.get_file_path import get_extra_check_file_path
from api.models.docker import DockerImage
from api.models.extension import FileExtension
from api.models.project import Project
from api.signals import run_extra_checks
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


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


@receiver(post_save, sender=ExtraCheck)
@receiver(pre_delete, sender=ExtraCheck)
def run_checks(sender, instance: ExtraCheck, **kwargs):
    print("Hoi", flush=True)
    # TODO: Use querysets
    for group in instance.project.groups.all():
        submissions = group.submissions.order_by("submission_time")
        if submissions:
            run_extra_checks.send(sender=ExtraCheck, submission=submissions[0])

            for submission in submissions[1:]:
                submission.is_valid = False
                submission.save()
