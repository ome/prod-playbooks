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
def test_redirects(host, base_folder):
    v = host.ansible.get_variables()
    hostname = host.backend.get_hostname()
    f = host.file('%s/component/3.2/.htaccess' % base_folder)
    if hostname == 'release':
        assert f.exists
        assert f.content == (
            'Redirect 301 /component/3.2 /component/%s' % v['version'])
    elif hostname == 'prelease':
        assert not f.exists
    f = host.file('%s/component/3/.htaccess' % base_folder)
    assert f.exists
    if hostname == 'release':
        assert f.content == (
            'Redirect 301 /component/3 /component/%s' % v['version'])
    elif hostname == 'prelease':
        assert f.content == 'Redirect 301 /component/3 /component/3.1.8'
    f = host.file('%s/component/latest/.htaccess' % base_folder)
    assert f.exists
    if hostname == 'release':
        assert f.content == (
            'Redirect 301 /component/latest /component/%s' % v['version'])
    elif hostname == 'prelease':
        assert f.content == 'Redirect 301 /component/latest /component/3.1.8'
