# CYME ASCII: estructura recuperada (REA, ADR-0012)

**Fuente analizada:** export `eldu-cyme-ascii-2026-08` del caso `pe-ica-electrodunas` (red, cargas y catálogo de equipos). El perfil completo es evidencia local (`local-data/evidence/format-profile-eldu-cyme-ascii.json`). La estructura sin valores está en [`cyme-ascii-structure.json`](cyme-ascii-structure.json).
**Comando:** `python scripts/unitesis.py profile-export --network … --loads … --equipment … --output … --structure-output …`

## Códigos recuperados

| Campo | Recuperado contra | Resultado | Evidencia |
|---|---|---|---|
| `CUSTOMER LOADS.Phase` | `SECTION.Phase` del tramo de la carga | **determinista**, máscara de bits A=1, B=2, C=4 (1=A, 3=AB, 5=AC, 6=BC, 7=ABC) | 7287 cargas, 0 conflictos; `SECTIONALIZER SETTING.EqPhase` coincide con la fase del tramo en 15 196 registros |
| `LOADS.Connection` | fase de la carga | un solo valor (`0`), usado también por 218 cargas en tramos **monofásicos**, donde una conexión delta es imposible: `0` = estrella | deducción lógica, no estadística; declarada en `config/cases/pe-ica-electrodunas.json` y pendiente de confirmación del propietario |

Los códigos 2 (B) y 4 (C) no aparecen solos en este export; la máscara se deduce de los cinco códigos observados, que la cumplen todos. Si un export futuro trae un código fuera de la máscara, el lector debe ponerlo en cuarentena.

## Información presente y no consumida (backlog)

| Sección y columnas | Filas | Uso previsto | Spec |
|---|---|---|---|
| ~~`CUSTOMER LOADS.Phase`, `LOADS.Connection`, `LINE.R0/X0/B0/B1`~~ | — | **consumidos desde 008-C3** (matrices por fase y cargas por fase) | 008-C3 hecho |
| `SUBSTATION` (R1, R0, KVLL, MVA, Conn) | 24 | impedancia equivalente de la fuente para cortocircuito y trifásico | 017, 008 |
| `CONCENTRIC NEUTRAL CABLE` (Dab, Dbc, Dac, NeutralWires, aislamiento) | 18 | geometría de cables subterráneos | 008-C3 |
| `LINE CONFIGURATION.Overhead` | 38 657 | separar aéreo y subterráneo | 001 |
| `HEADNODES` | 96 | verificación cruzada de las cabeceras | 001 |

## Secciones solo con plantilla

`CONDUCTOR`, `SPACING TABLE FOR LINE`, `LINE UNBALANCED`, `TRANSFORMER`, `REGULATOR`, `SHUNT CAPACITOR` y el resto de equipos traen una sola fila `DEFAULT` (o `DEFAULT` y `NONE`). No describen equipos reales: **no se usan como datos** y no se infiere geometría de ellas.
