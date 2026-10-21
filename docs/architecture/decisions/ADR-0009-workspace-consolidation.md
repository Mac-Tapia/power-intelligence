# ADR-0009 — Consolidación por contratos y evidencia

Fecha: 20/10/2026. Estado: propuesta documentada; implementación pendiente. Reafirma ADR-0001/0002/0004, no los sustituye.

## Contexto

El núcleo es scaffold con auxiliares; los proyectos vecinos contienen funciones valiosas y también contratos, runtimes y supuestos incompatibles. El hash actual solo representa equipos. La comparación de flujos puede aprobar resultados vacíos y el pipeline donante no exige cobertura de líneas ni calidad de catálogo como condición de `production_ready`. El informe del spec 028 separa reproducciones de observaciones estáticas.

## Decisión

Mantener monolito modular y workers por puertos; extracción gradual con source/hash/licencia/destino/cambios/tests. Evolucionar snapshot a v2, preservar identidad de fuente y escenario, y distinguir convergencia, cobertura, contraste, persistencia/relectura y aceptación. `power-topology` conserva propiedad física; proyecciones y grafos de mercado/comunicación/conocimiento no compiten por ella.

La primera capacidad prevista es radial equilibrada con catálogo explícito, referencia independiente y CLI auditable. No satisface por sí sola G3 trifásico. Se conservan fuentes únicas hasta verificar sustitución; cachés y duplicados de contexto prescindible pueden eliminarse bajo AC-028-01. No hay dependencia productiva de carpetas hermanas.

## Alternativas y consecuencias

Copiar aplicaciones completas acelera una demostración pero arrastra defaults y duplica autoridad. Convertir cada proyecto en servicio conserva heterogeneidad y añade operación antes de medirla. Reescribir todo descarta aportes sin evidencia. La extracción elegida exige más trabajo inicial de contratos y pruebas; deja motores propietarios en workers compatibles y retrasa UI/MARL hasta disponer de un recorrido físico verificable.

## Sustento y verificación

Spec: `specs/028-workspace-consolidation/spec.md`; tareas y evidencia en la misma carpeta. Faustino (maestría, 2021) sustenta evaluar costos por etapa; Gamvrinos (maestría, 2020) y Ragkhitwetsagul (doctorado, 2018) sostienen revisión de clones; Thwe et al. (IEEE Access indexado, 2025) trata interoperabilidad/fidelidad. Enlaces y límites de consulta en research.md del spec. La decisión es local, no una validación experimental de esas fuentes.
