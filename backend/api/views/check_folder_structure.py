import zipfile
import os
from api.models.checks import StructureCheck
from api.models.extension import FileExtension
from django.utils.translation import gettext
from django.conf import settings


def parseZipFile(project, dir_path):  # TODO block paths that start with ..
    dir_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, dir_path))
    struct = get_zip_structure(dir_path)

    sorted_keys = sorted(struct.keys())

    for key in sorted_keys:
        value = struct[key]
        check = StructureCheck.objects.create(
            name=key,
            project=project
        )
        for ext in value["obligated_extensions"]:
            extensie, _ = FileExtension.objects.get_or_create(
                extension=ext
            )
            check.obligated_extensions.add(extensie.id)
        project.structure_checks.add(check)


# TODO block paths that start with ..
def checkZipFile(project, dir_path, restrict_extra_folders=False):
    dir_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, dir_path))
    project_structure_checks = StructureCheck.objects.filter(
                                                project=project.id)
    structuur = {}
    for struct in project_structure_checks:
        structuur[struct.name] = {
            'obligated_extensions': set(),
            'blocked_extensions': set()
        }
        for ext in struct.obligated_extensions.all():
            structuur[struct.name]["obligated_extensions"].add(ext.extension)
        for ext in struct.blocked_extensions.all():
            structuur[struct.name]["blocked_extensions"].add(ext.extension)
    return check_zip_structure(
        structuur, dir_path, restrict_extra_folders=restrict_extra_folders)


def get_parent_directories(dir_path):
    components = dir_path.split('/')
    parents = set()
    current_path = ""
    for component in components:
        if current_path != "":
            current_path = current_path + "/" + component
        else:
            current_path = component
        parents.add(current_path)
    return parents


def list_zip_directories(zip_file_path):
    """
    List all directories in a zip file.
    :param zip_file_path: Path where the zip file is located.
    :return: List of directory names.
    """
    dirs = set()
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        info_list = zip_ref.infolist()
        for file in info_list:
            if file.is_dir():
                dir_path = file.filename[:-1]
                parent_dirs = get_parent_directories(dir_path)
                dirs.update(parent_dirs)
    return dirs


def get_zip_structure(root_path):
    directory_structure = {}
    base, _ = os.path.splitext(root_path)
    inhoud = list_zip_directories(root_path)
    inhoud.add(".")
    for inh in inhoud:
        directory_structure[inh] = {
            'obligated_extensions': set(),
            'blocked_extensions': set()
        }
    with zipfile.ZipFile(root_path, 'r') as zip_file:
        file_names = zip_file.namelist()
        for file_name in file_names:
            parts = file_name.rsplit('/', 1)
            if len(parts) == 2:
                map, file = parts
                _, file_extension = os.path.splitext(file)
                file_extension = file_extension[1:]
                if not file_extension == "":
                    directory_structure[map]["obligated_extensions"].add(
                                                                file_extension)
            else:
                _, file_extension = os.path.splitext(file_name)
                file_extension = file_extension[1:]
                directory_structure["."]["obligated_extensions"].add(
                                                                file_extension)
    return directory_structure


def check_zip_content(
        root_path,
        dir_path,
        obligated_extensions,
        blocked_extensions):
    """
    Check the content of a directory without traversing subdirectories.
    parameters:
    dir_path: The path of the zip we need to check.
    obligated_extensions: The file extensions that are obligated to be present.
    blocked_extensions: The file extensions that are forbidden to be present.
    :return:
        True: All checks pass.
        False: At least 1 blocked extension is found
                or 1 obligated extension is not found.
        """
    dir_path = dir_path.replace('\\', '/')
    with zipfile.ZipFile(root_path, 'r') as zip_file:
        zip_contents = set(zip_file.namelist())
        found_obligated = set()  # To track found obligated extensions
        if dir_path == ".":
            files_in_subdirectory = [
                file for file in zip_contents if "/" not in file
                ]
        else:
            files_in_subdirectory = [
                file[len(dir_path)+1:] for file in zip_contents
                if (file.startswith(dir_path) and
                    '/' not in file[len(dir_path)+1:] and
                    file[len(dir_path)+1:] != "")]

        for file in files_in_subdirectory:
            _, file_extension = os.path.splitext(file)
            # file_extension[1:] to remove the .
            file_extension = file_extension[1:]

            if file_extension in blocked_extensions:
                # print(
                # f"Error: {file_extension} found in
                # '{dir_path}' is not allowed.") TODO
                return False, gettext(
                    'zip.errors.invalid_structure.blocked_extension_found')
            elif file_extension in obligated_extensions:
                found_obligated.add(file_extension)
        if set(obligated_extensions) <= found_obligated:
            return True, gettext('zip.success')
        else:
            return False, gettext(
                'zip.errors.invalid_structure.obligated_extension_not_found')


def check_zip_structure(
        folder_structure,
        zip_file_path,
        restrict_extra_folders=False):
    """
    Check the structure of a zip file.

    parameters:
    zip_file_path: Path to the zip file.
    folder_structure: Dictionary representing the expected folder structure.
    :return:
        True: Zip file structure matches the expected structure.
        False: Zip file structure does not match the expected structure.
    """
    base, _ = os.path.splitext(zip_file_path)
    struc = [f for f in folder_structure.keys() if not f == "."]

    dirs = list_zip_directories(zip_file_path)
    for dir in struc:
        if dir not in dirs:
            # print(f"Error: Directory '{dir}' not defined.") TODO
            return False, gettext(
                'zip.errors.invalid_structure.directory_not_defined')

    for directory, info in folder_structure.items():
        obligated_extensions = info.get('obligated_extensions', set())
        blocked_extensions = info.get('blocked_extensions', set())

        result, message = check_zip_content(
            zip_file_path,
            directory,
            obligated_extensions,
            blocked_extensions)
        if not result:
            return result, message
    # Check for any directories not present in the folder structure dictionary
    if restrict_extra_folders:
        for actual_directory in dirs:
            if actual_directory not in struc:
                # print(f"Error: Directory '{actual_directory}'
                # not defined in the folder structure dictionary.") TODO
                return False, gettext(
                    'zip.errors.invalid_structure.directory_not_found_in_template')
    return True, gettext('zip.success')
