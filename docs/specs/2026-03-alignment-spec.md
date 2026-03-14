# 2026-03 Alignment Specification

> **layer:** product

**Overview (KR):** 구체적인 트리거 명칭과 파일 경로를 확정합니다.

## Mapping Table

| Intent | Root Marker | Target Rule File |
| :--- | :--- | :--- |
| Refactor | `[LOAD:RULES:REFACTOR]` | `docs/agentic/rules/refactor-rule.md` |
| Docs | `[LOAD:RULES:DOCS]` | `docs/agentic/rules/doc-maintenance-rule.md` |
| Infra | `[LOAD:RULES:INFRA]` | `docs/agentic/rules/lifecycle-rule.md` |
| Persona | `[LOAD:RULES:PERSONA]` | `docs/agentic/rules/persona-rule.md` |
| Ops | `[LOAD:RULES:OPS]` | `docs/agentic/rules/governance-rule.md` |

## Forbidden Paths

- `docs/plans/` (Must be `docs/plans/`)
- `docs/operations/incidents/subdir/` (Must be flat)

## Mandatory Metadata

```yaml
---
layer: <layer_name>
---
```

Must be the first lines of every file.
