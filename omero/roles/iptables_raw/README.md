Iptables Raw
============

[![Actions Status](https://github.com/ome/ansible-role-iptables-raw/workflows/Molecule/badge.svg)](https://github.com/ome/ansible-role-iptables-raw/actions)
[![Ansible Role](https://img.shields.io/badge/ansible--galaxy-iptables_raw-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/ome/iptables_raw/)

Import the Iptables Raw library and make it available as a task.
Ensure iptables is active.

See these links for full documentation on the `iptables_raw` module:
- https://nordeus.com/blog/engineering/managing-iptables-with-ansible-the-easy-way/
- https://github.com/Nordeus/ansible_iptables_raw
- https://github.com/ansible/ansible/pull/21054


Parameters
----------

Optional:
- `iptables_raw_disable_firewalld`: Disable the firewalld service (if installed and enabled it will conflict), default `True`


Development
-----------
The [`library/iptables_raw.py`](library/iptables_raw.py) version is https://github.com/Nordeus/ansible_iptables_raw/tree/34672590224f393016ad086f82054319108e67ad (2018-02-18) with the following change to prevent ansible-lint/flake8 failing:

```diff
diff --git a/library/iptables_raw.py b/library/iptables_raw.py
index 71dfc0d..978a6c7 100644
--- a/library/iptables_raw.py
+++ b/library/iptables_raw.py
@@ -344,7 +344,7 @@ class Iptables:
     def _is_debian(self):
         return os.path.isfile('/etc/debian_version')

-    # If /etc/arch-release exist, this means this is an ArchLinux OS
+    # If /etc/arch-release exist, this means this is an ArchLinux OS
     def _is_arch_linux(self):
         return os.path.isfile('/etc/arch-release')

```


Example Playbook
----------------

    - hosts: localhost
      roles:
        - role: ome.iptables-raw

      tasks:
        # Block all incoming connections apart from ssh
        - ome.iptables_raw:
            name: test_rules
            keep_unmanaged: no
            rules: |
              -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
              -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
              -A INPUT -j REJECT
              -A FORWARD -j REJECT
              -A OUTPUT -j ACCEPT
            state: present


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
