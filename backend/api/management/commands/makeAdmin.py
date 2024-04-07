from django.core.management.base import BaseCommand
from api.models.student import Student

class Command(BaseCommand):
    help = 'seed the db with data'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the student user to make admin')

    def handle(self, *args, **options):
        username = options['username']
        student = Student.objects.filter(username=username)
        if student.count()==0:
            self.stdout.write(self.style.ERROR('User not found, first log in !'))
            return
        student = student.get()
        student.is_staff = True
        student.save()
        self.stdout.write(self.style.SUCCESS('Successfully made yourself admin!'))