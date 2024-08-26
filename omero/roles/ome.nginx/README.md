Nginx
=====

[![Actions Status](https://github.com/ome/ansible-role-nginx/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-nginx/actions)
[![Ansible Role](https://img.shields.io/badge/ansible--galaxy-nginx-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/ome/nginx/)

Install upstream Nginx.

TODO: Add configuration options.


Role Variables
--------------

- `nginx_keep_default_configs`: If `true` keep the default site configuration files in `nginx/conf.d`, default `false` (disable them)
- `nginx_stable_repo`: If `false` use the mainline instead of stable repo, default `true`
- `nginx_version`: The packaged version of Nginx, optional, available versions depends on `nginx_stable_repo`. Not supported on Ubuntu.
- `nginx_systemd_setup`: Start/restart nginx using systemd, default `true`
, if you want to manage Nginx yourself set this to `false`

Log rotation:

- `nginx_logrotate_interval`: Rotate log files at this interval, default `daily`
- `nginx_logrotate_backlog_size`: Number of backlog files to keep, default `366`


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
