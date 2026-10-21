# Matriz de estudios para planificación de distribución con metodología PIDE (referencia 2017)

**Estado**: especificación de sistema, no funcionalidad construida, ni obligación normativa certificada.

| Fase | Entradas | Motor / algoritmo propuesto | Productos verificables | Gate |
|---|---|---|---|---|
| Inventario y calidad GIS | VNR-GIS/MDB/SQL/TXT, activos MT/BT | ETL, grafo terminal/fase, reglas QA | Red base georreferenciada, reporte faltantes | Ingeniería |
| Mercado eléctrico | Medidores 15min, clientes, demanda de nuevas cargas | Series temporales + espacial | Pronósticos P/Q/E por escenario; incertidumbre | Pronóstico validado |
| Diagnóstico | Red GIS y demanda histórica | Flujo de potencia AC trifásico, pérdidas, continuidad | Tensión, I, cargas, pérdidas, SAIDI/SAIFI con fuentes | Comparación de solver |
| Alternativas de largo plazo | Diagnóstico, crecimiento, política de expansión | Generador de variantes + búsqueda controlada | Conjunto de candidatos técnicos con topología independiente | Factibilidad |
| Cartera corto plazo | Plan de largo plazo y periodo seleccionado | Secuenciación presupuestaria | Proyectos y anualidades | Horizonte trazado |
| Evaluación técnica | Cada candidato / escena | Simulación y restricciones normativas seleccionadas | Resultado antes/después, violaciones, ENS | Sin soluciones inviables |
| Evaluación económica | CAPEX, O&M, pérdidas, fuentes de tarifas | Costos descontados, sensibilidad y ranking | Flujo anual, VP, coste total, incertidumbre | Auditoría económica |
| Priorización | Alternativas factibles + recursos disponibles | MILP/NSGA + revisión PMO | Cartera y justificación por alternativa | Comité humano |
| PMBOK6 / expediente | Cada proyecto seleccionado | Plantillas y aprobaciones | Acta, EDT, Gantt, presupuesto, riesgos, planos | Firma técnica/jurídica |

**Requisito especial:** ningún perfil de proyecto PIDE adopta por defecto tasas de descuento, umbrales, horizonte ni formatos del PIT R217. Los valores se ingresan por versión de fuente aprobada o aparecen claramente como `hypothesis`.
