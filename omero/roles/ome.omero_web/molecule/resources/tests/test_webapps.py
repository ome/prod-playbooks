import os
import json
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

OMERO = '/opt/omero/web/OMERO.web/bin/omero'


def assert_jcfg(host, key, value, isjson):
    with host.sudo('omero-web'):
        cfg = host.check_output("%s config get %s", OMERO, key)
    if isjson:
        cfg = json.loads(cfg)
    assert cfg == value


@pytest.mark.parametrize("key,value", [
    ('example.string', 'example value'),
])
#    ('example.boolean', True),
#    ('example.integer', 2),
def test_example_config(host, key, value):
    assert_jcfg(host, key, value, False)


def test_omero_web_apps(host):
    assert_jcfg(host, 'omero.web.apps', ["omero_mapr"], True)


def test_omero_web_mapr_config(host):
    expected = [
        {
            "menu": "gene", "config": {
                "default": ["Gene Symbol"],
                "case_sensitive": True,
                "all": ["Gene Symbol", "Gene Identifier"],
                "ns": ["openmicroscopy.org/mapr/gene"],
                "label": "Gene"
            }
        },
        {
            "menu": "genesupplementary",
            "config": {
                "default": [],
                "all": [],
                "ns": ["openmicroscopy.org/mapr/gene/supplementary"],
                "label": "Gene supplementary"
            }
        }
    ]
    assert_jcfg(host, 'omero.web.mapr.config', expected, True)


def test_omero_web_ui_toplinks(host):
    expected = [
        [
            "Data",
            "webindex",
            {"title": "Browse Data via Projects, Tags etc"}
        ],
        [
            "History",
            "history",
            {"title": "History"}
        ],
        [
            "Help",
            "https://help.openmicroscopy.org/",
            {"target": "new", "title": "Open OMERO user guide in a new tab"}
        ],
        [
            "OMERO",
            {
                "query_string": {"experimenter": -1},
                "viewname": "webindex"
            },
            {"title": "Image Data Repository"}
        ],
        [
            "Genes",
            {
                "query_string": {"experimenter": -1},
                "viewname": "maprindex_gene"
            },
            {"title": "Genes browser"}
        ]
    ]
    assert_jcfg(host, 'omero.web.ui.top_links', expected, True)


def test_mapr_config(host):
    config = {
        'gene': {
            'all': ['Gene Symbol', 'Gene Identifier'],
            'case_sensitive': True,
            'default': ['Gene Symbol'],
            'label': 'Gene',
            'ns': ['openmicroscopy.org/mapr/gene']},
        'genesupplementary': {
            'all': [],
            'default': [],
            'label': 'Gene supplementary',
            'ns': ['openmicroscopy.org/mapr/gene/supplementary']}
         }
    out = host.check_output('curl -L http://localhost/mapr/api/config/')
    assert json.loads(out) == config
