Postgresql Client
=================

[![Actions Status](https://github.com/ome/ansible-role-postgresql-client/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-postgresql-client/actions)
[![Ansible Role](https://img.shields.io/badge/ansible--galaxy-postgresql_client-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/ome/postgresql_client/)

Install PostgreSQL clients from the upstream distribution.

If you wish to use your distributions packages do not use this role.


Role Variables
--------------

Required:

- `postgresql_version`: The PostgreSQL major version, e.g. `11`, `12`, `13`, `14`, `15`, `16`

Optional:
- `postgresql_package_version`: The PostgreSQL full version, ignored on Ubuntu, e.g. `12.11`


Example Playbook
----------------

    # Simple example relying on the default Postgres PUBLIC privileges
    # which allow access to all users
    - hosts: localhost
      roles:
      - role: ome.postgresql_client
        postgresql_version: "12"


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
