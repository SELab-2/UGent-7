# Goofy import structure required to have type hints and avoid circular imports
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.models.checks import ExtraCheck
    from api.models.docker import DockerImage
    from api.models.project import Project
    from api.models.submission import ExtraChecksResult, Submission


def get_project_file_path(instance: Project) -> str:
    return f"projects/{instance.id}"


def get_submission_file_path(instance: Submission, _: str) -> str:
    return (f"{get_project_file_path(instance.group.project)}/"
            f"submissions/{instance.group.id}/{instance.id}_submission")


def get_extra_check_file_path(instance: ExtraCheck, _: str) -> str:
    return f"{get_project_file_path(instance.project)}/checks/{instance.id}"


def get_extra_check_result_file_path(instance: ExtraChecksResult, _: str) -> str:
    return (f"{get_project_file_path(instance.submission.group.project)}/"
            f"submissions/{instance.submission.group.id}/{instance.submission.id}__log{instance.id}")


def get_docker_image_file_path(instance: DockerImage, _: str) -> str:
    if instance.public:
        return f"docker_images/public/{instance.id}"
    else:
        return f"docker_images/private/{instance.id}"
