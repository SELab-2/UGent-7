from random import choice, randint, sample
from functools import wraps
from time import time
from django.db import connection
from django.utils import timezone


def format_time(execution_time):
    if execution_time < 1:
        return f"{execution_time * 1000:.2f} milliseconds"
    elif execution_time < 60:
        return f"{execution_time:.2f} seconds"
    elif execution_time < 3600:
        return f"{execution_time / 60:.2f} minutes"
    else:
        return f"{execution_time / 3600:.2f} hours"


def timer(func):
    """Helper function to estimate view execution time"""

    @wraps(func)
    def handle(*args, **kwargs):
        start = time()

        result = func(*args, **kwargs)

        print('Seeder {} took {}'.format(
            func.__name__, format_time((time() - start))
        ))

        return result

    return handle


@timer
def seed_users(faker, count: int, offset: int = 0, staff_prob: float = 0.001) -> list[list]:
    """Seed users into the database"""
    with connection.cursor() as cursor:
        users = [
            [
                id,
                faker.unique.user_name(),
                faker.unique.email(),
                faker.first_name(),
                faker.last_name(),
                timezone.now().year,
                timezone.now(),
                timezone.now(),
                faker.boolean(chance_of_getting_true=staff_prob),
            ] for id in range(offset, count + offset)
        ]

        cursor.executemany(
            "INSERT INTO authentication_user"
            "(id, username, email, first_name, last_name, last_enrolled, last_login, create_time, is_staff)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            users
        )

        return users


@timer
def seed_students(faker, count: int = 1_000, offset: int = 0) -> None:
    """Seed students into the database"""
    users = seed_users(faker, count, offset)

    with connection.cursor() as cursor:
        students = [
            [user[0], user[0], True] for user in users
        ]

        cursor.executemany(
            "INSERT INTO api_student(user_ptr_id, student_id, is_active) VALUES (?, ?, ?)", students
        )


@timer
def seed_assistants(faker, count: int = 500, offset: int = 0) -> None:
    """Seed assistants into the database"""
    users = seed_users(faker, count, offset)

    with connection.cursor() as cursor:
        assistants = [
            [user[0], True] for user in users
        ]

        cursor.executemany(
            "INSERT INTO api_assistant(user_ptr_id, is_active) VALUES (?, ?)", assistants
        )


@timer
def seed_teachers(faker, count: int = 250, offset: int = 0) -> None:
    """Seed assistants into the database"""
    users = seed_users(faker, count, offset)

    with connection.cursor() as cursor:
        teachers = [
            [user[0], True] for user in users
        ]

        cursor.executemany(
            "INSERT INTO api_teacher(user_ptr_id, is_active) VALUES (?, ?)", teachers
        )


@timer
def seed_courses(faker,
                 count: int = 1_000,
                 year_dev: int = 1,
                 max_students: int = 100,
                 max_teachers: int = 3,
                 max_assistants: int = 5,
                 min_students: int = 1,
                 min_teachers: int = 1,
                 min_assistants: int = 1
                 ) -> None:
    """Seed courses into the database"""
    with connection.cursor() as cursor:
        # Fetch existing faculties.
        faculties = list(
            map(lambda x: x[0],
                cursor.execute("SELECT id FROM authentication_faculty").fetchall()
                )
        )

        # Create courses.
        courses = [
            [
                faker.catch_phrase(),
                faker.paragraph(),
                timezone.now().year + faker.random_int(min=-year_dev, max=year_dev),
                choice(faculties)
            ] for _ in range(count)
        ]

        # Insert courses
        cursor.executemany(
            "INSERT INTO api_course(name, description, academic_startyear, faculty_id) VALUES (?, ?, ?, ?)", courses
        )

        # Link students, teachers, assistants to courses
        student_course = []
        teacher_course = []
        assistant_course = []

        courses = list(
            map(lambda x: x[0],
                cursor.execute("SELECT id FROM api_course").fetchall()
                )
        )

        students = list(
            map(lambda x: x[0],
                cursor.execute("SELECT user_ptr_id FROM api_student").fetchall()
                )
        )

        teachers = list(
            map(lambda x: x[0],
                cursor.execute("SELECT user_ptr_id FROM api_teacher").fetchall()
                )
        )

        assistants = list(
            map(lambda x: x[0],
                cursor.execute("SELECT user_ptr_id FROM api_assistant").fetchall()
                )
        )

        for course in courses:
            num_students = min(len(students), randint(min_students, max_students))
            num_assistants = min(len(assistants), randint(min_assistants, max_assistants))
            num_teachers = min(len(teachers), randint(min_teachers, max_teachers))

            chosen_students = sample(students, k=num_students)
            students = [student for student in students if student not in chosen_students]
            student_course.extend(
                zip([course] * num_students, chosen_students)
            )

            chosen_assistants = sample(assistants, k=num_assistants)
            assistants = [assistant for assistant in assistants if assistant not in chosen_assistants]
            assistant_course.extend(
                zip([course] * num_assistants, chosen_assistants)
            )

            chosen_teachers = sample(teachers, k=num_teachers)
            teachers = [teacher for teacher in teachers if teacher not in chosen_teachers]
            teacher_course.extend(
                zip([course] * num_teachers, chosen_teachers)
            )

        cursor.executemany(
            "INSERT INTO api_student_courses(course_id, student_id) VALUES (?, ?)", student_course
        )

        cursor.executemany(
            "INSERT INTO api_teacher_courses(course_id, teacher_id) VALUES (?, ?)", teacher_course
        )

        cursor.executemany(
            "INSERT INTO api_assistant_courses(course_id, assistant_id) VALUES (?, ?)", assistant_course
        )


@timer
def seed_projects(
        faker,
        count: int = 1_500,
        min_start_date_dev=-100,
        max_start_date_dev=100,
        min_deadline_dev=1,
        max_deadline_dev=100,
        visible_prob=80,
        archived_prob=10,
        score_visible_prob=30,
        locked_groups_prob=30,
        min_max_score=1,
        max_max_score=100,
        min_group_size=1,
        max_group_size=15
) -> None:
    """Seed projects into the database"""
    with connection.cursor() as cursor:
        # Fetch existing courses.
        courses = list(
            map(lambda x: x[0], cursor.execute("SELECT id FROM api_course").fetchall())
        )

        # Create projects
        projects = [
            [
                faker.catch_phrase(),
                faker.paragraph(),
                timezone.now() + timezone.timedelta(
                    days=faker.random_int(min=min_start_date_dev, max=max_start_date_dev)
                ),
                timezone.now() + timezone.timedelta(
                    days=faker.random_int(min=min_deadline_dev, max=max_deadline_dev)
                ),
                faker.random_int(min=min_max_score, max=max_max_score),
                faker.random_int(min=min_group_size, max=max_group_size),
                faker.boolean(chance_of_getting_true=score_visible_prob),
                faker.boolean(chance_of_getting_true=locked_groups_prob),
                faker.boolean(chance_of_getting_true=visible_prob),
                faker.boolean(chance_of_getting_true=archived_prob),
                choice(courses)
            ] for _ in range(count)
        ]

        # Insert projects
        cursor.executemany(
            "INSERT INTO api_project(name, description, start_date, deadline, "
            "max_score, group_size, score_visible, locked_groups, visible, archived, course_id)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            projects
        )


@timer
def seed_groups(faker, count: int = 4_000, min_score: int = 0) -> None:
    """Seed groups into the database"""
    with connection.cursor() as cursor:
        # Fetch existing projects.
        projects = list(
            cursor.execute("SELECT id, max_score FROM api_project").fetchall()
        )

        # Create groups
        groups = []

        for _ in range(count):
            project = choice(projects)

            groups.append([
                faker.random_int(min=min_score, max=project[1]), project[0]
            ])

        # Insert groups
        cursor.executemany(
            "INSERT INTO api_group(score, project_id)"
            " VALUES (?, ?)",
            groups
        )

        # Add students to groups
        student_group = []

        groups = list(
            map(lambda x: x[0], cursor.execute("SELECT id FROM api_group").fetchall())
        )

        students = list(
            map(lambda x: x[0], cursor.execute("SELECT user_ptr_id FROM api_student").fetchall())
        )

        for group in groups:
            num_students = min(len(students), randint(0, 6))

            chosen_students = sample(students, k=num_students)
            students = [student for student in students if student not in chosen_students]
            student_group.extend(
                zip([group] * num_students, chosen_students)
            )

        cursor.executemany(
            "INSERT INTO api_group_students(group_id, student_id) VALUES (?, ?)", student_group
        )


@timer
def seed_submissions(faker, count: int = 4_000, struct_check_passed_prob: float = 70):
    """Seed submissions into the database"""
    with connection.cursor() as cursor:
        # Fetch existing groups.
        groups = list(
            map(lambda group: group[0], cursor.execute("SELECT id FROM api_group").fetchall())
        )

        # Create submissions
        submissions = [
            [faker.date_this_month(), faker.boolean(chance_of_getting_true=struct_check_passed_prob), choice(groups)]
            for _ in range(count)
        ]

        # Insert submissions
        cursor.executemany(
            "INSERT INTO api_submission(submission_time, structure_checks_passed, group_id) VALUES (?, ?, ?)",
            submissions
        )
