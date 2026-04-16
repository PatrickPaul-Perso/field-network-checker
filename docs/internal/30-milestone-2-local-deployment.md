# Milestone 2, Local Deployment and Runtime Bring-Up

## Purpose

This milestone moves Field Network Checker from a manually bootstrapped host foundation to a locally deployable field runtime.

The goal of this phase is to:

- configure the Raspberry Pi host with the remaining Ansible roles
- prepare the wireless access point profile used for field access
- deploy the Flask application with Docker Compose
- keep the app runtime local-first, with persistent config and record storage on the host

This phase focuses on deployment and bring-up. It does not attempt to redefine the Milestone 1 bootstrap process.

## Scope Added in This Milestone

The repository now contains the main implementation pieces required for local deployment:

- `ansible/roles/network_ap/tasks/main.yml`
- `ansible/roles/app/tasks/main.yml`
- `deploy/compose.yaml`
- `app/src/app.py`
- `config/config.json`
- `data/records.jsonl`

Together, these files define the host setup for the access point and the containerized web application.

## Host Model

The intended deployment model is:

- Raspberry Pi host running Raspberry Pi OS
- local Ansible execution against `localhost`
- Ansible invoked from the checked-out repository on the host
- Docker Engine and Docker Compose plugin installed on the host
- NetworkManager managing the access point connection
- Flask app running as `fnc-app` through Docker Compose
- persistent bind mounts for `/data` and `/config`

## App Deployment Role

The `app` role is responsible for:

- ensuring the staged runtime root exists at `/opt/field-network-checker`
- ensuring the runtime `data` directory exists
- ensuring the runtime `config` directory exists
- seeding `config.json` when it is missing
- confirming the source Docker Compose file is present in the checked-out repository
- building and running the app directly from the checked-out repository
- running `docker compose up -d --build fnc-app`

The role uses shared variables from `ansible/group_vars/all.yml` to keep a minimal host runtime tree under `/opt/field-network-checker` while running Docker Compose from the checked-out repository.

The intended privilege split is:

- run `ansible-playbook` from the checked-out repository as a regular user
- use privilege escalation only for host-level changes such as package install, service changes, NetworkManager configuration, and creating the runtime root under `/opt`
- keep the runtime tree owned by the invoking user
- keep only the runtime directories under `/opt/field-network-checker`
- run the Flask app container as a regular user, while preserving the `SYS_TIME` capability for time updates

## Access Point Role

The `network_ap` role configures a local hotspot profile using NetworkManager.

At a high level, it:

- installs the packages required for AP mode
- ensures NetworkManager is active
- derives an SSID from the wireless MAC address
- creates the hotspot profile when needed
- applies AP, IPv4, and security settings

This keeps the access point configuration on the host, while leaving the application itself inside the container runtime.

## Validation Intent

The intended host-side validation flow for this milestone is:

```bash
cd /path/to/field-network-checker
ansible-playbook ansible/site.yml --syntax-check
ansible-playbook ansible/site.yml --tags app
docker compose -f deploy/compose.yaml ps
docker logs fnc-app --tail 50
curl http://192.168.50.1:8080/api/status
```

These commands are recorded here as the expected Raspberry Pi validation path. The Ansible commands and Compose file stay in the repository checkout, while the app runtime data lives under `/opt/field-network-checker`.

## Outcome

At the end of this milestone, the project is no longer just a prepared host foundation.

It now has a defined path to:

- bring up the local field access point
- start the web application locally on the device
- retain persistent configuration and captured records

This establishes the first repo-defined deployment path for a usable field demonstration on the target hardware.
