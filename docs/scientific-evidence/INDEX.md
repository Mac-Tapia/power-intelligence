# Biblioteca científica consultable por agentes

**Fecha de compilación:** 17 de octubre de 2026.  
**Total de fichas individuales:** 191 archivos Markdown.  
**Naturaleza:** fichas analíticas originales con enlace a la fuente; **no son PDFs descargados ni artículos científicos completos**.  
**Verificación:** páginas detectadas en web durante esta investigación y referencias heredadas de V2 distinguidas explícitamente; **no se ha realizado lectura integral ni auditoría bibliométrica de todas las fuentes**.

## Regla de investigación
Un paper revisado por pares, un preprint, una tesis, un libro, una especificación técnica y un manual de software **no poseen la misma fuerza de evidencia**. Consultar siempre `verification`, `kind` y `full_text_reviewed` de cada ficha. Evitar DOI inventados, extrapolaciones de porcentajes de precisión, citas sin comprobar y reproducción no autorizada.

## Estadísticas verificadas del repositorio creado
- Fuentes nuevas con página o registro localizado en esta investigación: **106**.
- Referencias heredadas del catálogo V2 con revisión pendiente: **85**.
- Entradas de tipo académico potencial (incluye preprints y tesis sin arbitraje): **122**.
- Otras referencias técnicas/estándares/manuales: **69**.
- Universidades y organizaciones entre las fuentes: Google Research, Google DeepMind, Anthropic, Microsoft Research, TU Delft, Georgia Tech, DTU, UNESP, UNICAMP, RWTH Aachen, TUM, UPM, UC3M, Universidad de Edimburgo, entre otras.
- Idiomas cubiertos en registros: DE, EN, ES, FR, PT.

## Árbol
```text
docs/scientific-evidence/
  INDEX.md                       <- punto de entrada para todos los agentes
  MATRIX-MODULES.md              <- capacidades -> fichas -> evidencia
  BIBLIOGRAPHY.md                <- índice completo con enlaces
  PRIMARY-EVIDENCE-ANALYSIS.md  <- 12 casos prioritarios con aportes y pruebas
  LITERATURE-REVIEW-PROTOCOL.md  <- auditoría y revisión sistemática pendiente
  sources/                       <- 191 fichas Markdown individuales
  modules/                       <- 18 síntesis técnicas por dominio
  agent-queries/                 <- consultas sugeridas y playbooks
  catalog.json                   <- índice complementario (metadatos)
  UPDATED-REFERENCES.md          <- 21 fuentes prioritarias verificadas (21/10/2026) y estado del catálogo
  prioritized-references.json    <- las mismas fuentes prioritarias en formato estructurado
```

## Lectura obligatoria para cualquier agente
1. `AGENTS.md` y `.specify/memory/constitution.md`.
2. `docs/scientific-evidence/MATRIX-MODULES.md` y el resumen del dominio.
3. Un mínimo de 3 fichas de tipo académico **relacionadas** antes de elegir tecnología, además de la norma correspondiente.
4. Registrar una tabla «afirmación / evidencia / supuesto / prueba» en el `specs/<feature>/research.md`.
5. No introducir features en producción por respaldo de artículo sin benchmark reproducido.

## Atajos de búsqueda local
```powershell
python scripts/research/query_evidence.py --list-modules
python scripts/research/query_evidence.py --module sciml --kind articulo --limit 12
python scripts/research/query_evidence.py --query "state estimation" --limit 10
python scripts/research/validate_library.py
```

## Trazabilidad científica por módulo
- [Arquitectura empresarial y plataforma](modules/arch.md) · 56 fuentes vinculadas.
- [Persistencia, linaje y series temporales](modules/bk.md) · 12 fuentes vinculadas.
- [Frontend, experiencia GIS y unifilar](modules/fe.md) · 6 fuentes vinculadas.
- [GIS, adquisición y topología de redes](modules/gis.md) · 39 fuentes vinculadas.
- [Grafo físico y GNN](modules/graph.md) · 37 fuentes vinculadas.
- [Estudios eléctricos verificables](modules/solver.md) · 75 fuentes vinculadas.
- [Expansión, optimización y planificación](modules/op.md) · 59 fuentes vinculadas.
- [PINN, GNN y simuladores sustitutos](modules/sciml.md) · 46 fuentes vinculadas.
- [MADRL seguro y critic centralizado](modules/marl.md) · 15 fuentes vinculadas.
- [LLM local, orquestación y permisos](modules/llm.md) · 6 fuentes vinculadas.
- [GraphRAG y conocimiento técnico](modules/graphrag.md) · 6 fuentes vinculadas.
- [P2P federación segura](modules/p2p.md) · 13 fuentes vinculadas.
- [Blockchain permissioned y evidencia](modules/ledger.md) · 5 fuentes vinculadas.
- [Mercado P2P y flexibilidad (simulado)](modules/market.md) · 44 fuentes vinculadas.
- [Seguridad, gobierno y control de agentes](modules/security.md) · 11 fuentes vinculadas.
- [SDD, GitHub, skills y worktrees](modules/sdd.md) · 51 fuentes vinculadas.
- [MLOps, DevOps y observabilidad](modules/ops.md) · 47 fuentes vinculadas.
- [Pruebas de aceptación científica y de agentes](modules/qa.md) · 45 fuentes vinculadas.
