OME production services playbooks
=================================

These playbooks encapsulate the running of various production servers run by the OME team.
If you are looking for examples of running your own production OMERO.server see

  https://github.com/ome/omero-deployment-examples


Details
-------

- Install `Ansible` and dependencies using the [ome-ansible-molecule package](https://pypi.org/project/ome-ansible-molecule/).
- Install required roles: `ansible-galaxy install -r requirements.yml`
- Run the [`site.yml` playbook](site.yml).

For details of individual playbooks see the comments in [`site.yml`](site.yml).

Testing
-------

All server playbooks have a corresponding [molecule](https://molecule.readthedocs.io/) test scenario under [`molecule`](molecule).
