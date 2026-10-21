# VNR-GIS: formato universal recuperado (REA, ADR-0012)

**Qué es:** el sistema de información que Osinergmin entrega a **todas** las concesionarias de distribución para el Valor Nuevo de Reemplazo (Ley de Concesiones Eléctricas, art. 77; *Guía de Elaboración del VNR*, Res. 232-2017-OS/CD). Cada empresa entrega un respaldo SQL Server con el mismo esquema, así que el lector de UNITESIS es **por versión del esquema, no por empresa**.

**Fuente analizada:** respaldos del caso `pe-ica-electrodunas`, corte abril 2024 (`ELDU_VNR_24_APR.bak` y `paramVNRGISELDU_24_APR.bak`), restaurados en bases nuevas de solo lectura (`unitesis_adapters.vnrgis_sql.restore_readonly`). Se registran el SHA-256 de cada `.bak` y su cabecera.

## Esquema (versión del respaldo: nivel de compatibilidad 100, intercalación `Modern_Spanish_CI_AS`)

| Base | Tablas | Con filas | Claves foráneas |
|---|---|---|---|
| VNR (red) | 75 | 51 | 62 |
| Parámetros | 24 | 20 | 13 |

Tablas que usa el lector MT (`vnrgis_reader.TABLES`):

| Tabla | Uso | Campos |
|---|---|---|
| `mtSalida` | alimentador MT y su tensión | `CodSalidaMT`, `CodTenNomi`, UTM de cabecera |
| `mtTramo` | tramos MT; árbol por `CodTramoMTPadre` (raíz `'0'`) | `CodNorma`, `Longitud` (m), `CodTenNomi`, `EstadoVnr` |
| `mtNodoEnlace` | nodo donde se conecta cada SED | `CodTramoMT`, `CodSed` |
| `Sed` | demanda de cada subestación de distribución | `MaxDemTotal` (kW), `PotInstalada` (kVA) |
| `mtEquipo` | maniobras MT | `CodEstadoOperacion` (NA/NC) |
| `verTramoMT` | vértices UTM de cada tramo (solo geometría) | `SecVertice`, `UTMEste`, `UTMNorte` |

La base de parámetros aporta las tablas oficiales de códigos (`cfgTablaCodigo`: ESTADO_VNR, ESTADO_OP_EPS, NIV_TENSION…), el diccionario de normas (`admCodigosNorma`, 9 644 códigos con descripción) y el diccionario de tablas del sistema (`cfgDiccionarioTabla`).

## Reglas recuperadas con evidencia

| Regla | Evidencia |
|---|---|
| `Longitud` en metros | tramo más largo: 23 240,5 m frente a 23 241,7 m de su polilínea UTM |
| `CodTenNomi`: D = 10 kV, G = 22,9 kV | 95 salidas emparejadas con alimentadores CYME por código; 69 + 26 observaciones, 0 conflictos (`infer_code_mapping`) |
| `CodNorma` = material + sección (mm²) + n.º de conductores (`AA05003` = AA 3×50 mm²) | `admCodigosNorma.Descripcion` |
| R/X: catálogo CYME con clave `CodNorma` + letra de tensión (`AA05003D`) | 55 códigos del catálogo cumplen el patrón. La R/X **sí** cambia entre D y G (p. ej. AA12003: 0,2828 frente a 0,349 Ω/km), así que no se sustituyen |
| `EstadoVnr` E/M/N incluidos; P (proyectado) y X (eliminado) excluidos | `cfgTablaCodigo` ESTADO_VNR |
| `NA` abre el tramo de su equipo | `cfgTablaCodigo` ESTADO_OP_EPS (68 NA, 2 461 NC) |
| Laterales de 1 o 2 conductores: VNR **no** indica qué fases usan | alimentadores en cuarentena (no se adivina la fase) |
| Factor de potencia de SED: 0,97 | VNR no lo trae; es el valor uniforme del estudio CYME del caso (modelado, no medido) |

## Resultado sobre el caso piloto

- 95 alimentadores leídos; 6 validados y 6 resueltos con Newton-Raphson.
- La longitud total coincide **exactamente** con CYME en 5 de 6 alimentadores (p. ej. SC215: 16,806 km).
- Los demás quedan en cuarentena por dos motivos: códigos `CodNorma` + tensión sin impedancia en el catálogo, y laterales de 1 o 2 conductores sin fase declarada.

## Hallazgos de calidad del catálogo CYME (para el propietario)

`catalogue_plausibility` encontró 10 familias donde la resistencia **no** disminuye al aumentar la sección, todas en la letra D (10 kV). Ejemplos: `AA01602D`, `AA02502D` y `AA03502D` comparten 1,0891 Ω/km; `AA12003D` = 0,2828 < `AA12503D` = 0,3062. Esos valores también los usan los estudios CYME y el dataset del GNN (spec 029). **No se corrigen**: deben confirmarse con el propietario o reemplazarse por una fuente de fabricante.
