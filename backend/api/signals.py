from api.models.student import Student
from authentication.models import User
from django.dispatch import Signal, receiver


# TODO: Signal?
def user_creation(user: User, attributes: dict, **_):
    """Upon user creation, auto-populate additional properties"""
    student_id: str = attributes.get("ugentStudentID")

    if student_id is not None:
        Student(user_ptr=user, student_id=student_id).save_base(raw=True)


run_extra_checks = Signal()


@receiver(run_extra_checks)
def _run_extra_checks(submission, **kwargs):
    # TODO: Set all previous submissions to invalid
    # TODO: Run extra checks
    print("Running extra checks", flush=True)
    return True
