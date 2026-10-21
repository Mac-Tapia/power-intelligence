# P2P federación segura — soporte científico y reglas implementables

**Área de código:** `power-p2p, p2p-sync`.  
**Consulta:** `python scripts/research/query_evidence.py --module p2p --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Usar peers autenticados para replicar resúmenes/evidencias; la red P2P no controla interruptores reales.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-081 · Federated Learning-Based State Estimation for Integrated Transmission–Distribution Networks](../sources/REF-081-federated-learning-based-state-estimation-for-integrated-transmissiondis.md) — tesis_maestria, EN; `identificado_en_fuente_web`.
- [REF-054 · P2P electricity trading: A systematic review on current developments and perspectives](../sources/REF-054-p2p-electricity-trading-a-systematic-review-on-current-developments-and-.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-055 · Peer-to-peer energy trading in smart grid: Frameworks implementation methodologies and demonstration projects](../sources/REF-055-peer-to-peer-energy-trading-in-smart-grid-frameworks-implementation-meth.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-056 · P2P energy trading via public power networks: Practical challenges emerging solutions](../sources/REF-056-p2p-energy-trading-via-public-power-networks-practical-challenges-emergi.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-057 · Peer-to-peer kilowatt and negawatt trading: A review](../sources/REF-057-peer-to-peer-kilowatt-and-negawatt-trading-a-review.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-058 · A survey on peer-to-peer energy trading for local communities](../sources/REF-058-a-survey-on-peer-to-peer-energy-trading-for-local-communities.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-059 · Recent developments and challenges using blockchain techniques for peer-to-peer energy trading](../sources/REF-059-recent-developments-and-challenges-using-blockchain-techniques-for-peer-.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-060 · Electricity powered by blockchain: A review with a European perspective](../sources/REF-060-electricity-powered-by-blockchain-a-review-with-a-european-perspective.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-061 · Applications of blockchain technology in peer-to-peer energy markets and green hydrogen supply chains](../sources/REF-061-applications-of-blockchain-technology-in-peer-to-peer-energy-markets-and.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-062 · A blockchain-based optimal peer-to-peer energy trading framework for decentralized energy management](../sources/REF-062-a-blockchain-based-optimal-peer-to-peer-energy-trading-framework-for-dec.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-063 · P2P Energy Trading of EVs Using Blockchain Technology in Centralized and Decentralized Networks](../sources/REF-063-p2p-energy-trading-of-evs-using-blockchain-technology-in-centralized-and.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-082 · Integration of electric vehicles in a flexible electricity demand side management framework](../sources/REF-082-integration-of-electric-vehicles-in-a-flexible-electricity-demand-side-m.md) — tesis_doctoral, EN; `identificado_en_fuente_web`.
- [REF-125 · Designing the future electricity spot market with high renewables (2025)](../sources/REF-125-designing-the-future-electricity-spot-market-with-high-renewables-2025.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.

## Documentación, guías o estándares útiles (no confundir con papers)
- Consultar fuentes institucionales oficiales a partir de las fichas científicas y agregar sus versiones al registro.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Usar peers autenticados para replicar resúmenes/evidencias; la red P2P no controla interruptores reales.
- **Benchmark mínimo propuesto:** Prueba de peer malicioso, replay, partición de red, aislamiento de empresa y sincronización.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-p2p-blockchain`
- `unitesis-security-threat-model`

## Palabras clave multilingües
peer-to-peer; federated learning; prosumer; energia distribuída; réseau pair à pair
