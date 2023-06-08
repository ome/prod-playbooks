# Test redirects
#
# Test the default host:
#   pytest check_redirects.py
#
# Test a different host:
#   HOST=http://www-dev.openmicroscopy.org pytest check_redirects.py

import os
import pytest
import requests

HOST_OME = os.getenv('HOST', 'https://ome-www.openmicroscopy.org')
HOST_OPENMICROSCOPY = os.getenv('HOST', 'https://www.openmicroscopy.org')
hosts = (HOST_OME, HOST_OPENMICROSCOPY)
suffixes = ['', '/']
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
    ('/site/community/minutes/meetings/10th-annual-users-meeting-june-2015', '/events/10th-annual-users-meeting-june-2015.html'),# noqa
    ('/site/community/minutes/meetings/9th-annual-users-meeting-june-2014', '/events/9th-annual-users-meeting-june-2014.html'),# noqa
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
external_uris = [
    ('/omero-blog', 'http://blog.openmicroscopy.org'),
    ('/site/about/development-teams/glencoe-software', 'https://www.glencoesoftware.com/team.html'),# noqa
    ('/site/community/scripts', 'https://docs.openmicroscopy.org/latest/omero/developers/scripts/index.html'),# noqa
    ('/site/support/bio-formats', 'https://docs.openmicroscopy.org/latest/bio-formats/'),# noqa
    ('/site/support/bio-formats5', 'https://docs.openmicroscopy.org/latest/bio-formats5/'),# noqa
    ('/site/support/bio-formats5.3', 'https://docs.openmicroscopy.org/latest/bio-formats5.3/'),# noqa
    ('/site/support/bio-formats5.4', 'https://docs.openmicroscopy.org/latest/bio-formats5.4/'),# noqa
    ('/site/support/bio-formats5.5', 'https://docs.openmicroscopy.org/latest/bio-formats5.5/'),# noqa
    ('/site/support/omero', 'https://docs.openmicroscopy.org/latest/omero/'),# noqa
    ('/site/support/omero5', 'https://docs.openmicroscopy.org/latest/omero5/'),# noqa
    ('/site/support/omero5.0', 'https://docs.openmicroscopy.org/latest/omero5.0/'),# noqa
    ('/site/support/omero5.1', 'https://docs.openmicroscopy.org/latest/omero5.1/'),# noqa
    ('/site/support/omero5.2', 'https://docs.openmicroscopy.org/latest/omero5.2/'),# noqa
    ('/site/support/omero5.3', 'https://docs.openmicroscopy.org/latest/omero5.3/'),# noqa
    ('/site/support/ome-model', 'https://docs.openmicroscopy.org/latest/ome-model/'),# noqa
    ('/site/support/file-formats', 'https://docs.openmicroscopy.org/latest/ome-model/'),# noqa
    ('/site/support/file-formats/schemas/specifications/compliant-file-specification', 'https://docs.openmicroscopy.org/latest/ome-model/specifications/'),# noqa
    ('/site/support/ome-tiff', 'https://docs.openmicroscopy.org/latest/ome-model/ome-tiff/'),# noqa
    ('/site/support/ome-files-cpp', 'https://docs.openmicroscopy.org/latest/ome-files-cpp/'),# noqa
    ('/site/support/contributing', 'https://docs.openmicroscopy.org/contributing/'),# noqa
    ('/site/support/previous', 'https://docs.openmicroscopy.org'),
    ('/info/OMERO.insight', 'https://docs.openmicroscopy.org/latest/omero/users/index.html'),# noqa
    ('/info/OMERO.importer', 'https://docs.openmicroscopy.org/latest/omero/users/index.html'),# noqa
    ('/info/OMERO.editor', 'https://docs.openmicroscopy.org/latest/omero/users/index.html'),# noqa
    ('/info/OMERO.web', 'https://docs.openmicroscopy.org/latest/omero/users/index.html'),# noqa
    ('/info/OMERO.server', 'https://docs.openmicroscopy.org/latest/omero/users/index.html'),# noqa
    ('/info/permissions', 'https://docs.openmicroscopy.org/latest/omero/sysadmins/server-permissions.html'),# noqa
    ('/info/demo', 'http://help.openmicroscopy.org/demo-server.html'),
    ('/info/lists', 'http://lists.openmicroscopy.org.uk/mailman/listinfo/'),
    ('/info/videos', 'https://www.youtube.com/channel/UCyySB9ZzNi8aBGYqcxSrauQ'),# noqa
    ('/info/downgrade', 'https://docs.openmicroscopy.org/latest/omero/developers/Model/XsltTransformations.html'),# noqa
    ('/info/flimfit', 'http://flimfit.org'),# noqa
    ('/info/scripts', 'https://docs.openmicroscopy.org/latest/omero/developers/scripts/index.html'),# noqa
    ('/info/bio-formats', 'https://docs.openmicroscopy.org/latest/bio-formats/'),# noqa
    ('/info/slidebook', 'https://www.intelligent-imaging.com/technical-answers'),# noqa
]
content_uris = [
    ('/community', 'This page was generated by phpBB'),
    ('/community/ucp.php?mode=login', ' Login</title>'),
    ('/community/viewtopic.php?f=6&t=8319',
     'UserId issues from Matlab.</title>'),
    ('/community/viewtopic.php?f=11&t=8320',
     'View topic - Release of Bio-Formats 5.5.3</title>'),
    ('/community/viewtopic.php?p=18303#p18303',
     '<div id="p18303" class="post bg1">'),
    ('/community/index.php', 'Index page</title>'),

    ('/Schemas', 'Open Microscopy Environment Schemas</title>'),
    ('/Schemas/ROI', 'Open Microscopy Environment ROI Schemas</title>'),
    ('/Schemas/broken-link', 'Open Microscopy Environment Schemas</title>'),

    ('/qa2', '<strong>OMERO.qa</strong>  provides support services'),
    ('/qa2/qa/feedback/17777', '<a href="/qa2/qa/feedback/">Go back</a>'),
    ('/qa2/qa/upload', 'Uploading sample images'),
    ('/qa2/qa/feedback/?status=1',
        'If you cannot view feedback you previously submitted'),
    ('/qa2/registry/demo_account', 'Requesting a demo server account'),
    ('/qa2/registry/statistic', 'File statistics.'),
]
content_uris_no_slash = [
    ('/Schemas/OME/2016-06/ome.xsd', 'Schema June 2016'),
    ('/Schemas/OME/2015-01/ome.xsd', 'Schema January 2015'),
    ('/Schemas/ROI/2015-01/ROI.xsd', 'Region of Interest'),
    ('/XMLschemas/OME/FC/ome.xsd', 'The OME element is a container'),
    ('/XMLschemas/CA/RC1/CA.xsd',
        'Conforms to w3c http://www.w3.org/2001/XMLSchema'),
    ('/XMLschemas/STD/RC2/STD.xsd', 'Defines a semantic type'),
]


# Based on
# https://github.com/openmicroscopy/prod-playbooks/blob/master/www/playbook.yml
@pytest.mark.parametrize('host', hosts)
@pytest.mark.parametrize('uri,expect', redirect_uris)
@pytest.mark.parametrize("suffix", suffixes)
def test_redirect_with_slash(host, uri, expect, suffix):
    r = requests.head('%s%s%s' % (host, uri, suffix))
    assert r.is_redirect
    assert r.headers['Location'] == '%s%s' % (host, expect)


@pytest.mark.parametrize('host', hosts)
@pytest.mark.parametrize('uri,expect', external_uris)
@pytest.mark.parametrize("suffix", suffixes)
def test_redirect_external(host, uri, expect, suffix):
    r = requests.head('%s%s%s' % (host, uri, suffix))
    assert r.is_redirect
    assert r.headers['Location'] == expect


@pytest.mark.parametrize('host', hosts)
def test_404(host):
    uri = '/non-existent/path'
    r = requests.head('%s%s' % (host, uri))
    assert r.status_code == 404


@pytest.mark.parametrize('host', hosts)
@pytest.mark.parametrize('uri,content', content_uris)
@pytest.mark.parametrize('suffix', suffixes)
def test_content(host, uri, content, suffix):
    r = requests.get('%s%s%s' % (host, uri, suffix))
    assert content in r.text


@pytest.mark.parametrize('host', hosts)
@pytest.mark.parametrize('uri,content', content_uris_no_slash)
def test_content_no_slash(host, uri, content):
    r = requests.get('%s%s' % (host, uri))
    assert content in r.text
