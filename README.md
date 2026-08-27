# FCH Ops — GreenRay / GRL

Custom Frappe app for the GreenRay regional operating model on ERPNext v16.

## Frappe Cloud target

Target site:

`https://conscienciahumana.l.frappe.cloud`

This branch is intentionally app-only so Frappe Cloud sees `pyproject.toml` at repository root.

Repository:

`https://github.com/marianodanielvolino-hash/GreenRayLeed_ERP.git`

Branch:

`frappe-cloud-v16`

## Required runtime

- Frappe v16 (`>=16.21.0,<17.0.0`)
- ERPNext v16 installed on the site
- HRMS and Frappe CRM are recommended for the GRL operating model
- Private Bench is required for this custom app on Frappe Cloud

## GRL post-install behavior

The app creates/seeds:

- FCH Market records: Argentina, Chile, Puerto Rico, Costa Rica, Mexico, Uruguay, USA / Offshore
- GRL operational roles
- Market as an ERPNext Accounting Dimension
- LED master-data fields on Item
- Market context on Warehouse, Sales Order, Purchase Order and Project
- Pricing approval fields on Quotation
- Five Gate controls on Sales Order
- Compliance, Cases, Decisions, Contracts and Collections
- COMEX Import Operation with Purchase Receipt loading and draft Landed Cost Voucher generation

The app does **not** auto-create legal Companies, tax IDs, charts of accounts, bank accounts, customers, suppliers, stock or opening balances. Those require validated GRL data.

## Frappe Cloud install sequence

1. Confirm target site is on Frappe v16.
2. Confirm the site is on a Private Bench. If it is on a shared/public bench, move it to a Private Bench first.
3. On the Bench Group, add this repository as a custom app using branch `frappe-cloud-v16`.
4. Grant the Frappe Cloud GitHub App access to this repository if requested.
5. Deploy/Update the Bench Group.
6. On the Site > Apps, install `fch_ops`.
7. Run site migration/update through Frappe Cloud.
8. Verify the site lists `frappe`, `erpnext`, and `fch_ops`. Install `hrms` and `crm` if they are not already present and are wanted for the pilot.

## GRL acceptance checks

- `FCH Market` contains seven regional markets.
- `Accounting Dimension` contains `Market` referencing `FCH Market`.
- Sales Order shows Five Gate Status and Gate Checks.
- A Sales Order cannot submit when a mandatory gate is NO GO.
- Item exposes LED technical fields.
- Quotation exposes margin and pricing approval fields.
- FCH Import Operation can load submitted Purchase Receipts from a Purchase Order.
- FCH Import Operation can create a **draft** ERPNext Landed Cost Voucher from reviewed charges and expense accounts.
- Compliance Requirement can block destination-country readiness when mandatory evidence is expired/missing.

## Pilot scope

Configure first with validated data for GRL Argentina + GRL LLC. Do not create fiscal settings until the corresponding accountant validates chart of accounts, tax IDs and statutory configuration.
