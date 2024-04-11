from faker import Faker
from api.seeders.providers.real_provider import real_group_provider, real_course_provider, real_faculty_provider, \
    real_file_extension_provider, real_structure_check_provider, real_project_provider, real_student_provider, \
    real_teacher_provider, real_assistant_provider, real_submission_provider
from api.seeders.providers.fake_provider import ModelProvider


def faker():
    fake = Faker()

    fake.add_provider(real_faculty_provider())
    fake.add_provider(real_student_provider())
    fake.add_provider(real_assistant_provider())
    fake.add_provider(real_teacher_provider())
    fake.add_provider(real_course_provider())
    fake.add_provider(real_project_provider())
    fake.add_provider(real_group_provider())
    fake.add_provider(real_submission_provider())
    fake.add_provider(real_file_extension_provider())
    fake.add_provider(real_structure_check_provider())

    fake.add_provider(ModelProvider)

    return fake
