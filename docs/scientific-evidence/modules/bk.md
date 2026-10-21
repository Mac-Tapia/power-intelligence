# Persistencia, linaje y series temporales — soporte científico y reglas implementables

**Área de código:** `PostGIS, snapshots, measurements, datasets`.  
**Consulta:** `python scripts/research/query_evidence.py --module bk --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Asegurar identidad de activos, versiones bitemporales y lecturas idempotentes con datos fuera de orden.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-003 · Bigtable: A Distributed Storage System for Structured Data](../sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-004 · Spanner: Google's Globally-Distributed Database](../sources/REF-004-spanner-google-s-globally-distributed-database.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-059 · Recent developments and challenges using blockchain techniques for peer-to-peer energy trading](../sources/REF-059-recent-developments-and-challenges-using-blockchain-techniques-for-peer-.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-060 · Electricity powered by blockchain: A review with a European perspective](../sources/REF-060-electricity-powered-by-blockchain-a-review-with-a-european-perspective.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-061 · Applications of blockchain technology in peer-to-peer energy markets and green hydrogen supply chains](../sources/REF-061-applications-of-blockchain-technology-in-peer-to-peer-energy-markets-and.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-062 · A blockchain-based optimal peer-to-peer energy trading framework for decentralized energy management](../sources/REF-062-a-blockchain-based-optimal-peer-to-peer-energy-trading-framework-for-dec.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-099 · OpenStreetMap: User-Generated Street Maps](../sources/REF-099-openstreetmap-user-generated-street-maps.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-100 · Citizens as sensors: the world of volunteered geography](../sources/REF-100-citizens-as-sensors-the-world-of-volunteered-geography.md) — articulo_revista, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-092 · Event Sourcing](../sources/REF-092-event-sourcing.md) — articulo_tecnico.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Asegurar identidad de activos, versiones bitemporales y lecturas idempotentes con datos fuera de orden.
- **Benchmark mínimo propuesto:** Prueba de reproducibilidad de snapshot + ausencia de contaminación entre tenants.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-db-postgis`
- `unitesis-evidence-audit`

## Palabras clave multilingües
Persistencia, linaje y series temporales; modularity; reproducibility; industrial validation
