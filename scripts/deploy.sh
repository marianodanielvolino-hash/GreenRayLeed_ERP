#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker is not installed." >&2; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "ERROR: Docker Compose v2 is required." >&2; exit 1; }

if [[ ! -f fch_ops/pyproject.toml ]]; then
  bash scripts/bootstrap-source.sh
fi

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env. Set DB_PASSWORD and ADMIN_PASSWORD, then run deploy again." >&2
  exit 2
fi

getenv() { awk -F= -v key="$1" '$1==key {sub(/^[^=]*=/, ""); print; exit}' .env; }
DB_PASSWORD_VALUE="$(getenv DB_PASSWORD)"
ADMIN_PASSWORD_VALUE="$(getenv ADMIN_PASSWORD)"
[[ -n "$DB_PASSWORD_VALUE" ]] || { echo "ERROR: DB_PASSWORD is empty." >&2; exit 2; }
[[ -n "$ADMIN_PASSWORD_VALUE" ]] || { echo "ERROR: ADMIN_PASSWORD is empty." >&2; exit 2; }

bash scripts/validate.sh

echo "Building GreenRay ERP image..."
docker compose build --pull

echo "Starting GreenRay ERP..."
docker compose up -d --remove-orphans

docker compose ps

PORT="$(getenv HTTP_PORT)"
PORT="${PORT:-8080}"
printf '\nGreenRay ERP started at http://localhost:%s\n' "$PORT"
printf 'Verify the create-site container completed and run bench list-apps before production use.\n'
