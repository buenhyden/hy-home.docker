---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md -->

# Reference: Workspace Rules and Environment Implementation

## Overview

This reference assesses the provider-neutral workspace rule and environment
substrate that makes the harness usable across providers. Runtime Compose and
security depth are owned by Task 6; this report stays on common agentic rules.

## Purpose

Show which common contracts are canonical, synchronized, automated, measured,
or unobservable without overstating documentation as runtime enforcement.

## Repository Role

This Stage 90 report supports follow-up planning. Stage 00/99, scripts, CI,
provider adapters, and actual executing environments remain authoritative.

## Scope

### In Scope

- Workspace purpose, instruction/stage routing, role/skill catalogs, approval,
  evidence/memory, local validation entry points, and source corroboration.

### Out of Scope

- Compose/runtime/security assessment owned by Task 6.
- Governance, template, script, CI, provider, model, secret, or remote mutation.

## Definitions / Facts

- Stage 00 is the provider-neutral policy authority; provider files are adapters.
- The tracked catalog has one supervisor, fourteen workers, and 22 functions,
  with name-set projections across all three provider surfaces.
- No per-agent concrete model selector was available to the collaboration
  runtime for this implementation. The dispatch recorded the repository role
  (`code-reviewer`) and requested Senior tier while the platform chose
  the concrete model; no policy inference or mutation follows.

## Assessment Method

The audit read root shims, Stage 00 rules/scopes/catalog/progress, provider
adapters, Stage 99 routing, scripts, and current task evidence. Required sync
and eval checks were reproduced. Stale/advisory Graphify data was corroborated
against tracked source and was never treated as implementation truth.

## Audit Criteria

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| WRE-01 | Maintain one provider-neutral instruction authority. | Stage 00 governance hub, bootstrap, agentic rule, and thin root/provider shims define canonical ownership. | Implemented | 3 | Retain | `docs/00.agent-governance/` | Existing repo contracts and provider sync. | Inspect shims and Stage 00 authority statements. | High. |
| WRE-02 | Route work through explicit lifecycle stages and one primary scope. | Bootstrap, persona, task checklists, scopes, stage matrix, Spec 123, plan, and task evidence form a tracked chain. | Implemented | 2 | Retain | Stage 00 plus canonical lifecycle stages | Metadata/semantic enforcement is owned by Tasks 7-8, not this audit. | Trace current Spec/Plan/Task links and loaded scope. | High. |
| WRE-03 | Keep agent role names and model tiers synchronized across adapters. | Fifteen role names exist on Claude/Codex/`.agents`; the sync generator reports no drift. | Implemented | 3 | Retain | Stage 00 agent catalog and provider sync | Existing name/model validation; native-schema checks remain separate. | Provider role inventory and sync check. | High. |
| WRE-04 | Keep reusable function/skill names synchronized across adapters. | Twenty-two skill directories exist on each provider surface; `.agents` entries are pointers. | Implemented | 3 | Retain | Stage 00 function catalog and provider sync | Existing generation/check mode. | Skill inventory and sync check. | High. |
| WRE-05 | Bind protected changes to explicit approval, evidence, rollback, and redaction. | Approval boundaries, task checklists, Spec 123, and Task 5 brief prohibit protected mutations and secret/log persistence. | Implemented | 2 | Retain | Stage 00 approval boundaries and Stage 04 task owner | Future high-risk tasks may add denied-action tests; no audit-only gate. | Inspect approval/task contracts and changed paths. | High. |
| WRE-06 | Maintain advisory memory and durable task/review evidence without making memory policy. | Memory README/progress, task evidence, SDD reports, and independent review ledger exist; closure metrics are not generated. | Partial | 2 | Improve | Stage 00 memory plus Stage 04 task owner | Candidate ledger consistency check after Task 6 consolidation. | Inspect progress/task/review records. | High. |
| WRE-07 | Provide deterministic local validation and CI routing by change type. | Scripts README, task checklists, repo contracts, provider sync, wiki generators, and fixture runner exist; not every semantic behavior is testable. | Partial | 3 | Improve | QA scope and scripts catalog | Retain existing checks; add semantic gates only with approved false-positive review. | Run Task 5 validation bundle. | High. |
| WRE-08 | Treat executing sandbox, network, provider entitlement, and global config as observed environment facts. | Rules state boundaries, but tracked files cannot prove the active provider profile, account access, egress, MCP servers, or global settings. | Needs Revalidation | 1 | Retain | Executing environment/provider owner | Explicit non-automation unless scoped observation is authorized. | Authorized runtime evidence only. | Medium by design. |
| WRE-09 | Corroborate generated/navigation evidence against tracked canonical source. | Bootstrap/Spec 123 require tracked evidence; Graphify report was stale and all Task 5 claims were rechecked directly. | Implemented | 2 | Retain | Audit/task owner | Keep Graphify advisory; no status automation from graph edges. | Compare Graphify commit metadata with `git rev-parse HEAD` and cited tracked files. | High. |
| WRE-10 | Preserve implementation/review separation and honest lifecycle state. | Fresh implementer and separate review are required; Task 5 task row and phase checkbox remain `Todo`/unchecked while implementation is recorded `In Review`. | Implemented | 2 | Retain | Workflow supervisor and Stage 04 task owner | Task ledger update after independent approval only. | Inspect task row, phase checkbox, and report/review package. | High. |

## Findings

- Name/model projection and skill projection are automated at depth 3.
- Environment facts that live outside tracked scope remain `Needs Revalidation`;
  adding more policy text would not make them implemented.
- Evidence is durable but not depth 4 because closure, drift, and semantic quality
  are not measured as a single feedback system.

## Gap / Follow-up

| Gap | Action | Owner |
| --- | --- | --- |
| Native provider schema/event compatibility | Fix in approved provider synchronization work. | Task 10 |
| Evidence-ledger consistency and full audit-matrix coverage | Improve generator only in its planned owner task. | Task 6 |
| Live/global environment facts | Retain unknown unless a task needs and is authorized to observe them. | Executing task owner |
| Semantic behavior coverage | Improve through a separately designed eval contract. | QA/eval follow-up |

## Automation Impact

Retain provider sync and deterministic repository checks. Task 6 owns the
ten-report audit-generator consolidation; this Task 5 report does not modify
that generator and any generated audit matrix remains an interim historical
subset.

## Source Rules

- Tracked files and active stage documents support workspace status.
- Generated or graph evidence must be fresh and corroborated.
- User-global, live, remote, and secret state remains unknown unless explicitly
  authorized and observed.

## Sources

- [Workspace baseline research](../../research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md)
- [Stage 00 governance hub](../../../00.agent-governance/README.md)
- [Agentic rule](../../../00.agent-governance/rules/agentic.md)
- [Task checklists](../../../00.agent-governance/rules/task-checklists.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)

## Maintenance

- **Owner**: Agentic Workflow Specialist / Repository Maintainer.
- **Review Cadence**: After Stage 00, provider, validation, or evidence changes.
- **Update Trigger**: Common rule state, enforcement depth, or environment evidence changes.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [Provider audit](./provider-harness-loop-implementation.md)
- [Agent instruction/catalog/model audit](./agent-instructions-catalog-vibe-models.md)
