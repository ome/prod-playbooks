import testinfra.utils.ansible_runner
import os

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_psql_version(host):
    variables = host.ansible.get_variables()
    version = variables["postgresql_version"]
    out = host.check_output('psql --version')
    assert out.startswith('psql (PostgreSQL) {}.'.format(version))
