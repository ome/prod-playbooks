import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service_running_and_enabled(host):
    assert host.service('postgresql-9.6').is_running
    assert host.service('postgresql-9.6').is_enabled


def test_dbs(host):
    out = host.check_output(
        'PGPASSWORD=idr-redmine psql -hlocalhost -Uidr-redmine -l -tA')
    assert 'idr-redmine|idr-redmine|UTF8|' in out
