from django.core.management.base import BaseCommand
from authentication.models import User


class Command(BaseCommand):

    help = 'make yourself admin'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the student user to make admin')

    def handle(self, *args, **options):
        username = options['username']
        user = User.objects.filter(username=username)
        if user.count() == 0:
            self.stdout.write(self.style.ERROR('User not found, first log in !'))
            return
        user = user.get()
        user.make_admin()
        self.stdout.write(self.style.SUCCESS('Successfully made the user admin!'))