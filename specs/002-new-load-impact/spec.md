# 002 — Impacto de nueva carga en red de distribución

**Dependencias explícitas:** 001 + motor AC trifásico G3 validado + perfiles de carga autorizados + reglas normativas seleccionadas por jurisdicción/edición.

**Alcance:** clonar snapshot, asignar una nueva demanda real al nodo/equipo de conexión aprobado, simular antes/después y comparar cargabilidad, tensión por fase, pérdidas, capacidad remanente, alternativas y CAPEX/OPEX rastreables.

**Criterios de aceptación:** ningún `StudyResult` sin version de solver, convergencia, unidades, inputs hash y revisión; prohibido escribir en snapshot original; si faltan parámetros se rechaza la simulación con reporte; alternativas pasan validación física; nunca inventar valores de potencia por feeder.
