#!/usr/bin/env bash
set -euo pipefail
ROOT=/opt/greenray/GreenRayLeed_ERP
cd "$ROOT"
[[ -f .env ]] || exit 0
SITE=$(awk -F= '$1=="SITE_NAME" {print $2; exit}' .env)
[[ -n "$SITE" ]] || exit 0
BUCKET=${OCI_BACKUP_BUCKET:-greenray-erp-backups}
NAMESPACE=$(oci os ns get --auth instance_principal --query data --raw-output)

docker compose exec -T backend bench --site "$SITE" backup --with-files --compress
TMP=$(mktemp --suffix=.tgz)
trap 'rm -f "$TMP"' EXIT
docker compose exec -T backend bash -lc "tar -C sites/$SITE/private/backups -czf - ." > "$TMP"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
oci os object put --auth instance_principal --namespace-name "$NAMESPACE" --bucket-name "$BUCKET" --name "backups/$SITE/$STAMP.tgz" --file "$TMP" --force
docker compose exec -T backend bash -lc "find sites/$SITE/private/backups -type f -mtime +2 -delete"
