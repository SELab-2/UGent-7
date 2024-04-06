from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from faker.providers import BaseProvider

from api.models.student import Student


fake = Faker()

def create_student(first_name, last_name, email, faculty=None, courses=None):
    """
    Create a student with the given arguments.
    """
    username = f"{first_name}_{last_name}"
    student = Student.objects.create(
        id=fake.unique.random_int(min=1, max = 9999999999999999999999),
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        create_time=timezone.now(),
    )

    if faculty is not None:
        for fac in faculty:
            student.faculties.add(fac)

    if courses is not None:
        for cours in courses:
            student.courses.add(cours)

    return student

# create new provider class
class Providers(BaseProvider):
    def provide_student(self) -> Student:
        return create_student(first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email())

    # then add new provider to faker instance
fake.add_provider(Providers)

def getFakeStudent():
    return fake.provide_student()

class Command(BaseCommand):
    help = 'seed the db with data'

    def handle(self, *args, **options):
        # Your command logic here
        # Create a fake student instance
        fake_student = getFakeStudent()

        self.stdout.write(self.style.SUCCESS('Successfully ran my custom command!'))
