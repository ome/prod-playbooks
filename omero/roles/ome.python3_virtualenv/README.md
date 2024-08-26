Python3 Virtualenv
==================

[![Actions Status](https://github.com/ome/ansible-role-python3-virtualenv/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-python3-virtualenv/actions)
[![Ansible Role](https://img.shields.io/badge/ansible--galaxy-python3_virtualenv-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/ome/python3_virtualenv/)

Install Python3 virtualenv dependencies and a wrapper script for the Ansible `pip` module.

There are multiple ways of creating Python virtualenvs including `virtualenv`, `python3 -mvenv`, but these may take different parameters.
In some situations, particularly if `ansible_python_interpreter` is set, the Ansible `pip` modules pass unrecognised parameters.
This role installs a wrapper script `/usr/local/bin/ome-python3-virtualenv` should work in all cases.


The compatibility with Python 2 has been removed in version 0.2.0.

Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk

License
-------

BSD
