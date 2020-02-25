import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_services_running_and_enabled(host):
    assert host.service('jupyterhub').is_running
    assert host.service('jupyterhub').is_enabled


def test_tmplogin(host):
    out = host.check_output(
        'curl --dump-header - -k https://localhost/training/hub/tmplogin')
    assert 'location: /training/hub/spawn' in out

# TODO: check notebook container runs after login
