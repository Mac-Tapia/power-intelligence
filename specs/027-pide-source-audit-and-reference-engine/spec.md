# 027 — Auditoría de Anexo PIDE y motor de referencia

## User stories
- Como ingeniero necesito aplicar un protocolo de distribución documentado por fuentes y ver su naturaleza no vinculante.
- Como regulador/auditor necesito saber qué viene del TDR 2018 frente al anexo MINEM 2017.
- Como agente IA necesito 15 placeholders de formatos cuya oficialidad permanezca bloqueada hasta auditar el PDF de origen.

## Acceptance scenarios
- Given perfil histórico 2018, when hay menos de 3 opciones, then no satisface integridad documental.
- Given cualquier perfil prepublicado, when se solicita certificación, then error bloqueante.
- Given alternativa declarada viable sin solver independiente, then queda evidencia incompleta.
- Given costos/tasa/vida explicitados, when se calcula anualidad, then salida etiqueta `illustrative`.
- Given empresa diferente, when aplica un estudio corporativo, then no hereda 20/4 ni tres opciones por defecto.
- Given PDF original, when se registra, then se calcula SHA real y NO se certifica hasta revisión humana.
