#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
EXPECTED="83421d3f46ae8fee650f2c808f17927a39fff7208384db79e4a4250212f90a7b"
BUNDLE_DIR="bootstrap/v040"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

parts=("$BUNDLE_DIR"/fch_ops_v040.part*.txt)
[[ -e "${parts[0]}" ]] || { echo "ERROR: fch_ops v0.4 source bundle is missing." >&2; exit 1; }
cat "${parts[@]}" | base64 --decode > "$TMP"
ACTUAL="$(sha256sum "$TMP" | awk '{print $1}')"
[[ "$ACTUAL" == "$EXPECTED" ]] || {
  echo "ERROR: fch_ops source checksum mismatch: $ACTUAL" >&2
  exit 1
}
rm -rf fch_ops
tar -xzf "$TMP" -C "$ROOT"
[[ -f fch_ops/pyproject.toml ]] || { echo "ERROR: reconstructed fch_ops is incomplete." >&2; exit 1; }
echo "fch_ops v0.4.0 reconstructed and checksum verified."
