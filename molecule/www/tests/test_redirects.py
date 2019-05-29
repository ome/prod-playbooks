import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

external_uris = [
    ('/forums', 'https://forum.image.sc/tags/ome'),
    ('/omero-blog', 'http://blog.openmicroscopy.org'),
    ('/site/about/development-teams/glencoe-software',
     'https://www.glencoesoftware.com/team.html'),
    ('/site/community/scripts',
     'https://docs.openmicroscopy.org/latest/omero/developers/'
     'scripts/index.html'),
    ('/site/support/bio-formats',
     'https://docs.openmicroscopy.org/latest/bio-formats/'),
    ('/site/support/omero',
     'https://docs.openmicroscopy.org/latest/omero/'),
    ('/site/support/ome-model',
     'https://docs.openmicroscopy.org/latest/ome-model/'),
    ('/site/support/file-formats',
     'https://docs.openmicroscopy.org/latest/ome-model/'),
    ('/site/support/file-formats/schemas/specifications/'
     'compliant-file-specification',
     'https://docs.openmicroscopy.org/latest/ome-model/specifications/'),
    ('/site/support/ome-tiff',
     'https://docs.openmicroscopy.org/latest/ome-model/ome-tiff/'),
    ('/site/support/ome-files-cpp',
     'https://docs.openmicroscopy.org/latest/ome-files-cpp/'),
    ('/site/support/contributing',
     'https://docs.openmicroscopy.org/contributing/'),
    ('/info/flimfit', 'http://flimfit.org'),
    ('/info/scripts',
     'https://docs.openmicroscopy.org/latest/omero/developers/'
     'scripts/index.html'),
    ('/info/bio-formats',
     'https://docs.openmicroscopy.org/latest/bio-formats/'),
    ('/info/slidebook',
     'https://www.intelligent-imaging.com/technical-answers'),
]

redirect_uris = [
    ('/site', '/'),
    ('/site/about', '/about'),
    ('/site/about/licensing', '/licensing'),
    ('/site/about/licensing-attribution', '/licensing'),
    ('/site/about/licensing-attribution/licensing', '/licensing'),
    ('/site/about/ome-contributors', '/contributors'),
    ('/site/about/partners', '/commercial-partners'),
    ('/site/about/development-teams', '/teams'),
    ('/site/about/publications', '/citing-ome'),
    ('/site/about/who-ome', '/teams'),
    ('/site/about/what-omero/overview', '/omero'),
    ('/site/about/roadmap', '/about'),
    ('/site/about/project-history', '/about'),

    ('/site/community', '/support'),
    ('/site/community/mailing-lists', '/support'),
    ('/site/events', '/events'),
    ('/site/community/minutes/conference-calls', '/on-the-web'),
    ('/site/community/minutes/meetings/12th-annual-users-meeting-2017',
     '/events/12th-annual-users-meeting-2017.html'),
    ('/site/community/minutes/meetings/11th-annual-users-meeting-2016',
     '/events/11th-annual-users-meeting-2016.html'),
    ('/site/community/minutes/meetings/10th-annual-users-meeting-june-2015',
     '/events/10th-annual-users-meeting-june-2015.html'),
    ('/site/community/minutes/meetings/9th-annual-users-meeting-june-2014',
     '/events/9th-annual-users-meeting-june-2014.html'),
    ('/site/community/jobs', '/careers'),

    ('/site/products', '/products'),
    ('/site/products/bio-formats', '/bio-formats'),
    ('/site/products/bio-formats/downloads', '/bio-formats/downloads/'),
    ('/site/products/omero', '/omero'),
    ('/site/products/omero/downloads', '/omero/downloads/'),
    ('/site/products/omero/feature-list', '/omero/features/'),
    ('/site/products/omero/secvuln', '/security/advisories/'),
    ('/site/products/ome5/secvuln', '/security/advisories/'),
    ('/site/products/omero/secvuln/2014-SV3-csrf',
     '/security/advisories/2014-SV3-csrf/'),

    ('/site/support', '/docs'),
    ('/site/support/ome-artwork', '/artwork'),
    ('/site/support/ome-artwork/artwork-usage', '/artwork'),
    ('/site/news', '/announcements'),

    ('/info/vulnerabilities', '/security/advisories/'),
    ('/info/vulnerabilities/2014-SV3-csrf',
     '/security/advisories/2014-SV3-csrf/'),
    ('/info/omero', '/omero'),
    ('/info/cls', '/omero/downloads/'),
    ('/info/download', '/omero/downloads/'),
    ('/info/downloads', '/omero/downloads/'),
    ('/info/attribution', '/licensing/'),
]


@pytest.mark.parametrize('path,redirect', redirect_uris)
def test_internal_redirects(host, path, redirect):
    out = host.check_output('curl -I http://localhost%s' % path)
    assert 'HTTP/1.1 302' in out
    assert 'Location: http://localhost%s' % redirect in out


@pytest.mark.parametrize('path,redirect', external_uris)
def test_external_redirects(host, path, redirect):
    out = host.check_output('curl -I http://localhost%s' % path)
    assert 'HTTP/1.1 302' in out
    assert 'Location: %s' % redirect in out
