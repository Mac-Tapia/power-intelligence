# 028 — Consolidación de aportes del workspace

Estado (revisión 20/10/2026): diagnóstico, mejora de especificación y limpieza autorizados expresamente por el usuario. Esta arquitectura es objetivo: no se declara implementada ni aceptada eléctricamente. El desarrollo de funcionalidades mantiene sus gates de diseño, pruebas y revisión.

## Intención y alcance

El usuario identificó `power-intelligence` como proyecto principal y solicitó revisar todas las carpetas, seleccionar duplicados y aportes, integrar y fortalecer el núcleo y eliminar archivos sin aporte. Se protegen fuentes únicas, datos, licencias y cambios Git. La eliminación exige justificación por archivo y evidencia; no se deduce inutilidad de un import ausente ni del nombre «copia». La integración debe producir módulos ejecutables con procedencia, no una copia de proyectos completos.

La revisión estructural original cubre 33 carpetas raíz y 1.227.720 archivos. Esta revisión analiza el texto Python mediante AST: 3.492 entradas originales, 3.435 analizadas, seis con error sintáctico y 51 ausentes por el archivo externo anterior. No equivale a revisión semántica manual de todos los archivos ni a validación de documentos/binarios. Véase `architecture-review.md` y su registro por archivo.

El núcleo tiene 19 paquetes Python: seis con auxiliares implementados y 13 scaffold. Economía y regulación carecen de manifest. Las aplicaciones/workers todavía no constituyen un recorrido operativo; bootstrap no demuestra precisión eléctrica ni aceptación normativa.

Se recomienda adaptar componentes al monolito modular existente. La alternativa de mantener cada aplicación como worker externo reduce cambios iniciales, pero conserva contratos y runtimes heterogéneos; se reserva para CYME/PowerFactory. No se decide una versión canónica por el nombre v1/v16/copia.

## Primer bloque entregable

1. Endurecer `power-economics` y `power-regulation`: factibilidad y autorizaciones booleanas estrictas (incluido A06), casos sin alternativas bloqueados, validación económica independiente del bucle, anualidad numéricamente estable y manifests de empaquetado.
2. `power-domain`/`power-ports`: modelo neutral inmutable con unidades explícitas; evolucionar `NetworkSnapshot` a esquema v2 sin crear otra identidad competidora. Su hash v1 actual solo cubre equipos y no identifica un estudio eléctrico completo. Tomar semántica de `flujos` y `grid-bridge`, conservando dominio stdlib sin Pydantic ni motores.
3. `power-adapters`/`power-evidence`: ingesta JSON neutral de esquema declarado, SHA-256 y procedencia, rechazo de parámetros ausentes/no finitos y lectura posterior de evidencias. Adaptar custodia de `Prodma` y auditoría de `PITELD`; trasladar el principio de comparación de lectura efectiva de `RECYM` sin afirmar persistencia CYME.
4. `power-simulation`: estudio AC radial equilibrado de alcance explícito, barrido atrás/adelante basado en el componente de `SelecCablesAAAC`, con adaptador independiente pandapower inspirado en `flujos`. Rechazar mallas, islas, tensiones incompatibles y elementos no soportados; no sustituir parámetros faltantes.
5. `power-application` y CLI: fuente -> snapshot -> estudio -> evidencia JSON con hashes, versiones, convergencia, magnitudes/unidades y diferencias frente al solver independiente. No aprobación eléctrica/regulatoria automática. Sin UI nueva en este bloque.
6. Registro de aportes: source path, SHA-256, destino, tipo de reutilización, pruebas y límites. Un manifiesto distingue integrado, adaptado, reservado, externo y ajeno al núcleo para todas las áreas del workspace.

## Criterios de aceptación

- AC-028-01: cada eliminación autorizada tiene motivo por archivo, alcance, journal previo y verificación posterior. Se protegen Git/worktrees, licencias, fuentes únicas y datos. Un duplicado exige SHA completo y referencia retenida; una caché exige regenerabilidad, patrón conocido y ausencia de archivos versionados. No eliminar código por alcance estático incompleto. El archivo externo es recuperable y no se contabiliza como espacio liberado.
- AC-028-02: pruebas negativas reproducen y bloquean F01–F04 y A05–A07; factibilidad/autorización son booleanos estrictos, valores y tolerancias finitos. La validación cruzada rechaza resultados vacíos, duplicados, no finitos y de otro escenario, y exige cobertura contra el snapshot esperado.
- AC-028-03: ingesta y cálculo son reproducibles con entradas idénticas; modificar P/Q, conexión, fase, estado, R/X o tensión cambia el hash eléctrico v2; reordenar registros no lo cambia. Geometría/CRS conservan política e identidad de fuente explícitas. Ningún R/X, longitud, tensión, carga, ampacidad o CRS se inventa.
- AC-028-04: un caso radial sintético de dos barras converge con balance de potencia, y coincide con pandapower bajo tolerancia declarada (tensión 1e-6 pu, ángulo 1e-4 grados, pérdidas 1e-6 MW). El solver externo ausente produce estado no disponible, nunca éxito fingido.
- AC-028-05: caso radial de referencia abierto permite comparación independiente, registrando motor y versión. No se extrapola a redes reales desbalanceadas.
- AC-028-06: CLI ejecutable desde el núcleo; evidencia persistida se relee y su integridad se comprueba. Corridas fallidas no se etiquetan exitosas.
- AC-028-07: pruebas existentes siguen pasando; nuevos módulos tienen pruebas funcionales, contratos y regresión. Lint se informa distinguiendo deuda previa.
- AC-028-08: antes de implementar se establece baseline verificable e historia/aislamiento del núcleo, actualmente sin Git. No afirmar rama/worktree mientras no exista. No modificar repositorios vecinos ni hacer push.
- AC-028-09: resultados con IDs coincidentes entre sí pero distintos del modelo esperado fallan cobertura; también fallan con IDs duplicados, otro escenario, motor proxy o valores no finitos. No basta convertir listas a diccionarios.
- AC-028-10: CYME sin catálogo, CRS ausente o secciones sin prefijo `SEC_` conserva todos los elementos contados y sus motivos de rechazo; no filtra ni completa silenciosamente. Datos necesarios ausentes bloquean cálculo.
- AC-028-11: nueva carga/optimización/MARL actúa sobre escenario clonado; no modifica origen ni acepta propuestas por recompensa/economía. Requiere solver independiente y revisión.
- AC-028-12: cada aporte registra source/hash/licencia/destino/cambios/tests/estado. Selección no significa integración. No eliminar un original único hasta demostrar sustitución y recuperación.

## Bloques siguientes y límites

Las capacidades de forecasting/optimización de Prodma/informe, importación DGS/CYME completa, GIS/unifilar de flujos, backends propietarios RECYM/EVATE y MADRL/CityLearn se integran por contratos después del primer recorrido verificable. El registro no las presenta como implementadas por haber seleccionado sus archivos.

No se instalan dependencias ni se descargan datos confidenciales. Se puede usar el pandapower ya instalado en el entorno local de flujos para contrastar el núcleo; eso no convierte a flujos en dependencia de runtime del código entregado. Infraestructura, UI, SCADA, entrenamiento GPU, aprobación normativa y transacciones reales quedan fuera de este primer bloque.

## Evidencia científica

Consultar `research.md` y el diagnóstico `_diagnostico_2026-10-20/FUENTES.md` del workspace. Tesis y artículos justifican detección de clones, trazabilidad e independencia de validación; no certifican esta implementación. Los criterios y contratos siguientes son decisiones de ingeniería sujetas a pruebas locales.

## Propiedad de módulos y aportes

| Módulo | Responsabilidad / donantes | Límite |
|---|---|---|
| power-domain | Identidades y modelo neutral; flujos/grid-bridge | Solo stdlib; tipos finitos, unidades, referencias |
| power-ports | Protocolos de fuentes, solver, custodia y repositorios | Dominio; sin implementaciones de I/O/motores |
| power-config | Perfiles y capacidades versionados | Configuración efectiva registrada; sin defaults eléctricos |
| power-adapters | JSON, DGS/CYME, OOXML; flujos/EVATE/CorrecionDatos/PITELD | Traduce y reporta rechazos; no repara silenciosamente |
| power-topology | Conectividad física equipo-terminal-fase y estado | Único dueño físico; inferencias son propuestas separadas |
| power-simulation | Solvers y comparación; AAAC/flujos | Capacidades explícitas, convergencia, cobertura y balance |
| power-application | Casos de uso y jobs | Orquesta puertos; sin cálculo eléctrico ni motores en handlers |
| power-evidence | Custodia, publicación y relectura; Prodma/PITELD/RECYM | Integridad local no equivale a persistencia en motor |
| power-economics | Flujos monetarios y ranking factible | Moneda/año base/tasa/fuente/horizonte explícitos |
| power-regulation | Fuentes y perfiles documentales | PIT/PIDE separados; prepublicación/TDR no norma vigente |
| power-optimization | Dimensionamiento y propuestas; AAAC | Solver independiente valida toda propuesta |
| power-sciml | Forecast/PINN/GNN; Prodma/informe/CityLearn | Causalidad, OOD, observaciones separadas de escenarios |
| power-marl | Políticas experimentales y entrenamiento | Sandbox; no sustituye solver ni altera red fuente |
| power-agents | Propuestas y herramientas acotadas | Sin credenciales productivas ni aprobación automática |
| power-graph | Proyecciones físicas de lectura | No es otro dueño de topología |
| power-graphrag | Grafo documental; smartgridiq | Citas/procedencia; no verdad eléctrica |
| power-p2p | Mensajes/escenarios simulados | Autenticidad/replay no demuestra factibilidad |
| power-market | Compuertas de propuestas de mercado | Booleanos estrictos, evidencia y revisión humana |
| power-ledger | Digest y simulación | Digest no prueba autoría, consenso ni notarización |

Las decisiones por todas las raíces están en `docs/workspace-audit/2026-10-20/decision_carpetas_raiz.csv` (baseline histórico). Movimientos y eliminaciones posteriores están en `docs/workspace-cleanup/2026-10-20/` y esta revisión. No mezclar contadores previos con estado actual.

## Contratos versionados

**SourceManifest:** ID, archivos originales, SHA-256 de bytes, formato/versión, autorización/licencia, fecha de captura, parser/versión, esquema de mapeo, unidades y CRS. Preservar valor/unidad original y conversión. Ausencia, inferencia y rechazo tienen campo, motivo y referencia al origen.

**ElectricalSnapshot v2:** evolución de `NetworkSnapshot`; hash canónico sobre equipos, terminales, fases, conexiones, estados abiertos/en servicio, frecuencia, tensiones, cargas P/Q, impedancias, longitudes, límites y parámetros soportados. IDs únicos, orden estable, números finitos y representación numérica documentada. Coordenadas/CRS y hashes documentales se conservan en manifest de fuente con relación explícita al contenido eléctrico. Probar por separado reordenamiento, geometría y parámetros eléctricos. No interpretar un hash v1 como v2 sin migración y etiqueta de esquema.

**StudyRequest:** snapshot/hash, escenario separado del origen, capacidades, parámetros de cálculo, tolerancias de convergencia/comparación/balance, motores/versiones. Fuente, modelo, solicitud y resultado tienen hashes distintos; tiempo de ejecución no forma parte de identidad del modelo.

**StudyResult:** ID/hash de solicitud y snapshot; estado, motor/versión/capacidad efectiva, convergencia/residual/iteraciones, IDs de barras/ramas/fases, unidades, tensiones/corrientes/flujos/pérdidas/balance/límites y omisiones. Resultado vacío, duplicado, no finito, de otro escenario o sin cobertura esperada falla comparación.

**EvidenceManifest:** hashes de entradas, código (commit cuando exista; digest de árbol en su ausencia), configuración y resultados; versiones, logs sanitizados, métricas y límites. Escritura temporal, publicación atómica local y relectura cotejan existencia e integridad; corrupción bloquea éxito. CYME/PowerFactory exigen además relectura del motor efectivo y alimentador identificado.

Compatibilidad: `contracts/schemas/json/study-run.schema.json` es borrador 0.1.0, exige `git_commit` y usa `completed/rejected`; no admite todavía todos estos estados ni el digest de árbol. Crear versión nueva con migración explícita, no enviar campos nuevos bajo 0.1.0 ni inventar un commit. Probar validación real de payloads y reglas entre campos; `tests/bootstrap/test_contracts.py` hoy solo inspecciona declaraciones del esquema. Evolución de contrato es tarea I03/I04, no cambio ya efectuado.

## Estados y aceptación

Ingesta: `inventoried -> parsed -> quarantined | model_validated`. Estudio: `requested -> running -> failed | unavailable | computed`. Comparación: `not_run | failed | passed`. Evidencia: `not_persisted | persisted | reread_verified`. Aceptación técnica/humana y normativa son campos independientes, inicialmente pendientes/bloqueados. Son contratos objetivo, no un workflow implementado.

No obtener éxito solo de `converged`, HTTP 200, `bool(valor)`, figura o digest. Prohibir cadenas truthy como `"false"`, tolerancias negativas/NaN/inf y referencias de evidencia sin comprobar identidad/escenario/alcance. Conservar causa y resultados parciales al fallar. No copiar `production_ready = validation.ok` de flujos ni tratar `estimated_without_equipment_catalog` como parámetros aceptados.

## Alcance eléctrico inicial y tolerancias

El BFS inicial admite radial equilibrado, una slack, cargas PQ explícitas y líneas serie con frecuencia declarada. Rechaza mallas/islas energizadas no soportadas, múltiples slack, transformadores/taps, generadores PV, shunts, desbalance y elementos fuera del perfil inicial. Elementos abiertos se conservan en snapshot y se excluyen explícitamente del grafo energizado, sin desaparecer del inventario. No etiquetar este recorrido como G3 trifásico desbalanceado; la aceptación de `002-new-load-impact` permanece pendiente.

Además de AC04, comparar corriente <= max(1e-3 A, 1e-4 de referencia) y balance complejo <= max(1e-6 MVA, 1e-6 de demanda aparente de base). Ángulo relativo a misma slack con diferencia circular. Límites térmicos usan el mismo catálogo verificado. Son tolerancias iniciales por caso, sujetas a calibración documentada; no relajarlas automáticamente. Paso de iteración pequeño no sustituye residual/balance físico.

CLI debe distinguir entrada inválida, motor ausente, no convergencia, contraste fallido y evidencia corrupta. La API futura invoca el mismo caso de uso con jobs externos al handler. No añadir una UI antes del recorrido fuente -> snapshot -> estudio -> evidencia -> relectura.

## Prioridad de extracción y eliminación

Primero contratos/economía/ingesta/BFS/evidencia/CLI; después DGS/CYME completos y G3 (specs 001/002), GIS (003), forecast/optimización y motores propietarios. Forecasting se ubica inicialmente en `power-sciml` con puerto consumido por aplicación; un paquete nuevo requiere ADR de cohesión/dependencias. Observaciones y escenarios futuros permanecen separados. MADRL/CityLearn y P2P/ledger siguen experimentales.

No hay imports productivos desde proyectos vecinos ni mezcla de sus site-packages. Workers propietarios usan runtime/arquitectura/licencia compatibles; motor ausente produce `unavailable`. La licencia desconocida bloquea incorporación, no autoriza borrar la fuente.

Backups VNR de Electro Dunas y documentos de inversión son fuentes protegidas aunque no contengan Python. GeoAI conserva licencia y no sustituye topología. Audio y seguridad urbana tienen objetivo independiente: el archivo externo previo es recuperable; `madrl_lima` sigue en la raíz por acceso denegado, sin pérdida tras restauración verificada. No repetir movimientos fallidos ni eliminar carpetas heterogéneas completas.
