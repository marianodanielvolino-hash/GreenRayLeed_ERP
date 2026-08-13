# Deployment

## Local / UAT

Prerequisites: Docker Engine 23+ and Docker Compose v2.

```bash
cp .env.example .env
# Edit .env and replace CHANGE_ME values
./scripts/validate.sh
./scripts/deploy.sh
```

Open `http://localhost:8080` (or the port configured in `.env`).

## What the deployment does

The stack starts MariaDB, Redis, Frappe backend, websocket, workers, scheduler and nginx frontend. A one-shot `create-site` service creates the configured site only if it does not already exist, installs ERPNext and `fch_ops`, runs migrations and sets the default site.

The deployment is idempotent and preserves Docker named volumes.

## Update

```bash
git pull
./scripts/deploy.sh
```

The app is built into the custom image. Site migrations run during the one-shot setup step.

## Stop without deleting data

```bash
docker compose stop
```

## Destructive reset

Do not run this in production without a verified backup:

```bash
docker compose down -v
```

## Production notes

For internet-facing production add TLS/reverse proxy, external backups, monitoring, secret management and a tested disaster-recovery process. Fiscal/e-invoicing setup remains country-specific and requires local accountant validation before go-live.
