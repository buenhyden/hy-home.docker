# Spec-0001: Documentation Taxonomy and Plural Migration
n**Overview (KR):** 문서 분류 체계 변경 및 복수형 경로 전환을 위한 기초 사양입니다.

- **Status**: Implementation
- **Scope**: master
- **layer:** architecture
- **Related PRD**: `[../prd/refactor-prd.md]`
- **Related Architecture**: `[../ard/2026-03-15-agentic-ard.md]`
- **Decision Record**: `[../adr/0002-doc-taxonomy.md]`

**Overview (KR):** 인프라 리포지토리의 모든 문서를 평탄화된 계층으로 재배치하고, 실행 관련 파일들의 경로를 복수형으로 통일하기 위한 기술적 세부 사항을 정의합니다.

## 1. Technical Baseline

The system uses `docker-compose.yml` include directives. Documentation must support this by being easily discoverable by both humans and agents.

## 2. Directory Mapping

| Alias      | Current Path           | Target Path                | Template                   |
| ---------- | ---------------------- | -------------------------- | -------------------------- |
| ADR        | `docs/adr/`            | `docs/adr/`                | `adr-template.md`          |
| ARD        | `docs/ard/`            | `docs/ard/`                | `ard-template.md`          |
| PRD        | `docs/prd/`            | `docs/prd/`                | `prd-template.md`          |
| Plan       | `docs/plans/`           | `docs/plans/`              | `plan-template.md`         |
| Spec       | `docs/spec/`           | `docs/specs/`              | `spec-template.md`         |
| Runbook    | `docs/runbook/`        | `docs/runbooks/`           | `runbook-template.md`      |
| Operations | `docs/operations/`     | `docs/operations/incidents`| `incident-template.md`     |

## 3. Metadata Contract

Every file MUST contain:

```yaml
---
layer: [core|agentic|entry|ops|meta|...]
---
```

## 4. Verification Plan

- **VAL-01**: `grep -r "docs/plans/" .` must return 0 hits for active functional links.
- **VAL-02**: `ls docs/plans/` should show all migrated plans.
