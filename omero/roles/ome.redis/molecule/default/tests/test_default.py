import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service_running_and_enabled(host):
    assert host.service('redis').is_running
    assert host.service('redis').is_enabled


def test_redis_config(host):
    assert host.file('/etc/redis/redis.conf').contains('bind 0.0.0.0')
