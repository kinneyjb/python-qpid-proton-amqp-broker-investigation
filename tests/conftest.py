import pytest
import yaml
from os.path import basename, dirname, abspath
import docker
from docker import DockerClient
from typing import Generator, Tuple, Optional
from time import sleep


@pytest.fixture
def docker_client() -> DockerClient:
    return docker.from_env()


@pytest.fixture
def activemq_broker(docker_client):
    containers = run_broker(docker_client, 'activemq')
    sleep(20)
    yield containers
    for container in containers:
        container.kill()


@pytest.fixture
def artemis_broker(docker_client):
    containers = run_broker(docker_client, 'artemis')
    yield containers
    for container in containers:
        container.kill()


@pytest.fixture
def rabbitmq_broker(docker_client):
    containers = run_broker(docker_client, 'rabbitmq')
    yield containers
    for container in containers:
        container.kill()


def run_broker(docker_client, name):
    docker_compose_path = abspath(f'./brokers/{name}/docker-compose.yml')
    build_images(docker_client, load_build_configs(docker_compose_path))
    containers = run_containers(docker_client, load_deploy_configs(docker_compose_path))
    return containers



def load_build_configs(
        docker_compose_path: str
) -> Generator[Tuple[str, dict], None, None]:

    with open(docker_compose_path) as stream:
        compose = yaml.load(stream)

    for name, service in compose['services'].items():
        yield name, dict(
            path=dirname(docker_compose_path),
            tag=service['image'],
            rm=True
        )


def load_deploy_configs(
        docker_compose_path: str
) -> Generator[Tuple[str, dict], None, None]:

    with open(docker_compose_path) as stream:
        compose = yaml.load(stream)

    def unpack_ports() -> Optional[dict]:
        if 'ports' not in service:
            return None
        return {
            key: value
            for key, value in
            [attr.split(":") for attr in service['ports']]
        }

    def unpack_volumes() -> Optional[dict]:
        if 'volumes' not in service:
            return None
        basedir = dirname(docker_compose_path)

        return {
            abspath(f'{basedir}/{key}'): dict(bind=value, mode='rw')
            for key, value in
            [attr.split(":") for attr in service['volumes']]
        }

    for name, service in compose['services'].items():
        yield name, dict(
            detach=True,
            remove=True,
            image=service['image'],
            ports=unpack_ports(),
            volumes=unpack_volumes()
        )


def build_images(
        docker_client: DockerClient,
        build_configs: Generator[Tuple[str, dict], None, None]
):
    for name, build_config in build_configs:
       image, logs = docker_client.images.build(**build_config)


def run_containers(
        docker_client: DockerClient,
        deploy_configs: Generator[Tuple[str, dict], None, None]
):
    containers = []
    for name, deploy_config in deploy_configs:
        image = deploy_config.pop('image')
        container = docker_client.containers.run(image, **deploy_config)
        containers.append(container)

    return containers
