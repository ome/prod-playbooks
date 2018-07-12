import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize("address", [
    "http://localhost/",
    "https://localhost/",
])
def test_web(Command, address):
    out = Command.check_output('curl -k %s' % address)
    assert '<title>Home | Open Microscopy Environment (OME)</title>' in out
