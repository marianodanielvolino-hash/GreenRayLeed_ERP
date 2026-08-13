#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/terraform"

echo "=== WARNING: Destroying OCI Infrastructure for GreenRay ERP ==="
read -p "Are you sure you want to destroy all cloud resources? (y/N): " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
  terraform destroy -auto-approve
  echo "Infrastructure destroyed successfully."
else
  echo "Destroy cancelled."
fi
