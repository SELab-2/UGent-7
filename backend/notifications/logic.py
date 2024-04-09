import threading
from collections import defaultdict
from os import error
from smtplib import SMTPException
from typing import DefaultDict, Dict, List

from celery import shared_task
from django.core import mail
from django.core.cache import cache
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


# Call the function after 60 seconds and no more than once in that period
def schedule_send_mails():
    if not cache.get("notifications_send_mails"):
        cache.set("notifications_send_mails", True)
        _send_mails.apply_async(countdown=60)


# Try to send one email and set the result
def _send_mail(mail: mail.EmailMessage, result: List[bool]):
    try:
        mail.send(fail_silently=False)
        result[0] = True
    except SMTPException:
        result[0] = False


# Send all unsent emails
@shared_task
def _send_mails():
    # All notifications that need to be sent
    notifications = Notification.objects.filter(is_sent=False)
    # Dictionary with the number of errors for each email
    errors: DefaultDict[str, int] = cache.get(
        "notifications_send_mails_errors", defaultdict(int)
    )

    # No notifications to send
    if notifications.count() == 0:
        return

    # Connection with the mail server
    connection = mail.get_connection()

    # Construct and send each mail
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

        # Email failed to send
        if thread.is_alive() or not result[0]:
            # Increase the number of errors for the email
            errors[notification.user.email] += 1
            # Mark notification as sent if the maximum number of errors is reached
            if errors[notification.user.email] >= EMAIL_CUSTOM["max_errors"]:
                errors.pop(notification.user.email)
                notification.sent()

            continue

        # Email sent successfully
        if notification.user.email in errors:
            errors.pop(notification.user.email)

        # Mark the notification as sent
        notification.sent()

    # Save the number of errors for each email
    cache.set("notifications_send_mails_errors", errors)

    # Restart the process if there are any notifications left that were not sent
    unsent_notifications = Notification.objects.filter(is_sent=False)
    cache.set("notifications_send_mails", False)
    if unsent_notifications.count() > 0:
        schedule_send_mails()
