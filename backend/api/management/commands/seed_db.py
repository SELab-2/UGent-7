from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from django.db.models import Max
from faker.providers import BaseProvider, DynamicProvider
import random
import time

from authentication.models import Faculty
from api.models.student import Student
from api.models.assistant import Assistant
from api.models.teacher import Teacher
from api.models.course import Course
from api.models.group import Group
from api.models.project import Project
from api.models.submission import Submission
from api.models.checks import FileExtension, StructureCheck
fake = Faker()

# Faker.seed(4321) # set to make data same each time

faculty_provider = DynamicProvider(
    provider_name="faculty_provider",
    elements=Faculty.objects.all(),
)

student_provider = DynamicProvider(
    provider_name="student_provider",
    elements=Student.objects.all(),
)

assistant_provider = DynamicProvider(
    provider_name="assistant_provider",
    elements=Assistant.objects.all(),
)

teacher_provider = DynamicProvider(
    provider_name="teacher_provider",
    elements=Teacher.objects.all(),
)

course_provider = DynamicProvider(
    provider_name="course_provider",
    elements=Course.objects.all(),
)

project_provider = DynamicProvider(
    provider_name="project_provider",
    elements=Project.objects.all(),
)

group_provider = DynamicProvider(
    provider_name="group_provider",
    elements=Group.objects.all(),
)

Submission_provider = DynamicProvider(
    provider_name="Submission_provider",
    elements=Submission.objects.all(),
)

fileExtension_provider = DynamicProvider(
    provider_name="fileExtension_provider",
    elements=FileExtension.objects.all(),
)

structureCheck_provider = DynamicProvider(
    provider_name="structureCheck_provider",
    elements=StructureCheck.objects.all(),
)


# create new provider class
class Providers(BaseProvider):

    MAX_TRIES = 1000
    min_id = 1
    max_id = 999_999_999_99

    min_salt = 1
    max_salt = 100_000

    def provide_teacher(self, errHandler, min_faculty=1, max_faculty=2, staf_prob=0.1):
        """
        Create a teacher with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                first = fake.first_name()
                last = fake.last_name()
                id = fake.unique.random_int(min=self.min_id, max=self.max_id)
                faculty = [
                    fake.faculty_provider().id for _ in range(0, fake.random_int(min=min_faculty, max=max_faculty))
                ]  # generate 1 or 2 facultys
                username = f"{first.lower()}{last.lower()}_{fake.random_int(min=self.min_salt, max=self.max_salt)}"[:12]
                teacher = Teacher.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username + "@example.com",
                    create_time=timezone.now(),
                    last_enrolled=timezone.now().year,
                    is_staff=fake.boolean(chance_of_getting_true=staf_prob)
                )

                if faculty is not None:
                    teacher.faculties.add(*faculty)  # Add faculties in bulk

                return teacher
            except Exception:
                tries += 1
        errHandler.stdout.write(
            errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique teacher."))

    def provide_assistant(self, errHandler, min_faculty=1, max_faculty=3, staf_prob=0.01):
        """
        Create a assistant with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                first = fake.first_name()
                last = fake.last_name()
                id = fake.unique.random_int(min=self.min_id, max=self.max_id)
                faculty = [
                    fake.faculty_provider().id for _ in range(0, fake.random_int(min=min_faculty, max=max_faculty))
                ]  # generate 1 or 2 or 3 facultys
                username = f"{first.lower()}{last.lower()}_{fake.random_int(min=self.min_salt, max=self.max_salt)}"[:12]
                assistant = Assistant.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username + "@example.com",
                    create_time=timezone.now(),
                    last_enrolled=timezone.now().year,
                    is_staff=fake.boolean(chance_of_getting_true=staf_prob)
                )

                if faculty is not None:
                    assistant.faculties.add(*faculty)  # Add faculties in bulk

                return assistant
            except Exception:
                tries += 1
        errHandler.stdout.write(
            errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique assistant."))

    def provide_student(self, errHandler, min_faculty=1, max_faculty=3, staf_prob=0.01):
        """
        Create a student with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                first = fake.first_name()
                last = fake.last_name()
                id = fake.unique.random_int(min=self.min_id, max=self.max_id)
                faculty = [
                    fake.faculty_provider().id for _ in range(0, fake.random_int(min=min_faculty, max=max_faculty))
                ]  # generate 1 or 2 or 3 facultys
                username = f"{first.lower()}{last.lower()}_{fake.random_int(min=self.min_salt, max=self.max_salt)}"[:12]
                student = Student.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username + "@example.com",
                    create_time=timezone.now(),
                    last_enrolled=timezone.now().year,
                    student_id=id,
                    is_staff=fake.boolean(chance_of_getting_true=staf_prob)
                )

                if faculty is not None:
                    student.faculties.add(*faculty)  # Add faculties in bulk

                return student
            except Exception:
                tries += 1
        errHandler.stdout.write(
            errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique student."))

    def provide_course(
            self,
            errHandler,
            min_year_passed=0,
            max_year_passed=3,
            min_students=1,
            max_students=100,
            min_teachers=1,
            max_teachers=5,
            min_assistants=0,
            max_assistants=5):
        """
        Create a Course with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                parent_course = None  # TODO make this sometimes a course
                course_name = fake.catch_phrase()
                course: Course = Course.objects.create(
                    name=course_name,
                    academic_startyear=timezone.now().year - fake.random_int(min=min_year_passed, max=max_year_passed),
                    faculty=fake.faculty_provider(),
                    description=fake.paragraph(),
                    parent_course=parent_course
                )

                # add students
                student_count = fake.random_int(min=min_students, max=max_students)
                students_list = []
                while len(students_list) < student_count:
                    student = fake.student_provider()
                    if student not in students_list:
                        students_list.append(student)
                course.students.add(*students_list)  # Add students in bulk

                # add teachers
                teacher_count = fake.random_int(min=min_teachers, max=max_teachers)
                teachers_list = []
                while len(teachers_list) < teacher_count:
                    teacher = fake.teacher_provider()
                    if teacher not in teachers_list:
                        teachers_list.append(teacher)
                course.teachers.add(*teachers_list)  # Add teachers in bulk

                # add assistants
                assistant_count = fake.random_int(min=min_assistants, max=max_assistants)
                assistants_list = []
                while len(assistants_list) < assistant_count:
                    assistant = fake.assistant_provider()
                    if assistant not in assistants_list:
                        assistants_list.append(assistant)
                course.assistants.add(*assistants_list)  # Add assistants in bulk

                return course
            except Exception as e:
                print(e)
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique Course."))

    def provide_project(
            self,
            errHandler,
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
            max_group_size=15):
        """Create a Project with the given arguments."""
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                start_date = timezone.now() + timezone.timedelta(
                    days=fake.random_int(min=min_start_date_dev, max=max_start_date_dev))
                deadline = start_date + timezone.timedelta(days=fake.random_int(min=min_deadline_dev, max=max_deadline_dev))
                course = fake.course_provider()
                return Project.objects.create(
                    name=fake.catch_phrase(),
                    description=fake.paragraph(),
                    visible=fake.boolean(chance_of_getting_true=visible_prob),
                    archived=fake.boolean(chance_of_getting_true=archived_prob),
                    score_visible=fake.boolean(chance_of_getting_true=score_visible_prob),
                    locked_groups=fake.boolean(chance_of_getting_true=locked_groups_prob),
                    deadline=deadline,
                    course=course,
                    start_date=start_date,
                    max_score=fake.random_int(min=min_max_score, max=max_max_score),
                    group_size=fake.random_int(min=min_group_size, max=max_group_size)
                )
            except Exception:
                tries += 1
        errHandler.stdout.write(
            errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique project."))

    def provide_group(self, errHandler, min_score=0):
        """Create a Group with the given arguments."""
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                project: Project = fake.project_provider()
                group: Group = Group.objects.create(
                    project=project,
                    score=fake.random_int(min=min_score, max=project.max_score)
                )

                max_group_size = group.project.group_size

                students = group.project.course.students.all()
                groups = group.project.groups.all()
                joined_students = []

                for groupStudents in groups:
                    joined_students.extend(groupStudents.students.all())

                students_not_in_group = [student for student in students if student not in joined_students]

                if len(students_not_in_group) == 0:
                    pass
                elif len(students_not_in_group) < max_group_size:
                    group.students.extend(students_not_in_group)
                else:
                    choosen_students = []
                    for _ in range(0, max_group_size):
                        random_student = students_not_in_group[fake.random_int(min=0, max=len(students_not_in_group))]
                        choosen_students.append(random_student)
                        students_not_in_group.remove(random_student)
                    group.students.add(*choosen_students)  # bulk add the students

                return group
            except Exception:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique group."))

    def provide_submission(self, errHandler, struct_check_passed_prob=70):
        """Create an Submission with the given arguments."""
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                group: Group = fake.group_provider()
                # Generate a random timestamp between start and end timestamps
                random_timestamp = random.uniform(group.project.start_date.timestamp(), group.project.deadline.timestamp())

                # Convert the random timestamp back to a datetime object
                random_datetime = timezone.make_aware(timezone.datetime.fromtimestamp(random_timestamp))

                # get all submisions of this group
                max_submission_number = Submission.objects.filter(
                    group=group
                ).aggregate(Max('submission_number'))['submission_number__max'] or 0

                # print(fake.zip(uncompressed_size=10, num_files=5, min_file_size=1))
                return Submission.objects.create(  # TODO add fake files
                    group=group,
                    submission_time=random_datetime,
                    structure_checks_passed=fake.boolean(chance_of_getting_true=struct_check_passed_prob),
                    submission_number=max_submission_number + 1
                )
            except Exception:
                tries += 1
        errHandler.stdout.write(
            errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique submission."))

    def provide_fileExtension(self, errHandler):
        """
        Create a FileExtension with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                ext = fake.file_extension()
                return FileExtension.objects.create(extension=ext)
            except Exception:
                tries += 1
        errHandler.stdout.write(
            errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique file extension."))

    def provide_structure_check(self, errHandler, min_extensions=1, max_extensions=5, min_path_depth=1, max_path_depth=10):
        """
        Create a StructureCheck with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                check = StructureCheck.objects.create(
                    name=fake.file_path(extension="", depth=fake.random_int(min=min_path_depth, max=max_path_depth)),
                    project=fake.project_provider()
                )

                obligated_extensions = []
                obl_amount = fake.random_int(min=min_extensions, max=max_extensions)
                while len(obligated_extensions) < obl_amount:
                    extension = fake.fileExtension_provider()
                    if extension not in obligated_extensions:
                        obligated_extensions.append(extension)

                blocked_extensions = []
                blo_amount = fake.random_int(min=min_extensions, max=max_extensions)
                while len(blocked_extensions) < blo_amount:
                    extension = fake.fileExtension_provider()
                    if extension not in blocked_extensions and extension not in obligated_extensions:
                        blocked_extensions.append(extension)

                check.obligated_extensions.add(*obligated_extensions)
                check.blocked_extensions.add(*blocked_extensions)

                return check
            except Exception:
                tries += 1
        errHandler.stdout.write(
            errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique structure check."))


def update_providers():
    faculty_provider.elements = Faculty.objects.all()
    student_provider.elements = Student.objects.all()
    assistant_provider.elements = Assistant.objects.all()
    teacher_provider.elements = Teacher.objects.all()
    course_provider.elements = Course.objects.all()
    project_provider.elements = Project.objects.all()
    group_provider.elements = Group.objects.all()
    Submission_provider.elements = Submission.objects.all()
    fileExtension_provider.elements = FileExtension.objects.all()
    structureCheck_provider.elements = StructureCheck.objects.all()


def update_Faculty_providers():
    faculty_provider.elements = Faculty.objects.all()


def update_Student_providers():
    student_provider.elements = Student.objects.all()


def update_Assistant_providers():
    assistant_provider.elements = Assistant.objects.all()


def update_Teacher_providers():
    teacher_provider.elements = Teacher.objects.all()


def update_Course_providers():
    course_provider.elements = Course.objects.all()


def update_Project_providers():
    project_provider.elements = Project.objects.all()


def update_Group_providers():
    group_provider.elements = Group.objects.all()


def update_Submission_providers():
    Submission_provider.elements = Submission.objects.all()


def update_FileExtension_providers():
    fileExtension_provider.elements = FileExtension.objects.all()


def update_StructureCheck_providers():
    structureCheck_provider.elements = StructureCheck.objects.all()


# add new providers to faker instance
fake.add_provider(Providers)
fake.add_provider(faculty_provider)
fake.add_provider(student_provider)
fake.add_provider(assistant_provider)
fake.add_provider(teacher_provider)
fake.add_provider(course_provider)
fake.add_provider(project_provider)
fake.add_provider(group_provider)
fake.add_provider(Submission_provider)
fake.add_provider(fileExtension_provider)
fake.add_provider(structureCheck_provider)


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

    def seed_data(self, amount, provider_function, update_function):
        for _ in range(amount):
            provider_function(self)
        update_function()

    def handle(self, *args, **options):
        start_time = time.time()
        # TODO maybey take as option
        # amount_of_students = 50_000
        # amount_of_assistants = 300
        # amount_of_teachers = 500
        # amount_of_courses = 1_000
        # amount_of_projects = 3_000
        # amount_of_groups = 9_000
        # amount_of_submissions = 50_000
        # amount_of_file_extensions = 20
        # amount_of_structure_checks = 12_000

        amount_of_students = 10
        amount_of_assistants = 0
        amount_of_teachers = 0
        amount_of_courses = 0
        amount_of_projects = 0
        amount_of_groups = 0
        amount_of_submissions = 0
        amount_of_file_extensions = 0
        amount_of_structure_checks = 0

        self.seed_data(amount_of_students, fake.provide_student, update_Student_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded students!'))
        self.seed_data(amount_of_assistants, fake.provide_assistant, update_Assistant_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded assistants!'))
        self.seed_data(amount_of_teachers, fake.provide_teacher, update_Teacher_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded teachers!'))
        self.seed_data(amount_of_courses, fake.provide_course, update_Course_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded courses!'))
        self.seed_data(amount_of_projects, fake.provide_project, update_Project_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded projects!'))
        self.seed_data(amount_of_groups, fake.provide_group, update_Group_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded groups!'))
        self.seed_data(amount_of_submissions, fake.provide_submission, update_Submission_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded submissions!'))
        self.seed_data(amount_of_file_extensions, fake.provide_fileExtension, update_FileExtension_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded fileExtensions!'))
        self.seed_data(amount_of_structure_checks, fake.provide_structure_check, update_StructureCheck_providers)
        self.stdout.write(self.style.SUCCESS('Successfully seeded structure_checks!'))

        end_time = time.time()
        execution_time = end_time - start_time
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded db in {format_time(execution_time)}!"))
