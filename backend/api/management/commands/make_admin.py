from django.core.management.base import BaseCommand
from api.models.student import Student


class Command(BaseCommand):

    help = 'make yourself admin'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the student user to make admin')

    def handle(self, *args, **options):
        username = options['username']
        student = Student.objects.filter(username=username)
        if student.count() == 0:
            self.stdout.write(self.style.ERROR('User not found, first log in !'))
            return
        student = student.get()
        student.make_admin()
        self.stdout.write(self.style.SUCCESS('Successfully made the user admin!'))
