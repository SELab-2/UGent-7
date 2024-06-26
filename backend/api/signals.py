
from typing import cast

from api.models.checks import ExtraCheck, StructureCheck
from api.models.docker import DockerImage
from api.models.docker import StateEnum as DockerStateEnum
from api.models.student import Student
from api.models.submission import (ExtraCheckResult, StateEnum,
                                   StructureCheckResult, Submission)
from api.models.teacher import Teacher
from api.tasks.docker_image import (task_docker_image_build,
                                    task_docker_image_remove)
from api.tasks.extra_check import task_extra_check_start
from api.tasks.structure_check import task_structure_check_start
from authentication.models import User
from authentication.signals import user_created
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import Signal, receiver
from notifications.signals import NotificationType, notification_create

# MARK: Signals


run_docker_image_build = Signal()
run_docker_image_remove = Signal()
run_all_checks = Signal()
run_structure_checks = Signal()
run_extra_checks = Signal()


# MARK: Receivers


@receiver(user_created)
def _user_creation(user: User, attributes: dict, **_):
    """Upon user creation, auto-populate additional properties"""
    student_id: str = cast(str, attributes.get("ugentStudentID"))

    if student_id is not None:
        Student.create(user, student_id=student_id)
    else:
        # For now, we assume that everyone without a student ID is a teacher.
        Teacher.create(user)


@receiver(run_docker_image_build)
def _run_docker_image_build(docker_image: DockerImage, **_):
    docker_image.state = DockerStateEnum.QUEUED
    docker_image.save()

    task_docker_image_build.apply_async((docker_image,))


@receiver(run_docker_image_remove)
def _run_docker_image_remove(docker_image: DockerImage, **_):
    task_docker_image_remove.apply_async((docker_image,))


@receiver(run_all_checks)
def _run_all_checks(submission: Submission, **_):
    # Get all checks
    structure_check_results = get_structure_check_results(submission)
    extra_check_results = get_extra_check_results(submission)

    # Link all tasks
    signature = task_structure_check_start.s(structure_check_results)
    for extra_check_result in extra_check_results:
        signature.link(task_extra_check_start.s(extra_check_result))

    # Execute
    signature.apply_async()


@receiver(run_structure_checks)
def _run_structure_checks(submission: Submission, **_):
    structure_check_results = get_structure_check_results(submission)

    if len(structure_check_results) >= 0:
        task_structure_check_start.apply_async((tuple(structure_check_results),))


@receiver(run_extra_checks)
def _run_extra_checks(submission: Submission, **_):
    extra_check_results = get_extra_check_results(submission)

    for extra_check_result in extra_check_results:
        task_extra_check_start.apply_async((True, extra_check_result,))


# MARK: Hooks


@receiver(post_save, sender=StructureCheck)
@receiver(post_delete, sender=StructureCheck)
def hook_structure_check(sender, instance: StructureCheck, **kwargs):
    if not kwargs.get('raw', False):
        for group in instance.project.groups.all():
            submissions = group.submissions.order_by("-submission_time")
            if submissions:
                run_structure_checks.send(sender=StructureCheck, submission=submissions[0])

                for submission in submissions[1:]:
                    submission.is_valid = False
                    submission.save()


@receiver(post_save, sender=ExtraCheck)
@receiver(post_delete, sender=ExtraCheck)
def hook_extra_check(sender, instance: ExtraCheck, **kwargs):
    if not kwargs.get('raw', False):
        for group in instance.project.groups.all():
            submissions = group.submissions.order_by("-submission_time")
            if submissions:
                run_extra_checks.send(sender=ExtraCheck, submission=submissions[0])

                for submission in submissions[1:]:
                    submission.is_valid = False
                    submission.save()


@receiver(post_save, sender=Submission)
def hook_submission(sender, instance: Submission, created: bool, **kwargs):
    if created and not kwargs.get('raw', False):
        run_all_checks.send(sender=Submission, submission=instance)
        pass

        notification_create.send(
            sender=Submission,
            type=NotificationType.SUBMISSION_RECEIVED,
            queryset=list(instance.group.students.all()),
            arguments={}
        )


@receiver(post_save, sender=DockerImage)
def hook_docker_image(sender, instance: DockerImage, created: bool, **kwargs):
    if created:
        run_docker_image_build.send(sender=DockerImage, docker_image=instance)


@receiver(pre_delete, sender=DockerImage)
def hook_docker_image_delete(sender, instance: DockerImage, **kwargs):
    run_docker_image_remove.send(sender=DockerImage, docker_image=instance)


# MARK: Helpers


# Get all structure checks and create a result for each one
def get_structure_check_results(submission: Submission) -> list[StructureCheckResult]:
    structure_check_results: list[StructureCheckResult] = []
    for structure_check in submission.group.project.structure_checks.all():
        structure_check_result: StructureCheckResult
        if submission.results.filter(structurecheckresult__structure_check__id=structure_check.id).exists():
            structure_check_result = submission.results.get(structurecheckresult__structure_check__id=structure_check.id)
            structure_check_result.result = StateEnum.QUEUED
        else:
            structure_check_result = StructureCheckResult(
                submission=submission,
                result=StateEnum.QUEUED,
                error_message=None,
                structure_check=structure_check
            )
        structure_check_result.save()
        structure_check_results.append(structure_check_result)

    return structure_check_results


# Get all extra checks and create a result for each one
def get_extra_check_results(submission: Submission) -> list[ExtraCheckResult]:
    extra_check_results: list[ExtraCheckResult] = []
    for extra_check in submission.group.project.extra_checks.all():
        extra_check_result: ExtraCheckResult
        if submission.results.filter(extracheckresult__extra_check__id=extra_check.id).exists():
            extra_check_result = submission.results.get(extracheckresult__extra_check__id=extra_check.id)
            extra_check_result.result = StateEnum.QUEUED
        else:
            extra_check_result = ExtraCheckResult(
                submission=submission,
                result=StateEnum.QUEUED,
                error_message=None,
                extra_check=extra_check,
                log_file=None
            )

        extra_check_result.save()
        extra_check_results.append(extra_check_result)

    return extra_check_results
