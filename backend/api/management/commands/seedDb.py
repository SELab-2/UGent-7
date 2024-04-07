from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from django.db.models import Max
from faker.providers import BaseProvider, DynamicProvider
import random

from authentication.models import Faculty
from api.models.student import Student
from api.models.assistant import Assistant
from api.models.teacher import Teacher
from api.models.course import Course
from api.models.group import Group
from api.models.project import Project
from api.models.submission import Submission
from api.models.checks import FileExtension

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

# create new provider class
class Providers(BaseProvider):

    MAX_TRIES = 1000

    def provide_teacher(self, errHandler, courses=None):
        """
        Create a teacher with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                first = fake.first_name()
                last = fake.last_name()
                id = fake.unique.random_int(min=1, max = 9999999999999999999999)
                faculty = [fake.faculty_provider().id for _ in range(0,fake.random_int(min=1, max = 2))] # generate 1 or 2 facultys
                username = f"{first}_{last}_{fake.unique.random_int(min=1, max = 9999999999999999999999)}"
                teacher = Teacher.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username+"@example.com",
                    create_time=timezone.now(),
                    last_enrolled= timezone.now().year,
                    is_staff=fake.boolean(chance_of_getting_true=0.01)
                )

                if faculty is not None:
                    for fac in faculty:
                        teacher.faculties.add(fac)

                if courses is not None:
                    for cours in courses:
                        teacher.courses.add(cours)

                return teacher
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique teacher."))

    def provide_assistant(self, errHandler, courses=None):
        """
        Create a assistant with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                first = fake.first_name()
                last = fake.last_name()
                id = fake.unique.random_int(min=1, max = 9999999999999999999999)
                faculty = [fake.faculty_provider().id for _ in range(0,fake.random_int(min=1, max = 3))] # generate 1 or 2 or 3 facultys
                username = f"{first}_{last}_{fake.unique.random_int(min=1, max = 9999999999999999999999)}"
                assistant = Assistant.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username+"@example.com",
                    create_time=timezone.now(),
                    last_enrolled= timezone.now().year,
                    is_staff=fake.boolean(chance_of_getting_true=0.01)
                )

                if faculty is not None:
                    for fac in faculty:
                        assistant.faculties.add(fac)

                if courses is not None:
                    for cours in courses:
                        assistant.courses.add(cours)

                return assistant
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique assistant."))

    def provide_student(self, errHandler, courses=None):
        """
        Create a student with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                first = fake.first_name()
                last = fake.last_name()
                id = fake.unique.random_int(min=1, max = 9999999999999999999999)
                faculty = [fake.faculty_provider().id for _ in range(0,fake.random_int(min=1, max = 3))] # generate 1 or 2 or 3 facultys
                username = f"{first}_{last}_{fake.unique.random_int(min=1, max = 9999999999999999999999)}"
                student = Student.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username+"@example.com",
                    create_time=timezone.now(),
                    last_enrolled= timezone.now().year,
                    student_id=id,
                    is_staff=fake.boolean(chance_of_getting_true=0.01)
                )

                if faculty is not None:
                    for fac in faculty:
                        student.faculties.add(fac)

                if courses is not None:
                    for cours in courses:
                        student.courses.add(cours)

                return student
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique student."))

    def provide_course(self, errHandler):
        """
        Create a Course with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                parent_course = None # TODO make this sometimes a course
                course_name = fake.catch_phrase()
                return Course.objects.create(
                    name=course_name,
                    academic_startyear=timezone.now().year,
                    faculty=fake.faculty_provider(),
                    description=fake.paragraph(),
                    parent_course=parent_course,
                )
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique Course."))

    def provide_project(self, errHandler):
        """Create a Project with the given arguments."""
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                start_date = timezone.now() + timezone.timedelta(days=fake.random_int(min=-100, max = 100))
                deadline = start_date + timezone.timedelta(days=fake.random_int(min=1, max = 100))
                course = fake.course_provider()
                return Project.objects.create(
                    name=fake.catch_phrase(),
                    description=fake.paragraph(),
                    visible=fake.boolean(chance_of_getting_true=80),
                    archived=fake.boolean(chance_of_getting_true=10),
                    score_visible=fake.boolean(chance_of_getting_true=30),
                    locked_groups=fake.boolean(chance_of_getting_true=30),
                    deadline=deadline,
                    course=course,
                    start_date=start_date,
                    max_score=fake.random_int(min=1, max = 100),
                    group_size=fake.random_int(min=1, max = 8)
                )
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique project."))

    def provide_group(self, errHandler):
        """Create a Group with the given arguments."""
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                project: Project = fake.project_provider()
                return Group.objects.create(
                    project=project,
                    score=fake.random_int(min=0, max = project.max_score)
                )
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique group."))

    def provide_submission(self, errHandler):
        """Create an Submission with the given arguments."""
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                group:Group = fake.group_provider()
                # Generate a random timestamp between start and end timestamps
                random_timestamp = random.uniform(group.project.start_date.timestamp(), group.project.deadline.timestamp())

                # Convert the random timestamp back to a datetime object
                random_datetime = timezone.make_aware(timezone.datetime.fromtimestamp(random_timestamp))

                # get all submisions of this group
                max_submission_number = Submission.objects.filter(
                    group=group
                ).aggregate(Max('submission_number'))['submission_number__max'] or 0

                # print(fake.zip(uncompressed_size=10, num_files=5, min_file_size=1))
                return Submission.objects.create( # TODO add fake files
                    group=group,
                    submission_time=random_datetime,
                    structure_checks_passed=fake.boolean(chance_of_getting_true=70),
                    submission_number=max_submission_number + 1
                )
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique submission."))

    def provide_fileExtension(self, errHandler):
        """
        Create a FileExtension with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                ext = fake.file_extension()
                return FileExtension.objects.create(extension=ext)
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique file extension."))

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


    # then add new provider to faker instance
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

class Command(BaseCommand):
    help = 'seed the db with data'

    def handle(self, *args, **options):

        amountOfStudents = 5
        amountOfAssistants = 5
        amountOfTeachers = 5
        amountOfCourses = 10
        amountOfProjects = 10
        amountOfGroups = 20
        amountOfSubmissions = 50
        amountOfFileExtensions = 5

        for _ in range(0,amountOfStudents):
            fake.provide_student(self)

        update_providers()

        for _ in range(0,amountOfAssistants):
            fake.provide_assistant(self)

        update_providers()

        for _ in range(0,amountOfTeachers):
            fake.provide_teacher(self)

        update_providers()

        for _ in range(0,amountOfCourses):
            fake.provide_course(self)

        update_providers()

        for _ in range(0,amountOfProjects):
            fake.provide_project(self)

        update_providers()

        for _ in range(0,amountOfGroups):
            fake.provide_group(self)

        update_providers()

        for _ in range(0,amountOfSubmissions):
            fake.provide_submission(self)

        update_providers()

        for _ in range(0,amountOfFileExtensions):
            fake.provide_fileExtension(self)

        update_providers()

        self.stdout.write(self.style.SUCCESS('Successfully seeded db!'))
