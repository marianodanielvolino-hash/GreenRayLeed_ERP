#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
import json, pathlib, sys
root = pathlib.Path('.')
errors = []

for p in root.rglob('*.json'):
    try:
        json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'{p}: JSON: {exc}')

for p in root.rglob('*.py'):
    if '__pycache__' in p.parts:
        continue
    try:
        compile(p.read_text(encoding='utf-8'), str(p), 'exec')
    except Exception as exc:
        errors.append(f'{p}: PY: {exc}')

if list(root.rglob('__pycache__')) or list(root.rglob('*.pyc')):
    errors.append('Compiled Python artifacts must not be committed.')

required = [
    'Dockerfile', 'compose.yaml', '.env.example',
    'fch_ops/pyproject.toml', 'fch_ops/fch_ops/hooks.py',
    'fch_ops/fch_ops/fch_ops/doctype/fch_import_charge/fch_import_charge.json',
    'fch_ops/fch_ops/fch_ops/doctype/fch_import_receipt/fch_import_receipt.json',
]
for path in required:
    if not (root / path).exists():
        errors.append(f'Missing required file: {path}')

compose = (root / 'compose.yaml').read_text(encoding='utf-8')
if 'build:' not in compose or 'ERPNEXT_VERSION' not in compose:
    errors.append('compose.yaml must build the custom GreenRay image with ERPNEXT_VERSION.')

dockerfile = (root / 'Dockerfile').read_text(encoding='utf-8')
if 'v16.32.0' not in dockerfile:
    errors.append('Dockerfile must pin ERPNext v16.32.0.')

hooks = (root / 'fch_ops/fch_ops/hooks.py').read_text(encoding='utf-8')
if 'fch_import_operation.js' not in hooks:
    errors.append('Import Operation client integration is missing from hooks.py.')

doctype_dir = root / 'fch_ops/fch_ops/fch_ops/doctype'
custom_names = set()
custom_json = []
for p in doctype_dir.glob('*/*.json'):
    data = json.loads(p.read_text(encoding='utf-8'))
    custom_names.add(data.get('name'))
    custom_json.append((p, data))
for p, data in custom_json:
    for field in data.get('fields', []):
        if field.get('fieldtype') in {'Link', 'Table'} and str(field.get('options','')).startswith('FCH '):
            if field['options'] not in custom_names:
                errors.append(f'{p}: missing custom DocType referenced by {field["fieldname"]}: {field["options"]}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('Static validation: OK')
PY

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  docker compose --env-file .env.example config >/dev/null
  echo "Docker Compose validation: OK"
else
  echo "Docker unavailable: skipped docker compose runtime validation"
fi
