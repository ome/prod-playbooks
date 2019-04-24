import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service_running_and_enabled(Service):
    assert Service('postgresql-9.6').is_running
    assert Service('postgresql-9.6').is_enabled


def test_dbs(Command):
    out = Command.check_output(
        'PGPASSWORD=idr-redmine psql -hlocalhost -Uidr-redmine -l -tA')
    assert 'idr-redmine|idr-redmine|UTF8|' in out
