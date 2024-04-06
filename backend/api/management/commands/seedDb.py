from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from faker.providers import BaseProvider
from faker.providers import DynamicProvider

from api.models.student import Student
from api.models.assistant import Assistant
from api.models.course import Course
from authentication.models import Faculty

fake = Faker()

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

course_provider = DynamicProvider(
     provider_name="course_provider",
     elements=Course.objects.all(),
)

# create new provider class
class Providers(BaseProvider):
    def provide_assistant(self, courses=None):
        """
        Create a assistant with the given arguments.
        """
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

    def provide_course(description=None, parent_course=None):
        """
        Create a Course with the given arguments.
        """
        course_name = fake.catch_phrase()
        return Course.objects.create(
            name=course_name,
            academic_startyear=timezone.now().year,
            faculty=fake.faculty_provider(),
            description=fake.paragraph(),
            parent_course=parent_course,
        )

    def provide_student(self, courses=None):
        """
        Create a student with the given arguments.
        """
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

def update_providers():
    faculty_provider.elements = Faculty.objects.all()
    student_provider.elements = Student.objects.all()
    assistant_provider.elements = Assistant.objects.all()
    course_provider.elements = Course.objects.all()


    # then add new provider to faker instance
fake.add_provider(Providers)
fake.add_provider(faculty_provider)
fake.add_provider(student_provider)
fake.add_provider(course_provider)
fake.add_provider(assistant_provider)

class Command(BaseCommand):
    help = 'seed the db with data'

    def handle(self, *args, **options):

        amountOfStudents = 1
        amountOfAssistants = 1
        amountOfCourses = 1

        for _ in range(0,amountOfStudents):
            fake.provide_student()

        update_providers()

        for _ in range(0,amountOfCourses):
            fake.provide_course()

        update_providers()

        for _ in range(0,amountOfAssistants):
            fake.provide_assistant()

        update_providers()

        self.stdout.write(self.style.SUCCESS('Successfully ran my custom command!'))
