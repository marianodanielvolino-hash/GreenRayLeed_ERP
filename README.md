# GreenRay ERPNext

Base de implementación del ERP regional de GreenRay sobre **ERPNext v16 + Frappe + `fch_ops`**.

## Para Antigravity

Abrir este repositorio como proyecto y pedirle:

> Leé `AGENTS.md` y `docs/BUILD_SPEC.md`. Completá/validá la app `fch_ops` sin modificar el core de ERPNext. Después ejecutá `scripts/validate.sh`, configurá `.env` desde `.env.example` y desplegá con `scripts/deploy.sh`. Verificá el sitio y reportá cualquier error antes de cambiar arquitectura.

## Arranque

```bash
cp .env.example .env
# completar DB_PASSWORD y ADMIN_PASSWORD
./scripts/validate.sh
./scripts/deploy.sh
```

URL local esperada: `http://localhost:8080`

## Principios

- Company es razón social; Market es una dimensión diferente.
- El propietario legal del stock y su ubicación física se modelan por separado.
- Un SKU maestro global; códigos locales/proveedor son mappings.
- Sales Order tiene 5 gates: Comercial, Stock, Compliance, Finanzas y Logística.
- Un `NO GO` obligatorio bloquea la promesa/confirmación al cliente.
- Toda lógica propia de GreenRay vive en `fch_ops`; no se modifica ERPNext core.
- No versionar secretos, saldos reales ni información fiscal no validada.

## Estado

El repositorio contiene Docker Compose, Dockerfile, plantilla de entorno, scripts de bootstrap/validación/deploy y la especificación funcional de GreenRay. Antes del primer deploy productivo, Antigravity debe completar y probar el modelo `fch_ops` definido en `docs/BUILD_SPEC.md`.
