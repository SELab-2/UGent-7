from django.dispatch import Signal

user_created_signal = Signal()
user_login_signal = Signal()
user_logout_signal = Signal()