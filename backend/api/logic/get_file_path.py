# Goofy import structure required to have type hints and avoid circular imports
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api.models.checks import ExtraCheck
    from api.models.docker import DockerImage
    from api.models.project import Project
    from api.models.submission import (ExtraChecksResult, Submission,
                                       SubmissionFile)


def _get_uuid() -> str:
    return str(uuid.uuid4())


def get_project_file_path(instance: Project) -> str:
    # Can use instance.id as the project will always be a foreign key and therefore already be in the database
    return f"projects/{instance.course.id}/{instance.id}/"


def get_submission_file_path(instance: SubmissionFile, name: str) -> str:
    return (f"{get_project_file_path(instance.submission.group.project)}"
            f"submissions/{instance.submission.group.id}/{instance.submission.id}/{name}")


def get_extra_check_file_path(instance: ExtraCheck, _: str) -> str:
    return f"{get_project_file_path(instance.project)}checks/{_get_uuid()}"


def get_extra_check_result_file_path(instance: ExtraChecksResult, _: str) -> str:
    return (f"{get_project_file_path(instance.submission.group.project)}"
            f"submissions/{instance.submission.group.id}/{instance.submission.id}/{_get_uuid()}")


def get_docker_image_file_path(instance: DockerImage, _: str) -> str:
    if instance.public:
        return f"docker_images/public/{_get_uuid()}"
    else:
        return f"docker_images/private/{_get_uuid()}"
