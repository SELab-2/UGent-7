from authentication.models.user import User


class Teacher(User):
    """This model represents a single teacher.
    It extends the User model from the authentication app with
    teacher-specific attributes.
    """

    # At the moment, there are no additional attributes for the Teacher model.
