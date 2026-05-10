---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md -->

# Docs Taxonomy and AI Agent-first Contract Migration Plan

## Overview (KR)

이 문서는 문서 taxonomy와 AI Agent-first 계약을 새 canonical 경로로 이관하는 실행 계획이다. 목표는 Docker runtime을 바꾸지 않고 docs SSOT, validator, runtime mirror 용어를 한 번에 맞추는 것이다.

## Context

기존 저장소 계약은 legacy requirements, execution, operations stage 이름을 문서, templates, validators, runtime docs에 고정하고 있었다. 새 계약은 더 짧은 active stage와 목적별 operations 하위 폴더를 사용한다.

## Goals & In-Scope

- 문서 파일을 새 taxonomy로 이동한다.
- governance, provider, runtime, template, infra README 링크를 새 경로로 갱신한다.
- validators를 새 taxonomy와 runtime agent/function catalog 기준으로 갱신한다.
- migration evidence를 새 taxonomy 안에 남긴다.

## Non-Goals & Out-of-Scope

- Docker Compose runtime 동작 변경
- secret 값 또는 credential 파일 분석
- GitHub-native instruction layer 추가
- Graphify advisory 상태를 hard gate로 승격

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Move stage docs to the new taxonomy | `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations` | REQ-TAX-001 | top-level docs contract passes |
| PLN-002 | Split operations docs by purpose | `docs/05.operations/{guides,policies,runbooks,incidents}` | REQ-OPS-001 | service coverage and traceability pass |
| PLN-003 | Update governance and runtime references | `docs/00.agent-governance`, `.claude`, `.codex`, `.github`, `infra` | REQ-AGENT-001 | stale-reference scan passes |
| PLN-004 | Update validators | `scripts/check-repo-contracts.sh`, `scripts/check-doc-traceability.sh` | REQ-VAL-001 | validators pass |
| PLN-005 | Record migration evidence | this plan, spec, task evidence | REQ-EVD-001 | evidence docs exist and link back |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Syntax | Bash and JSON syntax | `bash -n ...`; `python3 -m json.tool ...` | exit 0 |
| VAL-PLN-002 | Contract | Repository docs/runtime contract | `bash scripts/check-repo-contracts.sh` | failures=0 |
| VAL-PLN-003 | Traceability | Execution to operations links | `bash scripts/check-doc-traceability.sh` | failures=0 |
| VAL-PLN-004 | Runtime | Docker Compose config remains valid | `bash scripts/validate-docker-compose.sh` | pass |
| VAL-PLN-005 | Advisory graph | Graphify state reported | `bash scripts/report-graphify-health.sh` | status reported |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Relative links break during moves | High | Run stale-reference scans and validators after migration |
| Validator passes stale taxonomy | High | Update allowed docs, stale regex, coverage and traceability checks together |
| Operations split creates duplicate SSoT | Medium | Do not require every service to have all guide/policy/runbook documents |
| Graphify output is contaminated | Low | Keep Graphify advisory and corroborate against tracked files |

## Completion Criteria

- [x] Scoped migration completed
- [x] Validators pass under the new taxonomy
- [x] Docker Compose validation still passes
- [x] Graphify advisory status reported

## Related Documents

- **Spec**: [../../03.specs/docs-taxonomy-agent-first-migration/spec.md](../../03.specs/docs-taxonomy-agent-first-migration/spec.md)
- **Task Evidence**: [../tasks/2026-05-10-docs-taxonomy-agent-first-migration.md](../tasks/2026-05-10-docs-taxonomy-agent-first-migration.md)
- **Docs Index**: [../../README.md](../../README.md)
