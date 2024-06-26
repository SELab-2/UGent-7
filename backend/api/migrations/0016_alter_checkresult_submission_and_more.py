# Generated by Django 5.0.4 on 2024-04-14 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_checkresult_remove_extrachecksresult_error_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkresult',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='api.submission'),
        ),
        migrations.AlterField(
            model_name='extracheckresult',
            name='extra_check',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_check', to='api.extracheck'),
        ),
        migrations.AlterField(
            model_name='structurecheckresult',
            name='structure_check',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='structure_check', to='api.structurecheck'),
        ),
    ]
