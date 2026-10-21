# Definition of Done: funcionalidad de ingeniería

- [ ] Spec aceptada con casos normales, límites y fallas; requerimientos vinculados a IDs.
- [ ] Plan y ADR si cambia un contrato o arquitectura.
- [ ] Código tipado, con dependencias acordes al grafo permitido.
- [ ] Tests unitarios, integrales y de contrato.
- [ ] Estudios eléctricos: golden feeder/analítico, tolerancias documentadas, solver y versión, matriz de fallos.
- [ ] Provenance: hash de datos, configuración, commit y versión de motor.
- [ ] Inexistencia de datos fabricados, secretos y fuentes sin permiso.
- [ ] CI verde, revisión humana del PR, changelog si hay contrato público.
- [ ] Spec y pruebas convergen; documentación actualizada.

### DoD adicional: grafo, P2P, ledger y mercado
- Graph: consistencia de terminal/fase/versiones, comparación de proyecciones y ACL.
- P2P: identidad verificable y ataques replay, peer desconocido, partición y retry cubiertos.
- Ledger: no datos personales on-chain, integridad, idempotencia y fail-open *solo para disponibilidad de estudios*, nunca para aprobación de trade.
- P2P Market: modo simulación por defecto, solver AC y revisión jurídica antes de liquidación; pruebas de no autorizados.
- GraphRAG: citas/evidencia, tenant isolation, pruebas prompt-injection.

### Gates de IA de programación
- [ ] Skills del rol aplicados y versionados; contrato y tests vinculados a spec.
- [ ] MCP/tools usados documentados; conexiones externas explícitamente aprobadas; producción inaccesible por defecto.
- [ ] Backend: roles/tenants, contratos, serialización/validación y idempotencia cubiertos.
- [ ] Frontend: TypeScript estricto, cliente API generado, accesibilidad, empty/error/stale y Playwright en entorno aplicable.
- [ ] Scan de secretos, autorización negativa, control de egress y evidencias CI.
