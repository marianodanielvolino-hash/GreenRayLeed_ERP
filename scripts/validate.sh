#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f fch_ops/pyproject.toml ] || ./scripts/bootstrap-source.sh
if command -v docker >/dev/null 2>&1; then
  docker compose --env-file .env.example config >/dev/null
  echo "Docker Compose validation: OK"
else
  echo "Docker not installed: compose validation skipped"
fi
