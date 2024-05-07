from functools import wraps
from random import choice, randint, sample
from time import time
from typing import Literal

from api.models.submission import StructureCheckResult
from api.models.submission import ExtraCheckResult

from django.db import connection
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

generated_usernames = set()


def fillFaculties():
    with connection.cursor() as cursor:
        faculties = [
            ["Bio-ingenieurswetenschappen", "faculties.bioscience_engineering"],
            ["Diergeneeskunde", "faculties.veterinary_medicine"],
            ["Economie_Bedrijfskunde", "faculties.economics_business_administration"],
            ["Farmaceutische_Wetenschappen", "faculties.pharmaceutical_sciences"],
            ["Geneeskunde_Gezondheidswetenschappen", "faculties.medicine_health_sciences"],
            ["Ingenieurswetenschappen_Architectuur", "faculties.engineering_architecture"],
            ["Letteren_Wijsbegeerte", "faculties.arts_philosophy"],
            ["Politieke_Sociale_Wetenschappen", "faculties.political_social_sciences"],
            ["Psychologie_PedagogischeWetenschappen", "faculties.psychology_educational_sciences"],
            ["Recht_Criminologie", "faculties.law_criminology"],
            ["Wetenschappen", "faculties.sciences"]
        ]

        cursor.executemany(
            "INSERT INTO authentication_faculty(id, name) VALUES (?, ?)", faculties
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


def timer(func):
    """Helper function to estimate view execution time"""

    @wraps(func)
    def handle(*args, **kwargs):
        start = time()

        # print(f"{func.__name__} running")
        result = func(*args, **kwargs)

        print('Seeder {} took {}'.format(
            func.__name__, format_time((time() - start))
        ), flush=True)

        return result

    return handle


@timer
def seed_users(faker, count: int, offset: int = 0, staff_prob: float = 0.001) -> list[list]:
    """Seed users into the database"""
    global generated_usernames
    with connection.cursor() as cursor:
        # Create a set to store generated usernames

        users = []
        for id in range(offset, count + offset):
            # Generate username
            first_name = faker.first_name()
            last_name = faker.last_name()
            username_base = first_name + last_name
            username = username_base[:12]  # Truncate if longer than 12 characters

            # Check if the username is unique
            suffix = 1
            while username in generated_usernames:
                username = username_base[:12 - len(str(suffix))] + str(suffix)  # Append a unique suffix
                suffix += 1

            # Add the username to the set
            generated_usernames.add(username)

            # Append user data to the list
            users.append([
                id,
                username,
                username + "@ugent.be",
                first_name,
                last_name,
                timezone.now().year,
                timezone.now(),
                timezone.now(),
                faker.boolean(chance_of_getting_true=staff_prob),
            ])

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
                 year_dev_min: int = -3,
                 year_dev_max: int = 1,
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
                timezone.now().year + faker.random_int(min=year_dev_min, max=year_dev_max),
                choice(faculties),
                faker.sentence(),
                faker.pybool()
            ] for _ in range(count)
        ]

        # Insert courses
        cursor.executemany(
            "INSERT INTO api_course(name, description, academic_startyear, faculty_id, excerpt, private_course) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            courses
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
        locked_groups_prob=0,
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
        projects = []
        for _ in range(count):
            start_date = timezone.now() + timezone.timedelta(
                days=faker.random_int(min=min_start_date_dev, max=max_start_date_dev)
            )
            projects.append([
                faker.catch_phrase(),
                faker.paragraph(),
                start_date,
                start_date + timezone.timedelta(
                    days=faker.random_int(min=min_deadline_dev, max=max_deadline_dev)
                ),
                faker.random_int(min=min_max_score, max=max_max_score),
                faker.random_int(min=min_group_size, max=max_group_size),
                faker.boolean(chance_of_getting_true=score_visible_prob),
                faker.boolean(chance_of_getting_true=locked_groups_prob),
                faker.boolean(chance_of_getting_true=visible_prob),
                faker.boolean(chance_of_getting_true=archived_prob),
                choice(courses)
            ])

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
def seed_file_extensions(faker, count: int = 50):
    """Seed file extensions into the database"""
    with connection.cursor() as cursor:
        extensions: list[list[str]] = []
        while len(extensions) < count:
            extension: str = faker.file_extension()
            if [extension] not in extensions:
                extensions.append([extension])

        cursor.executemany(
            "INSERT INTO api_fileextension(extension) VALUES (?)",
            extensions
        )


@timer
def seed_docker_images(faker, count: int = 50):
    with connection.cursor() as cursor:
        users = list(
            cursor.execute(sql="SELECT id FROM authentication_user").fetchall()
        )

        states = ["QUEUED", "BUILDING", "SUCCESS", "FAILED"]

        docker_images = [
            [
                faker.file_name(category="image"),
                faker.file_path(extension="", depth=faker.random_int(min=0, max=5)),
                choice(users)[0],
                True,
                choice(states)[0]
            ]
            for _ in range(count)
        ]

        cursor.executemany(
            "INSERT INTO api_dockerimage(name, file, owner_id, public, state) VALUES (?, ?, ?, ?, ?)",
            docker_images
        )


@timer
def seed_structure_checks(faker, count: int = 1_500):
    with connection.cursor() as cursor:
        projects = list(
            cursor.execute(sql="SELECT id FROM api_project").fetchall()
        )
        extensions = list(
            cursor.execute(sql="SELECT id FROM api_fileextension").fetchall()
        )

        structure_checks = [
            [
                i,
                faker.file_path(extension="", depth=faker.random_int(min=0, max=5)),
                choice(projects)[0]
            ]
            for i in range(count)
        ]

        obligated_extensions = []
        while len(obligated_extensions) < count * 2:
            project = faker.pyint(min_value=0, max_value=count - 1)
            extension = choice(extensions)[0]
            if [project, extension] not in obligated_extensions:
                obligated_extensions.append([project, extension])

        blocked_extensions = []
        while len(blocked_extensions) < count * 2:
            project = faker.pyint(min_value=0, max_value=count - 1)
            extension = choice(extensions)[0]
            if ([project, extension] not in blocked_extensions) and ([project, extension] not in obligated_extensions):
                blocked_extensions.append([project, extension])

        cursor.executemany(
            "INSERT INTO api_structurecheck(id, path, project_id) VALUES (?, ?, ?)",
            structure_checks
        )
        cursor.executemany(
            "INSERT INTO api_structurecheck_obligated_extensions(structurecheck_id, fileextension_id) VALUES (?, ?)",
            obligated_extensions

        )
        cursor.executemany(
            "INSERT INTO api_structurecheck_blocked_extensions(structurecheck_id, fileextension_id) VALUES (?, ?)",
            blocked_extensions

        )


@timer
def seed_extra_checks(faker, count: int = 750):
    with connection.cursor() as cursor:
        projects = list(
            cursor.execute(sql="SELECT id FROM api_project").fetchall()
        )
        docker_images = list(
            cursor.execute(sql="SELECT id FROM api_dockerimage").fetchall()
        )

        extra_checks = [
            [
                choice(projects)[0],
                faker.word(),
                faker.boolean(chance_of_getting_true=50),
                choice(docker_images)[0],
                faker.file_path(extension="", depth=faker.random_int(min=0, max=5)),
                faker.pyint(min_value=10, max_value=1000),
                faker.pyint(min_value=50, max_value=1024),
            ]
            for _ in range(count)
        ]

        cursor.executemany(
            "INSERT INTO api_extracheck(project_id, name, show_log, docker_image_id, file, time_limit, memory_limit) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            extra_checks
        )


@timer
def seed_submissions(faker, count: int = 4_000):
    """Seed submissions into the database"""
    with connection.cursor() as cursor:
        # Fetch existing groups.
        groups = list(
            map(lambda group: group[0], cursor.execute("SELECT id FROM api_group").fetchall())
        )

        # Create submissions
        submissions = [
            [
                faker.date_this_month(),
                choice(groups),
                faker.boolean(chance_of_getting_true=80),
                faker.file_path(extension=faker.file_extension(), depth=faker.random_int(min=0, max=5))
            ]
            for _ in range(count)
        ]

        # Insert submissions
        cursor.executemany(
            "INSERT INTO api_submission(submission_time, group_id, is_valid, zip) VALUES (?, ?, ?, ?)",
            submissions
        )


@timer
def seed_submission_results(faker):
    with connection.cursor() as cursor:
        groups = list(
            cursor.execute(sql="SELECT id, project_id FROM api_group").fetchall()
        )
        submissions = list(
            cursor.execute(sql="SELECT id, group_id FROM api_submission").fetchall()
        )
        structure_checks = list(
            cursor.execute(sql="SELECT id, project_id FROM api_structurecheck").fetchall()
        )
        extra_checks = list(
            cursor.execute(sql="SELECT id, project_id FROM api_extracheck").fetchall()
        )

        check_result = ("QUEUED", "RUNNING", "SUCCESS", "FAILED")
        error_structure = ("BLOCKED_EXTENSION", "OBLIGATED_EXTENSION_NOT_FOUND",
                           "FILE_DIR_NOT_FOUND")
        error_extra = ("DOCKER_IMAGE_ERROR", "TIME_LIMIT", "MEMORY_LIMIT",
                       "CHECK_ERROR", "RUNTIME_ERROR", "UNKNOWN", "FAILED_STRUCTURE_CHECK")

        results = []
        structure_results = []
        extra_results = []
        # Get the content type for the StructureCheckResult model
        structure_content_type = ContentType.objects.get_for_model(StructureCheckResult)

        # Get the ID of the content type
        structure_content_type_id = structure_content_type.id

        # Get the content type for the ExtraCheckResult model
        extra_content_type = ContentType.objects.get_for_model(ExtraCheckResult)

        # Get the ID of the content type
        extra_content_type_id = extra_content_type.id

        for submission in submissions:
            project = next(filter(lambda group: group[0] == submission[1], groups))[1]
            structure_checks_project = list(filter(lambda check: check[1] == project, structure_checks))
            extra_checks_project = list(filter(lambda check: check[1] == project, extra_checks))

            for check in structure_checks_project:
                result = choice(check_result)
                id = faker.unique.random_int(min=111111, max=999999)
                results.append([
                    id,
                    result,
                    choice(error_structure) if result == "FAILED" else None,
                    structure_content_type_id,
                    submission[0],
                ])

                structure_results.append([
                    id,
                    check[0],
                ])

            for check in extra_checks_project:
                result = choice(check_result)
                id = faker.unique.random_int(min=111111, max=999999)
                results.append([
                    id,
                    result,
                    choice(error_extra) if result == "FAILED" else None,
                    extra_content_type_id,
                    submission[0],
                ])

                extra_results.append([
                    id,
                    faker.file_path(extension=faker.file_extension(category="text"), depth=faker.random_int(min=0, max=5)),
                    check[0],
                ])

        cursor.executemany(
            "INSERT INTO api_checkresult(id, result, error_message, polymorphic_ctype_id, submission_id) VALUES (?, ?, ?, ?, ?)",
            results
        )
        cursor.executemany(
            "INSERT INTO api_structurecheckresult(checkresult_ptr_id, structure_check_id) VALUES (?, ?)",
            structure_results
        )
        cursor.executemany(
            "INSERT INTO api_extracheckresult(checkresult_ptr_id, log_file, extra_check_id) VALUES (?, ?, ?)",
            extra_results
        )
