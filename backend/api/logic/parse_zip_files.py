import zipfile

from api.models.checks import FileExtension, StructureCheck
from api.models.project import Project
from django.core.files.uploadedfile import InMemoryUploadedFile


def parse_zip(project: Project, zip_file: InMemoryUploadedFile) -> bool:
    if not zipfile.is_zipfile(zip_file):
        return False

    zip_file.seek(0)

    with zipfile.ZipFile(zip_file, 'r') as zip:
        files = zip.namelist()
        directories = [file.filename for file in zip.infolist() if file.is_dir()]

    # Add for each directory a structure check
    for directory in directories:
        create_check(project, directory, files)

    # Add potential top level files
    top_level_files = [file for file in files if '/' not in file]
    if top_level_files:
        create_check(project, '', files)

    return True


def create_check(project: Project, directory_path: str, files: list[str]):
    check = StructureCheck.objects.create(
        path=directory_path,
        project=project
    )

    # Get all files in the directory but not in subdirectories
    files_in_directory = [
        file for file
        in files
        if file.startswith(directory_path) and file != directory_path and '/' not in file[len(directory_path):]
    ]

    # Add for each file the (blocked or obligated) extension to the check
    for file in files_in_directory:
        file_extension = file.split('.')[-1]

        if file_extension.startswith('-'):
            # Blocked extension
            extension, _ = FileExtension.objects.get_or_create(extension=file_extension[1:])
            check.blocked_extensions.add(extension.id)
        else:
            # Obligated extension
            extension, _ = FileExtension.objects.get_or_create(extension=file_extension)
            check.obligated_extensions.add(extension.id)
