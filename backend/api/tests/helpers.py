from django.utils import timezone
from api.models.course import Course
from api.models.student import Student
from api.models.assistant import Assistant
from api.models.teacher import Teacher
from api.models.extension import FileExtension
from api.models.checks import StructureCheck, ExtraCheck
from api.models.project import Project
from api.models.group import Group
from api.models.submission import Submission
from authentication.models import Faculty, User


def create_faculty(name: str | int) -> Faculty:
    """Create a Faculty with the given arguments."""
    return Faculty.objects.create(id=name, name=name)


def create_user(id: str | int, first_name: str, last_name: str, email: str, faculty: list[Faculty] = None) -> User:
    username = f"{first_name.lower()}{last_name.lower()}"

    user = User.objects.create(
        id=id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    if faculty is not None:
        for faculty in faculty:
            user.faculties.add(faculty)

    return user


def create_admin(id: str | int, first_name: str, last_name: str, email: str, faculty: list[Faculty] = None):
    """Create an Admin with the given arguments."""
    admin = create_user(id, first_name, last_name, email, faculty)
    admin.make_admin()
    return admin


def create_student(
        id: str | int,
        first_name: str,
        last_name: str,
        email: str,
        student_id: str = "",
        is_active: bool = True,
        faculty: list[Faculty] = None,
        courses: list[Course] = None
) -> Student:
    """Create a student with the given arguments."""
    username = f"{first_name.lower()}{last_name.lower()}"

    student = Student.objects.create(
        id=id,
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        is_active=is_active,
        create_time=timezone.now(),
    )

    if faculty is not None:
        for fac in faculty:
            student.faculties.add(fac)

    if courses is not None:
        for course in courses:
            student.courses.add(course)

    return student


def create_assistant(id, first_name, last_name, email, is_active: bool = True, faculty=None, courses=None):
    """Create an assistant with the given arguments."""
    username = f"{first_name.lower()}{last_name.lower()}"

    assistant = Assistant.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        is_active=is_active,
        create_time=timezone.now(),
    )

    if faculty is not None:
        for fac in faculty:
            assistant.faculties.add(fac)

    if courses is not None:
        for course in courses:
            assistant.courses.add(course)

    return assistant


def create_teacher(id, first_name, last_name, email, is_active: bool = True, faculty=None, courses=None):
    """Create an assistant with the given arguments."""
    username = f"{first_name.lower()}{last_name.lower()}"

    assistant = Teacher.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        is_active=is_active,
        create_time=timezone.now(),
    )

    if faculty is not None:
        for fac in faculty:
            assistant.faculties.add(fac)

    if courses is not None:
        for course in courses:
            assistant.courses.add(course)

    return assistant


def create_file_extension(extension):
    """Create a FileExtension with the given arguments."""
    return FileExtension.objects.create(extension=extension)


def create_structure_check(name, project, obligated_extensions, blocked_extensions):
    """Create a StructureCheck with the given arguments."""
    check = StructureCheck.objects.create(name=name, project=project)

    for ext in obligated_extensions:
        check.obligated_extensions.add(ext)

    for ext in blocked_extensions:
        check.blocked_extensions.add(ext)

    return check


def create_project(name, description, days, course, max_score=5, group_size=5, visible=True, archived=False):
    """Create a Project with the given arguments."""
    deadline = timezone.now() + timezone.timedelta(days=days)

    return Project.objects.create(
        name=name,
        description=description,
        visible=visible,
        archived=archived,
        deadline=deadline,
        course=course,
        max_score=max_score,
        group_size=group_size,
    )


def create_course(name: str | int, academic_startyear: int, description: str = None, parent_course: Course = None) -> Course:
    """Create a Course with the given arguments."""
    return Course.objects.create(
        name=name,
        academic_startyear=academic_startyear,
        description=description,
        parent_course=parent_course,
    )


def create_group(project: Project, score: int = 0) -> Group:
    """Create a Group with the given arguments."""
    return Group.objects.create(project=project, score=score)


def create_submission(submission_number: int, group: Group, structure_checks_passed: bool) -> Submission:
    """Create a Submission with the given arguments."""

    return Submission.objects.create(
        submission_number=submission_number,
        group=group,
    )
