from authentication.models.user import User


class Student(User):
    """This model represents a single student.
    It extends the User model from the authentication app with
    student-specific attributes.
    """

    # At the moment, there are no additional attributes for the Student model.
