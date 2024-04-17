from django.core.management.base import BaseCommand
from api.models.assistant import Assistant
from authentication.models import User


class Command(BaseCommand):

    help = 'make yourself assistant'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the user to make assistant')

    def handle(self, *args, **options):
        username = options['username']
        user = User.objects.filter(username=username)

        if user.count() == 0:
            self.stdout.write(self.style.ERROR('User not found, first log in !'))
            return

        user = user.get()
        Assistant.create(user)

        self.stdout.write(self.style.SUCCESS('Successfully made the user assistant!'))
