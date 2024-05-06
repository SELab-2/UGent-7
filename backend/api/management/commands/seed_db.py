import time
from random import choices, randint

from api.models.assistant import Assistant
from api.models.course import Course
from api.models.group import Group
from api.models.project import Project
from api.models.student import Student
from api.models.teacher import Teacher
from api.seeders.faker import faker
from api.seeders.seeder import (fillFaculties, seed_assistants, seed_courses,
                                seed_docker_images, seed_extra_checks,
                                seed_file_extensions, seed_groups,
                                seed_projects, seed_structure_checks,
                                seed_students, seed_submission_results,
                                seed_submissions, seed_teachers)
from authentication.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand


def _seed_users(num: int = 500, student_prob: int = 70, assistant_prob: int = 20, teacher_prob: int = 10):
    fake = faker()
    User.objects.all().delete()

    users: list[User] = User.objects.bulk_create(
        [fake.fake_user(fake, id) for id in range(num)]
    )

    roles = choices(['student'] * student_prob + ['assistant'] * assistant_prob + ['teacher'] * teacher_prob, k=num)

    for user, role in zip(users, roles):
        if role == 'assistant':
            Assistant.create(user)
        elif role == 'teacher':
            Teacher.create(user)
        elif role == 'student':
            Student.create(user, student_id=user.id)

        user.faculties.add(
            *[fake.real_faculty() for _ in range(randint(1, 2))]
        )


def _seed_courses(num: int = 200):
    fake = faker()
    Course.objects.all().delete()

    courses: list[Course] = Course.objects.bulk_create(
        [fake.fake_course(fake) for _ in range(num)]
    )

    for course in courses:
        course.students.add(
            *[fake.real_student() for _ in range(randint(10, 100))]
        )
        course.teachers.add(
            *[fake.real_teacher() for _ in range(randint(1, 3))]
        )
        course.assistants.add(
            *[fake.real_assistant() for _ in range(randint(2, 5))]
        )


def _seed_projects(num: int = 1_000):
    fake = faker()
    Project.objects.all().delete()

    Project.objects.bulk_create(
        [fake.fake_project(fake) for _ in range(num)]
    )


def _seed_groups(num: int = 3_000):
    fake = faker()
    Group.objects.all().delete()

    groups = Group.objects.bulk_create(
        [fake.fake_group(fake) for _ in range(num)]
    )

    for group in groups:
        group.students.add(
            *[fake.real_student() for _ in range(randint(1, group.project.group_size))]
        )


def format_time(execution_time):
    if execution_time < 1:
        return f"{execution_time * 1000:.2f} milliseconds"
    elif execution_time < 60:
        return f"{execution_time:.2f} seconds"
    elif execution_time < 3600:
        return f"{execution_time / 60:.2f} minutes"
    else:
        return f"{execution_time / 3600:.2f} hours"


class Command(BaseCommand):
    help = 'seed the db with data'

    def add_arguments(self, parser):
        parser.add_argument('size', type=str, help='The size you want to seed')

    def handle(self, *args, **options):
        size = options['size']
        if size == "small":
            amount_of_students = 10
            amount_of_assistants = 5
            amount_of_teachers = 3
            amount_of_courses = 3
            amount_of_projects = 4
            amount_of_groups = 7
            amount_of_file_extensions = 5
            amount_of_docker_images = 5
            amount_of_structure_checks = 2
            amount_of_extra_checks = 1
            amount_of_submissions = 10
        elif size == "medium":
            amount_of_students = 5_000
            amount_of_assistants = 500
            amount_of_teachers = 250
            amount_of_courses = 250
            amount_of_projects = 500
            amount_of_groups = 500
            amount_of_file_extensions = 32  # Max amount of file extensions in Faker
            amount_of_docker_images = 50
            amount_of_structure_checks = 250
            amount_of_extra_checks = 125
            amount_of_submissions = 500
        elif size == "large":
            amount_of_students = 50_000
            amount_of_assistants = 5_000
            amount_of_teachers = 1_500
            amount_of_courses = 1_500
            amount_of_projects = 3_000
            amount_of_groups = 3_000
            amount_of_file_extensions = 32  # Max amount of file extensions in Faker
            amount_of_docker_images = 50
            amount_of_structure_checks = 1_500
            amount_of_extra_checks = 750
            amount_of_submissions = 3_000
        else:
            self.stdout.write(self.style.ERROR("give a size from small, medium or large!"))
            return

        # Reset DB
        call_command('flush', '--noinput')
        fillFaculties()  # fill the faculty table again

        # Seed students
        fake = faker()
        start_time = time.time()
        seed_students(fake, amount_of_students)

        # Seed assistants
        seed_assistants(fake, amount_of_assistants, amount_of_students)

        # Seed teachers
        seed_teachers(fake, amount_of_teachers, amount_of_students + amount_of_assistants)

        # Seed courses
        seed_courses(faker(), amount_of_courses)

        # Seed projects
        seed_projects(faker(), amount_of_projects)

        # Seed groups
        seed_groups(faker(), amount_of_groups)

        # Seed file extensions
        seed_file_extensions(faker(), amount_of_file_extensions)

        # Seed docker images
        seed_docker_images(faker(), amount_of_docker_images)

        # Seed structure checks
        seed_structure_checks(faker(), amount_of_structure_checks)

        # Seed extra checks
        seed_extra_checks(faker(), amount_of_extra_checks)

        # Seed submissions
        seed_submissions(faker(), amount_of_submissions)

        # Seed submission results
        seed_submission_results(faker())

        end_time = time.time()
        execution_time = end_time - start_time
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded db in {format_time(execution_time)}!"))
