---
title: Deploy GreenRay ERP
description: Validate, build, deploy and verify the GreenRay ERP Docker stack without destroying persistent data.
---

# /deploy-greenray

1. Read `AGENTS.md`, `docs/DEPLOYMENT.md`, `.env.example`, `compose.yaml`, and the `fch_ops` install hooks.
2. Verify Docker Engine and Docker Compose v2 are available.
3. If `.env` is missing, copy `.env.example` to `.env` and stop before deployment if any `CHANGE_ME_` values remain.
4. Run `./scripts/validate.sh` (or `powershell -ExecutionPolicy Bypass -File scripts/validate.ps1` on Windows).
5. Run `docker compose build --pull`.
6. Run `docker compose up -d`.
7. Wait for the one-shot `create-site` service to finish successfully.
8. Run `./scripts/healthcheck.sh`.
9. If healthcheck fails, inspect `docker compose ps` and `docker compose logs --tail=250` before changing code.
10. Never use `docker compose down -v` unless the user explicitly requests destructive reset and confirms data loss.
11. Report the final URL, container state, installed apps, and any migration warnings.
