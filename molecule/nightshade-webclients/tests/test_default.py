import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
OMERO_LOGIN = '-C -s localhost -u root -w omero'


@pytest.mark.parametrize("name", [
    'nginx',
    'omero-web',
    'prometheus-node-exporter',
])
def test_service_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_running
    assert service.is_enabled


def test_omero_metrics(host):
    out = host.check_output(
        'curl -f -u monitoring:monitoring -k '
        'https://localhost/django_prometheus/metrics')
    assert "django_http_responses_body_total_bytes_count" in out


def test_omero_metrics_auth_fail(host):
    out = host.run(
        'curl -f -u monitoring:incorrect -k '
        'https://localhost/django_prometheus/metrics')
    assert out.rc == 22
    assert '401' in out.stderr


def test_omero_nginx_ssl(host):
    out = host.check_output('curl -fkI https://localhost/')
    assert 'Location: /webclient/' in out
