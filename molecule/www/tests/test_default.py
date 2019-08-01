import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("address", [
    "http://localhost/",
    "https://localhost/",
])
def test_web(host, address):
    out = host.check_output('curl -k %s' % address)
    assert '<title>Home | Open Microscopy Environment (OME)</title>' in out


def test_archived_community(host):
    out = host.check_output('curl -kL https://localhost/community')
    assert 'Powered by <a href="http://www.phpbb.com/">phpBB</a>' in out

    out = host.check_output('curl -kIL https://localhost/community')
    assert 'Set-Cookie: phpbb' not in out
