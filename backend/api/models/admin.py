from authentication.models.user import User


class Admin(User):
    """This model represents the admin.
    It extends the User model from the authentication app with
    admin-specific attributes.
    """

    # At the moment, there are no additional attributes for the Admin model.
