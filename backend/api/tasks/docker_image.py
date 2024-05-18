import docker
import docker.errors
from api.logic.get_file_path import get_docker_image_tag
from api.models.docker import DockerImage, StateEnum
from celery import shared_task
from ypovoli.settings import MEDIA_ROOT


@shared_task
def task_docker_image_build(docker_image: DockerImage):
    # Set state
    docker_image.state = StateEnum.BUILDING
    docker_image.save()

    # Build the image
    try:
        client = docker.from_env()
        client.images.build(path=MEDIA_ROOT, dockerfile=docker_image.file.path,
                            tag=get_docker_image_tag(docker_image), rm=True, quiet=True, forcerm=True)
        docker_image.state = StateEnum.READY
    except (docker.errors.APIError, docker.errors.BuildError, TypeError):
        docker_image.state = StateEnum.ERROR
        # TODO: Sent notification

    # Update the state
    docker_image.save()


@shared_task
def task_docker_image_remove(docker_image: DockerImage):
    try:
        client = docker.from_env()
        client.images.remove(get_docker_image_tag(docker_image))
    except docker.errors.APIError:
        pass
