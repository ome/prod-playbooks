import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')

external_redirect_uris = [
    ('/forums', 'https://forum.image.sc/tags/ome')
]


@pytest.mark.parametrize('path,redirect', external_redirect_uris)
def test_external_redirect(host, path, redirect):
    out = host.check_output('curl -k http://localhost/%s' % path)
    assert 'HTTP/1.1 302' in out
    assert 'Location: %s' % redirect in out
