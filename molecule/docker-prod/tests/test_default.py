import json
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_targets(host):
    out = host.check_output(
        'curl -k -f --user admin:monitoring '
        'https://localhost/prometheus/api/v1/targets')
    d = json.loads(out)
    assert d['status'] == 'success'
    assert d['data']['droppedTargets'] == []
    unique_instances = set(
        t['labels']['instance'] for t in d['data']['activeTargets'])
    assert len({
        'node.example.org:443',
        'pg.example.org:443',
        'omeroserver.example.org:443',
        'omeroweb.example.org:443',
        'idr.openmicroscopy.org:443',
        'idr1.openmicroscopy.org:443',
        'idr2.openmicroscopy.org:443',
        'localhost:9090',
    }.difference(unique_instances)) == 0
