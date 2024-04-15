from api.models.submission import StateEnum, StructureCheckResult
from celery import shared_task


@shared_task()
def task_structure_check_start(structure_check_result: StructureCheckResult):
    structure_check_result.result = StateEnum.SUCCESS
    structure_check_result.save()
