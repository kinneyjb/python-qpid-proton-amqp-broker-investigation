import pytest
from os.path import abspath
from tests.conftest import (
    load_build_configs,
    load_deploy_configs,
    build_images,
    run_containers
)


@pytest.mark.parametrize('docker_compose_path', [
    abspath('./brokers/activemq/docker-compose.yml'),
    abspath('./brokers/rabbitmq/docker-compose.yml'),
    abspath('./brokers/artemis/docker-compose.yml'),
])
def test_load(docker_compose_path):
    for name, config in load_build_configs(docker_compose_path):
        print(name, config)

    for name, config in load_deploy_configs(docker_compose_path):
        print(name, config)


@pytest.mark.parametrize('docker_compose_path', [
    abspath('./brokers/activemq/docker-compose.yml'),
    abspath('./brokers/rabbitmq/docker-compose.yml'),
    abspath('./brokers/artemis/docker-compose.yml'),
])
def test_build(docker_client, docker_compose_path):
    build_images(docker_client,
                 load_build_configs(docker_compose_path))

