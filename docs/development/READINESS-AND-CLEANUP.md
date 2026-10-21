# Preparación integral e integración del proyecto

Estado: diseño y plan aprobados por el usuario el 21/10/2026. Primer lote local implementado y verificado; preparación productiva e implementación integral pendientes.

## Objetivo y alcance

Completar las capacidades declaradas de UNITESIS, integrar los aportes útiles y
mantener una sola carpeta activa `power-intelligence`. Cada entrega exige trazabilidad
entre requisito, código, ejecución y evidencia releída. Los documentos, fixtures,
contratos, skills y catálogos son componentes de soporte: no necesitan importarse
desde Python para justificar su conservación.

El inventario ejecutado cubre los archivos versionados y los metadatos de archivos
locales, excluyendo Git, el entorno virtual y cachés regenerables. El detalle está en
`local-data/diagnostics/readiness-20261021/file-inventory.json`, fuera de Git.
El archivo externo de proyectos donantes permanece fuera de la raíz activa.

## Hallazgos que determinan el diseño

- 578 archivos versionados presentes; no había archivos ajenos sin seguimiento
  fuera de `local-data` en el momento del inventario.
- 19 paquetes: 12 tienen consumidores Python detectados; 7 carecen de importadores
  estáticos. Esto último no prueba inutilidad ni autoriza borrar sus contratos.
- Los siete paquetes son `power-agents`, `power-graph`, `power-graphrag`,
  `power-ledger`, `power-market`, `power-marl` y `power-p2p`. Sus specs
  030/010–014 declaran capacidades todavía pendientes o auxiliares mínimos.
- El registro conserva 32 aportes candidatos y 6 excluidos por APIs propietarias.
  Ningún candidato se considera integrado por existir en dicho registro.
- La industrialización (004/005/007/031), las autorizaciones/datasets gold 035 y parte del
  alcance eléctrico 008 siguen abiertos.
- Se preservó el cambio previo de `cyme_ascii.py`; cualquier integración posterior
  debe compararse con este estado, sin sobrescribirlo.

## Decisión propuesta

Completar las specs existentes en el monolito modular y sus puertos, con entregas
independientes verificables. Se conserva el solver propio como confirmación física.
No se sustituye la implementación pendiente por indicadores verdes ni se eliminan
capacidades prometidas para aparentar completitud.

Alternativas consideradas: copiar proyectos donantes enteros aumentaría duplicidad
y dependencias sin probar integración; reducir el alcance borrando los scaffolds
contradiría el pedido de completar el producto. Se recomienda adaptar únicamente
las contribuciones justificadas, preservando procedencia y exclusiones.

## Entregas y criterios de aceptación

| Entrega | Specs y responsables | Criterios antes de cerrar |
|---|---|---|
| Inventario y limpieza | 000, `scripts/verify_structure.py`, trazabilidad | Cada archivo clasificado; rutas verificadas antes de mover/borrar; fuentes y cambios previos preservados; sin pérdida de archivos versionados. |
| Fuentes e ingesta | 001/035, adapters/config/sciml | Autorización del propietario registrada; lectores con dependencias aprobadas; linaje raw→gold, unidades, CRS y cuarentena; sin inventar parámetros. |
| Cobertura eléctrica | 006/008/017, domain/topology/simulation | Transformadores con migración del snapshot; benchmarks independientes por fase IEEE 13/123 y cortocircuito; tolerancias y cobertura declaradas; no relajar umbrales. |
| Producto durable | 005/007/031, API/adapters/infra | Autenticación; pruebas 401/403 y aislamiento entre tenants; jobs PostgreSQL persistentes recuperables tras reinicio; logs sin secretos; restauración de backup comprobada; contenedor y CI reproducibles. |
| Estudios y GIS | 002/003/018/019, application/optimization/UI | Carga, alternativas y GIS/unifilar unidos por snapshot e IDs; resultados factibles confirmados por solver; costos con fuente; pruebas de interfaz y accesibilidad. |
| SciML | 029/035, sciml | Dataset gold autorizado; entrenamiento real; evaluación fuera de muestra por alimentador; superar criterios vigentes con idéntico split; artefacto y backend registrados. |
| MADRL y LLM | 030/014, marl/agents/graphrag | Entorno y línea base; entrenamiento/evaluación multisemilla; corpus con derechos; citas y herramientas tipadas; pruebas adversariales; propuestas verificadas por solver y revisión humana. |
| Grafo y colaboración | 010–013, graph/p2p/market/ledger | Proyecciones separadas del grafo físico; firmas, TTL y anti-replay; mercado solo simulado; anclajes verificables sin datos sensibles; consumidores reales vía aplicación. |
| Conectores | 015, tools/mcp/connectors | Arranque y llamada real por transporte MCP; pruebas negativas de acceso; cliente usa intérprete del entorno; servicios opcionales verificados individualmente. |
| Regulación y entrega | 020–027, regulation/templates | Cálculo trazable a fuente vigente y cláusula; borradores explícitos; evidencias y revisión humana independientes de convergencia numérica. |

La dependencia es datos autorizados → ingesta/topología → solver por alcance →
estudios e IA. La industrialización puede avanzar de forma independiente, pero
ninguna exposición fuera de localhost precede a autenticación y aislamiento.

## Política de integración y purga

1. Código usado, documentación vigente, contratos, fixtures y pruebas se conservan.
2. Código desconectado con spec vigente se integra mediante su caso de uso y prueba
   de aceptación; no se borra por falta de importación estática.
3. Un aporte donante requiere licencia, hash de origen, destino y prueba del caso
   antes de copiarse o reescribirse. Las seis exclusiones propietarias se mantienen.
4. Solo se eliminan cachés regenerables o duplicados cuya identidad y falta de
   necesidad estén demostradas. No se purgan `.venv`, `.git`, datasets ni evidencias
   originales como si fueran basura.
5. El registro de coordinación anterior y las evidencias del navegador se conservaron
   en `local-data/diagnostics/readiness-20261021/root-evidence`. La raíz del workspace
   queda con una sola carpeta activa. Se retiró la caché externa de mypy.

## Decisiones que requieren información externa

La orden de preparar el producto no demuestra autorización del propietario de
Electro Dunas. Sigue pendiente ese documento. Las dependencias nuevas o actualizadas
requieren autorización explícita conforme a `AGENTS.md`, regla 9; no se instalaron
paquetes durante esta limpieza. GitHub necesita repositorio remoto identificado y
servicios de destino reales antes de verificar despliegue/CI remoto.

El diseño y `READINESS-IMPLEMENTATION-PLAN.md` están aprobados. El primer lote implementa
inventario reproducible, jobs SQLite durables, recuperación y selección del intérprete
MCP; las demás entregas siguen abiertas. La limpieza y la trazabilidad no equivalen
a completar todos los módulos ni a aceptación productiva.

## Evidencia de la primera entrega

Inventario actualizado: `local-data/diagnostics/inventory.json`; 587 archivos de
producto vinculados a propietario y spec, sin archivos sin dueño ni specs faltantes.
Este control también se ejecuta en CI. Los datos locales se resumen únicamente por
cantidad y bytes, sin publicar nombres de clientes.

Aceptación local ejecutada entre procesos independientes:
`local-data/diagnostics/readiness-20261021/acceptance-d3a701b9/acceptance.json`.
Confirma estudio con contraste, reapertura del job, backup, restauración y relectura
de evidencia. Las pruebas por tarea y el estado detallado constan en el plan y en
`specs/000`, la antigua `specs/009` (hoy 004/005/007/031) y `specs/015`. No se instalaron dependencias ni modificaron
autorizaciones del caso.

## Fundamento científico y límites

- Thurner et al. (2018), *IEEE Transactions on Power Systems*, 33(6), 6510–6521,
  [doi:10.1109/TPWRS.2018.2829021](https://doi.org/10.1109/TPWRS.2018.2829021):
  herramienta de análisis eléctrico y caso de estudio reproducible; fundamenta
  contrastes y benchmarks, no certifica UNITESIS.
- Tadvin, S. M. (2024), tesis de maestría, University of Rhode Island,
  [HELICSAuto](https://digitalcommons.uri.edu/theses/2568/): integración demostrada
  mediante ejecución de componentes; respalda distinguir registro de integración real.
- Alvarez, M. (2019), tesis doctoral, Luleå University of Technology,
  [Distribution Network Planning Considering Capacity Mechanisms and Flexibility](https://ltu.diva-portal.org/smash/record.jsf?pid=diva2:1283534):
  integración entre planificación, operación y recursos flexibles; no sustituye
  la validación de datos, algoritmos y restricciones del caso piloto.

Se verificaron registros y resúmenes web, sin afirmar revisión integral de las tesis.
La secuencia de entregas y la política de limpieza son decisiones de ingeniería del
proyecto, no resultados experimentales derivados de esas publicaciones.
