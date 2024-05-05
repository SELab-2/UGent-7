# Goofy import structure required to have type hints and avoid circular imports
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from ypovoli.settings import DOCKER_BUILD_ROOT_NAME, MEDIA_ROOT, ROOT_DIR

if TYPE_CHECKING:
    from api.models.checks import ExtraCheck
    from api.models.docker import DockerImage
    from api.models.project import Project
    from api.models.submission import ExtraCheckResult, Submission


def _get_uuid() -> str:
    return str(uuid.uuid4())


def _get_project_dir_path(instance: Project) -> str:
    return f"projects/{instance.course.id}/{instance.id}/"


# Absolute path starting from outside the container to the submission directory
def get_submission_full_dir_path(instance: Submission) -> str:
    return (f"{ROOT_DIR}/{MEDIA_ROOT}/{_get_project_dir_path(instance.group.project)}"
            f"submissions/{instance.group.id}/{instance.id}")


def get_submission_file_path(instance: Submission, name: str) -> str:
    return (f"{_get_project_dir_path(instance.group.project)}"
            f"submissions/{instance.group.id}/{_get_uuid()}/{name}")


# Absolute path starting from outside the container to the extra check file
def get_extra_check_file_full_path(instance: ExtraCheck, name: str) -> str:
    return (f"{ROOT_DIR}/{MEDIA_ROOT}/{_get_project_dir_path(instance.project)}checks/{name}")


def get_extra_check_file_path(instance: ExtraCheck, _: str) -> str:
    return f"{_get_project_dir_path(instance.project)}checks/{_get_uuid()}"


def get_extra_check_result_file_path(instance: ExtraCheckResult, _: str) -> str:
    return (f"{_get_project_dir_path(instance.submission.group.project)}"
            f"submissions/{instance.submission.group.id}/{instance.submission.id}/{_get_uuid()}")


def get_docker_image_file_path(instance: DockerImage, _: str) -> str:
    if instance.public:
        return f"docker_images/public/{_get_uuid()}"
    else:
        return f"docker_images/private/{_get_uuid()}"


def get_docker_image_tag(instance: DockerImage) -> str:
    return f"{DOCKER_BUILD_ROOT_NAME}_{instance.id}"
