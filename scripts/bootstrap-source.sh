#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -f fch_ops/pyproject.toml ]; then echo "fch_ops ready"; exit 0; fi
mkdir -p fch_ops/fch_ops
printf '%s\n' '[project]' 'name = "fch_ops"' 'dynamic = ["version"]' 'dependencies = []' '' '[build-system]' 'requires = ["flit_core >=3.4,<4"]' 'build-backend = "flit_core.buildapi"' > fch_ops/pyproject.toml
printf '%s\n' '__version__ = "0.1.0"' > fch_ops/fch_ops/__init__.py
printf '%s\n' 'app_name = "fch_ops"' 'app_title = "FCH Ops"' 'app_publisher = "GreenRay / FCH"' 'app_license = "GPL-3.0"' > fch_ops/fch_ops/hooks.py
printf '%s\n' 'FCH Ops' > fch_ops/fch_ops/modules.txt
: > fch_ops/fch_ops/patches.txt
echo "Minimal fch_ops source created. Continue from docs/BUILD_SPEC.md before deployment."
