from django.db import models
from api.models.course import Course
from api.models.mixins.role import RoleMixin
from authentication.models import User


class Teacher(RoleMixin, User):
    """This model represents a single teacher.
    It extends the User model from the authentication app with
    teacher-specific attributes.
    """

    # All the courses the teacher is teaching
    courses = models.ManyToManyField(
        Course,
        # Allows us to access the teachers from the course
        related_name="teachers",
        blank=True,
    )

    def has_course(self, course: Course) -> bool:
        """Checks if the teacher has the given course."""
        return self.courses.contains(course)


def make_teacher(user: User) -> Teacher:
    """Activates the Teacher role for the given user."""
    teacher: Teacher = Teacher.objects.filter(id=user.id).first()

    if teacher is not None:
        teacher.is_active = True
        teacher.save()
        return teacher

    return Teacher(user_ptr=user).save_base(raw=True)
