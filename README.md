OME production services playbooks
=================================

These playbooks encapsulate the running of various production servers run by the OME team.

At the moment, only the `ome-demoserver.yml` playbook is available here. This is a playbook for OMERO.demo server on https://demo.openmicroscopy.org OMERO.server and OMERO.web. You can read more about this [OMERO.demo server on our website](https://www.openmicroscopy.org/explore/).

We are in the process of adding more OME team's production playbooks here.

If you are looking for examples of running your own production OMERO.server see

  https://github.com/ome/omero-deployment-examples


Details
-------

- Install `Ansible` >2.10
- Install required roles: `ansible-galaxy install -r requirements.yml`
- Run the `ome-demoserver.yml` playbook:

```
cd omero
ansible-playbook --ask-become --become -i $PATH/TO/INVENTORY ome-demoserver.yml -l $YOUR-HOST-ADDRESS-OR-IP --diff
```



Testing
-------

We test the playbooks here on Rocky Linux 9 platform via [Ansible Molecule](https://molecule.readthedocs.io/), see test scenarios under [`molecule`](molecule).

The main components of the playbooks (roles) are being independently tested on both Rocky Linux 9 and Ubuntu 22.04. See e.g. [ome.omero_server role](https://github.com/ome/ansible-role-omero-server/tree/master/molecule).
