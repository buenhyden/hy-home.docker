---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md -->

# Task: Docs Taxonomy and AI Agent-first Contract Migration

## Overview (KR)

이 문서는 새 docs taxonomy와 AI Agent-first 계약 정렬 작업의 구현 및 검증 evidence를 추적한다.

## Inputs

- **Parent Spec**: [../../03.specs/docs-taxonomy-agent-first-migration/spec.md](../../03.specs/docs-taxonomy-agent-first-migration/spec.md)
- **Parent Plan**: [../plans/2026-05-10-docs-taxonomy-agent-first-migration.md](../plans/2026-05-10-docs-taxonomy-agent-first-migration.md)

## Working Rules

- 구 경로 redirect 파일은 만들지 않는다.
- secret 값, token, credential, private key 원문은 읽지 않는다.
- Graphify는 advisory evidence로만 사용한다.
- `.claude` runtime mirror와 governance catalog parity는 유지한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Move active docs into the new taxonomy | doc | Core Design | PLN-001 | `find docs -maxdepth 3 -type d` | Codex | Done |
| T-002 | Split operations docs into guides, policies, runbooks, incidents | doc | Operations Contract | PLN-002 | `find docs/05.operations -maxdepth 3 -type f` | Codex | Done |
| T-003 | Update governance, runtime, template, and infra references | doc | Agent Governance Contract | PLN-003 | stale-reference scan | Codex | Done |
| T-004 | Update repository validators | test | Validation Contract | PLN-004 | `check-repo-contracts.sh`, `check-doc-traceability.sh` | Codex | Done |
| T-005 | Run final verification bundle | test | Verification | VAL-PLN-* | command outputs in conversation | Codex | Done |

## Verification Summary

- **Test Commands**:
  - `bash -n scripts/*.sh scripts/lib/*.sh .claude/hooks/*.sh`
  - `python3 -m json.tool .claude/settings.json`
  - `python3 -m json.tool .codex/hooks.json`
  - `bash scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/validation/validate-docker-compose.sh`
  - `bash scripts/validation/check-template-security-baseline.sh`
  - `bash scripts/validation/check-quickwin-baseline.sh`
  - `bash scripts/hardening/check-all-hardening.sh`
  - `bash scripts/knowledge/report-graphify-health.sh`
  - `git diff --check`
  - local Markdown link scan excluding templates and inline command regex
- **Eval Commands**: not applicable
- **Logs / Evidence Location**: this task document and conversation command outputs
- **Result**: all verification commands passed; Graphify reported `status=advisory` because of known runtime-volume and gitlink contamination.
- **Graphify Refresh**: skipped because `graphify` was not available on `PATH`.
