from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path('/opt/greenray/GreenRayLeed_ERP')
os.chdir(ROOT)


def run(args: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(args, check=True, text=True, capture_output=capture)
    return result.stdout.strip() if capture else ''


def read_env() -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in (ROOT / '.env').read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        values[key.strip()] = value.strip()
    return values


env = read_env()
site = env.get('SITE_NAME', '')
if not site:
    raise SystemExit('SITE_NAME is missing')
bucket = os.environ.get('OCI_BACKUP_BUCKET', 'greenray-erp-backups')
namespace = run([
    'oci', 'os', 'ns', 'get', '--auth', 'instance_principal',
    '--query', 'data', '--raw-output'
], capture=True)

run(['docker', 'compose', 'exec', '-T', 'backend', 'bench', '--site', site,
     'backup', '--with-files', '--compress'])

with tempfile.NamedTemporaryFile(suffix='.tgz') as archive:
    command = (
        f'tar -C sites/{site}/private/backups -czf - .'
    )
    with open(archive.name, 'wb') as target:
        subprocess.run(
            ['docker', 'compose', 'exec', '-T', 'backend', 'bash', '-lc', command],
            check=True, stdout=target
        )
    slot = datetime.now(timezone.utc).isoweekday()
    object_name = f'backups/{site}/day-{slot}.tgz'
    run([
        'oci', 'os', 'object', 'put', '--auth', 'instance_principal',
        '--namespace-name', namespace, '--bucket-name', bucket,
        '--name', object_name, '--file', archive.name, '--force'
    ])
