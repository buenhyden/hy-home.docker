---
status: draft
---

# Task: Infra / Secrets / Docs Refresh

## Overview (KR)

이 문서는 infra/secrets/docs 운영 문서 최신화 작업의 실행 단위와 검증 증거를 기록한다. 작업은 문서 보강에 한정하며 Docker Compose runtime과 secret 값 파일은 변경하지 않는다.

## Inputs

- **Parent Spec**: [../04.specs/infra-secrets-docs-refresh/spec.md](../04.specs/infra-secrets-docs-refresh/spec.md)
- **Parent Plan**: [../05.plans/2026-05-09-infra-secrets-docs-refresh.md](../05.plans/2026-05-09-infra-secrets-docs-refresh.md)

## Working Rules

- Documentation-only work still needs validation evidence.
- Secret value files under `secrets/**/*.txt` must not be opened or copied.
- Existing document content should be preserved unless it is unsafe or stale.
- Runtime files are analysis inputs only unless a separate user approval changes scope.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create spec/plan/task documents for this refresh | doc | Contracts | PLN-001 | Stage docs include template sections | Codex | Done |
| T-002 | Refresh root, docs, and secrets README files | doc | Core Design | PLN-002 | README heading audit missing=0 | Codex | Done |
| T-003 | Align target README files under infra/docs/90 with base template headings | doc | Interfaces | PLN-003 | README heading audit missing=0 | Codex | Done |
| T-004 | Align guide/operation/runbook/reference docs with their templates | doc | Interfaces | PLN-004 | Stage heading audit missing=0 | Codex | Done |
| T-005 | Run repository validation commands and record results | test | Verification | PLN-005 | Command output summary recorded below | Codex | Done |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [x] T-001 Create spec/plan/task documents.
- [x] T-002 Refresh root, docs, and secrets README files.

### Phase 2

- [x] T-003 Align target README files.
- [x] T-004 Align stage documents.

### Phase 3

- [x] T-005 Run validation and capture evidence.

## Verification Summary

- **Test Commands**:
  - `bash scripts/check-repo-contracts.sh`
  - `bash scripts/check-doc-traceability.sh`
  - `bash scripts/validate-docker-compose.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-quickwin-baseline.sh`
  - `bash scripts/check-all-hardening.sh`
  - `git diff --check`
- **Eval Commands**:
  - README heading audit over `infra`, `secrets`, `docs/07.guides`, `docs/08.operations`, `docs/09.runbooks`, `docs/90.references`
  - Stage heading audit over non-README Markdown in `docs/07.guides`, `docs/08.operations`, `docs/09.runbooks`, `docs/90.references`
- **Logs / Evidence Location**:
  - `README_HEADING_GAPS=0`
  - `STAGE_HEADING_GAPS=0`
  - `MARKDOWN_LINK_GAPS=0`
  - `bash scripts/check-repo-contracts.sh`: `failures=0`
  - `bash scripts/check-doc-traceability.sh`: `failures=0`
  - `bash scripts/validate-docker-compose.sh`: `Docker Compose validation passed. services_total=5`
  - `bash scripts/check-template-security-baseline.sh`: pass
  - `bash scripts/check-quickwin-baseline.sh`: pass
  - `bash scripts/check-all-hardening.sh`: pass
  - `git diff --check`: pass
