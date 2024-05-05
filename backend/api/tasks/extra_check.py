from typing import cast

import docker
import docker.errors
from api.logic.get_file_path import (get_docker_image_tag,
                                     get_extra_check_file_full_path,
                                     get_submission_full_dir_path)
from api.models.docker import StateEnum as DockerStateEnum
from api.models.submission import ErrorMessageEnum, ExtraCheckResult, StateEnum
from celery import shared_task
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

        return False

    # Start the process
    extra_check_result.result = StateEnum.RUNNING
    extra_check_result.save()

    # Check if the docker image is ready
    if extra_check_result.extra_check.docker_image.state != DockerStateEnum.READY:
        extra_check_result.result = StateEnum.FAILED
        extra_check_result.error_message = ErrorMessageEnum.DOCKER_IMAGE_ERROR
        extra_check_result.save()

        return True

    container: Container | None = None

    try:
        # Get docker client
        client: docker.DockerClient = docker.from_env()
        # Get the name of the extra check file
        extra_check_name = extra_check_result.extra_check.file.name.split("/")[-1]

        # Create and run container
        container = cast(Container, client.containers.run(
            image=get_docker_image_tag(extra_check_result.extra_check.docker_image),
            command=f"bash {extra_check_name}",
            detach=True,
            log_config=LogConfig(type=LogConfig.types.JSON, config={"max-size": "50kb"}),
            mem_limit=f"{extra_check_result.extra_check.memory_limit}m",
            privileged=False,
            remove=False,  # Don't remove yet as we need the logs first
            stdout=True,
            stderr=True,
            volumes={
                get_submission_full_dir_path(extra_check_result.submission): {
                    "bind": "/submission", "mode": "rw"
                },
                get_extra_check_file_full_path(extra_check_result.extra_check, extra_check_name): {
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
    finally:
        logs: str = "Could not retrieve logs"
        if container:
            try:
                logs = container.logs(stream=False, timestamps=False).decode()
                container.remove(v=False)
            except docker.errors.APIError:
                pass

        extra_check_result.log_file.save("logs.txt", content=ContentFile(logs), save=False)
        extra_check_result.save()

    return True
