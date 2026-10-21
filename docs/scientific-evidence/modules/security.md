# Seguridad, gobierno y control de agentes — soporte científico y reglas implementables

**Área de código:** `connectors, identity, audits`.  
**Consulta:** `python scripts/research/query_evidence.py --module security --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Permiso mínimo, RBAC/ABAC, secrets fuera de repositorio, auditoría y entornos con aislamiento.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-009 · Attention Is All You Need](../sources/REF-009-attention-is-all-you-need.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-020 · Constitutional AI: Harmlessness from AI feedback](../sources/REF-020-constitutional-ai-harmlessness-from-ai-feedback.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-081 · Federated Learning-Based State Estimation for Integrated Transmission–Distribution Networks](../sources/REF-081-federated-learning-based-state-estimation-for-integrated-transmissiondis.md) — tesis_maestria, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-021 · Mitigating the risk of prompt injections in browser use](../sources/REF-021-mitigating-the-risk-of-prompt-injections-in-browser-use.md) — guia_tecnica.
- [REF-022 · Trustworthy agents in practice](../sources/REF-022-trustworthy-agents-in-practice.md) — guia_tecnica.
- [REF-095 · Model Context Protocol authorization specification](../sources/REF-095-model-context-protocol-authorization-specification.md) — especificacion.
- [REF-187 · NIST Cybersecurity Framework 2.0](../sources/REF-187-nist-cybersecurity-framework-2-0.md) — norma_o_estandar.
- [REF-188 · OWASP ASVS](../sources/REF-188-owasp-asvs.md) — norma_o_estandar.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Permiso mínimo, RBAC/ABAC, secrets fuera de repositorio, auditoría y entornos con aislamiento.
- **Benchmark mínimo propuesto:** Pentest focalizado: MCP prompt injection, SSRF, escalada de privilegios y fuga entre tenants.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-security-threat-model`
- `unitesis-mcp-connectors`

## Palabras clave multilingües
Seguridad, gobierno y control de agentes; modularity; reproducibility; industrial validation
