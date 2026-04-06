#!/usr/bin/env bash
set -euo pipefail

cd /opt/field-network-checker/ansible
sudo ansible-playbook -i inventory/localhost.ini site.yml
