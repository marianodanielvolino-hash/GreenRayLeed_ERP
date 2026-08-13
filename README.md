# GreenRay ERPNext

Regional GreenRay ERP built on **ERPNext v16 + Frappe Framework + `fch_ops`**.

This repository is deployment-ready for local/UAT Docker environments and intentionally prepared for agent-assisted operation with **Google Antigravity**.

## Scope

The custom `fch_ops` app implements the GreenRay operating model on top of ERPNext without modifying ERPNext core:

- Company != Market
- regional multi-company model
- global SKU + local/provider mapping
- five sales gates (Commercial, Stock, Compliance, Finance, Logistics)
- import/landed-cost tracking
- compliance by SKU and destination country
- collections with next action
- CASE-ID and Decision Log
- contracts and expirations

## Quick start

```bash
cp .env.example .env
# Replace CHANGE_ME values
./scripts/deploy.sh
./scripts/healthcheck.sh
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
# Edit .env
powershell -ExecutionPolicy Bypass -File scripts/deploy.ps1
```

Then open `http://localhost:8080`.

## Antigravity

Open this Git repository as an Antigravity Project. The agent receives repository-specific instructions from `AGENTS.md` and `.agents/rules/`, and can execute the included `/deploy-greenray` workflow.

See `docs/ANTIGRAVITY.md`.

## Safety

Do not commit `.env`, credentials, customer data, database dumps or production backups. Do not invent tax IDs, opening balances or fiscal configurations. Country fiscal configuration requires local validation before go-live.

## Documentation

- `AGENTS.md` — mandatory engineering constraints
- `docs/ARCHITECTURE.md` — target architecture
- `docs/DEPLOYMENT.md` — deployment/runbook
- `fch_ops/docs/blueprint_greenray.md` — full business blueprint
- `fch_ops/TEST_PLAN.md` — functional test plan
