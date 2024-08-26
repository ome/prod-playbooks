import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_selinux_custom_policy(host):
    out = host.check_output('semodule -l')
    assert 'django' in out
