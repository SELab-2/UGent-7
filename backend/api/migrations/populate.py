from django.db import migrations, transaction


def populate_teacher_student_courses(apps, schema_editor):
    with transaction.atomic():

        Teacher = apps.get_model("api", "Teacher")
        Student = apps.get_model("api", "Student")
        Course = apps.get_model("api", "Course")
        Assistant = apps.get_model("api","Assistant")

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
    
        course = Course.objects.create(
            name="Math",
            academic_startyear=2023,
            description="Math course",
        )

        teacher1.courses.add(course)
        teacher2.courses.add(course)
        student1.courses.add(course)
        #course.assistants.add(assistant1)
        #course.assistants.add(assistant2)



class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_teacher_student_courses),
    ]