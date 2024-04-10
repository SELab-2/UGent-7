from random import choices, randint
from django.core.management.base import BaseCommand
from authentication.models import User
from api.seeders.faker import faker
from api.seeders.seeder import seed_students, seed_assistants, seed_teachers, seed_courses, seed_projects, seed_groups, \
    seed_submissions
from api.models.course import Course
from api.models.group import Group
from api.models.project import Project
from api.models.teacher import Teacher
from api.models.student import Student
from api.models.assistant import Assistant
from api.models.submission import Submission


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

    amount_of_students = 50_000
    amount_of_assistants = 5_000
    amount_of_teachers = 1_500
    amount_of_courses = 1_500
    amount_of_projects = 3_000
    amount_of_groups = 3_000
    amount_of_submissions = 3_000

    def handle(self, *args, **options):
        # Reset DB
        User.objects.all().delete()
        Student.objects.all().delete()
        Assistant.objects.all().delete()
        Teacher.objects.all().delete()
        Course.objects.all().delete()
        Project.objects.all().delete()
        Submission.objects.all().delete()

        # Seed students
        fake = faker()
        seed_students(fake, self.amount_of_students, 0)

        # Seed assistants
        seed_assistants(fake, self.amount_of_assistants, self.amount_of_students)

        # Seed teachers
        seed_teachers(fake, self.amount_of_teachers, self.amount_of_students + self.amount_of_assistants)

        # Seed courses
        seed_courses(faker(), self.amount_of_courses)

        # Seed projects
        seed_projects(faker(), self.amount_of_projects)

        # Seed groups
        seed_groups(faker(), self.amount_of_groups)

        # Seed submissions
        seed_submissions(faker(), self.amount_of_submissions)
