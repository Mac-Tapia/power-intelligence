# Plan — SPEC-004: fullstack-runtime


## Plan ejecutable — SPEC-004

**Gate de entrega:** G0 · **Dependencias aprobadas:** SPEC-000.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `apps/control-api/, apps/workstation-web/, infra/compose/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Crear backend FastAPI y frontend React operativos, con contratos y entorno local reproducible. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** API responde health/readiness, UI carga rutas reales, OpenAPI genera cliente TypeScript y CI ejecuta build completo. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module backend --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.

## Plan incorporado (antes spec 009)

Mandato del usuario: completar lo pendiente, mantener specs y archivos sincronizados.
Dependencias extendidas y datos locales autorizados por el usuario el 21/10/2026.

1. Credenciales bearer con hash, rol, tenant y caducidad en archivo local fuera de Git.
   Adaptador HTTP en `unitesis_api/security.py`; `create_app` selecciona perfil protegido
   si `UNITESIS_CREDENTIALS_FILE` está definido. Reader solo GET/HEAD, engineer crea
   estudios; tenant determina el almacén, nunca un header modificable por el cliente.
   Cada tenant usa archivo distinto. Rechazar tokens vencidos/configuración inválida.
2. Pruebas negativas 401/403, snapshots/jobs/resultados de otro tenant devuelven 404;
   conservar perfil local existente y no abrir escucha externa durante desarrollo.
3. Extraer ejecución durable a caso de uso y worker; PostgreSQL se verifica con motor
   real si está disponible. No presentar el driver instalado como servicio probado.
4. Instalar dependencias extendidas con versiones fijadas; verificar imports, handshake
   MCP real y UI mediante Chromium. Registrar backend real de entrenamiento.
5. Conectar proyección de grafo (010) y recuperación documental citada (008/014) a API,
   con mismo ámbito de tenant/snapshot; sin ejecución de instrucciones documentales.
6. Ejecutar regresiones, suite completa, inventario, Ruff y verificación estructural.
   Revisar cambios independientemente antes de declarar terminada la entrega.

La elección de bearer local es un perfil inicial autenticado: no sustituye OIDC,
TLS/proxy o aceptación de producción. No se habilita ningún servicio externo por defecto.
