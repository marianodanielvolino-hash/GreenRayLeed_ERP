# Instalación sugerida

## 1. Preparar ERPNext v16

Usar una release estable de `version-16`, no `develop`.

## 2. App

Copiar este directorio `fch_ops` al host/servidor que ejecute Bench y luego:

```bash
cd ~/frappe-bench
bench get-app /ruta/fch_ops
bench --site greenray.local install-app fch_ops
bench --site greenray.local migrate
```

## 3. Verificaciones mínimas post-install

```bash
bench --site greenray.local list-apps
bench --site greenray.local console
```

Dentro de consola:

```python
frappe.get_all("FCH Market", pluck="name")
frappe.get_all("Accounting Dimension", filters={"document_type": "FCH Market"}, pluck="name")
```

## 4. Compañías

Cargar `data/companies_seed.csv` una vez validados Tax IDs y Chart of Accounts con cada contador local.

## 5. Primera carga

Orden recomendado:

1. Companies.
2. Warehouses.
3. Items.
4. Customers / Suppliers.
5. Price Lists.
6. Opening Stock.
7. AR/AP.
8. Open SO / PO.
9. Import Operations.
10. Contracts / Compliance / Cases.
