import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("name", ["omero-web", "nginx"])
def test_services_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_running
    assert service.is_enabled


def test_nginx_gateway(host):
    out = host.check_output('curl -L localhost')
    assert 'OMERO.web - Login' in out


def test_omero_web_config_applied(host):
    out = host.check_output('curl -L localhost')
    assert 'molecule-test:12345' in out
