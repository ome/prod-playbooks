import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


OMERO = '/opt/omero/web/OMERO.web/bin/omero'
# Need to match 5.6.dev2
# VERSION_PATTERN = re.compile('(\d+)\.(\d+)\.(\d+)-ice36-')
VERSION_PATTERN = re.compile(r'(\d+)\.(\d+)\.(\w+)')


def test_omero_web_config(host):
    with host.sudo('omero-web'):
        cfg = host.check_output("%s config get omero.web.server_list" % OMERO)
    assert cfg == '[["localhost", 12345, "molecule-test"]]'

    with host.sudo('omero-web'):
        keys = host.check_output("%s config keys" % OMERO)
    assert sorted(keys.split()) == [
        'example.boolean',
        'example.integer',
        'example.string',
        'omero.web.apps',
        'omero.web.mapr.config',
        'omero.web.server_list',
        'omero.web.ui.top_links',
    ]


def test_omero_version(host):
    with host.sudo('omero-web'):
        ver = host.check_output("%s version" % OMERO)
    m = VERSION_PATTERN.match(ver)
    assert m is not None
    assert int(m.group(1)) >= 5
    assert int(m.group(2)) > 3
