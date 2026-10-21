# Metodología de evaluación de alternativas — diseño UNITESIS

## Etapa técnica
- Caso base y cada alternativa mantienen snapshot de red, demanda, generación y año.
- Corre flujos AC, caídas de tensión, sobrecargas, cortocircuito y contingencias cuando aplican. Cada restricción registra fuente normativa, versión y fecha.
- Excluye alternativas inviables antes de la comparación económica.

## Función de costo PIT (R. 217-2013 original art. 11.3)

$$VP(C)=\sum_{t=0}^{T}\frac{I_t+O_t+M_t+L_t}{(1+r)^t}$$

En estudios PIT en norma base $T=10$ años; proyección demanda 30 años (art. 6.2.1), período inversiones 4 años (art. 10.2). El $L_t$ regulatorio requiere construir **diferencia de pérdidas vs referencia** tal como el art. 11.3 lo define, no simplemente pérdidas brutas. Costos de pérdidas de potencia/energía valorados a precios regulatorios aplicables. Los módulos de inversión deberán usar base vigente para período de precios y ubicaciones de costos. $r$ se obtiene del marco legal vigente, NO queda fijada numéricamente en el código.

## Funciones internas opcionales (no normativas por defecto)
- VAN/VPN financiero del promotor vs mínimo VP costo regulatorio (objetivos distintos).
- Beneficio/costo, TIR (cuando ingresos consistentes), recuperación descontada.
- ENS, penalizaciones de calidad, resiliencia, valor de opciones, demoras del cliente y distribuidora.
- Escenarios (demanda, PBI, geografía, módulos, costo de energía, tasas, cronograma) y Monte Carlo de distribuciones identificadas.

## Campos económicos obligatorios
Fuente de costos, moneda, base temporal, tipo de cambio, índice de actualización, tasa efectiva y su fuente, cronograma anual, potencia/energía de pérdidas separadas y método de valorización, impuestos si aplican, valor residual si autorizado, horizonte por norma, referencia de precios, resultado por alternativa y trazabilidad estadística.

**Demostración actual del scaffold**: función VP para flujos anuales con costos no negativos. No implementa reglas regulatorias de pérdidas incrementales, módulos, peajes ni CMA.
