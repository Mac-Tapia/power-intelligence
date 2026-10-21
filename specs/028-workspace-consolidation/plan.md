# Plan propuesto de integración 028

Estado: el usuario autorizó profundizar arquitectura, mejorar el spec y continuar limpieza justificada. Este bloque documental/diagnóstico se ejecuta; la implementación de capacidades se mantiene pendiente de sus contratos, pruebas y revisión. Proteger aportes únicos; aplicar política de eliminación de AC-028-01, no conservación absoluta de todos los archivos.

1. Registrar baseline y procedencia; definir historia/aislamiento del núcleo actualmente sin Git. Probar F01–F03 y A06 antes de corregirlos y dar empaquetado a economía/regulación.
2. Definir tipos neutrales, evolución del snapshot v1 a v2 y puertos. Pruebas negativas de números, referencias, parámetros, fases, estado de ramas e identidad antes de implementar.
3. Adaptar ingesta/custodia y evidencia persistida. Verificar hash estable, ausencia de defaults, corrupción y comparación por identidad de cargas/alimentador.
4. Integrar barrido radial y adaptador pandapower. Probar convergencia, balance, cobertura contra snapshot esperado y rechazo de redes no soportadas; reproducir F04/A05/A07 antes de adaptar comparador/modelo. Comparar contra referencia independiente instalada con tolerancias de spec.md; no afirmar G3 trifásico desbalanceado.
5. Conectar CLI y workflow. Probar fuente -> snapshot -> resultados -> archivo -> relectura y fallos; registrar commit y motores. No afirmar aprobación automática.
6. Revisión del conjunto, regresión, lint del código nuevo y actualización del mapa de aportes y README. Mantener el informe de diagnóstico como baseline previo a cambios.

Archivos previstos: nuevos módulos `network.py` en dominio; `power_flow.py` en puertos; ingesta neutral en adapters; solver radial y comparador en simulation; custodia/readback en evidence; caso de uso en application; `scripts/studies/run_reference.py`; fixtures y tests de integración/golden. Cambios compatibles en `models.py`, economía y regulación. No copiar imports de proyectos vecinos en producción.

Los siguientes módulos se habilitan por bloques comprobables, sin confundir selección de código con integración operativa: DGS/CYME, GIS/unifilar, forecasting, optimización, backends propietarios y MADRL.

## Riesgos que condicionan la extracción

| Riesgo observado | Tratamiento y evidencia |
|---|---|
| Hash de equipos usado como identidad eléctrica | Migración de esquema y pruebas de mutación de conexiones/cargas/fases/estados |
| Comparación vacía/incompleta/tolerancias inválidas | Cobertura contra modelo esperado, IDs únicos y números finitos |
| Defaults CYME/BFS trasladados como datos fuente | Cuarentena por campo y catálogo/unidades/CRS verificables |
| Runtimes 3.12/3.11/CYME incompatibles | Procesos y puertos versionados; no mezclar site-packages |
| Fork más nuevo pierde funciones exclusivas | Comparación por archivo, regresiones y licencia |
| Limpieza elimina contexto dinámico | No usar imports como prueba de inutilidad; journal y referencia retenida |
| Tests documentales se presentan como operación | Distinguir declarado, implementado, probado, ejecutado y aceptado |

No ejecutar correcciones masivas de lint ni suites RECYM que alteran catálogos. Ver tareas en `tasks.md` y evidencia/limitaciones en `architecture-review.md`.
