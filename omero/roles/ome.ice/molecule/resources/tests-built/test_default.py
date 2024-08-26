import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('binary', [
    'glacier2router',
    'icegridadmin',
    'icegridnode',
])
def test_ice_version(host, binary):
    assert host.exists('icegridnode')
    c = host.run('icegridnode --version')
    assert c.rc == 0
    assert c.stderr.startswith('3.6.5')
