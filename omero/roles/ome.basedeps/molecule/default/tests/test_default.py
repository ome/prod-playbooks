import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "package", ["curl", "patch", "rsync", "tar", "unzip", "wget", "zip"]
)
def test_command(host, package):
    assert host.exists(package)
