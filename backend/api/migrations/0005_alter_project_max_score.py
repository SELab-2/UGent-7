# Generated by Django 5.0.2 on 2024-03-06 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_submission_structure_checks_passed_extrachecksresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='max_score',
            field=models.PositiveSmallIntegerField(default=20),
        ),
    ]
