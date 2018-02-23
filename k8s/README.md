# OME kubernetes suport playbooks

## `bootstrap`

Provisioning tasks intended to be run once when provisioning a new system.
This includes networking configuration.


## `prerequisites`

These tasks should be run before a Kubernetes cluster is promoted to production use.
It should be safe to re-run these playbooks at any time.


## `postgres`

An standalone PostgreSQL server for use by Kubernetes applications.
