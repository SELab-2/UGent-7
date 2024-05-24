import zipfile
from io import BytesIO
from time import sleep

from api.models.submission import (ErrorMessageEnum, StateEnum,
                                   StructureCheckResult)
from celery import shared_task
from notifications.signals import NotificationType, notification_create


@shared_task()
def task_structure_check_start(structure_check_results: list[StructureCheckResult]):
    if len(structure_check_results) == 0:
        return True

    # Will probably never happen but doesn't hurt to check
    while structure_check_results[0].submission.running_checks:
        sleep(1)

    # Lock
    structure_check_results[0].submission.running_checks = True

    # Notification type
    notification_type = NotificationType.STRUCTURE_CHECK_SUCCESS

    all_checks_passed = True  # Boolean to check if all structure checks passed
    name_ext = _get_all_name_ext(structure_check_results[0].submission.zip.path)  # Dict with file name and extension

    # Check each structure check
    for structure_check_result in structure_check_results:
        # Only check in given path and not in subdirectories
        extensions = [
            ext for (name, ext)
            in name_ext.items()
            if name.startswith(structure_check_result.structure_check.path)
            and '/' not in name[len(structure_check_result.structure_check.path):]
        ]

        structure_check_result.result = StateEnum.SUCCESS

        # Check if path is present in the zip
        if len(extensions) == 0:
            structure_check_result.result = StateEnum.FAILED
            structure_check_result.error_message = ErrorMessageEnum.FILE_DIR_NOT_FOUND
            notification_type = NotificationType.STRUCTURE_CHECK_FAIL

        # Check if no blocked extension is present
        if structure_check_result.result == StateEnum.SUCCESS:
            for extension in structure_check_result.structure_check.blocked_extensions.all():
                if extension.extension in extensions:
                    structure_check_result.result = StateEnum.FAILED
                    structure_check_result.error_message = ErrorMessageEnum.BLOCKED_EXTENSION
                    notification_type = NotificationType.STRUCTURE_CHECK_FAIL

        # Check if all obligated extensions are present
        if structure_check_result.result == StateEnum.SUCCESS:
            for extension in structure_check_result.structure_check.obligated_extensions.all():
                if extension.extension not in extensions:
                    structure_check_result.result = StateEnum.FAILED
                    structure_check_result.error_message = ErrorMessageEnum.OBLIGATED_EXTENSION_NOT_FOUND
                    notification_type = NotificationType.STRUCTURE_CHECK_FAIL

        all_checks_passed = all_checks_passed and structure_check_result.result == StateEnum.SUCCESS
        structure_check_result.save()

    # Release
    structure_check_results[0].submission.running_checks = False

    # Send notification
    notification_create.send(
        sender=StructureCheckResult,
        type=notification_type,
        queryset=list(structure_check_results[0].submission.group.students.all()),
        arguments={},
    )

    return all_checks_passed


def _get_all_name_ext(path: str) -> dict[str, str]:
    # Get all files inside the zip
    with zipfile.ZipFile(path, 'r') as zip:
        file_list = zip.namelist()

        if len(file_list) == 1:
            # There's a chance that we zipped a submitted zip file
            zip_data = BytesIO(zip.read(file_list[0]))
            if zipfile.is_zipfile(zip_data):
                with zipfile.ZipFile(zip_data, 'r') as inner_zip:
                    file_list = inner_zip.namelist()

    return {'/'.join(file.split('/')[:-1]): file.split('.')[-1] for file in file_list}
