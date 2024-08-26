OMERO Web
=========

[![Actions Status](https://github.com/ome/ansible-role-omero-web/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-omero-web/actions)
[![Ansible Role](https://img.shields.io/badge/ansible--galaxy-omero_web-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/ome/omero_web/)

Installs and configures OMERO.web and Nginx.
Uses a conf.d style configuration directory for managing the OMERO.web configuration.

**Warning:** Python 2 support is dropped.
See [`CHANGES.md`](./CHANGES.md) for details.


Role Variables
--------------

All variables are optional, see `defaults/main.yml` for the full list

OMERO.web version and installation.
- `omero_web_release`: The OMERO.web release, e.g. `5.9.1`.
  The default is `present` which will install the latest version if web is not already installed, but will not modify an existing web.
  Use `latest` to automatically upgrade when a new version is released.
- `omero_web_system_user`: OMERO.web system user, default `omero-web`.
- `omero_web_system_uid`: OMERO.web system user ID (default automatic)

OMERO.web configuration.
- `omero_web_config_set`: A dictionary of `config-key: value` which will be used for the initial OMERO.web configuration, default empty.
  `value` can be a string, or an object (list, dictionary) that will be automatically converted to quoted JSON.
  Note configuration can also be done pre/post installation using the `web/config` conf.d style directory.
- `omero_web_setup_nginx`: Install and configure Nginx, default `True`.

OMERO.web systemd configuration
- `omero_web_systemd_setup`: Create and start the `omero-web` systemd service, default `True`
- `omero_web_systemd_limit_nofile`: Systemd limit for number of open files (default ignore)
- `omero_web_systemd_after`: A list of strings with additional service names to appear in systemd unit file "After" statements. Default empty/none.
- `omero_web_systemd_requires`: A list of strings with additional service names to appear in systemd unit file "Requires" statements. Default empty/none.

Python 3 only parameters.
- `omero_web_python_addons`: List of additional Python packages to be installed into virtualenv

The [omero-web-apps](https://galaxy.ansible.com/ome/omero_web_apps) role has been merged into this role for Python 3 deployments.
All variables are optional:
- `omero_web_apps_names`: List of web application names to be appended to `omero.web.apps`
- `omero_web_apps_packages`: List of pip installable packages
- `omero_web_apps_top_links`: Lists of top link dictionaries to be appended to `omero.web.ui.top_links`, of the form:
  - `label`: Label
  - `link`: URL or a dict
  - `attrs`: Dictionary of attributes (optional)
- `omero_web_apps_ui_metadata_panes`: Items to be appended to `omero.web.ui.metadata_panes`
- `omero_web_apps_config_append`: Dictionary of other key-[list of values] pairs to be appended (multiple values can be appended to the same key)
- `omero_web_apps_config_set`: Dictionary of other key-value pairs to be set
- `omero_web_apps_config_name`: The basename of the configuration file (`web/config/{{ omero_web_apps_config_name }}.omero`)



Unstable features
-----------------

Variables :
- `omero_web_systemd_start`: Automatically enable and start/restart systemd omero-web service, default `True`.
  This is intended for use in server images where installation may be separate from configuration and execution.
- `omero_web_always_reset_config`: Clear the existing configuration before regenerating, default `True`.

It should be safe to use this role to deploy OMERO.web inside a standard `centos:7` Docker container without systemd (`omero_web_systemd_setup: False`).



Configuring OMERO.web
---------------------

This role regenerates the OMERO.web configuration file using the configuration files and helper script in `/opt/omero/web/config`.
`omero_web_config_set` can be used for simple configurations, for anything more complex consider creating one or more configuration files under: `/opt/omero/web/config/` with the extension `.omero`.

Manual configuration changes (`omero config ...`) will be lost following a restart of `omero-web` with systemd, you can disable this by setting `omero_web_always_reset_config: False`.
Manual configuration changes will never be copied during an upgrade.

See https://github.com/ome/design/issues/70 for a proposal to add support for a conf.d style directory directly into OMERO.


Example Playbooks
-----------------

OMERO.web with the default backend server, `localhost:4064`:

    - hosts: localhost
      roles:
        - role: ome.omero_web

OMERO.web with a custom configuration using `omero_web_config_set`:

    - hosts: localhost
      roles:
        - role: ome.omero_web
          omero_web_config_set:
            omero.web.server_list:
              - [omero.example.org, 4064, omero-example]
            omero.web.public.enabled: True
            omero.web.public.server_id: 1
            omero.web.public.user: public
            omero.web.public.password: secret-password

OMERO.web with the redis session engine    
   
    hosts: localhost    
    roles:
    - role: ome.omero_web
      omero_web_setup_redis_session: true
      omero_web_config_set:
        "omero.web.caches":
           "default": 
              "BACKEND": "django_redis.cache.RedisCache"
              "LOCATION": "redis://127.0.0.1:6379/0"
        "omero.web.session_engine": "django.contrib.sessions.backends.cache"

OMERO.web with a custom configuration using a configuration file `web-custom-config.omero`:

    - hosts: localhost
      roles:
        - role: ome.omero_web
      tasks:
        - copy:
            content: >
              config set omero.web.server_list '[["omero.example.org", 4064, "omero-example"]'
            dest: /opt/omero/web/config/web-custom-config.omero
          notify:
            - restart omero-web


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
