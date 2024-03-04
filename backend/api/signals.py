from authentication.models import User
from api.models.student import Student


def user_creation(user: User, attributes: dict, **kwargs):
    """Upon user creation, auto-populate additional properties"""
    student_id = attributes.get("ugentStudentID")

    if student_id:
        Student(user_ptr=user, student_id=student_id).save_base(raw=True)
