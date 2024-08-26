OME production services playbooks
=================================

**NOTE: We are in the process of migration of the playbooks in this repo to Rocky Linux 9/RHEL 9 OS but at the moment, they function only on CentOS 7 !!**
These playbooks encapsulate the running of various production servers run by the OME team.
If you are looking for examples of running your own production OMERO.server see

  https://github.com/ome/omero-deployment-examples


Details
-------

- Install `Ansible` >2.10.
- Install required roles: `ansible-galaxy install -r requirements.yml`
- Run the [`site.yml` playbook](site.yml).

For details of individual playbooks see the comments in [`site.yml`](site.yml).

Testing
-------

All server playbooks have a corresponding [molecule](https://molecule.readthedocs.io/) test scenario under [`molecule`](molecule).
