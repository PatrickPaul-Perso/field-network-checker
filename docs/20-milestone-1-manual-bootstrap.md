# Milestone 1, Manual Bootstrap Summary

## Purpose

This milestone established the minimum host-side foundation required to continue building Field Network Checker, or FNC.

The goal of this phase was to:

- boot a clean Raspberry Pi OS system
- gain remote access over SSH
- install the minimum host tools needed to manage the rest of the platform
- prepare a self-contained project structure for source control, Ansible, Docker, and documentation

This phase intentionally stopped before configuring the local access point, the containerized web application, or the data capture workflow.

## Current Status

The Raspberry Pi was successfully:

- written with Raspberry Pi OS Lite 64-bit
- booted on a normal physical network
- reached over SSH using the local account `fnc`
- prepared with the minimum packages needed for local automation and container deployment

The temporary Docker validation artifacts created by the `hello-world` test were also removed afterward.

## Manual Steps Completed

### 1. Wrote the OS image

The SD card was written using Raspberry Pi Imager with a minimal configuration.

Configured during imaging:

- username: `fnc`
- initial password: set during imaging
- SSH: enabled
- Wi-Fi client settings: left blank

This kept the first boot simple and avoided preconfiguring network behavior that will later be managed by the project itself.

### 2. Booted the Raspberry Pi on a normal Ethernet network

For the first startup, the Raspberry Pi was connected to a standard local network through its physical Ethernet port.

This provided:

- DHCP address assignment
- easy SSH access
- a clean environment for the initial bootstrap

### 3. Connected over SSH

The Raspberry Pi was accessed remotely using the initial local account.

Example login form:

    ssh fnc@<ip-address>

### 4. Installed the minimum host packages

The first host packages installed were:

- `git`
- `ansible`
- `ca-certificates`
- `curl`
- `tree`

These provide the minimum support needed to:

- clone and manage the project repository
- run Ansible locally on `localhost`
- add external package repositories safely
- inspect the project directory structure during setup

### 5. Installed Docker Engine from the official Docker repository

The host was prepared for containerized application deployment using Docker Engine and the Docker Compose plugin.

Installed components:

- `docker-ce`
- `docker-ce-cli`
- `containerd.io`
- `docker-buildx-plugin`
- `docker-compose-plugin`

This gives the project a lightweight and reproducible application runtime while keeping host responsibilities limited.

### 6. Validated Docker installation

A basic Docker validation was performed using the `hello-world` image.

After confirming that Docker worked correctly, the temporary validation image and container were removed. This kept the host tidy and avoided leaving non-project runtime artifacts behind.

### 7. Created the local project structure

A self-contained project root was created under:

    /opt/field-network-checker

The initial folder structure includes:

    /opt/field-network-checker/
    ├── ansible/
    │   ├── inventory/
    │   ├── group_vars/
    │   └── roles/
    │       ├── base/
    │       │   └── tasks/
    │       ├── docker/
    │       │   └── tasks/
    │       ├── network_ap/
    │       │   └── tasks/
    │       └── app/
    │           └── tasks/
    ├── app/
    │   └── src/
    ├── bootstrap/
    ├── deploy/
    ├── docs/
    └── images/

This structure is designed to keep the solution self-contained and portfolio-friendly.

### 8. Prepared local Ansible execution

The project was set up so Ansible runs directly on the Raspberry Pi against `localhost`.

This avoids the need for a separate controller machine and keeps the repository self-contained.

The local inventory model is based on:

    localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3

### 9. Added the initial playbook structure

A top-level Ansible playbook was created to organize the project into clear functional roles:

- `base`
- `docker`
- `network_ap`
- `app`

At this stage, the `base` role contains the first actual task, which installs `tree` using an Ansible package list with a single element.

## Architecture at the End of Milestone 1

```mermaid
flowchart TD
    A[MicroSD with Raspberry Pi OS Lite 64-bit] --> B[Raspberry Pi 4 host]
    B --> C[SSH access as fnc]
    C --> D[Manual bootstrap]
    D --> E[Git installed on host]
    D --> F[Ansible installed on host]
    D --> G[Docker Engine installed on host]
    D --> H[Docker Compose plugin installed on host]
    D --> I[Project tree under /opt/field-network-checker]

    I --> J[docs]
    I --> K[ansible]
    I --> L[app]
    I --> M[deploy]
    I --> N[bootstrap]
    I --> O[images]

    K --> P[localhost inventory]
    K --> Q[site.yml]
    K --> R[roles]
    R --> S[base]
    R --> T[docker]
    R --> U[network_ap]
    R --> V[app]

    G -. validated with .-> W[hello-world test]
    W -. removed after validation .-> X[Clean host state]
```

## Host Responsibilities Defined So Far

The host currently owns only the minimum required responsibilities:

- operating system
- SSH access
- Git repository checkout
- local Ansible execution
- Docker runtime
- future host-side wireless access point configuration

This remains aligned with the design goal of keeping the host minimal while moving most project logic into containers later.

## What Is Not Done Yet

The following items are still out of scope for this milestone:

- configuring `wlan0` as a local access point
- defining the host network profile for offline field use
- creating the containerized web application
- reading link and IP state from the field interface
- writing `records.jsonl`
- exporting CSV from JSONL
- adding an admin page
- archiving and reset actions

## Next Step

The next logical step is to continue with the Ansible roles in this order:

1. `base`
2. `docker`
3. `network_ap`
4. `app`

The immediate technical target is to move from a manually bootstrapped host to a reproducible local Ansible run that configures the remaining platform components.

## Notes

This milestone is intentionally simple.

The objective was not to build a finished product, but to establish a clean, reproducible base for the first working proof of concept.
