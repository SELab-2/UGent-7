from api.models.checks import ExtraCheck
from api.models.student import Student
from api.models.submission import Submission
from api.tasks.extra_checks import task_extra_check_start
from authentication.models import User
from authentication.signals import user_created
from django.db.models.signals import post_delete, post_save
from django.dispatch import Signal, receiver

# Signals

run_extra_checks = Signal(providing_args=["submission"])


# Receivers
@receiver(user_created)
def _user_creation(user: User, attributes: dict, **_):
    print(user)
    """Upon user creation, auto-populate additional properties"""
    student_id: str = attributes.get("ugentStudentID")

    if student_id is not None:
        Student.create(user, student_id=student_id)


@receiver(run_extra_checks)
def _run_extra_checks(submission: Submission, **kwargs):
    task_extra_check_start.apply_async((submission,))
    return True


@receiver(post_save, sender=ExtraCheck)
@receiver(post_delete, sender=ExtraCheck)  # TODO: Does this work post_delete
def hook_extra_check(sender, instance: ExtraCheck, **kwargs):
    for group in instance.project.groups.all():
        submissions = group.submissions.order_by("submission_time")  # TODO: Ordered in the right way?
        if submissions:
            run_extra_checks.send(sender=[ExtraCheck], submissions=submissions[0])

            for submission in submissions[1:]:
                submission.is_valid = False
                submission.save()


@receiver(post_save, sender=Submission)
def hook_submission(sender, instance: Submission, **kwargs):
    run_extra_checks.send(sender=[Submission], submission=instance)
