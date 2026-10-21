# Política GitHub Flow + Spec Kit

`main` siempre protegido. Ramas cortas `NNN-nombre-descriptivo`, p.ej. `001-vnrgis-ingestion`; PR pequeño y vinculado a `specs/NNN-*/`.

CI requeridas: `scaffold`, `unit`, `contract`, `security` (las últimas tres se activan por etapas reales), sin aprobar scripts de ingeniería ficticios. Habilitar reglas de protección en GitHub, no en Git local: revisión obligatoria, sin force-push, estado CI requerido, protección de CODEOWNERS cuando se definan equipos reales.

Se recomienda Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`) y versionado SemVer a partir del primer release verificable.
