import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# The behaviour of this test depends on whether it's running with a docker
# container or full VM
def test_selinux_utils(host):
    # We could do this by having separate test_files, but by keeping it
    # in one we can guarantee we always match one of the test conditions
    hostname = host.backend.get_hostname()

    if hostname == 'selinux-utils-docker':
        assert not host.exists('/usr/sbin/getenforce')
        assert not host.package('policycoreutils-python').is_installed
    else:
        getenforce = host.check_output('/usr/sbin/getenforce')
        assert getenforce == 'Enforcing'
        assert host.package('policycoreutils-python').is_installed
