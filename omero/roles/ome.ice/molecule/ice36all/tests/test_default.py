import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ice_version(host):
    assert host.exists('icegridnode')
    c = host.run('icegridnode --version')
    assert c.rc == 0
    assert c.stderr.startswith('3.6.')


def test_icepy_version(host):
    c = host.run('python -c "import Ice; print (Ice.stringVersion())"')
    assert c.stdout.startswith('3.6.')


def test_ice_devel(host):
    assert not host.package('ice-all-devel').is_installed
