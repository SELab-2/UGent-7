import threading
from smtplib import SMTPException
from typing import Dict, List

from django.core import mail
from django.utils.translation import gettext as _
from notifications.models import Notification
from ypovoli.settings import EMAIL_CUSTOM


# Returns a dictionary with the title and description of the notification
def get_message_dict(notification: Notification) -> Dict[str, str]:
    return {
        "title": _(notification.template_id.title_key),
        "description": _(notification.template_id.description_key)
        % notification.arguments,
    }


# Try to send one email and set the result
def _send_mail(mail: mail.EmailMessage, result: List[bool]):
    try:
        mail.send(fail_silently=False)
        result[0] = True
    except SMTPException:
        result[0] = False


# Send all unsent emails
def send_mails():
    notifications = Notification.objects.filter(is_sent=False)

    # No notifications to send
    if notifications.count() == 0:
        return

    # Connection with the mail server
    connection = mail.get_connection()

    for notification in notifications:
        message = get_message_dict(notification)
        content = _("Email %(name)s %(title)s %(description)s") % {
            "name": notification.user.username,
            "title": message["title"],
            "description": message["description"],
        }

        # Construct the email
        email = mail.EmailMessage(
            subject=EMAIL_CUSTOM["subject"],
            body=content,
            from_email=EMAIL_CUSTOM["from"],
            to=[notification.user.email],
            connection=connection,
        )

        # Send the email with a timeout
        result: List[bool] = [False]
        thread = threading.Thread(target=_send_mail, args=(email, result))
        thread.start()
        thread.join(timeout=EMAIL_CUSTOM["timeout"])

        # If the email was not sent, continue
        if thread.is_alive() or not result[0]:
            continue

        # Mark the notification as sent
        notification.sent()
