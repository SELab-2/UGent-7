from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("authentication", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="NotificationTemplate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title_key", models.CharField(max_length=255)),
                ("description_key", models.CharField(max_length=511)),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        to="authentication.User",
                        on_delete=models.deletion.CASCADE,
                    ),
                ),
                (
                    "template_id",
                    models.ForeignKey(
                        to="notifications.NotificationTemplate",
                        on_delete=models.deletion.CASCADE,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("arguments", models.JSONField(default=dict)),
                ("is_read", models.BooleanField(default=False)),
                ("is_sent", models.BooleanField(default=False)),
            ],
        ),
    ]
