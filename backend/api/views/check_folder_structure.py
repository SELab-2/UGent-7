import zipfile
import os
from api.models.checks import StructureCheck
from api.models.project import Project
from api.models.extension import FileExtension

data_directory = "../../../data"  # ../data\structures\zip_struct1.zip


def parseZipFile(project, dir_path):
    struct = get_zip_structure(dir_path)
    for key, value in struct.items():
        check = StructureCheck.objects.create(
            name=key,
            project=project
        )
        for ext in value["obligated_extensions"]:
            extensie, _ = FileExtension.objects.get_or_create(
                extension=ext
            )
            print(extensie)
            check.obligated_extensions.add(extensie.id)
        project.structure_checks.add(check)
        print(key, value)



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
            # print(file_name)
            parts = file_name.rsplit('/', 1)  # You can also use '\\' if needed
            if len(parts) == 2:
                map, file = parts
                _, file_extension = os.path.splitext(file)
                file_extension = file_extension[1:]
                if not file_extension == "":
                    directory_structure[map]["obligated_extensions"].add(file_extension)
            else:
                _, file_extension = os.path.splitext(file_name)
                file_extension = file_extension[1:]
                directory_structure["."]["obligated_extensions"].add(file_extension)
    return directory_structure


def check_zip_content(root_path, dir_path, obligated_extensions, blocked_extensions):
    """
        Check the content of a directory without traversing subdirectories.
        :param dir_path: The path of the zip we need to check.
        :param obligated_extensions: The file extensions that are obligated to be present.
        :param blocked_extensions: The file extensions that are forbidden to be present.
        :return:
            True: All checks pass.
            False: At least 1 blocked extension is found or 1 obligated extension is not found.
        """
    dir_path = dir_path.replace('\\', '/')
    # print(f"looking in the {dir_path} subdirectory")
    with zipfile.ZipFile(root_path, 'r') as zip_file:
        zip_contents = set(zip_file.namelist())
        #print(zip_contents)
        found_obligated = set()  # To track found obligated extensions
        if dir_path == ".":
            files_in_subdirectory = [file for file in zip_contents if "/" not in file]
        else:
            files_in_subdirectory = [file[len(dir_path)+1:] for file in zip_contents if (file.startswith(dir_path) and '/' not in file[len(dir_path)+1:] and file[len(dir_path)+1:] != "")]
        # print(files_in_subdirectory)
        for file in files_in_subdirectory:
            _, file_extension = os.path.splitext(file)
            file_extension = file_extension[1:]  # file_extension[1:] to remove the .
            # print(file_extension)
            if file_extension in blocked_extensions:
                print(f"Error: {file_extension} found in '{dir_path}' is not allowed.")
                return False
            elif file_extension in obligated_extensions:
                found_obligated.add(file_extension)
        return set(obligated_extensions) <= found_obligated


def check_zip_structure(folder_structure, zip_file_path, restrict_extra_folders=False):
    """
    Check the structure of a zip file.
    :param zip_file_path: Path to the zip file.
    :param folder_structure: Dictionary representing the expected folder structure.
    :return:
        True: Zip file structure matches the expected structure.
        False: Zip file structure does not match the expected structure.
    """
    base, _ = os.path.splitext(zip_file_path)
    struc = [f for f in folder_structure.keys() if not f == "."]
    # print(struc)
    dirs = list_zip_directories(zip_file_path)
    for dir in struc:
        if dir not in dirs:
            print(f"Error: Directory '{dir}' not defined.")
            return False

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        # zip_contents = set(zip_file.namelist())
        # print(f"all contents in the zip are {zip_contents}")
        for directory, info in folder_structure.items():
            # base_name, _ = os.path.splitext(zip_file_path)
            obligated_extensions = info.get('obligated_extensions', set())
            blocked_extensions = info.get('blocked_extensions', set())

            result = check_zip_content(zip_file_path, directory, obligated_extensions, blocked_extensions)
            if not result:
                return False
    # Check for any directories not present in the folder structure dictionary
    # print(struc)
    # print(dirs)
    if restrict_extra_folders:
        for actual_directory in dirs:
            if actual_directory not in struc:
                print(f"Error: Directory '{actual_directory}' not defined in the folder structure dictionary.")
                return False
    return True
