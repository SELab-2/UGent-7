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
    max_id = 9_999_999_999_999_999_999_999

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
                id = fake.unique.random_int(min=self.min_id, max = self.max_id)
                faculty = [fake.faculty_provider().id for _ in range(0,fake.random_int(min=min_faculty, max = max_faculty))] # generate 1 or 2 facultys
                username = f"{first}_{last}_{fake.random_int(min=self.min_salt, max = self.max_salt)}"
                teacher = Teacher.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username+"@example.com",
                    create_time=timezone.now(),
                    last_enrolled= timezone.now().year,
                    is_staff=fake.boolean(chance_of_getting_true=staf_prob)
                )

                if faculty is not None:
                    for fac in faculty:
                        teacher.faculties.add(fac)

                # if courses is not None:
                #     for cours in courses:
                #         teacher.courses.add(cours)

                return teacher
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique teacher."))

    def provide_assistant(self, errHandler, min_faculty=1, max_faculty=3, staf_prob=0.01):
        """
        Create a assistant with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                first = fake.first_name()
                last = fake.last_name()
                id = fake.unique.random_int(min=self.min_id, max = self.max_id)
                faculty = [fake.faculty_provider().id for _ in range(0,fake.random_int(min=min_faculty, max = max_faculty))] # generate 1 or 2 or 3 facultys
                username = f"{first}_{last}_{fake.random_int(min=self.min_salt, max = self.max_salt)}"
                assistant = Assistant.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username+"@example.com",
                    create_time=timezone.now(),
                    last_enrolled= timezone.now().year,
                    is_staff=fake.boolean(chance_of_getting_true=staf_prob)
                )

                if faculty is not None:
                    for fac in faculty:
                        assistant.faculties.add(fac)

                # if courses is not None:
                #     for cours in courses:
                #         assistant.courses.add(cours)

                return assistant
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique assistant."))

    def provide_student(self, errHandler, min_faculty=1, max_faculty=3, staf_prob=0.01):
        """
        Create a student with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                first = fake.first_name()
                last = fake.last_name()
                id = fake.unique.random_int(min=self.min_id, max = self.max_id)
                faculty = [fake.faculty_provider().id for _ in range(0,fake.random_int(min=min_faculty, max = max_faculty))] # generate 1 or 2 or 3 facultys
                username = f"{first}_{last}_{fake.random_int(min=self.min_salt, max = self.max_salt)}"
                student = Student.objects.create(
                    id=id,
                    first_name=first,
                    last_name=last,
                    username=username,
                    email=username+"@example.com",
                    create_time=timezone.now(),
                    last_enrolled= timezone.now().year,
                    student_id=id,
                    is_staff=fake.boolean(chance_of_getting_true=staf_prob)
                )

                if faculty is not None:
                    for fac in faculty:
                        student.faculties.add(fac)

                # if courses is not None:
                #     for cours in courses:
                #         student.courses.add(cours)

                return student
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique student."))

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
            max_assistants=5
            ):
        """
        Create a Course with the given arguments.
        """
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                parent_course = None # TODO make this sometimes a course
                course_name = fake.catch_phrase()
                course: Course = Course.objects.create(
                    name=course_name,
                    academic_startyear=timezone.now().year - fake.random_int(min=min_year_passed, max = max_year_passed) ,
                    faculty=fake.faculty_provider(),
                    description=fake.paragraph(),
                    parent_course=parent_course
                )

                # add students
                student_count = fake.random_int(min=min_students, max = max_students)
                while course.students.count() < student_count:
                    student = fake.student_provider()
                    if student not in course.students.all():
                        course.students.add(student)

                # add teachers
                teacher_count = fake.random_int(min=min_teachers, max = max_teachers)
                while course.teachers.count() < teacher_count:
                    teacher = fake.teacher_provider()
                    if teacher not in course.teachers.all():
                        course.teachers.add(teacher)

                # add assistants
                assistant_count = fake.random_int(min=min_assistants, max = max_assistants)
                while course.assistants.count() < assistant_count:
                    assistant = fake.assistant_provider()
                    if assistant not in course.assistants.all():
                        course.assistants.add(assistant)

                # print(course_name)
                return course
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique Course."))

    def provide_project(
            self,
            errHandler,
            min_start_date_dev = -100,
            max_start_date_dev = 100,
            min_deadline_dev = 1,
            max_deadline_dev = 100,
            visible_prob = 80,
            archived_prob = 10,
            score_visible_prob = 30,
            locked_groups_prob = 30,
            min_max_score = 1,
            max_max_score = 100,
            min_group_size = 1,
            max_group_size = 15
            ):
        """Create a Project with the given arguments."""
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                start_date = timezone.now() + timezone.timedelta(days=fake.random_int(min=min_start_date_dev, max = max_start_date_dev))
                deadline = start_date + timezone.timedelta(days=fake.random_int(min=min_deadline_dev, max = max_deadline_dev))
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
                    max_score=fake.random_int(min=min_max_score, max = max_max_score),
                    group_size=fake.random_int(min=min_group_size, max = max_group_size)
                )
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique project."))

    def provide_group(self, errHandler, min_score=0):
        """Create a Group with the given arguments."""
        tries = 0
        while tries < self.MAX_TRIES:
            try:
                project: Project = fake.project_provider()
                group:Group = Group.objects.create(
                    project=project,
                    score=fake.random_int(min=min_score, max = project.max_score)
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
                    for _ in range(0, max_group_size):
                        random_student = students_not_in_group[fake.random_int(min=0,max=len(students_not_in_group))]
                        group.students.add(random_student)
                        students_not_in_group.remove(random_student)

                return group
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique group."))

    def provide_submission(self, errHandler, struct_check_passed_prob=70):
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
                    structure_checks_passed=fake.boolean(chance_of_getting_true=struct_check_passed_prob),
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

    def provide_structure_check(self, errHandler, min_extensions=1, max_extensions = 5, min_path_depth=1, max_path_depth=10):
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
                # print([x.extension for x in obligated_extensions])
                # print([x.extension for x in blocked_extensions])

                for ext in obligated_extensions:
                    check.obligated_extensions.add(ext)
                for ext in blocked_extensions:
                    check.blocked_extensions.add(ext)
                return check
            except:
                tries += 1
        errHandler.stdout.write(errHandler.style.WARNING("Exceeded maximum number of attempts to generate a unique structure check."))

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
fake.add_provider(structureCheck_provider)

class Command(BaseCommand):
    help = 'seed the db with data'

    def handle(self, *args, **options):

        #TODO maybey take as option
        amountOfStudents = 10_000
        amountOfAssistants = 1_000
        amountOfTeachers = 1_000
        amountOfCourses = 1_000
        amountOfProjects = 5_000
        amountOfGroups = 20_000
        amountOfSubmissions = 50_000
        amountOfFileExtensions = 20
        amountOfStructureChecks = 10_000

        # amountOfStudents = 0
        # amountOfAssistants = 0
        # amountOfTeachers = 0
        # amountOfCourses = 0
        # amountOfProjects = 0
        # amountOfGroups = 1
        # amountOfSubmissions = 0
        # amountOfFileExtensions = 0
        # amountOfStructureChecks = 0

        for _ in range(0,amountOfStudents):
            fake.provide_student(self)

        if amountOfStudents: update_providers()

        for _ in range(0,amountOfAssistants):
            fake.provide_assistant(self)

        if amountOfAssistants: update_providers()

        for _ in range(0,amountOfTeachers):
            fake.provide_teacher(self)

        if amountOfTeachers: update_providers()

        for _ in range(0,amountOfCourses):
            fake.provide_course(self)

        if amountOfCourses: update_providers()

        for _ in range(0,amountOfProjects):
            fake.provide_project(self)

        if amountOfProjects: update_providers()

        for _ in range(0,amountOfGroups):
            fake.provide_group(self)

        if amountOfGroups: update_providers()

        for _ in range(0,amountOfSubmissions):
            fake.provide_submission(self)

        if amountOfSubmissions: update_providers()

        for _ in range(0,amountOfFileExtensions):
            fake.provide_fileExtension(self)

        if amountOfFileExtensions: update_providers()

        for _ in range(0,amountOfStructureChecks):
            fake.provide_structure_check(self)

        if amountOfStructureChecks: update_providers()

        self.stdout.write(self.style.SUCCESS('Successfully seeded db!'))
