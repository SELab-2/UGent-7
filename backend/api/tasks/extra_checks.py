from api.models.submission import Submission
from celery import shared_task


@shared_task
def task_extra_check_start(submission_id):
    pass
