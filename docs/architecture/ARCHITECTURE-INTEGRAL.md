# Arquitectura integral — sincronizada con specs, módulos y datos

**Estado:** referencia vigente y única del proyecto (revisada el 20/10/2026).
**Regla de lectura:** cada capacidad tiene **una** spec dueña, **un** paquete dueño, **una** fuente de datos declarada y **un** estado verificable. Si alguno de los cuatro falta, la capacidad no existe todavía.

## 0. Producto universal y casos de aplicación

UNITESIS es universal: el código no contiene supuestos de país, empresa, frecuencia, CRS, moneda ni norma. Lo local se declara en tres registros sincronizados, validados por `unitesis_config.cases.check_consistency`:

| Registro | Archivo |
|---|---|
| Caso de aplicación | `config/cases/<case_id>.json` (plantilla `_template.json`) |
| Fuentes de datos (`case_id`, `role`) | `config/datasets/sources.v2.json` |
| Perfiles regulatorios por `jurisdiction` | `config/regulations/profiles/*.json` |

**Caso piloto de aplicación:** `pe-ica-electrodunas` (Electro Dunas: Ica, Chincha, Pisco, Nasca). Genera datasets y pruebas con datos reales que validan el producto. Los datos de otras localidades de proyectos previos (p. ej. Iquitos) son `method_reference`: sirven para desarrollar métodos y nunca son evidencia de un caso. Un caso nuevo se agrega copiando la plantilla, sin cambiar código.

## 1. Puertas de calidad (constitución) y nomenclatura

| Puerta | Significado (`.specify/memory/constitution.md`) | Estado |
|---|---|---|
| G0 | repositorio, pruebas, contratos | **cumplida** (suites unit, contract, integration, security y governance; `verify_structure.py`) |
| G1 | ingesta sin pérdida, manifiestos raw, invalidación | **parcial**: JSON neutral sí; VNR-GIS no (spec 001) |
| G2 | consistencia topología ↔ GIS ↔ unifilar | **parcial**: topología radial sí; GIS no (spec 003) |
| G3 | benchmark de flujo de potencia y validación independiente | **cumplida para el alcance radial equilibrado** (BFS propio frente a pandapower, diferencias ≤ 1e-11) |
| G4+ | optimización e IA, solo con las puertas anteriores en verde | optimización de conductores operativa; PINN/MADRL/LLM **bloqueados por datos** (spec 029) |

**Corrección de nomenclatura:** "trifásico desbalanceado" no es G3; es una capacidad de la spec 004 (`004-B`). En adelante, G3 se califica por alcance: `G3[radial-equilibrado]` cumplida y `G3[trifásico-desbalanceado]` pendiente.

## 2. Capas y regla de dependencia

```mermaid
flowchart TB
  subgraph Fuentes["Fuentes (fuera de Git, solo lectura)"]
    VNR["VNR-GIS SQL Server<br/>.bak por empresa/fecha"]
    BILL["Facturas / medidores<br/>alimentadores 15 min"]
    DOCS["Normas, TDR, estudios DGER"]
    CAT["Catálogos de conductores<br/>con fuente"]
  end
  subgraph Datos["Capa de datos — spec 029"]
    RAW["raw + SHA-256"] --> BRZ["bronze (tipado)"] --> SLV["silver (reglas con evidencia)"] --> GLD["gold por tarea + splits"]
    QA["quality gates<br/>unitesis_sciml.quality"]
  end
  subgraph Nucleo["Núcleo determinista — verdad eléctrica (ADR-0002)"]
    ADP["power-adapters<br/>JSON · VNR-GIS · DGS offline"] --> DOM["power-domain<br/>ElectricalSnapshot v2"]
    DOM --> TOP["power-topology"] --> SIM["power-simulation<br/>BFS propio + contraste"]
    SIM --> EVD["power-evidence"]
  end
  subgraph Decision["Decisión e IA (G4+)"]
    OPT["power-optimization + power-economics"]
    SCI["power-sciml<br/>forecast · GNN/PINN sustituto"]
    MARL["power-marl<br/>MADRL CityLearn + red"]
    LLM["power-graphrag + power-agents<br/>RAG + tool calling"]
  end
  APP["power-application (casos de uso)"]
  UI["CLI unitesis · control-api · workstation"]

  VNR --> RAW
  BILL --> RAW
  DOCS --> RAW
  CAT --> ADP
  GLD --> ADP
  GLD --> SCI
  GLD --> MARL
  GLD --> LLM
  QA -. bloquea .-> GLD
  SIM -- etiquetas físicas --> SCI
  SIM -- restricciones AC --> MARL
  SIM -- herramienta verificable --> LLM
  OPT --> SIM
  SCI -. propuesta, nunca verdad .-> APP
  MARL -. propuesta .-> APP
  LLM -. propuesta citada .-> APP
  APP --> SIM
  APP --> EVD
  UI --> APP
```

Reglas inamovibles: `power-domain` solo usa la stdlib. Toda salida de IA vuelve a pasar por el solver propio antes de mostrarse como resultado (ADR-0002). Ningún módulo escribe en la topología fuente. Los motores propietarios están excluidos (ADR-0010).

## 3. Matriz sincronizada spec ↔ módulo ↔ datos ↔ estado

Estados: **operativo** (código, pruebas y uso por CLI/API), **parcial**, **scaffold** (solo estructura), **sin spec** (la capacidad se declara en el FEATURE-MAP pero no tiene archivo de spec).

| Spec | Capacidad | Paquete dueño | Datos | Estado |
|---|---|---|---|---|
| 000 | repo, CI, contratos | raíz, `tests/governance`, `scripts/verify_structure.py` | — | operativo (T006–T008 abiertas) |
| 001 | ingesta VNR-GIS multiempresa | `power-adapters` (`vnrgis_sql.py`, pendiente) | piloto: `.bak` VNR Electro Dunas abr‑2024 + parámetros | **pendiente**; esquema relevado (§4.1) |
| 002 | nueva carga | `power-application` | snapshot | parcial: cribado equilibrado operativo; versión por fase depende de 004‑B |
| 003 | GIS ↔ unifilar | `power-topology`, `apps/workstation-web` | coordenadas UTM VNR | parcial: unifilar desde snapshot; GIS pendiente |
| **004** | motores de simulación | `power-simulation` | snapshots | A (BFS) y B1 (Newton-Raphson, radial/mallado) operativos; B2 trafos, C desbalanceado, D cortocircuito pendientes |
| **005** | expansión, SED, BESS, DER, EV | `power-optimization`, `power-economics` | catálogos, base económica | parcial: alternativas de conductor + VPN — **spec creada** |
| **006** | SciML GNN/PINN sustituto | `power-sciml`, `workers/ml-training` | gold `vnr-pf-scenarios-<case_id>` desde redes reales TXT/MDB/VNR (029) | **sin código**; Y-bus y residuo listos (004-B1); faltan lectores 001 |
| **007** | MADRL seguro | `power-marl`, `workers/ml-training` | gold `district-flex-<case_id>` (029) | **sin código**; datos del piloto pendientes de lector — **spec creada** |
| **008** | LLM local + RAG + herramientas | `power-agents`, `power-graphrag` | corpus y trazas (029) | **sin código**; corpus inexistente — **spec creada** |
| **009** | industrialización | `infra/`, `apps/control-api` | — | no iniciado: sin auth, jobs en memoria — **spec creada** |
| 010–014 | grafo, P2P, ledger, mercado, GraphRAG | `power-graph/p2p/ledger/market/graphrag` | — | scaffold (helpers mínimos) |
| 015 | skills/MCP | `.agents`, `connectors`, `tools/mcp` | — | operativo en modo lectura |
| 020–025 | regulación PIT/PIDE, PMBOK, UI regulatoria | `power-regulation` | `config/regulations` | registro documental; los cálculos no se han iniciado |
| 026–027 | PIDE metodológico y auditoría | `power-regulation` | fuentes PIDE | parcial: anualidad ilustrativa y bloqueos |
| 029 | fundación de datasets por caso | `power-config.cases`, `power-sciml.quality`, `scripts/datasets` | registro v2 | piloto: 5 fuentes aprobadas, 7 pendientes de lector, 2 de restauración |

## 4. Pipelines de datos por capacidad

### 4.1 VNR-GIS → ElectricalSnapshot (001, prerrequisito de 006)

El esquema VNR-GIS es un formato estándar de las distribuidoras peruanas: el adaptador es por formato y versión, no por empresa. Relevado sobre una base VNR ya restaurada en la instancia local (solo metadatos); las cifras se confirmarán sobre el backup del caso piloto al restaurarlo:

| Elemento VNR | Tabla y campos | Uso | Brecha |
|---|---|---|---|
| Alimentador MT | `mtSalida` (`CodSalidaMT`, `CodSet`, `CodTenNomi`, `MaxDemRegistrada`) | slack y demanda de cabecera | código de tensión → kV por tabla de códigos |
| Tramo MT | `mtTramo` (`CodTramoMTPadre`, `Longitud`, `CodNorma`, `CodTipoCircuito`) | líneas; conectividad explícita padre → hijo (raíz = padre `'0'`) | **no hay R/X**: `CodNorma` solo describe material y sección ("AA 3x10 mm2") |
| Geometría | `verTramoMT` (vértices UTM) | GIS (003), no conectividad | zona UTM/CRS no declarada en la base |
| SED MT/BT | `Sed` (`PotInstalada`, `MaxDemTotal`, `CodSalidaMT`) | cargas agregadas y trafos | sin P/Q ni perfil horario; sin impedancia de trafo |
| Equipos | `mtEquipo` (`CodEstadoOperacion` NC/NA) | interruptores y estado | NA/NC → `closed` por regla documentada |
| BT | `btTramo`, `btSalida`, `Suministro` | red secundaria | fuera del primer corte |

Calidad observada: 15 304 tramos MT, 92 alimentadores, 106 raíces (hay alimentadores con varias raíces o islas: control G1/G2), 42 normas de conductor y 6 SED sin demanda.
Regla: el mapeo `CodNorma` → conductor del catálogo y la geometría (DMG) se registran como tabla versionada con fuente. Lo que no se pueda mapear va a cuarentena y no se completa por defecto.

### 4.2 Capa PINN / GNN sustituto (006)

Objetivo: un **aproximador rápido** del flujo de potencia y del estado de la red (tensiones y cargabilidad) para cribar miles de escenarios: planificación, MADRL y nueva carga. Nunca reemplaza al solver propio (ADR-0002).

```text
redes reales TXT (CYME ASCII) + MDB + VNR-GIS (001) ──► snapshots por alimentador
     (topología real; R/X del catálogo real BD_Equipo mapeado a CodNorma; IEEE solo valida el motor)
     │
     ├─► generador de escenarios (029): demanda por SED = MaxDemTotal × perfil (forecast gold)
     │     × factor de potencia declarado como supuesto de escenario; cambios de topología N-1
     ▼
solver propio (004-A) ──► etiquetas: V, ángulo, I, pérdidas, convergencia (descarta no convergentes)
     ▼
dataset gold `vnr-pf-scenarios` (grafo por muestra + etiquetas + hash de snapshot)
     ▼
entrenamiento GNN con pérdida física (residuo de balance de potencia AC sobre la Y-bus propia)
     ▼
validación: error en p.u. por nodo, residuo KCL, OOD por alimentador no visto; contraste
en una muestra por pandapower/solver propio; el modelo solo prioriza, el solver confirma
```

Decisiones de experto incorporadas:

- **Split por alimentador, no aleatorio.** Si un mismo alimentador aparece en train y en test, el modelo memoriza la topología. Los 92 alimentadores se dividen en grupos disjuntos para estimar el error fuera de distribución.
- **La pérdida física se calcula con la Y-bus del dominio propio**, no con otra implementación paralela. Así el residuo se mide igual que en el solver.
- **"PINN" en sentido estricto** (resolver EDP con autodiferenciación) no aplica al flujo estacionario. Lo correcto aquí es un *GNN informado por la física* (residuo AC como regularizador) y, para dinámica, PINN de transitorios en una fase posterior. La spec 006 lo distingue para no prometer lo que el método no da.
- Dependencia de software: `torch` no está instalado; se necesita autorización para instalarlo (constitución: no instalar sin permiso).

### 4.3 MADRL (007)

`district-flex-<case_id>` (029; piloto construido con clientes importantes, medidores y exógenas reales de Electro Dunas; sin oráculo; splits por año) → entorno CityLearn → **acople a red**: cada edificio se asigna explícitamente a una barra del snapshot. Las violaciones de tensión o cargabilidad del solver (o del sustituto 006, confirmado por el solver) entran en la recompensa y en la restricción. Algoritmos de referencia: HAPPO, MAPPO, MASAC y MATD3 frente a una línea base basada en reglas. Ninguna política actúa sobre SCADA (spec 011 y constitución).

### 4.4 LLM (008)

No se preentrena ni se ajusta un modelo con datos de clientes. Hay tres activos:

1. **Corpus RAG** de normas, specs y ADR con fragmentos citables, licencia por documento y versión.
2. **Herramientas tipadas**: la CLI y la API (`study`, `new-load`, `alternatives`, `verify-evidence`).
3. **Trazas y evaluación generadas por el sistema**: las respuestas numéricas las produce el solver, no el LLM; las preguntas sin fuente esperan "no fundamentado".

El ajuste fino (SFT/LoRA) de un modelo local solo se hace sobre las trazas de herramientas, y solo si la evaluación muestra una mejora frente a RAG + tool calling.

### 4.5 Forecast de demanda (insumo de 006 y 007)

`feeder-load-15min-<case_id>` gold (piloto: medidores P/Q 2023‑2026, líneas L‑6605/6606 y cabeceras de Electro Dunas, con las exógenas aprobadas de Ica) → `unitesis_sciml.datasets` (ya operativo: splits cronológicos con hueco y manifiesto) → modelos base (persistencia estacional, CatBoost de Prodma adaptado) → perfiles para los escenarios de 006/007.

## 5. Ruta crítica (orden obligatorio)

1. **004-B1 Newton-Raphson y Y-bus compartida**: hecho (benchmark IEEE 33 radial y mallado).
2. **001 lectores de redes reales**: TXT CYME ASCII (fuente ya auditada: 96 alimentadores), luego MDB (requiere lector Access autorizado) y VNR-GIS (restaurar el `.bak`). Incluye el mapeo `BD_Equipo` ↔ `CodNorma` para la R/X real.
3. **004-B2 transformadores**, necesarios para alimentadores reales MT/BT.
4. **029 autorización y datos gold** (medidores, perfiles, pronósticos causales).
5. **006 GNN informado por la física** entrenado con las redes reales del caso; **007 MADRL** acoplado a red; **005 expansión**: el sustituto criba y el solver confirma.
6. **008 LLM** con citas y herramientas; **009 industrialización** antes de cualquier uso compartido.

## 6. Reglas de sincronización (una fuente de verdad por concepto)

| Concepto | Fuente única | Prohibido |
|---|---|---|
| Identidad eléctrica | `ElectricalSnapshot.content_sha256` (v2) | usar `NetworkSnapshot` v1 (legado, retirada en T004-A4) como identidad de estudio |
| Topología | `power-topology` sobre el snapshot | inferir conectividad por proximidad GIS (ADR-0003) |
| Parámetros de conductor | `config/catalogs/conductors/*.json` con fuente | defaults, o R/X dentro de redes neuronales |
| Datos de entrenamiento | manifiestos gold de la spec 029 por `case_id` | entrenar con archivos sueltos; mezclar casos o referencias de método |
| Supuestos locales | `config/cases/` + perfiles por jurisdicción | constantes de país o empresa en el código |
| Resultado eléctrico | solver propio + contraste + evidencia | resultados de GNN, MADRL o LLM sin confirmación |
| Estado de capacidades | esta matriz (§3) + `tasks.md` de cada spec | README o planes que contradigan la matriz |
