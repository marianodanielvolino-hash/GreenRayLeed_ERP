#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ "$(uname -m)" == "aarch64" ]] || { echo "ARM64 required"; exit 1; }
[[ -f .env ]] || { echo "Create .env first"; exit 2; }
set -a; source .env; set +a
: "${SITE_NAME:?}" "${DB_PASSWORD:?}" "${ADMIN_PASSWORD:?}" "${PUBLIC_HOSTNAME:?}" "${ACME_EMAIL:?}"
bash scripts/bootstrap-source.sh
bash scripts/validate.sh
TAG=${GREENRAY_TAG:-oci-arm64}
docker build -f Dockerfile.oci -t "greenray-erp:$TAG" .
docker compose -f compose.yaml -f compose.https.yaml up -d --no-build --remove-orphans
for i in $(seq 1 60); do
  docker compose exec -T backend bench --site "$SITE_NAME" list-apps >/tmp/gr-apps 2>/dev/null && break
  sleep 5
done
for app in hrms crm fch_ops; do
  grep -qx "$app" /tmp/gr-apps || docker compose exec -T backend bench --site "$SITE_NAME" install-app "$app"
done
docker compose exec -T backend bench --site "$SITE_NAME" migrate
echo "https://$PUBLIC_HOSTNAME"
