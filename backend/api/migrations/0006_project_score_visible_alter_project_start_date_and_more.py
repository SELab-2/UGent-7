# Generated by Django 5.0.2 on 2024-03-12 09:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_project_max_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='score_visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submission_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
