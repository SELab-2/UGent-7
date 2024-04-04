from django.db import migrations, models
from ypovoli.settings import FILE_PATHS


# TODO: Incorperate new model changes
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
                ('file_path', models.FileField(upload_to=FILE_PATHS["docker_images"], max_length=256, blank=False, null=False)),
                ('custom', models.BooleanField(default=False, blank=False, null=False)),
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
            field=models.ForeignKey(to="api.dockerimage", on_delete=models.CASCADE, related_name="extra_checks"),
        ),
        migrations.AddField(
            model_name="extracheck",
            name="file_path",
            field=models.CharField(max_length=256, blank=False, null=False)
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
            field=models.CharField(max_length=256, blank=False, null=True)
        )
    ]
