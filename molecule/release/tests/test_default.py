import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

DOWNLOADS_URL = "/uod/idr/www/downloads.openmicroscopy.org"
DOCS_URL = "/uod/idr/www/docs.openmicroscopy.org"


@pytest.mark.parametrize('base_folder', [DOWNLOADS_URL, DOCS_URL])
def test_htaccess(host, base_folder):
    assert not host.file('%s/component/3.2.10/.htaccess' % base_folder).exists


@pytest.mark.parametrize('base_folder', [DOWNLOADS_URL, DOCS_URL])
def test_permissions(host, base_folder):
    f = host.file('%s/component/3.2.10' % base_folder)
    assert f.exists
    assert f.user == 'root'
    assert oct(f.mode) == '01555'


@pytest.mark.parametrize('base_folder', [DOWNLOADS_URL, DOCS_URL])
def test_symlinks(host, base_folder):
    f = host.file('%s/component/3.2' % base_folder)
    assert f.is_symlink
    assert f.linked_to == '%s/component/3.2.10' % base_folder
    f = host.file('%s/component/3' % base_folder)
    assert f.is_symlink
    assert f.linked_to == '%s/component/3.2.10' % base_folder
    f = host.file('%s/component/latest' % base_folder)
    assert f.is_symlink
    assert f.linked_to == '%s/component/3.2.10' % base_folder
