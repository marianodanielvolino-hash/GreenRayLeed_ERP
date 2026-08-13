# Architecture Summary

## Functional model

`Lead -> Deal -> Quotation -> Pricing approval -> Sales Order -> 5 Gates -> Delivery -> Invoice -> Collection`

Mandatory sales gates:

1. Commercial
2. Stock
3. Compliance
4. Finance
5. Logistics

## Legal entities seeded as reference data

- GRL LLC
- GRL Argentina
- GRL Chile
- GRL Puerto Rico
- GRL Costa Rica
- S-Pagers (Mexico)
- Ekant (Uruguay)

Seed files are references only; company records requiring fiscal/accounting configuration must be validated before production import.

## Custom application

`fch_ops` owns GreenRay-specific logic including:

- Case / Decision Log
- Gate checks
- Compliance by SKU + destination country
- Import operations and landed-cost context
- Contract register
- Country SKU mapping
- Collection actions
- GreenRay custom fields and validations

See `fch_ops/docs/blueprint_greenray.md` for the full operating blueprint.
