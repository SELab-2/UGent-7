from faker.providers import DynamicProvider
from authentication.models import Faculty
from api.models.student import Student
from api.models.assistant import Assistant
from api.models.teacher import Teacher
from api.models.course import Course
from api.models.group import Group
from api.models.project import Project
from api.models.submission import Submission
from api.models.checks import FileExtension, StructureCheck


def real_faculty_provider():
    return DynamicProvider(
        provider_name="real_faculty",
        elements=Faculty.objects.all(),
    )


def real_student_provider():
    return DynamicProvider(
        provider_name="real_student",
        elements=Student.objects.all(),
    )


def real_assistant_provider():
    return DynamicProvider(
        provider_name="real_assistant",
        elements=Assistant.objects.all(),
    )


def real_teacher_provider():
    DynamicProvider(
        provider_name="real_teacher",
        elements=Teacher.objects.all(),
    )


def real_course_provider():
    DynamicProvider(
        provider_name="real_course",
        elements=Course.objects.all(),
    )


def real_project_provider():
    DynamicProvider(
        provider_name="real_project",
        elements=Project.objects.all(),
    )


def real_group_provider():
    DynamicProvider(
        provider_name="real_group",
        elements=Group.objects.all(),
    )


def real_submission_provider():
    DynamicProvider(
        provider_name="real_submission",
        elements=Submission.objects.all(),
    )


def real_file_extension_provider():
    DynamicProvider(
        provider_name="real_file_extension",
        elements=FileExtension.objects.all(),
    )


def real_structure_check_provider():
    DynamicProvider(
        provider_name="real_structure_check",
        elements=StructureCheck.objects.all(),
    )
