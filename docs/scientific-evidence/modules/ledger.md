# Blockchain permissioned y evidencia — soporte científico y reglas implementables

**Área de código:** `power-ledger, ledger-anchoring`.  
**Consulta:** `python scripts/research/query_evidence.py --module ledger --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Blockchain es opcional; se almacenan hashes y referencias, no mediciones ni planos sensibles.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-059 · Recent developments and challenges using blockchain techniques for peer-to-peer energy trading](../sources/REF-059-recent-developments-and-challenges-using-blockchain-techniques-for-peer-.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-060 · Electricity powered by blockchain: A review with a European perspective](../sources/REF-060-electricity-powered-by-blockchain-a-review-with-a-european-perspective.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-061 · Applications of blockchain technology in peer-to-peer energy markets and green hydrogen supply chains](../sources/REF-061-applications-of-blockchain-technology-in-peer-to-peer-energy-markets-and.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-062 · A blockchain-based optimal peer-to-peer energy trading framework for decentralized energy management](../sources/REF-062-a-blockchain-based-optimal-peer-to-peer-energy-trading-framework-for-dec.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-081 · Federated Learning-Based State Estimation for Integrated Transmission–Distribution Networks](../sources/REF-081-federated-learning-based-state-estimation-for-integrated-transmissiondis.md) — tesis_maestria, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- Consultar fuentes institucionales oficiales a partir de las fichas científicas y agregar sus versiones al registro.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Blockchain es opcional; se almacenan hashes y referencias, no mediciones ni planos sensibles.
- **Benchmark mínimo propuesto:** Ensayos contra falsificación, duplicidad, reorg y costo; comparación contra log firmado sin cadena.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-p2p-blockchain`
- `unitesis-evidence-audit`

## Palabras clave multilingües
blockchain; Hyperledger; Vertrauenswürdigkeit; rastreabilidade; trazabilidad
