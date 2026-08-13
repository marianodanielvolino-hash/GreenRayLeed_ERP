#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example. Fill DB_PASSWORD and ADMIN_PASSWORD before deploying."
  exit 2
fi
if grep -Eq '^(DB_PASSWORD|ADMIN_PASSWORD)=$' .env; then
  echo "ERROR: DB_PASSWORD or ADMIN_PASSWORD is empty." >&2
  exit 2
fi

./scripts/validate.sh
docker compose build --pull
docker compose up -d
docker compose ps
