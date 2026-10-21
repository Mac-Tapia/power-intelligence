# 009 — Industrialización

**Estado:** no iniciada. control-api v0.2 es solo local: sin autenticación, con jobs en memoria y SQLite.

## Criterios de aceptación

- AC-009-01: autenticación y autorización por rol y tenant antes de cualquier exposición fuera de localhost.
- AC-009-02: jobs persistentes (cola) y repositorio PostgreSQL/PostGIS con las mismas reglas append-only (`infra/db/postgres`).
- AC-009-03: observabilidad (logs estructurados sin datos de clientes, métricas y trazas) y recuperación probada.
- AC-009-04: empaquetado reproducible (lockfile y contenedor) y CI con todas las suites.
