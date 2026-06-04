---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md -->

# Task: LLM Wiki Agent-first Completion

## Overview (KR)

이 문서는 LLM Wiki generator, generated index, `wiki-curator`, 운영 가이드, validator 강제력 구현 작업을 추적한다.

## Inputs

- **Parent Spec**: [../../03.specs/llm-wiki-agent-first-completion/spec.md](../../03.specs/llm-wiki-agent-first-completion/spec.md)
- **Parent Plan**: [../plans/2026-05-10-llm-wiki-agent-first-completion.md](../plans/2026-05-10-llm-wiki-agent-first-completion.md)

## Working Rules

- Keep root shims thin.
- Do not add public wiki behavior, `llms-full.txt`, external model calls, Graphify authority, or Docker runtime changes.
- Treat `docs/90.references/llm-wiki/index.md` as a generated tracked repo-local path index.
- Record verification evidence before marking this task done.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add generator and generated index | impl | Contracts | PLN-001 | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` passed | wiki-curator | Done |
| T-002 | Add mirrored `wiki-curator` role | impl | Agent Role & IO Contract | PLN-002 | `bash scripts/validation/check-repo-contracts.sh` passed | wiki-curator | Done |
| T-003 | Add maintenance guide and reference links | doc | Prompt / Policy Contract | PLN-003 | `bash scripts/validation/check-doc-traceability.sh` passed | doc-writer | Done |
| T-004 | Strengthen repo validator | test | Guardrails | PLN-004 | repo contract enforces stale/missing LLM Wiki pieces | wiki-curator | Done |
| T-005 | Record final evidence | ops | Verification | PLN-005 | validation bundle completed | doc-writer | Done |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`
- `guardrail`

## Phase View

### Phase 1

- [x] T-001 Add generator and generated index
- [x] T-002 Add mirrored `wiki-curator` role

### Phase 2

- [x] T-003 Add maintenance guide and reference links
- [x] T-004 Strengthen repo validator

### Phase 3

- [x] T-005 Record final evidence

## Verification Summary

- **Test Commands**: `bash -n scripts/*.sh scripts/lib/*.sh .claude/hooks/*.sh`; `python3 -m json.tool .claude/settings.json`; `python3 -m json.tool .codex/hooks.json`; `bash scripts/validation/check-repo-contracts.sh`; `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/validate-docker-compose.sh`; `bash scripts/validation/check-template-security-baseline.sh`; `bash scripts/validation/check-quickwin-baseline.sh`; `bash scripts/hardening/check-all-hardening.sh`; `git diff --check`
- **Eval Commands**: `bash scripts/knowledge/generate-llm-wiki-index.sh --check`; H100/source-label scan; stale taxonomy scan
- **Logs / Evidence Location**: This task file and `docs/00.agent-governance/memory/progress.md`

## Related Documents

- [Spec](../../03.specs/llm-wiki-agent-first-completion/spec.md)
- [Plan](../plans/2026-05-10-llm-wiki-agent-first-completion.md)
- [Maintenance Guide](../../05.operations/guides/90-knowledge/llm-wiki-maintenance.md)
- [LLM Wiki References](../../90.references/llm-wiki/README.md)
