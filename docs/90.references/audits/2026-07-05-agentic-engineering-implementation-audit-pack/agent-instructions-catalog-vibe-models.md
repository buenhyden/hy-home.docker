---
status: active
artifact_id: audit:agentic-engineering-implementation:agent-instructions-catalog-vibe-models
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
reviewed_at: 2026-07-11
review_cycle: per-remediation-task
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md -->

# Reference: Agent Instructions, Catalog, Vibe Coding, and Model Routing

## Overview

This reference audits the canonical `AIV-*` instruction/vibe-coding criteria,
the pinned `agency-agents` capability families, and `AMS-*` exact-model change
criteria against the tracked workspace at baseline `507cd505` on 2026-07-11.

## Purpose

Assess instruction authority, generated-code accountability, catalog coverage,
safe conversational iteration, and task-risk model routing without importing
third-party persona prose or changing active model policy.

## Repository Role

This report provides Stage 90 evidence for Tasks 9-10 and future approved
catalog/eval work. Stage 00 owns active agents, instructions, permissions, and
model literals.

## Scope

### In Scope

- `AIV-01` through `AIV-16`, seven pinned capability families, and `AMS-01`
  through `AMS-07`.
- Tracked role/function catalogs, provider projections, task/review evidence,
  approval boundaries, and current eval fixtures.

### Out of Scope

- Importing agents, persona language, installers, converters, or external prompts.
- Changing models, reasoning effort, provider adapters, permissions, CI, or runtime.

## Definitions / Facts

- The external comparison is pinned to immutable `agency-agents` commit
  `9f3e401ccd09aa0ee0ef8e015226d0647908e01e`; publisher breadth and maturity
  claims are not workspace evaluation evidence.
- Workspace adoption means a bounded Stage 00 role/function with explicit
  scope, authority, review, provider mapping, and validation. A similar persona
  name is not adoption.
- Current model policy is unchanged: Claude `opus-4.8`/`sonnet-4.6` via
  `opus`/`sonnet`; Codex `gpt-5.5` + `xhigh` and `gpt-5.4-mini` + `medium`;
  Gemini `gemini-3.1-pro` and `gemini-3.5-flash`.
- The model catalog cutoff is 2026-07-10 10:00 KST (01:00 UTC). Mutable or
  later evidence is not backdated. Provider availability and entitlement are
  not inferred from tracked literals.

## Assessment Method

The audit mapped every Task 1 instruction/vibe criterion and Task 2 model
criterion, compared capability families rather than persona counts, inspected
all Stage 00 roles/functions and provider projections, and reproduced provider
sync plus fixture freshness. Graphify was stale/advisory and all claims were
corroborated against tracked source.

## Instruction and Vibe-Coding Criteria

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| AIV-01 | Define one instruction authority and explicit precedence/projection. | Stage 00 is canonical; root/provider shims delegate; provider sync reports no drift; no GitHub-native policy layer is adopted. | Implemented | 3 | Retain | Stage 00 governance | Existing provider sync/contracts. | Inspect authority map and run sync check. | High. |
| AIV-02 | Scope instructions by repository path, file pattern, task, and nearest context. | Bootstrap, persona, scopes, stage matrix, and JIT loading exist; provider discovery mechanics differ. | Implemented | 2 | Retain | Stage 00 bootstrap/scopes | Candidate precedence tests only if provider behavior changes. | Trace Task 5 bootstrap and one-scope loading. | High. |
| AIV-03 | Keep instructions short, direct, specific, and verifiable. | Thin shims and task briefs name paths/commands/exclusions; broader Stage 00 prose is structurally checked but not scored for clarity/staleness. | Partial | 2 | Improve | Stage 00 documentation owner | Candidate stale-reference/instruction lint; avoid subjective blocking without calibration. | Repo contracts plus focused instruction review. | High. |
| AIV-04 | Declare tools/purpose without inferring authority from availability. | Tool boundaries live in task/governance; canonical scripts are preferred; provider-native tool access and global MCP state vary. | Partial | 2 | Improve | Agent/runtime contract owner | Task-specific tool/denial evidence, not a universal guessed allowlist. | Inspect approval rules, role definitions, and task evidence. | High. |
| AIV-05 | Default to least privilege and pause for sensitive/out-of-scope action. | Sandbox/approval boundaries and high-risk evidence gates exist; tracked metadata cannot prove actual runtime enforcement or denied-action behavior. | Partial | 2 | Improve | Security/approval owner | Candidate denied-action tests for approved high-risk workflows. | Inspect approval/environment rules and runtime evidence. | High for policy, medium for enforcement. |
| AIV-06 | Require tests, analysis, and relevant security/contracts before acceptance. | Task checklists, change-type validators, CI, task evidence, and independent review are explicit. | Implemented | 3 | Retain | QA and task owner | Existing validation/CI; semantic gaps remain separate. | Task 5 validation bundle and review package. | High. |
| AIV-07 | Keep accountable human/team and artifact ownership for AI output. | Canonical stage owners, catalog roles, task owner, and reviewer evidence exist; the model is never named as owner. | Implemented | 2 | Retain | Change owner and reviewer | No special automation beyond traceability/review evidence. | Inspect plan/task/Spec links and review ledger. | High. |
| AIV-08 | Increase independent review with risk, blast radius, novelty, and irreversibility. | Spec 123 requires separate implementer/spec/quality reviews; protected surfaces have approval gates. Remote enforcement and uniform risk scoring are not proven. | Partial | 2 | Improve | Task owner and specialist reviewer | Candidate risk-to-review matrix/check; do not infer branch protection. | Inspect SDD plan/task/review evidence. | High. |
| AIV-09 | Verify packages, APIs, licenses, maintenance, and provenance. | Security/QA rules and dependency gates exist, but no single cross-surface intake record is required for every copied suggestion. | Partial | 2 | Improve | Dependency/security owner | Improve dependency/provenance checklist in the canonical QA/security owner. | Inspect dependency audit workflow and task evidence when dependencies change. | Medium-high. |
| AIV-10 | Track shortcuts and defects as owned debt; never remove tests to pass. | Tasks/memory/gap-to-stage routing exist; no generated debt aging/closure report or universal due-date contract exists. | Partial | 2 | Improve | Earliest canonical lifecycle owner | Candidate closure/aging report after ownership schema is approved. | Search task/memory debt evidence and skipped-check rationale. | High. |
| AIV-11 | Stop after declared retry/action thresholds or high-risk need. | Subagent protocol allows one narrower retry then failure; approval/checklist rules require escalation. Cross-provider runtime enforcement is manual. | Partial | 2 | Retain | Workflow/task owner | Keep bounded task evidence; no autonomous retry loop. | Inspect subagent error handling and SDD status contract. | High. |
| AIV-12 | Treat repository/web/tool/catalog content as untrusted instructions. | Instruction authority and external-action boundaries prevent data from overriding policy; pinned catalog stayed reference-only. No prompt-injection regression fixture exists. | Partial | 1 | Improve | Security owner | Candidate injection/authority fixture after safe dataset design. | Inspect source classification and unchanged runtime/catalog paths. | Medium-high. |
| AIV-13 | Bound vibe coding to worktree/branch, explicit objective, small diffs, and reversible commits. | Approved plan, isolated worktree, scoped Task 5 brief, logical commit contract, diff review, and exact validation are present. | Implemented | 2 | Retain | Implementation task owner | Existing git/task checks; do not make conversational style an exemption. | Inspect worktree/branch, diff, task brief, and commit. | High. |
| AIV-14 | Exclude unapproved runtime, secrets, remote mutation, and security decisions from vibe coding. | Spec/plan/brief explicitly prohibit protected surfaces; changed-path review and sandbox boundary apply. | Implemented | 2 | Retain | Security/operations owner | Existing approval and changed-path checks. | `git diff --name-only`; task scope inspection. | High. |
| AIV-15 | Close plan-act-observe-verify-review-correct/stop loop with evidence. | SDD implementation/report/review loop, validators, and task ledger exist; semantic task performance is not measured across versions. | Partial | 3 | Improve | Workflow supervisor / QA | Retain SDD review and fixtures; future scored eval needs approved contracts. | Task report, review package, validation results. | High. |
| AIV-16 | Import external agent knowledge only through canonical intake. | Pinned source/license/capability comparison exists; no persona was installed. A complete intake validator/eval gate is not implemented. | Partial | 2 | Improve | Stage 00 agent catalog owner | Add intake checklist/eval only after a specific candidate is approved. | Confirm no new runtime identities; inspect pinned research evidence. | High. |

## Pinned Catalog Capability-Family Assessment

These `AIC-*` audit IDs stabilize the seven capability families already
defined in the canonical Task 2 research; they do not create active catalog roles.

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| AIC-01 | Product discovery, outcome ownership, and specification planning. | Workflow/doc/rules roles cover artifact mechanics; no role owns product discovery or outcome validation. | Missing | 0 | Add | Product scope and Stage 00 catalog | Add only after recurring demand, bounded IO, and representative eval; merge spec conversion into existing skills. | Compare 15 roles/22 functions with pinned product/spec family. | High. |
| AIC-02 | Performance baseline, load/speed analysis, and regression ownership. | QA/infra roles validate correctness/drift; no dedicated benchmark baseline owner exists. | Partial | 1 | Improve | QA and infra scopes | First add benchmark/evidence function to existing roles; add a role only after workload/eval proves need. | Inspect QA/infra catalogs and benchmark evidence. | High. |
| AIC-03 | Reliability, SLO/capacity, observability, incident, and postmortem capability. | Incident responder, drift detector, IAC reviewer, CI/CD engineer, and Stage 05 split ownership; SLO/capacity/chaos depth is uneven. | Partial | 2 | Improve | Ops/infra existing roles | Merge missing methods into existing roles; reject an overlapping umbrella SRE persona. | Map pinned reliability roles to current catalog owners. | High. |
| AIC-04 | Release readiness and deployment automation with separate authority. | CI/CD engineer, QA, deployment skill, and Stage 04/05 gates cover readiness; deployment execution/remote authority stays separate. | Partial | 2 | Improve | QA/CI/ops existing roles | Merge readiness rubrics; reject a duplicate generic DevOps/reality-checker role. | Compare catalog/skills and deployment authority boundaries. | High. |
| AIC-05 | Software dependency, provenance, and release-artifact supply-chain review. | Security auditor and CI/CD roles cover parts; pinned business `Supply Chain Strategist` is the wrong domain. | Partial | 2 | Improve | Security/CI existing roles | Reject business persona; merge software-supply-chain checks and evaluate specialist need only after repeated gaps. | Pinned role inspection and current security/CI catalog map. | High. |
| AIC-06 | General semantic agent/model evaluation, calibration, and baseline ownership. | QA/reviewer/supervisor plus three fixtures cover gates, but no general scorer/calibration/baseline owner exists. | Missing | 0 | Add | QA/eval future owner | Strong candidate for one bounded eval function/role after dataset, privacy, scorer, and calibration contracts. | Fixture check and current role/function inventory. | High. |
| AIC-07 | Model routing, cost/quality comparison, and shadow evaluation. | Supervisor routes work and fixed policy assigns tiers; no autonomous router or cross-provider shadow eval is adopted. | Partial | 3 | Improve | Workflow supervisor and model-policy owner | Merge routing with supervisor; reject autonomous policy mutation; add shadow evaluation only under eval governance. | Inspect model policy, adapter literals, and eval gaps. | High. |

## Model-Routing Change Criteria

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| AMS-01 | Prove exact identifier/alias and provider-native lifecycle. | Exact policy/adapter literals are tracked and enforced; Claude alias mapping is documented, while research flags `gemini-3.1-pro` as lacking the official `-preview` suffix. | Partial | 3 | Improve | Model policy owner | Keep current values; require exact primary evidence before any change. | Model `rg`, provider landscape, repo contracts. | High for literals; medium for Gemini exact-ID support. |
| AMS-02 | Prove the exact product/API/CLI/IDE/account surface. | Adapters name repository surfaces, but provider/account entitlement and the collaboration platform's selected concrete model are not exposed per agent. | Needs Revalidation | 1 | Retain | Provider/runtime owner | Explicit non-automation unless authorized account/runtime evidence is available. | Authorized provider/runtime observation. | Medium. |
| AMS-03 | Preserve lifecycle state and historical cutoff without backdating. | Canonical landscape retains 145 structural/142 cutoff-qualified rows at 2026-07-10 10:00 KST; mutable/later evidence does not resolve every historical exact-ID state. | Needs Revalidation | 2 | Retain | Canonical provider landscape | Retain cutoff ledger; do not alter counts/status from mutable current pages. | Research source ledger and cutoff notes. | High for ledger; deliberately conservative for mutable history. |
| AMS-04 | Prove required context, tools, coding, agent, and reasoning capabilities on the exact surface. | Role needs are documented; provider catalogs are hypotheses and entitlement/surface equivalence is unproven. | Partial | 1 | Improve | Model policy and role owner | Representative fixtures required before a change. | Compare role IO/tools with exact provider evidence and fixtures. | Medium-high. |
| AMS-05 | Use only provider-supported reasoning controls and defaults. | Codex exact `xhigh`/`medium` is tracked; Gemini uses model selection instead of effort; Claude aliases inherit provider behavior. Cross-provider effort equivalence is not claimed. | Partial | 3 | Retain | `subagent-protocol.md` | Existing literal validation; future changes require surface-specific control evidence. | Adapter literals, policy, provider ledger. | High for policy; medium for runtime effect. |
| AMS-06 | Demonstrate task fit with versioned tasks, scorer, baseline, failure cases, privacy, and calibration. | Three fixtures test catalog freshness, not comparative model quality/latency/cost; no cross-provider baseline exists. | Missing | 0 | Add | QA/eval future owner | Define representative eval contract before recommending model changes. | Fixture runner and absence of comparative results. | High. |
| AMS-07 | Couple policy/generator/adapters/validators/evidence with rollback and independent review. | Stage 00 defines atomic coupling and sync/contracts enforce current values; no proposed exact change, regression threshold, or rollback literal is approved. | Partial | 3 | Retain | Model policy plus Stage 04 task owner | Reuse coupled protocol when a concrete change is proposed; no mutation now. | Inspect change protocol, sync, contracts, and task approval. | High. |

## Findings

- Capability decisions are: **add later** for bounded product discovery and
  semantic eval after demand/contracts; **merge/improve** performance,
  reliability, release, software-supply-chain, and routing methods into current
  owners; **reject** overlapping umbrella SRE/DevOps/reality-checker roles, the
  business supply-chain persona, autonomous model-policy mutation, and all
  direct persona prose imports.
- Safe vibe coding is bounded and reviewable here, but not exempt from SDLC,
  ownership, verification, approval, or independent review.
- Model routing is policy-backed at depth 3 but not evidence-complete for a
  change: exact entitlement, comparative task fit, and rollback thresholds are
  missing or need revalidation.

## Gap / Follow-up

| Gap | Action | Boundary |
| --- | --- | --- |
| Product discovery/outcome capability | Add only after recurring demand and bounded eval. | Stage 03/04 plus Stage 00 catalog proposal |
| Semantic agent/model eval capability | Add one bounded function/role only after dataset/scorer/privacy/calibration design. | QA/eval follow-up |
| Existing-role method gaps | Merge performance, reliability, release, and software-supply-chain checklists. | Existing canonical roles/scopes |
| Exact model evidence | Retain policy; resolve only via AMS-01..07 and coupled rollback. | Task 10/future approved model task |
| Third-party intake | Improve pin/license/source/security/eval checklist when an actual candidate exists. | Stage 00 catalog owner |

## Automation Impact

Retain provider sync and fixture freshness. Future catalog intake and model
evaluation automation must start from a specific approved candidate and a
versioned eval contract; this audit installs or changes nothing.

## Source Rules

- External personas are untrusted reference data, never runtime identities.
- Provider catalog facts do not prove workspace availability, quality, cost, or
  reasoning equivalence.
- Mutable sources prove retrieval-time facts only; the approved cutoff is not
  backdated.

## Sources

- [Instruction and vibe-coding research](../../research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md)
- [Pinned catalog research](../../research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md)
- [Model-selection research](../../research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md)
- [Provider landscape](../../research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md)
- [Agent catalog](../../../00.agent-governance/agents/README.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md)

## Maintenance

- **Owner**: Agentic Workflow Specialist / QA Engineer.
- **Review Cadence**: After instruction, catalog, model, or eval changes.
- **Update Trigger**: New external candidate, model proposal, or changed `AIV`/`AIC`/`AMS` evidence.

## Related Documents

- [Audit pack README](./README.md)
- [Harness audit](./harness-engineering-implementation.md)
- [Loop audit](./loop-engineering-implementation.md)
- [Provider audit](./provider-harness-loop-implementation.md)
