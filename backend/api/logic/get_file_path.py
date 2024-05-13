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
    return f"production/projects/{instance.course.id}/{instance.id}/"


# Absolute path starting from outside the container to the submission directory
def get_submission_full_dir_path(instance: Submission) -> str:
    submission_path = "/".join(instance.zip.path.split("/")[3:-1])
    return f"{ROOT_DIR}/{MEDIA_ROOT}/{submission_path}"


def get_submission_file_path(instance: Submission, name: str) -> str:
    return (f"{_get_project_dir_path(instance.group.project)}"
            f"submissions/{instance.group.id}/{instance.submission_number}/{name}")


# Absolute path starting from outside the container to the extra check file
def get_extra_check_file_full_path(instance: ExtraCheck) -> str:
    extra_check_path = "/".join(instance.file.path.split("/")[3:])
    return f"{ROOT_DIR}/{MEDIA_ROOT}/{extra_check_path}"


def get_extra_check_file_path(instance: ExtraCheck, _: str) -> str:
    return f"{_get_project_dir_path(instance.project)}checks/{_get_uuid()}"


def get_extra_check_log_file_path(instance: ExtraCheckResult, uuid: str) -> str:
    return (f"{_get_project_dir_path(instance.submission.group.project)}"
            f"submissions/{instance.submission.group.id}/{uuid}/logs/{_get_uuid()}.txt")


def get_docker_image_file_path(instance: DockerImage, _: str) -> str:
    if instance.public:
        return f"production/docker_images/public/{_get_uuid()}"
    else:
        return f"production/docker_images/private/{_get_uuid()}"


def get_docker_image_tag(instance: DockerImage) -> str:
    return f"{DOCKER_BUILD_ROOT_NAME}_{instance.id}"


def get_extra_check_artifact_file_path(instance: ExtraCheckResult, uuid: str) -> str:
    return (f"{_get_project_dir_path(instance.submission.group.project)}"
            f"submissions/{instance.submission.group.id}/{uuid}/artifacts/{_get_uuid()}.zip")
