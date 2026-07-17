---
status: active
artifact_id: audit:agentic-engineering-implementation:workspace-rules-environment
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
reviewed_at: 2026-07-12
review_cycle: per-remediation-task
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
- The independently enforced, non-stage `_workspace` repo-support boundary.

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
- `_workspace` is an ignored, non-secret repo-support surface outside docs
  metadata inference. Only `_workspace/README.md` and
  `_workspace/repo-support/README.md` may be tracked; non-secret scratch remains
  ignored, and repository contracts enforce this boundary independently.

## Assessment Method

The audit read root shims, Stage 00 rules/scopes/catalog/progress, provider
adapters, Stage 99 routing, the two tracked `_workspace` README contracts,
scripts, and current task evidence. Required sync and eval checks were
reproduced. Stale/advisory Graphify data was corroborated against tracked source
and was never treated as implementation truth.

## Audit Criteria

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| WRE-01 | Maintain one provider-neutral instruction authority. | Stage 00 governance hub, bootstrap, agentic rule, and thin root/provider shims define canonical ownership. | Implemented | 3 | Retain | `docs/00.agent-governance/` | Existing repo contracts and provider sync. | Inspect shims and Stage 00 authority statements. | High. |
| WRE-02 | Route work through explicit lifecycle stages and one primary scope. | Bootstrap, persona, task checklists, scopes, stage matrix, Spec 123, plan, and task evidence form a tracked chain. T-AER-008/012 now enforce typed changed/new lifecycle metadata. | Implemented | 2 | Retain | Stage 00 plus canonical lifecycle stages | Retain canonical routing and metadata enforcement without making this audit a policy source. | Trace current Spec/Plan/Task links, loaded scope, and changed/new metadata evidence. | High. |
| WRE-03 | Keep agent role names and model tiers synchronized across adapters. | Four role surfaces each contain the same 14 canonical IDs; Claude, Codex, and Gemini use native generated schemas and `.agents` is the shared compatibility projection. The sync check reports three providers and zero drift. | Implemented | 3 | Retain | Stage 00 agent catalog and provider renderer | Existing exact name/model/schema validation; live native acceptance remains separate. | Provider role inventory and sync check. | High. |
| WRE-04 | Keep reusable function/skill names synchronized across adapters. | Twenty-two canonical functions project to 22 Claude and 22 shared `.agents` skill directories; the absence of `.gemini/skills` is an intentional provider projection, not drift. | Implemented | 3 | Retain | Stage 00 function catalog and provider renderer | Existing generation/check mode. | Function/skill inventory and sync check. | High. |
| WRE-05 | Bind protected changes to explicit approval, evidence, rollback, and redaction. | Approval boundaries, task checklists, Spec 123, and the completed T-AER task chain bind protected mutations to scoped approval and prohibit secret/log persistence. | Implemented | 2 | Retain | Stage 00 approval boundaries and Stage 04 task owner | Future high-risk tasks may add denied-action tests; no audit-only gate. | Inspect approval/task contracts, protected-surface evidence, and changed paths. | High. |
| WRE-06 | Maintain advisory memory and durable task/review evidence without making memory policy. | Memory README/progress, task evidence, SDD reports, final PASS/APPROVED review ledgers, and generated audit coverage exist; a unified quality/closure time series does not. | Partial | 2 | Improve | Stage 00 memory plus Stage 04 task owner | Retain deterministic ledgers and generated coverage; add metrics only under a separately defined contract. | Inspect progress/task/review records and audit coverage output. | High. |
| WRE-07 | Provide deterministic local validation and CI routing by change type. | The local runner owns 20 script-backed and 18 harness steps, changed-path selection routes every coupled governance/eval/provider surface, repo contracts enforce exact CI markers, and the evaluator requires eight fixtures plus ten regressions. The controlled all-files wrapper remains separate and evidence-gated. | Implemented | 3 | Retain | QA scope and scripts catalog | Retain one canonical local runner, typed selectors, exact CI markers, and the controlled-wrapper boundary. | Run `--list`, selector tests, `validate-harness.sh`, and repository contracts. | High. |
| WRE-08 | Treat executing sandbox, network, provider entitlement, and global config as observed environment facts. | Rules state boundaries, but tracked files cannot prove the active provider profile, account access, egress, MCP servers, or global settings. | Needs Revalidation | 1 | Retain | Executing environment/provider owner | Explicit non-automation unless scoped observation is authorized. | Authorized runtime evidence only. | Medium by design. |
| WRE-09 | Corroborate generated/navigation evidence against tracked canonical source. | Bootstrap/Spec 123 require tracked evidence; the advisory Graphify report is stale relative to this branch, so current claims are corroborated directly against tracked source and generated owner checks. `_workspace` is separately bounded to two tracked READMEs plus ignored non-secret scratch, excluded from docs metadata inference, and enforced by repository contracts. | Implemented | 2 | Retain | Audit/task owner and `_workspace` repository-contract owner | Keep Graphify advisory and `_workspace` independent from docs metadata; no status automation from graph edges or scratch files. | Compare Graphify commit metadata with `git rev-parse HEAD`, generators, cited tracked files, the `_workspace` allowlist, and repository-contract checks. | High. |
| WRE-10 | Preserve implementation/review separation and honest lifecycle state. | The T-AER chain used fresh implementers and independent reviewers and closed only after final PASS/APPROVED, C0/I0/M0, and `READY_FOR_RECLOSURE: YES`; T-AHC-002 and T-DCC-004 remain Done/PASS/Approved. Spec 129 reopened after its failed post-closure review, resolved I-01 through I-03, reclosed after PASS/APPROVED C0/I0/M0 and `READY_FOR_RECLOSURE: YES`, and passed a new final whole-branch review with `READY_FOR_HANDOFF: YES`. | Implemented | 2 | Retain | Workflow supervisor and Stage 04 task owner | Preserve the completed lifecycle and keep later migration/runtime/remote waves independently approval-gated. | Inspect T-AER-012 final evidence, completed T-AHC-002/T-DCC-004 rows, the failed Spec 129 review, remediation commits, Attempt 4, reclosure, final C0/I0/M0 handoff review, and completed T-DCC-006 row. | High. |

## Findings

- Name/model projection and skill projection are automated at depth 3.
- Environment facts that live outside tracked scope remain `Needs Revalidation`;
  adding more policy text would not make them implemented.
- Evidence is durable but not depth 4 because closure, drift, and semantic quality
  are not measured as a single feedback system.
- `_workspace` is covered without adding a new criterion or importing it into
  the docs metadata corpus: two README contracts are tracked, non-secret scratch
  is ignored, and prohibited sensitive artifacts remain outside the surface.

## Gap / Follow-up

| Gap | Action | Owner |
| --- | --- | --- |
| Native provider schema/event acceptance | Retain tracked sync/parity; verify live acceptance only in separate approved scope. | Provider/runtime owner |
| Evidence-ledger consistency and full audit-matrix coverage | Retain the eleven-report / 161-row generator contract and freshness checks. | Canonical audit generator owner |
| Live/global environment facts | Retain unknown unless a task needs and is authorized to observe them. | Executing task owner |
| Semantic behavior coverage | Improve through a separately designed eval contract. | QA/eval follow-up |

## Automation Impact

Retain provider sync, deterministic repository checks, changed/new metadata,
and the complete eleven-report audit-generator contract. The generated matrix
contains every canonical criterion row; README and overview counts remain
separate.

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
- [`_workspace` contract](../../../../_workspace/README.md)
- [`_workspace` repo-support contract](../../../../_workspace/repo-support/README.md)

## Maintenance

- **Owner**: Agentic Workflow Specialist / Repository Maintainer.
- **Review Cadence**: After Stage 00, provider, validation, or evidence changes.
- **Update Trigger**: Common rule state, enforcement depth, or environment evidence changes.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [Provider audit](./provider-harness-loop-implementation.md)
- [Agent instruction/catalog/model audit](./agent-instructions-catalog-vibe-models.md)
