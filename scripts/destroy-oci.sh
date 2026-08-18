#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../terraform"
terraform plan -destroy -out=destroy.tfplan
echo "Review the destroy plan above. To execute it run: terraform apply destroy.tfplan"
