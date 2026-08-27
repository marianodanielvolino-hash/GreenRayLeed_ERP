# Estado de configuración — GreenRay ERP

## Ya construido en esta entrega

1. App independiente `fch_ops` para ERPNext v16.
2. Siete mercados regionales como maestro inicial.
3. Roles operativos iniciales.
4. Accounting Dimension `FCH Market` para separar Company de Market.
5. `FCH Case` (CASE-ID).
6. `FCH Decision` (Decision Log).
7. Five Gate Engine en Sales Order.
8. Bloqueo de Sales Order al enviar si cualquiera de los cinco gates no está `GO`.
9. Validación de compliance obligatorio por SKU + país.
10. `FCH Import Operation` con ETD/ETA y cálculo de landed cost operativo.
11. `FCH Compliance Requirement`.
12. `FCH Contract Register` con estado y alertas 90/60/30.
13. `FCH Country SKU Mapping`.
14. `FCH Collection Action` con obligación de próxima acción.
15. Especificaciones técnicas LED agregadas a Item.
16. Control de pricing/margen en Quotation.
17. Campos de lead time y demanda en Purchase Order.
18. Propietario legal de stock vía Company nativa de Warehouse + ubicación física propia.
19. Workspace `FCH Ops`.
20. Plantillas de migración.

## Deliberadamente no inventado

- Tax ID / CUIT / RFC de las sociedades.
- Plan de cuentas definitivo por país.
- Cuentas bancarias y saldos.
- Matriz real de usuarios y aprobadores.
- Margen mínimo corporativo.
- Listas de precio reales.
- Productos/SKU reales.
- Clientes/proveedores reales.
- Stock real.
- Datos fiscales/e-invoicing locales.

Esos datos se cargan después sin cambiar la arquitectura.
