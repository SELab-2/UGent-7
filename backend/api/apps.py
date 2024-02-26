from django.apps import AppConfig
from authentication.signals import user_created_signal

def receiver(sender, **kwargs):
    # todo: handle the user created event
    # todo: move this function to a more appropriate module
    pass

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        user_created_signal.connect(
            receiver=receiver,
            dispatch_uid='user_created_signal'
        )