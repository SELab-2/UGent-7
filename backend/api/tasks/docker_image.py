import docker
import docker.errors
from api.logic.get_file_path import get_docker_image_tag
from api.models.docker import DockerImage, StateEnum
from celery import shared_task
from notifications.signals import NotificationType, notification_create
from ypovoli.settings import MEDIA_ROOT


@shared_task
def task_docker_image_build(docker_image: DockerImage):
    # Set state
    docker_image.state = StateEnum.BUILDING
    docker_image.save()

    notification_type = NotificationType.DOCKER_IMAGE_BUILD_SUCCESS

    # Build the image
    try:
        client = docker.from_env()
        client.images.build(path=MEDIA_ROOT, dockerfile=docker_image.file.path,
                            tag=get_docker_image_tag(docker_image), rm=True, quiet=True, forcerm=True)
        docker_image.state = StateEnum.READY
    except (docker.errors.BuildError, docker.errors.APIError):
        docker_image.state = StateEnum.ERROR
        notification_type = NotificationType.DOCKER_IMAGE_BUILD_ERROR
    finally:
        # Update the state
        docker_image.save()

        # Send notification
        notification_create.send(
            sender=DockerImage,
            type=notification_type,
            queryset=[docker_image.owner],
            arguments={"name": docker_image.name},
        )


@shared_task
def task_docker_image_remove(docker_image: DockerImage):
    try:
        client = docker.from_env()
        client.images.remove(get_docker_image_tag(docker_image))
    except docker.errors.APIError:
        pass
