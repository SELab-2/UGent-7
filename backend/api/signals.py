from authentication.models import User
from api.models.student import Student


def user_creation(user: User, attributes: dict, **_):
    """Upon user creation, auto-populate additional properties"""
    student_id: str = attributes.get("ugentStudentID")

    if student_id is not None:
        Student(user_ptr=user, student_id=student_id).save_base(raw=True)
