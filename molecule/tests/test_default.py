import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
OMERO_LOGIN = '-C -s localhost -u root -w omero'


@pytest.mark.parametrize("name", [
    'nginx',
    'omero-server',
    'omero-web',
    'postgresql-16',
])
def test_service_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_running
    assert service.is_enabled


def test_omero_login(host):
    with host.sudo('omero-server'):
        host.check_output(
            '/opt/omero/server/OMERO.server/bin/omero '
            'login -C -s localhost -u root -w omero')


def test_omero_nginx_ssl(host):
    out = host.check_output('curl -fkI https://localhost/')
    assert 'Location: /webclient/' in out
