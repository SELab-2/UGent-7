import io
import os
import shutil
import zipfile
from time import sleep
from typing import cast

import docker
import docker.errors
from api.logic.get_file_path import (get_docker_image_tag,
                                     get_extra_check_file_full_path,
                                     get_submission_full_dir_path)
from api.models.docker import StateEnum as DockerStateEnum
from api.models.submission import ErrorMessageEnum, ExtraCheckResult, StateEnum
from celery import shared_task
from django.core.files import File
from django.core.files.base import ContentFile
from docker.models.containers import Container
from docker.types import LogConfig
from requests.exceptions import ConnectionError


@shared_task
def task_extra_check_start(structure_check_result: bool, extra_check_result: ExtraCheckResult):
    # Check if the structure checks were succesful
    if not structure_check_result:
        extra_check_result.result = StateEnum.FAILED
        extra_check_result.error_message = ErrorMessageEnum.FAILED_STRUCTURE_CHECK
        extra_check_result.save()

        return structure_check_result

    # Check if the docker image is ready
    if extra_check_result.extra_check.docker_image.state != DockerStateEnum.READY:
        extra_check_result.result = StateEnum.FAILED
        extra_check_result.error_message = ErrorMessageEnum.DOCKER_IMAGE_ERROR
        extra_check_result.save()

        return structure_check_result

    # Will probably never happen but doesn't hurt to check
    while extra_check_result.submission.running_checks:
        sleep(1)

    # Lock
    extra_check_result.submission.running_checks = True

    # Start the process
    extra_check_result.result = StateEnum.RUNNING
    extra_check_result.save()

    submission_directory = "/".join(extra_check_result.submission.zip.path.split("/")
                                    [:-1]) + "/submission/"  # Directory where the files will be extracted
    artifacts_directory = f"{submission_directory}/artifacts"  # Directory where the artifacts will be stored
    extra_check_name = extra_check_result.extra_check.file.name.split("/")[-1]  # Name of the extra check file
    submission_uuid = extra_check_result.submission.zip.path.split("/")[-2]  # Uuid of the submission

    # Unzip the files
    with zipfile.ZipFile(extra_check_result.submission.zip.path, 'r') as zip:
        zip.extractall(submission_directory)

    # Create artifacts directory
    os.makedirs(artifacts_directory, exist_ok=True)

    container: Container | None = None

    try:
        # Get docker client
        client: docker.DockerClient = docker.from_env()

        # Create and run container
        container = cast(Container, client.containers.run(
            image=get_docker_image_tag(extra_check_result.extra_check.docker_image),
            command=f"sh {extra_check_name}",
            detach=True,
            log_config=LogConfig(type=LogConfig.types.JSON, config={"max-size": "50kb"}),
            mem_limit=f"{extra_check_result.extra_check.memory_limit}m",
            privileged=False,
            remove=False,  # Don't remove yet as we need the logs first
            stdout=True,
            stderr=True,
            volumes={
                f"{get_submission_full_dir_path(extra_check_result.submission)}/submission": {
                    "bind": "/submission", "mode": "rw"
                },
                f"{get_submission_full_dir_path(extra_check_result.submission)}/submission/artifacts": {
                    "bind": "/submission/artifacts", "mode": "rw"
                },
                get_extra_check_file_full_path(extra_check_result.extra_check): {
                    "bind": f"/submission/{extra_check_name}", "mode": "ro"
                }
            },
            working_dir="/submission"
        ))

        # Wait for container to finish
        container.wait(timeout=extra_check_result.extra_check.time_limit)

        # Check for possible (custom) error types / codes
        container_info: dict = client.api.inspect_container(container.id)

        # Memory limit
        if container_info["State"]["OOMKilled"]:
            extra_check_result.result = StateEnum.FAILED
            extra_check_result.error_message = ErrorMessageEnum.MEMORY_LIMIT

        # Exit codes
        match container_info["State"]["ExitCode"]:
            # Success!
            case 0:
                extra_check_result.result = StateEnum.SUCCESS

            # Custom check error
            case 1:
                extra_check_result.result = StateEnum.FAILED
                extra_check_result.error_message = ErrorMessageEnum.CHECK_ERROR

            # Time limit
            case 2:
                extra_check_result.result = StateEnum.FAILED
                extra_check_result.error_message = ErrorMessageEnum.TIME_LIMIT

            # Memory limit
            case 3:
                extra_check_result.result = StateEnum.FAILED
                extra_check_result.error_message = ErrorMessageEnum.MEMORY_LIMIT

            # Catch all non zero exit codes
            case _:
                extra_check_result.result = StateEnum.FAILED
                extra_check_result.error_message = ErrorMessageEnum.RUNTIME_ERROR

    # Docker image error
    except (docker.errors.APIError, docker.errors.ImageNotFound):
        extra_check_result.result = StateEnum.FAILED
        extra_check_result.error_message = ErrorMessageEnum.DOCKER_IMAGE_ERROR

    # Runtime error
    except docker.errors.ContainerError:
        extra_check_result.result = StateEnum.FAILED
        extra_check_result.error_message = ErrorMessageEnum.RUNTIME_ERROR

    # Timeout error
    except ConnectionError:
        extra_check_result.result = StateEnum.FAILED
        extra_check_result.error_message = ErrorMessageEnum.TIME_LIMIT

    # Unknown error
    except Exception:
        extra_check_result.result = StateEnum.FAILED
        extra_check_result.error_message = ErrorMessageEnum.UNKNOWN

    # Cleanup and data saving
    # Start by saving any logs
    finally:
        logs: str
        if container:
            try:
                logs = container.logs(stream=False, timestamps=False).decode()
                container.remove(v=False)
            except docker.errors.APIError:
                logs = "Could not retrieve logs"
        else:
            logs = "Container error"

        extra_check_result.log_file.save(submission_uuid, content=ContentFile(logs), save=False)

    # Zip and save any possible artifacts
    memory_zip = io.BytesIO()
    if os.listdir(artifacts_directory):
        with zipfile.ZipFile(memory_zip, 'w') as zip:
            for root, _, files in os.walk(artifacts_directory):
                for file in files:
                    zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), artifacts_directory))

    memory_zip.seek(0)
    extra_check_result.artifact.save(submission_uuid, ContentFile(memory_zip.read()), False)

    extra_check_result.save()

    # Remove directory
    try:
        shutil.rmtree(submission_directory)
    except Exception:
        pass

    # Release
    extra_check_result.submission.running_checks = False

    return True
