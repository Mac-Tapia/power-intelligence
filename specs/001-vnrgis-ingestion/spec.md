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

## Fuentes reales y formato universal VNR-GIS (decisión del usuario, 21/10/2026)

**VNR-GIS es un formato universal.** Osinergmin actualiza cada cuatro años el Valor Nuevo de Reemplazo (VNR) de las instalaciones de distribución con la información que presentan **todas** las concesionarias (Ley de Concesiones Eléctricas, art. 77). La *Guía de Elaboración del VNR de las Instalaciones de Distribución Eléctrica* (Res. 232-2017-OS/CD) fija requisitos, formatos y plazos, y Osinergmin publica el instalador, la base de datos y los manuales del sistema VNRGIS. Por eso el adaptador es **por versión del sistema VNRGIS, no por empresa**: el mismo lector sirve para cualquier distribuidora que entregue su respaldo VNR.

**El módulo de construcción de datasets se alimenta de fuentes reales:**

| Fuente | Contenido que aporta | Acceso |
|---|---|---|
| Respaldo VNR-GIS (`.bak` SQL Server, base y parámetros) | topología MT/BT, tramos, SED, equipos, coordenadas, demandas declaradas | restauración en una base **nueva y de solo lectura** de la instancia local; nunca se modifican bases existentes |
| Exportación CYME ASCII (`.txt`: red, cargas, equipos) | impedancias de catálogo, cargas por fase, estados de maniobra | lector offline propio (ADR-0010) |
| Bases de estudio CYME (`.mdb`) | modelos de estudio por alimentador y su catálogo | lectura offline con el controlador Access de Windows; sin automatizar CYME |

Los fixtures sintéticos sirven solo para pruebas. Si una fuente necesaria no está disponible, el sistema informa **qué falta y a quién pedirlo**; no la sustituye con datos inventados.

- AC-001-U01: el lector VNR-GIS identifica la versión del esquema VNRGIS y funciona con el respaldo de cualquier concesionaria que respete ese esquema; las diferencias de versión se resuelven con un mapeo versionado, nunca con reglas por empresa.
- AC-001-U02: cada restauración registra SHA-256 del `.bak`, `RESTORE HEADERONLY`/`VERIFYONLY`, nombre de base nueva y paso a solo lectura; una base ajena no se escribe.
- AC-001-U03: la estructura de cada fuente (VNR, MDB, TXT) se recupera con el perfilador REA (ADR-0012) antes de escribir su lector; los campos usados y no usados quedan documentados.
- AC-001-U04: los parámetros que VNR no trae (R/X, cargas por fase) se completan solo desde otra fuente real del mismo caso (catálogo CYME, MDB) mediante un mapeo versionado (`CodNorma` ↔ código de catálogo); lo que no se puede mapear va a cuarentena.
- AC-001-U05: todo dataset de entrenamiento (016, 029, 030) cita los manifiestos de las fuentes reales de las que deriva.

## Fuera de alcance

- Solvers de potencia, integración SCADA operativa, corrección automática silenciosa y certificación CIM.

## Entregables

`RawImportManifest`, `SourceSchemaMapping`, `ValidationReport`, `CanonicalAssetGraph`, `MissingAttributeCatalog`, y pruebas de conformidad contra fixtures.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-001` · **Gate:** `G1` · **Dependencias:** SPEC-006.  
**Alcance verificable:** Ingerir fuentes reales VNR-GIS y adaptadores autorizados con procedencia e inconsistencias explícitas.  
**Ubicación propuesta:** `workers/ingestion/, packages/python/power-adapters/, data contracts`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-001-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-001-02:** entrada válida: Importaciones de dos esquemas documentados conservan RAW, unidades, CRS, atributos faltantes y cuarentena; repetición determinista.
- **FR-001-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-001-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-001-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-001-01:** caso exitoso demuestra `FR-001-01/02` con fixture y evidencia automatizada.
- **AC-001-02:** caso negativo demuestra `FR-001-03`, sin alterar estado persistido ni fuente original.
- **AC-001-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-001-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
