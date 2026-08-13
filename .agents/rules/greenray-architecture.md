---
description: Always-on architecture and safety rules for GreenRay ERP
activation: always
---

# GreenRay ERP architecture rule

Follow @AGENTS.md as the source of persistent engineering constraints.

For any implementation or deployment task:

- Keep ERPNext core unmodified.
- Put GreenRay-specific logic in `fch_ops`.
- Preserve Company != Market.
- Preserve legal stock owner separately from physical location.
- Never bypass the five sales gates to make a test pass.
- Never invent fiscal identifiers, bank data, opening balances, customers, suppliers or inventory.
- Never commit `.env` or secrets.
- Use `docker compose config` and `scripts/validate.sh` before deploying.
- For schema changes, make them migration-safe and idempotent.
- When uncertain about a Frappe/ERPNext behavior, inspect upstream v16 source/documentation before changing code.
