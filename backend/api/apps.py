from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Only here we can import from apps.
        from authentication.signals import user_created
        from api.signals import user_creation

        user_created.connect(user_creation)
