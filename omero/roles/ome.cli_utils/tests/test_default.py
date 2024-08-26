import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_analysis_packages(Package):
    assert Package('bzip2')
    assert Package('zsh')
    assert Package('screen')
    assert Package('tmux')
