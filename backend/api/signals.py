from api.models.checks import ExtraCheck
from api.models.student import Student
from api.models.submission import Submission
from authentication.models import User
from authentication.signals import user_created
from django.db.models.signals import post_save, pre_delete
from django.dispatch import Signal, receiver

# Signals
run_extra_checks = Signal()

# Receivers


@receiver(user_created)
def user_creation(user: User, attributes: dict, **_):
    """Upon user creation, auto-populate additional properties"""
    student_id: str = attributes.get("ugentStudentID")

    if student_id is not None:
        Student(user_ptr=user, student_id=student_id).save_base(raw=True)


@receiver(run_extra_checks)
def _run_extra_checks(submission, **kwargs):
    # TODO: Actually run the checks
    print("Running extra checks", flush=True)
    return True


@receiver(post_save, sender=ExtraCheck)
@receiver(pre_delete, sender=ExtraCheck)
def run_checks_extra_check(sender, instance: ExtraCheck, **kwargs):
    for group in instance.project.groups.all():
        submissions = group.submissions.order_by("submission_time")
        if submissions:
            run_extra_checks.send(sender=ExtraCheck, submission=submissions[0])

            for submission in submissions[1:]:
                submission.is_valid = False
                submission.save()


@receiver(post_save, sender=Submission)
def run_checks_submission(sender, instance: Submission, **kwargs):
    run_extra_checks.send(sender=Submission, submission=instance)
