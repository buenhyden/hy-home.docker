---
status: completed
---

# LLM Wiki Agent-first Completion Plan

## Overview (KR)

이 문서는 `hy-home.docker` LLM Wiki를 생성·검증 가능한 repo-local path index로 보강하기 위한 실행 계획이다.

## Context

기존 agent-first/Harness-first 구조와 docs taxonomy migration은 완료되어 있다. 남은 gap은 LLM Wiki가 static entrypoint와 curated map에 머물러 있어 generator, generated index, explicit curator ownership, operations guide, validator freshness check를 제공하지 않는 점이다.

## Goals & In-Scope

- **Goals**: Add deterministic LLM Wiki generation, `wiki-curator` ownership, operations guidance, and validator enforcement.
- **In Scope**: `llms.txt`, `docs/90.references/llm-wiki/`, `docs/05.operations/guides/`, `.claude/agents/`, `docs/00.agent-governance/agents/`, `scripts/`.

## Non-Goals & Out-of-Scope

- **Non-goals**: Public wiki, `llms-full.txt`, external model call, Graphify publication, GitHub-native instruction layer.
- **Out of Scope**: Docker runtime behavior, secret contents, deployment workflow.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Add deterministic LLM Wiki generator and generated index | `scripts/generate-llm-wiki-index.sh`, `docs/90.references/llm-wiki/index.md` | VAL-SPC-001 | Generator and `--check` pass |
| PLN-002 | Add first-class `wiki-curator` role | `.claude/agents/`, `docs/00.agent-governance/agents/`, `subagent-protocol.md` | VAL-SPC-002 | Runtime/governance catalog parity passes |
| PLN-003 | Add maintenance guide and update LLM Wiki references | `docs/05.operations/guides/llm-wiki-maintenance.md`, `llms.txt`, reference READMEs | VAL-SPC-003 | Link and repo contract checks pass |
| PLN-004 | Strengthen repository contracts | `scripts/check-repo-contracts.sh`, `scripts/README.md` | VAL-SPC-003 | Missing or stale LLM Wiki assets fail validation |
| PLN-005 | Record implementation evidence | stage task docs and progress log | VAL-SPC-003 | Completion evidence is current |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Generated artifact | LLM Wiki index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-002 | Governance | Repo contract enforcement | `bash scripts/check-repo-contracts.sh` | PASS |
| VAL-PLN-003 | Traceability | Plan/operations traceability | `bash scripts/check-doc-traceability.sh` | PASS |
| VAL-PLN-004 | Runtime | Syntax and catalog validity | `bash -n scripts/*.sh scripts/lib/*.sh .claude/hooks/*.sh` | PASS |
| VAL-PLN-005 | Infra baseline | Compose and hardening unaffected | Baseline validation bundle | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Generated index becomes a content dump | High | Keep output to path links and roles only |
| Unsafe paths enter LLM Wiki | High | Generator exclusions and repo contract safety scan |
| `wiki-curator` duplicates `doc-writer` | Medium | Limit role to LLM Wiki freshness and boundaries |
| Graphify is over-trusted | Medium | Keep advisory wording and run graph health report |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: generator `--check`, repo contract, traceability check.
- **Sandbox / Canary Rollout**: local repository validation only.
- **Human Approval Gate**: required before expanding LLM Wiki beyond repo-local path index.
- **Rollback Trigger**: generated output includes unsafe paths or public/wiki deployment scope.
- **Prompt / Model Promotion Criteria**: `wiki-curator` remains `model: sonnet` unless the governance catalog changes.

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **Spec**: [../../03.specs/llm-wiki-agent-first-completion/spec.md](../../03.specs/llm-wiki-agent-first-completion/spec.md)
- **Task**: [../tasks/2026-05-10-llm-wiki-agent-first-completion.md](../tasks/2026-05-10-llm-wiki-agent-first-completion.md)
- **Guide**: [../../05.operations/guides/llm-wiki-maintenance.md](../../05.operations/guides/llm-wiki-maintenance.md)
- **Reference**: [../../90.references/llm-wiki/README.md](../../90.references/llm-wiki/README.md)
