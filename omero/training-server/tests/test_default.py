import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
OMERO_LOGIN = '-C -s localhost -u root -w omero'


@pytest.mark.parametrize("name", [
    'nginx',
    'omero-server',
    'omero-web',
    'postgresql-9.6',
    'prometheus-node-exporter',
    'prometheus-omero-exporter',
    'prometheus-postgres-exporter',
])
def test_service_running_and_enabled(Service, name):
    service = Service(name)
    assert service.is_running
    assert service.is_enabled


def test_omero_login(Command, Sudo):
    with Sudo('fm1'):
        Command.check_output(
            '/opt/omero/server/OMERO.server/bin/omero '
            'login -C -s localhost -u root -w omero')


@pytest.mark.parametrize("curl", [
    'localhost:9449/metrics',
    '-u monitoring:monitoring localhost/metrics/9449',
])
def test_omero_metrics(Command, curl):
    out = Command.check_output('curl -f %s' % curl)
    assert 'omero_sessions_active' in out


def test_omero_metrics_auth_fail(Command):
    out = Command(
        'curl -f -u monitoring:incorrect localhost/metrics/9449')
    assert out.rc == 22
    assert '401' in out.stderr
