import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

DOWNLOADS_URL = "/uod/idr/www/downloads.openmicroscopy.org"
DOCS_URL = "/uod/idr/www/docs.openmicroscopy.org"


@pytest.mark.parametrize('base_folder', [DOWNLOADS_URL, DOCS_URL])
def test_permissions(host, base_folder):
    v = host.ansible.get_variables()
    assert not host.file('%s/component/%s/.htaccess' % (
        base_folder, v['version'])).exists

    f = host.file('%s/component/%s' % (base_folder, v['version']))
    assert f.exists
    assert f.user == 'root'
    assert oct(f.mode) == '01555'


@pytest.mark.parametrize('base_folder', [DOWNLOADS_URL, DOCS_URL])
def test_symlinks(host, base_folder):
    v = host.ansible.get_variables()
    f = host.file('%s/component/3.2' % base_folder)
    assert f.is_symlink
    assert f.linked_to == '%s/component/%s' % (base_folder, v['version'])
    f = host.file('%s/component/3' % base_folder)
    assert f.is_symlink
    assert f.linked_to == '%s/component/%s' % (base_folder, v['version'])
    f = host.file('%s/component/latest' % base_folder)
    assert f.is_symlink
    assert f.linked_to == '%s/component/%s' % (base_folder, v['version'])
