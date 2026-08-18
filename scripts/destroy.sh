#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/terraform"
terraform plan -destroy -out=destroy.tfplan
echo "Review destroy.tfplan before running: terraform apply destroy.tfplan"
