# ADR-0001: monolito modular de control y workers científicos independientes

- **Estado:** Aceptada como objetivo, pendiente de validación operacional
- **Contexto:** plataforma multidominio GIS / G-T-D / SciML / LLM con modelos eléctricos que requieren reproducibilidad.
- **Decisión:** control en monolito modular hexagonal; trabajos pesados aislados por cola/workflow; APIs y contratos versionados.
- **Descartado por ahora:** microservicios independientes por cada bounded context; Kafka por defecto; un proceso monolítico que aloje UI, GPU y simuladores.
- **Consecuencias:** integración simple, menos fallas distribuidas al comienzo; workers independientes y observabilidad por job; la extracción a servicios sigue siendo posible.
- **Criterio para revisar:** pruebas de rendimiento, aislamiento de fallas y costos de mantenimiento de G3.
