from authentication.models import User

def get_by_id(user_id: str) -> User|None:
    """Get a user by its user id"""
    return User.objects.filter(id=user_id).first()

def get_by_username(username: str) -> User:
    """Get a user by its username"""
    return User.objects.filter(username=username).first()

def create(
    user_id: str, username: str, email: str,
    first_name: str, last_name: str,
    faculty: str = None,
    last_enrolled: str = None,
    student_id: str = None
) -> User:
    """Create a new user
    Note: this does not assign specific user classes.
    This should be handled by consumers of this package.
    """
    return User.objects.create(
        id = user_id,
        student_id = student_id,
        username = username,
        email = email,
        first_name = first_name,
        last_name = last_name,
        faculty = faculty,
        last_enrolled = last_enrolled
    )

def get_or_create(
    id: str, username: str, email: str,
    first_name: str, last_name: str,
    faculty: str = None,
    last_enrolled: str = None,
    student_id: str = None
) -> User:
    """Get a user by ID, or create if it doesn't exist"""
    user = get_by_id(id)

    if user is None:
        return create(
            id, username, email,
            first_name, last_name,
            faculty, last_enrolled, student_id
        )

    return user