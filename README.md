# Field Network Checker

Field Network Checker, or FNC, is a simple tool to validate network ports and record metadata.

## Status

Proof of concept in active development.

## Overview

FNC is a small local-first field tool designed to test Ethernet wall jacks without relying on Internet access or external services.

The first proof of concept is built around a simple workflow:

- boot the device
- expose a local Wi-Fi access point
- connect to it from a phone or tablet
- plug the Ethernet interface into the wall jack under test
- view live link and IP information in a local web page
- record metadata annotations and save the result locally in JSONL format

## Problem Statement

Validating physical network ports in the field often depends on improvised methods, handwritten notes, and unreliable connectivity. FNC aims to provide a self-contained workflow for testing a jack, observing network status, and saving structured field notes locally.

## Project Goals

- keep the host operating system minimal
- keep the build and deployment process reproducible
- keep the field workflow fully local
- prefer containers for the application layer
- store records in a durable structured format
- document the full build process from a clean OS image
- keep the solution simple enough for a first proof of concept

## Non-Goals for the First Iteration

- no cloud dependency during field collection
- no Microsoft 365 integration
- no external database
- no advanced multi-user features
- no production-grade hardening
- no complex orchestration

## Planned Technical Direction

The first working version will document and implement:

- target hardware platform
- base operating system choice
- host responsibilities
- container responsibilities
- local Wi-Fi access point setup
- minimal web application scope
- JSONL journal format
- local Ansible execution on localhost
- bootstrap and rebuild workflow

Detailed platform and architecture notes will be documented in the `docs/` folder.

## Expected Workflow

1. Boot the device
2. Join the local FNC Wi-Fi network from a phone
3. Open the local web interface
4. Plug the Ethernet port into a wall jack
5. Observe link state and DHCP result
6. Enter the wall jack label and optional notes
7. Save the record locally
8. Export the data after the field session

## Data Model

The primary journal format is JSONL.

Each saved record is expected to include fields such as:

- timestamp
- probe_id
- boot_id
- wall_label
- note
- city
- campus
- building
- eth_link
- ip
- dhcp_ok

The exact schema will be defined in project documentation.

## Repository Structure

Planned repository layout:

    field-network-checker/
    ├── README.md
    ├── LICENSE
    ├── NOTICE
    ├── docs/
    ├── bootstrap/
    ├── ansible/
    ├── app/
    ├── deploy/
    └── images/

## Documentation Plan

The repository will include documentation for:

- project scope
- architecture
- bootstrap steps
- runbook
- design decisions

## Build and Deployment Plan

The intended build process is:

- start from a clean Raspberry Pi OS image
- perform a minimal bootstrap on the host
- clone this repository
- run Ansible locally on `localhost`
- configure host network components
- build and start the application container
- validate the local field workflow

## Initial Host Bootstrap

The initial bootstrap is intentionally minimal.

Write the OS image with Raspberry Pi Imager, then enable SSH and set the initial local account during imaging.

Current initial user:

    fnc

After first boot, connect the device to a normal Ethernet network, then log in over SSH and continue the setup from the repository.

Example:

    ssh fnc@<ip-address>

## Current Milestones

### Milestone 1

- repository skeleton
- initial documentation
- local Ansible bootstrap
- host access point setup
- single application container
- JSONL record writing
- basic web interface

### Milestone 2

- admin page
- CSV export from JSONL
- archive and reset actions
- improved field metadata handling

## Why This Project Matters

This project demonstrates practical work across:

- Linux systems
- networking
- offline-first workflow design
- lightweight containerized application packaging
- Ansible automation
- documentation and reproducibility
- field-oriented problem solving

## Screenshots and Demo

This section will be populated once the first working proof of concept is running.

## License

This project is licensed under the Apache License 2.0.
