# GreenRay ERP — build specification

Antigravity must treat this file and `AGENTS.md` as the implementation contract.

## Platform

- Frappe Framework v16
- ERPNext v16
- custom app: `fch_ops`
- Docker Compose with MariaDB + Redis + backend + websocket + workers + scheduler + frontend
- never modify ERPNext core for GreenRay-specific behavior

## Legal entities

Prepare the model for these companies, but do not invent tax IDs, opening balances or fiscal settings:

- GRL LLC
- GRL Argentina
- GRL Chile
- GRL Puerto Rico
- GRL Costa Rica
- S-Pagers — Mexico
- Ekant — Uruguay

`Company` means legal entity. `Market` is a separate dimension. Stock ownership and physical location must remain separate.

## Custom domain model

Implement in `fch_ops` at minimum:

- FCH Market
- FCH Settings
- FCH Case
- FCH Decision
- FCH Gate Check
- FCH Compliance Requirement
- FCH Import Operation
- FCH Contract Register
- FCH Country SKU Mapping
- FCH Collection Action

## Five-gate sales control

Sales Orders must have five mandatory controls:

1. Commercial
2. Stock
3. Compliance
4. Finance
5. Logistics

A mandatory `NO GO` blocks order confirmation / customer promise. Keep an auditable approver, date and note for each gate.

## Product master

Use one global ERPNext Item/SKU. Store local/provider codes as mappings rather than duplicate masters. Support LED attributes such as family, model, power, lumens, CCT/Kelvin, CRI, IP, voltage, optics, driver, dimensions, weight, volume/CBM, warranty, preferred supplier and lead time.

## Imports / landed cost

`FCH Import Operation` must link Purchase Orders / receipts where applicable and track at least company owner/importer, origin, destination, supplier, forwarder, mode, Incoterm, ETD, ETA, actual arrival, FOB/EXW, freight, insurance, duty, customs, local freight, other costs, landed cost, customs status, compliance status, owner and next action.

## Compliance

Key compliance by `SKU + destination country + requirement`. Include required/optional, valid from/until, status, approval/evidence. Mandatory expired or missing compliance must be able to block the Compliance gate.

## Collections

Open overdue collection work must have owner, status, next action, next-action date, dispute indicator and payment promise where applicable.

## Cases and decisions

Use CASE-ID for operational topics requiring follow-up and a separate Decision Log for material exceptions/decisions. Include company, market, owner, decision maker, due date, financial/operational impact, risk and evidence.

## ERPNext extensions

Use custom fields/hooks rather than core edits. Extend standard records where useful:

- Item — GreenRay LED product attributes
- Warehouse — physical market/location context while Company remains legal owner
- Quotation — margin / pricing approval controls
- Sales Order — five gates and overall gate status
- Project — market / design-project context
- Customer/Supplier — market/regional metadata only when needed

## Permissions

Prepare roles for Direction/CEO, PMO, Finance, Accounting, Treasury, Sales Manager/User, Design, Purchasing, Supply, Warehouse, COMEX, HR, Support, Country Manager, Auditor and System Manager. Apply least privilege and Company User Permissions.

## Acceptance

Before calling the application deployable:

- `fch_ops` installs cleanly on ERPNext v16
- migrations are idempotent
- all custom DocType JSON is valid
- no secrets or invented business/fiscal data are committed
- a Sales Order cannot pass with a mandatory NO GO gate
- compliance can block the Compliance gate
- global SKU and local SKU mapping coexist without creating duplicate Items
- Docker build and `docker compose config` pass
- site can be created, ERPNext installed, `fch_ops` installed and migrated

The first business pilot is GRL Argentina + GRL LLC so intercompany, stock, sales, purchasing, imports and finance can be validated together.
