from api.models.submission import ExtraCheckResult, StateEnum
from celery import shared_task


@shared_task
def task_extra_check_start(extra_check_result: ExtraCheckResult):
    extra_check_result.result = StateEnum.SUCCESS
    extra_check_result.save()
