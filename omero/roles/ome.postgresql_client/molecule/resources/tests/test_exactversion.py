import testinfra.utils.ansible_runner
import os

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('exactversion')


def test_psql_version(host):
    out = host.check_output('psql --version')
    assert out == 'psql (PostgreSQL) 12.11'
