import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("package", ["bzip2", "screen", "tmux", "zsh"])
def test_analysis_packages(host, package):
    assert host.package(package).is_installed
