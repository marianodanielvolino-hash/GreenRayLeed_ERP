# GreenRay ERP — `fch_ops`

Aplicación propia para extender ERPNext v16 sin modificar el core.

## Alcance incluido

- Modelo regional Company ≠ Market.
- CASE-ID (`FCH Case`) y Decision Log (`FCH Decision`).
- Five Gate Engine para Sales Order: Comercial, Stock, Compliance, Finanzas y Logística.
- Compliance por SKU + país.
- Operaciones de importación / COMEX y landed cost operativo.
- Registro de contratos y alertas de vencimiento.
- Mapping SKU global ↔ SKU local/proveedor por país.
- Gestión de cobranzas con próxima acción.
- Campos técnicos para productos LED.
- Campos operativos para cotizaciones, compras, depósitos y proyectos.
- Accounting Dimension `FCH Market`.
- Workspace `FCH Ops`.

## Base soportada

- ERPNext: rama `version-16`, fijar siempre una release estable.
- Frappe: >=16.21.0,<17.0.0.
- Python: >=3.14.

## Instalación sobre un bench existente

```bash
cd ~/frappe-bench
bench get-app /ruta/al/repositorio/fch_ops
bench --site <sitio> install-app fch_ops
bench --site <sitio> migrate
bench restart
```

La app crea roles, mercados, la dimensión contable `FCH Market`, campos personalizados y configuraciones base de manera idempotente.

## Importante sobre las compañías

El blueprint define siete sociedades, pero faltan datos legales/fiscales y planes de cuentas definitivos. Por seguridad, la app **no crea automáticamente las Company**. Se incluye `data/companies_seed.csv` con la estructura propuesta para cargarlas cuando se confirme cada alta.

## Datos aún pendientes de migración

Las plantillas CSV están en `data/templates/` y cubren productos, clientes, proveedores, stock, cotizaciones/pedidos abiertos, compras, embarques, CxC y CxP.
