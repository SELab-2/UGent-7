# Generated by Django 5.0.3 on 2024-04-03 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_rename_name_faculty_id_faculty_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faculty',
            old_name='description',
            new_name='name',
        ),
    ]
