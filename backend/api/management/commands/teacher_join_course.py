from django.core.management.base import BaseCommand
from api.models.teacher import Teacher
from api.models.course import Course


class Command(BaseCommand):

    help = 'make a teacher join a course'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the teacher to join the course')
        parser.add_argument('course_id', type=str, help='The id of the course you want to join')

    def handle(self, *args, **options):
        username = options['username']
        course_id = options['course_id']
        teacher = Teacher.objects.filter(username=username)

        if teacher.count() == 0:
            self.stdout.write(self.style.ERROR('Teacher not found, first log in !'))
            return

        teacher = teacher.get()

        course = Course.objects.filter(id=course_id)

        if course.count() == 0:
            self.stdout.write(self.style.ERROR('Course not found, first create it !'))
            return

        course = course.get()

        teacher.courses.add(course_id)

        self.stdout.write(self.style.SUCCESS('Successfully add teacher to course!'))