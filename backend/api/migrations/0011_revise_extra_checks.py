from api.logic.get_file_path import (get_docker_image_file_path,
                                     get_extra_check_file_path,
                                     get_extra_check_result_file_path,
                                     get_submission_file_path)
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_errortemplate_errortemplates_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dockerimage",
            name="file_path"
        ),
        migrations.RemoveField(
            model_name="dockerimage",
            name="custom"
        ),
        migrations.AddField(
            model_name="dockerimage",
            name="file",
            field=models.FileField(upload_to=get_docker_image_file_path, max_length=256, blank=False, null=False)
        ),
        migrations.AddField(
            model_name="dockerimage",
            name="owner",
            field=models.ForeignKey(to="authentication.user", on_delete=models.SET_NULL,
                                    related_name="docker_images", blank=False, null=True)
        ),
        migrations.AddField(
            model_name="dockerimage",
            name="public",
            field=models.BooleanField(default=False, blank=False, null=False)
        ),
        migrations.AlterField(
            model_name="extracheck",
            name="docker_image",
            field=models.ForeignKey(to="api.dockerimage", on_delete=models.CASCADE,
                                    related_name="extra_checks", blank=False, null=False)
        ),
        migrations.RemoveField(
            model_name="extracheck",
            name="file_path"
        ),
        migrations.AddField(
            model_name="extracheck",
            name="file",
            field=models.FileField(upload_to=get_extra_check_file_path, max_length=256, blank=False, null=False)
        ),
        migrations.AlterField(
            model_name="extracheck",
            name="timeout",
            field=models.PositiveSmallIntegerField(default=60, blank=False, null=False)
        ),
        migrations.AlterField(
            model_name="extrachecksresult",
            name="error_message",
            field=models.ForeignKey(to="api.ErrorTemplates", on_delete=models.SET_NULL,
                                    related_name="extra_checks_results", blank=True, null=True)
        ),
        migrations.AlterField(
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
