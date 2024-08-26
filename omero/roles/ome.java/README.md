Java
====

[![Actions Status](https://github.com/ome/ansible-role-java/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-java/actions)
[![Ansible Role](https://img.shields.io/badge/ansible--galaxy-java-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/ome/java/)

Install Java JREs and optionally JDKs.


Role Variables
--------------

Optional variables:
- `java_versions`: A list of Java versions to install, default `["8"]`,
  versions other than `"8"` and `"11"` may work but are not supported
- `java_jdk_install`: If `True` install JDKs corresponding to the JRE versions, default `False`


Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: ome.java }


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk

License
-------

BSD
