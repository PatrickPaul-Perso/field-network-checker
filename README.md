<p align="center">
  <img src="docs/assets/images/IMG_3571.jpg" alt="Field Network Checker prototype" width="360">
</p>

# Field Network Checker

Field Network Checker is a local-first tool for validating unknown Ethernet ports in the field and capturing port metadata at the time of testing.

## Why this project exists

In buildings with mixed network environments, a live wall port does not tell you enough on its own. Staff need a fast way to answer a few practical questions on site:

- Is the link up or down?
- Did DHCP assign an address?
- Does the assigned address match the target legacy network pattern?
- What room and port did I test?

This project turns those checks into a small, direct workflow with immediate visual feedback and local record capture.

## What it does

- Monitors live Ethernet status
- Shows link down, link up with no IP, link up on a non-target network, and link up on the target legacy network
- Highlights target-network detection from the assigned IP
- Captures site, room, telecom room, and port number
- Saves records locally and exports JSONL for later consolidation

## Why local-first matters

The tool is designed for field work. It stays useful even before any central system integration. It gives the technician an immediate answer at the wall jack, then preserves the metadata for later import or reporting.

## Interface preview

### Link down
<img src="docs/assets/images/link_down.JPG" alt="Link down" width="320">

### Link up, no IP yet
<img src="docs/assets/images/link_up_no_ip.JPG" alt="Link up no IP" width="320">

### Link up, non-target network
<img src="docs/assets/images/link_up_private_ip.JPG" alt="Link up private IP" width="320">

### Link up, target legacy network
<img src="docs/assets/images/link_up_legacy_ip.JPG" alt="Link up on legacy IP" width="320">

## Public project page

[Open the Field Network Checker project page](https://patrickpaul-perso.github.io/field-network-checker/)

## Current implementation status

The repository now includes the main pieces needed for a host-managed proof of concept on Raspberry Pi:

- Ansible roles for `base`, `docker`, `network_ap`, and `app`
- a Docker Compose deployment for the Flask application
- local data and config directories for persistent records and defaults
- unit tests for core app behavior

The `app` role is intended to create the runtime directories, seed the default config when missing, and start `fnc-app` with Docker Compose on the host.

## Host deployment notes

The intended host model is:

- Raspberry Pi OS on the device
- local Ansible execution against `localhost`
- NetworkManager-managed hotspot setup for the field access point
- Docker Compose for the web app runtime

The main host-side playbook is [ansible/site.yml](/workspaces/field-network-checker/ansible/site.yml), and the current app deployment tasks live in [ansible/roles/app/tasks/main.yml](/workspaces/field-network-checker/ansible/roles/app/tasks/main.yml).

## Host test flow

These are the main commands intended for validation on the Raspberry Pi host:

```bash
ansible-playbook ansible/site.yml --syntax-check
ansible-playbook ansible/site.yml --tags app
docker compose -f deploy/compose.yaml ps
docker logs fnc-app --tail 50
curl http://192.168.50.1:8080/api/status
```

These commands are documented as the intended host-side validation flow only.

## Status

Prototype and presentation-ready proof of concept.
