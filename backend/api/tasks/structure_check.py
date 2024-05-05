import zipfile
from io import BytesIO

from api.models.submission import (ErrorMessageEnum, StateEnum,
                                   StructureCheckResult)
from celery import shared_task


@shared_task()
def task_structure_check_start(structure_check_results: list[StructureCheckResult]):
    all_checks_passed = True  # Boolean to check if all structure checks passed
    name_ext: dict[str, str]  # Dict with file name and extension

    # Get all files inside the zip
    with zipfile.ZipFile(structure_check_results[0].submission.zip.path, 'r') as zip:
        file_list = zip.namelist()

        if len(file_list) == 1:
            # There's a chance that we zipped a submitted zip file
            zip_data = BytesIO(zip.read(file_list[0]))
            if zipfile.is_zipfile(zip_data):
                with zipfile.ZipFile(zip_data, 'r') as inner_zip:
                    file_list = inner_zip.namelist()

        name_ext = {file: file.split('.')[-1] for file in file_list}

    # Check each structure check
    for structure_check_result in structure_check_results:
        extensions = [ext for (name, ext) in name_ext.items() if name.startswith(structure_check_result.structure_check.path)]

        structure_check_result.result = StateEnum.SUCCESS

        # Check if path is present in the zip
        if len(extensions) == 0:
            structure_check_result.result = StateEnum.FAILED
            structure_check_result.error_message = ErrorMessageEnum.FILE_DIR_NOT_FOUND

        # Check if no blocked extension is present
        if structure_check_result.result == StateEnum.SUCCESS:
            for extension in structure_check_result.structure_check.blocked_extensions.all():
                if extension.extension in extensions:
                    structure_check_result.result = StateEnum.FAILED
                    structure_check_result.error_message = ErrorMessageEnum.BLOCKED_EXTENSION

        # Check if all obligated extensions are present
        if structure_check_result.result == StateEnum.SUCCESS:
            for extension in structure_check_result.structure_check.obligated_extensions.all():
                if extension.extension not in extensions:
                    structure_check_result.result = StateEnum.FAILED
                    structure_check_result.error_message = ErrorMessageEnum.OBLIGATED_EXTENSION_NOT_FOUND

        all_checks_passed = all_checks_passed and structure_check_result.result == StateEnum.SUCCESS
        structure_check_result.save()

    return all_checks_passed
