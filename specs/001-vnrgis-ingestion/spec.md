# 001 — Ingesta universal de VNR-GIS y fuentes eléctricas

**Problema:** importar topologías heterogéneas (VNR-GIS multiempresa; opcional MDB, SQL autorizado, TXT, SHP, GeoPackage, DGS) sin asumir que el formato contiene impedancias, cargas ni estados de maniobra.

## Historias de usuario

- Como ingeniero quiero importar una fuente georreferenciada y conservar intactos los archivos originales para poder auditar el origen.
- Como ingeniero quiero detectar segmentos desconectados, terminales sin fase y atributos ausentes para corregirlos antes de simular.
- Como ingeniero quiero tener un mapping explícito por empresa-versión de origen, sin escribir un parser único con reglas ocultas.

## Criterios de aceptación (observables)

- AC-001-01: dada una fuente autorizada, guardar RAW hash SHA-256 + procedencia + formato + timestamp UTC sin modificaciones.
- AC-001-02: reconocer el esquema mediante un adapter/version y almacenar mapa de columnas, unidades, CRS y transformaciones reversible cuando aplique.
- AC-001-03: para un input sin R/X/kW/kvar/taps, producir `MissingElectricalParameters` y **bloquear flujo de potencia**, no crear valores por defecto.
- AC-001-04: toda conectividad eléctrica construida requiere terminales compatibles, fases y estado de switch; proximidad espacial no implica unión.
- AC-001-05: guardar reportes de conectividad y cuarentena; no destruir filas rechazadas.
- AC-001-06: el mismo fichero/schema genera snapshot idéntico bajo configuración/version semánticamente iguales.
- AC-001-07: fixtures sintéticos de 2+ esquemas con todos los casos positivos/negativos.
- AC-001-08: no acceder a SQL ni servicios privados sin autorización/credenciales seguras.

## Fuera de alcance

- Solvers de potencia, integración SCADA operativa, corrección automática silenciosa y certificación CIM.

## Entregables

`RawImportManifest`, `SourceSchemaMapping`, `ValidationReport`, `CanonicalAssetGraph`, `MissingAttributeCatalog`, y pruebas de conformidad contra fixtures.
