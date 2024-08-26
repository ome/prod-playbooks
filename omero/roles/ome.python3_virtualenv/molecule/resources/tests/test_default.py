import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_virtualenv(host):
    venv = '/opt/test/python3-virtualenv'
    host.check_output(venv + '/bin/python --version').startswith('Python 3.')
    host.check_output(venv + '/bin/pip --version').startswith('Python 3.')
    assert host.file(venv + '/bin/python').is_file
    assert host.file(venv + '/bin/python3').is_file
    assert host.file(venv + '/bin/pip').is_file
    assert host.file(venv + '/bin/pip3').is_file
    packages = host.check_output(venv + '/bin/pip freeze')
    assert 'omego==' in packages
    assert 'scc==' in packages
