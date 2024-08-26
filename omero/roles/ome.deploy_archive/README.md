Deploy Archive
==============

[![Actions Status](https://github.com/ome/ansible-role-deploy-archive/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-deploy-archive/actions)
[![Ansible Role](https://img.shields.io/badge/ansible--galaxy-deploy_archive-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/ome/deploy_archive/)

Deploys an archive.
Downloads, extracts and optionally creates a symlink.


Prerequisites
-------------

This role does not install tools such as `unzip` or `bzip` that may be required for extracting archives.

This role does not set `become: yes` on tasks. If you do not include this in your playbook you must ensure the Ansible user has write permissions on the destination directory.


Role Variables
--------------

Required:
- `deploy_archive_dest_dir`: The destination directory, will be automatically created
- `deploy_archive_src_url`: URL to the archive

Optional:
- `deploy_archive_sha256`: SHA256 checksum, ignored if empty
- `deploy_archive_filename`: Name of the downloaded file, default is the basename of the URL path.
- `deploy_archive_symlink`: Absolute path of a symlink to the unarchived deployment, ignored if empty
- `deploy_archive_internal_root`: Target of the symlink within the destination directory
- `deploy_archive_notifies`: List of handlers to notify if the downloaded archive changes


Example playbook
----------------

See [`playbook.yml`](molecule/default/playbook.yml)


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
