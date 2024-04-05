from api.logic.get_file_path import (get_docker_image_file_path,
                                     get_extra_check_file_path,
                                     get_extra_check_result_file_path,
                                     get_submission_file_path)
from django.db import migrations, models


# TODO: Move changes to new file, ER, db
class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_merge_20240313_0639'),
    ]

    operations = [
        migrations.CreateModel(
            name="dockerimage",
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, blank=False, null=False)),
                ('file', models.FileField(upload_to=get_docker_image_file_path, max_length=256, blank=False, null=False)),
                ('owner', models.ForeignKey(to="authentication.user", on_delete=models.SET_NULL,
                 related_name="docker_images", blank=False, null=True)),
                ('public', models.BooleanField(default=False, blank=False, null=False)),
            ]
        ),
        migrations.CreateModel(
            name="errortemplate",
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_key', models.CharField(max_length=256, blank=False, null=False)),
            ]
        ),
        migrations.RemoveField(
            model_name="extracheck",
            name="run_script",
        ),
        migrations.AddField(
            model_name="extracheck",
            name="docker_image",
            field=models.ForeignKey(to="api.dockerimage", on_delete=models.CASCADE,
                                    related_name="extra_checks", blank=False, null=False),
        ),
        migrations.AddField(
            model_name="extracheck",
            name="file",
            field=models.FileField(upload_to=get_extra_check_file_path, max_length=256, blank=False, null=False)
        ),
        migrations.AddField(
            model_name="extracheck",
            name="timeout",
            field=models.SmallIntegerField(default=300, blank=False, null=False)
        ),
        migrations.AddField(
            model_name="extracheck",
            name="show_log",
            field=models.BooleanField(default=True, blank=False, null=False)
        ),
        migrations.AddField(
            model_name="extrachecksresult",
            name="error_message",
            field=models.ForeignKey(to="api.errortemplate", on_delete=models.CASCADE,
                                    related_name="extra_checks_results", blank=True, null=True)
        ),
        migrations.AddField(
            model_name="extrachecksresult",
            name="log_file",
            field=models.FileField(upload_to=get_extra_check_result_file_path, max_length=256, blank=False, null=True)
        ),
        migrations.AddField(
            model_name="extrachecksresult",
            name="is_valid",
            field=models.BooleanField(default=True, blank=False, null=False)
        ),
        migrations.AlterField(
            model_name="submissionfile",
            name="file",
            field=models.FileField(upload_to=get_submission_file_path, max_length=265, blank=False, null=False)
        )
    ]
