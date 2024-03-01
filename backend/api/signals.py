from authentication.models import User


def user_creation(user: User, attributes: dict, **kwargs):
    # With Python 3.11, we need to import Student here.
    from api.models.student import Student

    """Upon user creation, auto-populate additional properties"""
    student_id = attributes.get("ugentStudentID")

    if student_id:
        Student(user_ptr=user, student_id=student_id).save_base(raw=True)
