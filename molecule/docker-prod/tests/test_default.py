import json
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_targets(host):
    out = host.check_output('curl -f http://localhost:9090/api/v1/targets')
    d = json.loads(out)
    assert d['status'] == 'success'
    assert d['data']['droppedTargets'] == []
    unique_instances = set(
        t['labels']['instance'] for t in d['data']['activeTargets'])
    assert unique_instances == {
        'idr-analysis.openmicroscopy.org:443',
        'idr.openmicroscopy.org:443',
        'idr1.openmicroscopy.org:443',
        'idr2.openmicroscopy.org:443',
        'localhost:9090',
        'ns-web-pub.openmicroscopy.org:443',
        'ns-web.openmicroscopy.org:443',
        'ome-demoserver.openmicroscopy.org:443',
        'ome-dockr-prod1.openmicroscopy.org:9090',
        'ome-dockr-prod1.openmicroscopy.org:9100',
        'ome-dundeeomero.openmicroscopy.org:443',
        'outreach.openmicroscopy.org:443',
        'pub-omero.openmicroscopy.org:443',
        'workshop.openmicroscopy.org:443',
    }