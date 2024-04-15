from api.models.checks import ExtraCheck, StructureCheck
from api.models.student import Student
from api.models.submission import (ExtraCheckResult, StateEnum,
                                   StructureCheckResult, Submission)
from api.tasks.extra_check import task_extra_check_start
from api.tasks.structure_check import task_structure_check_start
from authentication.models import User
from authentication.signals import user_created
from django.db.models.signals import post_delete, post_save
from django.dispatch import Signal, receiver

# Signals

run_structure_checks = Signal()
run_extra_checks = Signal()


# Receivers
@receiver(user_created)
def _user_creation(user: User, attributes: dict, **_):
    """Upon user creation, auto-populate additional properties"""
    student_id: str = attributes.get("ugentStudentID")

    if student_id is not None:
        Student.create(user, student_id=student_id)


@receiver(run_structure_checks)
def _run_structure_checks(submission: Submission, **kwargs):
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
        task_structure_check_start.apply_async((structure_check_result,))
    return True


@receiver(run_extra_checks)
def _run_extra_checks(submission: Submission, **kwargs):
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
        task_extra_check_start.apply_async((extra_check_result,))
    return True


@receiver(post_save, sender=StructureCheck)
@receiver(post_delete, sender=StructureCheck)
def hook_structure_check(sender, instance: StructureCheck, **kwargs):
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
    for group in instance.project.groups.all():
        submissions = group.submissions.order_by("-submission_time")
        if submissions:
            run_extra_checks.send(sender=ExtraCheck, submission=submissions[0])

            for submission in submissions[1:]:
                submission.is_valid = False
                submission.save()


@receiver(post_save, sender=Submission)
def hook_submission(sender, instance: Submission, created: bool, **kwargs):
    if created:
        run_structure_checks.send(sender=Submission, submission=instance)
        run_extra_checks.send(sender=Submission, submission=instance)
