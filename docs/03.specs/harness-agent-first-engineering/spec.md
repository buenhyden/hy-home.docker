---
status: approved
---

# Harness / Agent-first Engineering Specification

## Overview (KR)

이 문서는 `hy-home.docker` 워크스페이스의 목적, 규칙, 환경, 하네스 구성, Agent-first Engineering 구성을 파일 내용 기준으로 분석하고, 현재 구현이 충족하는 계약과 구현 보완이 필요한 gap을 명세한다.

## Strategic Boundaries & Non-goals

- 이 명세는 agent/runtime/governance 계약 분석을 다룬다.
- 새 agent catalog, parallel Codex catalog, root instruction 확장은 만들지 않는다.
- `docs/01.requirements`, `docs/02.architecture/requirements`, `docs/02.architecture/decisions`, `docs/05.operations/incidents`에는 새 산출물을 만들지 않는다.
- PRD/ARD/ADR은 새 product feature, architecture replacement, or durable decision이 아니라 existing harness context-quality fallback 보완이므로 생성하지 않는다.
- 런타임 변경은 현재 검증에서 gap이 발견된 hook quoting 보완처럼 작고 증명 가능한 변경으로 제한한다.
- `10-communication` Compose include/IP/network remediation은 별도 infra 작업으로 분리하고 이 HAFE 성공 기준에 포함하지 않는다.

## Related Inputs

- `README.md`
- `docs/README.md`
- `infra/README.md`
- `scripts/README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `RTK.md`
- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `.claude/CLAUDE.md`
- `.codex/README.md`
- `scripts/check-repo-contracts.sh`
- `scripts/check-doc-traceability.sh`
- `scripts/report-graphify-health.sh`
- `scripts/validate-docker-compose.sh`

## Contracts

| Contract | Source | Required Behavior |
| --- | --- | --- |
| Workspace purpose | `README.md`, `infra/README.md` | Docker Compose 기반 홈/개발 인프라를 계층형 `infra/`와 stage 문서로 운영한다. |
| Docs taxonomy | `docs/README.md`, `documentation-protocol.md` | 활성 문서는 `docs/01`-`docs/10`, `docs/90`, `docs/99`에만 둔다. |
| Thin root shims | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | 루트 파일은 진입과 import만 담당하고 세부 정책은 governance/runtime 문서로 위임한다. |
| Governance SSOT | `docs/00.agent-governance/` | shared rules, scopes, providers, agents catalog, memory, delegation protocol을 소유한다. |
| Runtime mirror | `.claude/agents`, `.claude/skills`, `docs/00.agent-governance/agents` | runtime agent/function catalog, model front matter, scope imports, protocol references가 governance catalog와 동기화되어야 한다. 이 검증은 semantic content parity가 아니라 catalog parity를 증명한다. |
| Codex boundary | `.codex/README.md`, `.codex/hooks.json` | Codex는 hook/context surface이며 parallel delegated-agent catalog를 만들지 않는다. |
| Graphify context health | `AGENTS.md`, runtime hooks, `scripts/report-graphify-health.sh` | Graphify는 clean corpus일 때 navigation aid이며, contamination이 있으면 advisory로 낮추고 tracked source와 canonical docs로 재확인한다. |
| Verification | `scripts/check-*.sh` | repository contract, docs traceability, default/core Compose profile, supported hardening tiers, hook payload simulation으로 완료를 증명한다. |

## Core Design

### File Analysis Summary

| Area | Files Analyzed | Finding |
| --- | --- | --- |
| Workspace purpose and environment | `README.md`, `docs/README.md`, `infra/README.md`, `scripts/README.md` | 목적, docs taxonomy, Compose tiering, validation scripts가 일관된다. |
| Agent entry and provider routing | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `RTK.md` | provider-neutral entry와 provider shim이 얇게 유지된다. `RTK.md`는 Codex CLI proxy convention을 설명하지만 현재 shell에서는 `rtk`가 없을 수 있다. |
| Governance rules | `bootstrap.md`, `persona.md`, `task-checklists.md`, `agentic.md`, `documentation-protocol.md`, `stage-authoring-matrix.md`, `scopes/agentic.md` | non-mutating discovery, persona routing, scope loading, template-first docs, completion checks가 명시되어 있다. |
| Harness runtime | `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/*.md`, `.claude/skills/*/skill.md`, `.claude/hooks/*.sh` | supervisor는 `opus`, workers는 `sonnet`, agents는 단일 scope import를 가진다. Claude hooks must preserve JSON output without shell command substitution. |
| Codex runtime | `.codex/README.md`, `.codex/hooks.json`, `providers/codex.md` | Codex hook은 graphify context와 post-edit validation을 제공하고 policy source가 아니다. |
| Agent/function catalog | `docs/00.agent-governance/agents/**`, `subagent-protocol.md` | 8 agents와 10 functions가 runtime mirror와 연결되어 있다. |
| Templates and validators | `docs/99.templates/*.md`, `scripts/check-repo-contracts.sh`, `scripts/check-doc-traceability.sh`, `scripts/validate-docker-compose.sh` | stage template contract와 runtime drift checks가 repository validation에 포함되어 있다. |

### Harness Engineering Components

- Entry shims: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- Governance hub: `docs/00.agent-governance/`.
- Runtime mirror: `.claude/agents/*.md`, `.claude/skills/*/skill.md`, `docs/00.agent-governance/agents/**`.
- Delegation protocol: `docs/00.agent-governance/subagent-protocol.md`.
- Provider overlays: `docs/00.agent-governance/providers/*.md`.
- Hooks: `.claude/hooks/*.sh`, `.codex/hooks.json`, `scripts/post-tool-validate.sh`; hook scripts must be validated with real `tool_input` payloads, not only JSON and shell syntax checks.
- Validation gates: `scripts/check-repo-contracts.sh`, `scripts/check-doc-traceability.sh`, `scripts/validate-docker-compose.sh`, security/hardening baseline scripts.
- Context graph: `graphify-out/GRAPH_REPORT.md`, with advisory health evidence from `scripts/report-graphify-health.sh`.

### Agent-first Engineering Components

- Agents are first-class workers with explicit routing, scoped ownership, and verification evidence.
- Work starts from repository discovery, not assumption.
- Execution is gated by persona, checklist, one primary scope, and JIT-loaded stage docs.
- Detailed policy stays in governance docs; root files remain concise.
- Agent/runtime changes are auditable through catalog parity, model/scope/protocol checks, hook payload simulation, and validation scripts.
- Memory notes record history but do not replace active policy.

## Data Modeling & Storage Strategy

No persistent data model is introduced. The implementation stores only Markdown documentation in canonical stage paths.

## Interfaces & Data Structures

### Core Interfaces

| Interface | Shape | Purpose |
| --- | --- | --- |
| Stage docs | Markdown with existing `status` front matter | Human and agent-readable analysis, plan, task, guide, policy, and runbook. |
| Runtime catalog | Markdown agent/function files | Delegated worker and function definitions. |
| Validation scripts | Bash commands returning non-zero on failure | Completion and drift evidence. |

## API Contract (If Applicable)

Not applicable. This change does not add or modify service APIs.

## Agent Role & IO Contract (If Applicable)

| Role | Input | Output |
| --- | --- | --- |
| Agentic Workflow Specialist | Root shims, governance docs, runtime files, validators, templates | Analysis, gap classification, and verification evidence. |
| Documentation Specialist | Stage templates and parent README files | Template-compliant stage docs and README links. |

## Tools & Tool Contract (If Applicable)

- Use `rg` for discovery where available.
- Use `bash scripts/check-repo-contracts.sh` for repository and runtime catalog drift.
- Use `bash scripts/check-doc-traceability.sh` for 05/08/09 traceability.
- Use `bash scripts/report-graphify-health.sh` for non-failing Graphify corpus health evidence.
- Use `bash scripts/validate-docker-compose.sh` for default/core Compose structural validation.
- Use security and hardening baseline scripts for supported tier operational confidence.
- Use hook payload simulation commands for Claude/Codex hook behavior.

## Prompt / Policy Contract (If Applicable)

- User-facing explanations are Korean by default.
- Governance/runtime docs remain English unless they are human-facing stage docs.
- Do not expose secrets.
- Do not create GitHub-native instruction layers or a parallel Codex agent catalog.

## Memory & Context Strategy (If Applicable)

- Load `graphify-out/GRAPH_REPORT.md` before architecture or codebase answers.
- Use Graphify as a navigation aid only when corpus health is clean.
- If Graphify includes `volumes/`, gitlink/submodule content, generated/minified artifacts, meaningless god nodes, or unrelated cross-root inferred edges, treat it as advisory and corroborate with tracked source, `docs/00.agent-governance/`, and active stage docs.
- Use `docs/00.agent-governance/memory/` for historical audit notes only.
- Use live repository files and validators as the current source of truth.

## Guardrails (If Applicable)

- Keep root instruction files thin.
- Use in-place refactors only.
- Preserve `.claude` as the canonical delegated-agent runtime mirror.
- Keep `.codex` limited to hooks and context wiring.
- Do not treat contaminated Graphify output as authority for architecture or codebase conclusions.
- Enforce zero external source-label references in runtime/governance files.
- Keep `10-communication` remediation outside this HAFE scope unless a separate infra plan is approved.

## Evaluation (If Applicable)

Evaluation is command-based:

- Repository contract passes.
- Documentation traceability passes.
- Default/core Compose validation passes.
- Template/security, QuickWin, and supported hardening baselines pass.
- Hook payload simulations return valid JSON/system-message output without command substitution side effects.
- Graphify health report exits 0 and records `status=clean|advisory` without being treated as architecture authority when advisory.
- Source-label scan returns no matches in active runtime/governance surfaces.

## Edge Cases & Error Handling

- If a validator fails, update the relevant stage task evidence and patch only the failing contract.
- If Graphify health is `advisory`, read it for navigation only and re-check claims against tracked files and canonical docs.
- If `graphify` CLI is unavailable after code changes, report graph refresh as skipped rather than claiming success.
- If `rtk` is unavailable in Codex shell, run the underlying shell commands directly and record the fallback.
- If a new stage artifact is added, update the parent README in the same change.
- If `10-communication` validation fails, record it as a separate infra remediation item unless that tier is explicitly in scope.

## Failure Modes & Fallback / Human Escalation

| Failure Mode | Fallback |
| --- | --- |
| Runtime catalog mismatch | Repair mirror parity between `.claude/` and `docs/00.agent-governance/agents/`. |
| Missing scope import or model split | Restore exact scope import and `opus`/`sonnet` hierarchy. |
| Stale source-label reference | Rewrite content to be self-contained, then rerun scans. |
| Contaminated Graphify context | Downgrade Graphify to advisory context and corroborate against tracked source and canonical docs. |
| Docs traceability failure | Add missing parent README or 05/08/09 reciprocal links. |
| Scoped Compose validation failure | Treat as infra blocker and inspect affected in-scope `infra/**/docker-compose*.yml`. |
| `10-communication` profile failure | Track separately as infra remediation; do not block HAFE completion. |
| Hook payload failure | Fix hook quoting/parsing and rerun the exact payload simulation. |

## Verification

```bash
python3 -m json.tool .codex/hooks.json >/dev/null
python3 -m json.tool .claude/settings.json >/dev/null
bash -n .claude/hooks/*.sh scripts/*.sh
printf '{"tool_input":{"file_path":"infra/10-communication/mail/docker-compose.yml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/docker-compose-pre.sh
CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/session-start.sh
printf '{"tool_input":{"file_path":".claude/settings.json"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/post-tool-validate.sh
bash scripts/report-graphify-health.sh
bash scripts/check-repo-contracts.sh
bash scripts/check-doc-traceability.sh
bash scripts/validate-docker-compose.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-quickwin-baseline.sh
bash scripts/check-all-hardening.sh
! rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md GEMINI.md .claude .codex docs/00.agent-governance --glob '!docs/00.agent-governance/memory/**'
```

## Success Criteria & Verification Plan

- Stage docs are created from the matching templates.
- Parent README files link to the new documents.
- Validators pass with zero failures for active governance/runtime contracts and scoped infra baselines.
- No new runtime or provider policy drift is introduced.
- No parallel Codex agent catalog is created.
- `10-communication` Compose remediation is recorded as out of scope for this HAFE pass.

## Related Documents

- [Plan](../../04.execution/plans/2026-05-09-harness-agent-first-engineering.md)
- [Task Evidence](../../04.execution/tasks/2026-05-09-harness-agent-first-engineering.md)
- [Guide](../../05.operations/policies/harness-agent-first-engineering.md)
- [Operations Policy](../../05.operations/policies/harness-agent-first-engineering.md)
- [Validation Runbook](../../05.operations/runbooks/harness-agent-first-engineering-validation.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
