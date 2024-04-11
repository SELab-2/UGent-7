from api.models.submission import Submission
from celery import shared_task


@shared_task
def task_extra_check_start(submissions: tuple[Submission]):
    pass
