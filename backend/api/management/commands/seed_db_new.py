from random import choices, randint
from django.core.management.base import BaseCommand
from api.seeders.faker import faker
from authentication.models import User
from api.models.course import Course
from api.models.group import Group
from api.models.project import Project
from api.models.teacher import Teacher
from api.models.student import Student
from api.models.assistant import Assistant


def _seed_users(num: int = 500):
    fake = faker()
    User.objects.all().delete()

    users: list[User] = User.objects.bulk_create(
        [fake.fake_user(fake, id) for id in range(num)]
    )

    roles = choices(['student'] * 70 + ['assistant'] * 20 + ['teacher'] * 10, k=num)

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


class Command(BaseCommand):
    help = 'seed the db with data'

    amount_of_users = 10_000
    amount_of_courses = 1_000
    amount_of_projects = 1_000
    amount_of_groups = 5_000

    def handle(self, *args, **options):
        # Users (Students, Teachers, Assistants)
        self.stdout.write('Seeding users...')
        _seed_users(self.amount_of_users)
        self.stdout.write(self.style.SUCCESS('Seeded users'))

        # Courses
        self.stdout.write('Seeding courses...')
        _seed_courses(self.amount_of_courses)
        self.stdout.write(self.style.SUCCESS('Seeded courses'))

        # Projects
        self.stdout.write('Seeding projects...')
        _seed_projects(self.amount_of_projects)
        self.stdout.write(self.style.SUCCESS('Seeded projects'))

        # Groups
        self.stdout.write('Seeding groups...')
        _seed_groups(self.amount_of_groups)
        self.stdout.write(self.style.SUCCESS('Seeded groups'))
