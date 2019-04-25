import os
import re
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_services_running_and_enabled(Service):
    assert Service('jupyterhub').is_running
    assert Service('jupyterhub').is_enabled


def test_tmplogin(host):
    out = host.check_output(
        'curl --dump-header - -k https://localhost/training/hub/tmplogin')
    pattern = re.compile(
        r'location: /training/user/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')
    assert any(pattern.search(line) for line in out.splitlines())


# TODO: check notebook container runs after login
