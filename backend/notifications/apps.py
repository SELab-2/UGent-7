from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"


# TODO: Allow is_sent to be adjusted
# TODO: Signals to send notifications
# TODO: Send emails
# TODO: Think about the required api endpoints
