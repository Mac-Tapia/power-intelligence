# apps/workstation-web

Workstation de estudios servida por `control-api` en `/`. Cliente delgado en HTML/CSS/JS sin build (`public/`): no realiza cálculo eléctrico.

**Estado:** implementada para el alcance radial equilibrado:

- importar red (ejemplos incluidos o archivo JSON neutral), con motivos de cuarentena visibles;
- unifilar generado desde el snapshot, coloreado por tensión y cargabilidad; elementos abiertos y barras sin tensión diferenciados;
- flujo de potencia con contraste pandapower, tablas de barras/ramas y balance;
- nueva carga en escenario clonado con detección de violaciones (V < 0.95 pu, carga > 100 %);
- alternativas de conductor con base económica explícita, contraste independiente y ranking por VPN.

La versión React + TypeScript (GIS, grafo, copiloto) descrita en `docs/architecture/BACKEND-FRONTEND-BLUEPRINT.md` se crea con su spec (003/008).

Uso: `python scripts/unitesis.py serve` y abrir http://127.0.0.1:8000/.
