---
status: approved
---
<!-- Target: docs/03.specs/docs-taxonomy-agent-first-migration/spec.md -->

# Docs Taxonomy and AI Agent-first Contract Migration Specification

## Overview (KR)

이 문서는 `hy-home.docker`의 문서 taxonomy를 `01.requirements`부터 `05.operations`까지의 새 canonical 구조로 이관하고, AI Agent-first Engineering 계약을 같은 경로 체계에 맞추는 작업의 기술 명세다.

## Strategic Boundaries & Non-goals

- 이 명세는 문서 경로, governance routing, validator 계약, runtime catalog 용어를 다룬다.
- Docker Compose runtime 동작, secret 값, credential, 배포 절차는 변경하지 않는다.
- 구 경로 redirect 문서는 만들지 않는다.

## Related Inputs

- **Requirements**: [../../01.requirements/README.md](../../01.requirements/README.md)
- **Architecture**: [../../02.architecture/README.md](../../02.architecture/README.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)

## Contracts

- **Docs Taxonomy Contract**: active stage 문서는 `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates` 아래에만 둔다.
- **Operations Contract**: guide, policy, runbook, incident 문서는 `docs/05.operations/{guides,policies,runbooks,incidents}`로 분리한다.
- **Agent Governance Contract**: root shim은 thin하게 유지하고 세부 정책은 `docs/00.agent-governance/`와 runtime mirror에 둔다.
- **Validation Contract**: `check-repo-contracts.sh`와 `check-doc-traceability.sh`가 새 taxonomy와 runtime agent/function catalog를 강제한다.

## Core Design

- 기존 stage 파일은 새 경로로 이동한다.
- legacy consolidated operations 문서는 소비 목적에 따라 `guides`, `policies`, `runbooks`로 나눈다.
- `docs/README.md`는 새 taxonomy SSOT이며, 과거 경로는 migration map으로만 설명한다.
- `docs/99.templates`는 기존 template 파일명을 유지하되 target examples를 새 경로로 맞춘다.

## Guardrails

- Secret values, private keys, tokens, auth files, shell history, credential logs are out of scope.
- Graphify remains advisory when contaminated or unavailable.
- `.claude/settings.json` remains team config; `.claude/settings.local.json` remains personal-only.
- GitHub-native instruction layers remain out of scope.

## Verification

```bash
bash -n scripts/*.sh scripts/lib/*.sh .claude/hooks/*.sh
python3 -m json.tool .claude/settings.json
python3 -m json.tool .codex/hooks.json
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/knowledge/report-graphify-health.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: old active taxonomy references are absent except the explicit migration map in `docs/README.md`.
- **VAL-SPC-002**: repository contract and doc traceability gates pass under the new taxonomy.
- **VAL-SPC-003**: Docker Compose validation remains unchanged and passes.
- **VAL-SPC-004**: Graphify health is reported as advisory when contaminated, not promoted to a hard gate.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md](../../04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md)
- **Tasks**: [../../04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md](../../04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md)
- **Operations Policy**: [../../05.operations/policies/harness-agent-first-engineering.md](../../05.operations/policies/harness-agent-first-engineering.md)
