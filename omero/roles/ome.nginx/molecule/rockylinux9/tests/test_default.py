import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_package(host):
    assert host.package('nginx').is_installed


def test_service(host):
    hostname = host.backend.get_hostname()
    service = host.service('nginx')
    if hostname == 'nginx-disabled':
        assert not service.is_running
    else:
        assert service.is_running


@pytest.mark.parametrize("configfile", ["example_ssl.conf", "default.conf"])
def test_configuration(host, configfile):
    c = host.file('/etc/nginx/conf.d/%s' % configfile)
    hostname = host.backend.get_hostname()
    if hostname != 'nginx-custom':
        assert (c.content_string ==
                "# This file is intentionally blank (Ansible)")


def test_logrotate(host):
    log = host.file("/etc/logrotate.d/nginx")
    hostname = host.backend.get_hostname()
    if hostname != 'nginx-custom':
        assert log.contains("daily")
        assert log.contains("rotate 366")
    else:
        assert log.contains("weekly")
        assert log.contains("rotate 5")


def test_version(host):
    hostname = host.backend.get_hostname()
    r = host.run('nginx -v')
    assert r.rc == 0
    ver = r.stderr.strip()
    if hostname == 'nginx-custom':
        assert ver == ('nginx version: nginx/1.20.2')
    else:
        assert ver.startswith('nginx version: nginx/1.24.0')


def test_nginx_configuration(host):
    c = host.file('/etc/nginx/nginx.conf')
    assert 'http {' in c.content_string
    assert 'server {' not in c.content_string
