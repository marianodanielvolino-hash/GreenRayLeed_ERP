# GreenRay ERP — Agent Instructions

This repository deploys GreenRay's regional ERP on Frappe/ERPNext v16 plus the custom `fch_ops` app.

## Non-negotiable architecture

1. Do not modify ERPNext core unless a requirement is impossible through configuration, hooks, custom fields, or `fch_ops`.
2. All GreenRay-specific business logic belongs in `fch_ops`.
3. `Company` is a legal entity and must never be used as a synonym for `Market`.
4. Stock must preserve both legal owner (`Company`) and physical location (`Warehouse` / market context).
5. Sales Orders use five mandatory gates: Commercial, Stock, Compliance, Finance, Logistics.
6. A mandatory `NO GO` blocks confirmation/promising to the customer.
7. The global SKU is the master. Local/provider SKUs are mappings, not duplicate masters.
8. ERPNext is the transactional source of truth. Email, Drive and WhatsApp are communication/evidence channels, not parallel operational databases.
9. Never commit credentials, `.env`, database dumps, private keys or customer data.
10. Prefer reversible migrations and idempotent setup tasks.

## Stack

- Frappe Framework v16
- ERPNext v16
- `fch_ops`
- MariaDB
- Redis
- Docker Compose

## Main commands

```bash
cp .env.example .env
./scripts/validate.sh
./scripts/deploy.sh
./scripts/healthcheck.sh
```

## Expected local URL

`http://localhost:8080`

## Before a production deployment

- Replace every `CHANGE_ME_*` secret.
- Confirm backups and restore procedure.
- Confirm company tax/fiscal settings with each local accountant.
- Do not seed invented tax IDs, balances, bank accounts or opening stock.
