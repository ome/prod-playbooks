import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dir(host):
    f = host.file('/opt/deploy-archive-test/idr.openmicroscopy.org-IDR-0.5.0')
    assert f.exists
    assert f.is_directory


def test_file(host):
    f = host.file(
        '/opt/deploy-archive-test/idr.openmicroscopy.org-IDR-0.5.0/index.html')
    assert f.exists
    assert f.is_file


def test_symlink(host):
    f = host.file('/opt/idr-web-src')
    assert f.exists
    assert f.is_symlink
    assert f.linked_to == (
        '/opt/deploy-archive-test/idr.openmicroscopy.org-IDR-0.5.0')


def test_handler_trigger_once(host):
    f = host.file('/opt/deploy-archive-test/handler-triggered')
    assert f.content.strip() == b'triggered'
