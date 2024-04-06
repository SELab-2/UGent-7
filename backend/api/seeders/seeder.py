from faker import Faker

# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

from api.models.student import Student

fake = Faker()

# create new provider class
class Providers(BaseProvider):
    def provide_student(self) -> Student:
        return Student()

# then add new provider to faker instance
fake.add_provider(Providers)

def printFakeStudent():
    print(fake.provide_student())