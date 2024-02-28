from django.db import migrations, transaction
from datetime import date


def populate_db(apps, schema_editor):
    with transaction.atomic():
        #Faculty = apps.get_model("api", "Faculty")
        Teacher = apps.get_model("api", "Teacher")
        Student = apps.get_model("api", "Student")
        Course = apps.get_model("api", "Course")
        Assistant = apps.get_model("api", "Assistant")
        Project = apps.get_model("api", "Project")
        Group = apps.get_model("api", "Group")

        #faculty = Faculty.objects.create(
        #    name = "science"
        #)

        teacher1 = Teacher.objects.create(
            id=123,
            first_name="Tom",
            last_name="Boonen",
            email="Tom.Boonen@gmail.be",
            faculty="Science",
            create_time="2023-01-01T00:00:00Z",
        )

        assistant1 = Assistant.objects.create(
            id=235,
            first_name="Bart",
            last_name="Simpson",
            email="Bart.Simpson@gmail.be",
            faculty="Science",
            create_time="2023-01-01T00:00:00Z",
        )

        assistant2 = Assistant.objects.create(
            id=236,
            first_name="Kim",
            last_name="Clijsters",
            email="Kim.Clijsters@gmail.be",
            faculty="Science",
            create_time="2023-01-01T00:00:00Z",
        )

        teacher2 = Teacher.objects.create(
            id=124,
            first_name="Peter",
            last_name="Sagan",
            email="Peter.Sagan@gmail.com",
            faculty="Engineering",
            create_time="2023-01-01T00:00:00Z",
        )

        student1 = Student.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            email="John.Doe@hotmail.com",
            faculty="Science",
            create_time="2023-01-01T00:00:00Z",
        )

        student2 = Student.objects.create(
            id=2,
            first_name="Bartje",
            last_name="Verhaege",
            email="Bartje.Verhaege@gmail.com",
            faculty="Science",
            create_time="2023-01-01T00:00:00Z",
        )

        course = Course.objects.create(
            name="Math",
            academic_startyear=2023,
            description="Math course",
        )

        course2 = Course.objects.create(
            name="Sel2",
            academic_startyear=2023,
            description="Software course",
        )

        project1 = Project.objects.create(
            id=123456,
            name="sel2",
            description="make a project",
            visible=True,
            archived=False,
            # Set the start date as 26th February 2024
            start_date=date(2024, 2, 26),
            # Set the deadline as 27th February 2024
            deadline=date(2024, 2, 27),
            course=course2
        )

        group1 = Group.objects.create(
            project=project1,
        )

        group1.students.add(student1)
        group1.students.add(student2)

        teacher1.courses.add(course)
        teacher2.courses.add(course)
        student1.courses.add(course)
        teacher2.courses.add(course2)

        course.assistants.add(assistant1)
        course2.assistants.add(assistant2)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_db),
    ]
