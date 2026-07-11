---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md -->

# Task: Agentic Engineering Audit and Remediation

## Overview

This document tracks the approved staged implementation of Spec 123 and its
Stage 04 plan. It records research and audit consolidation, typed document
metadata, controlled agent pre-commit execution, provider/CI synchronization,
runtime follow-up specifications, validation evidence, logical commits, and
independent task/branch reviews.

## Inputs

- **Parent Spec**: [Agentic engineering audit and remediation spec](../../03.specs/123-agentic-engineering-audit-remediation/spec.md)
- **Parent Plan**: [Agentic engineering audit and remediation plan](../plans/2026-07-11-agentic-engineering-audit-remediation.md)
- **Canonical Research**: [Agentic engineering research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Canonical Audit**: [Agentic engineering implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)

## Working Rules

- Execute tasks sequentially with a fresh implementer and separate
  spec-compliance and quality/security reviewers.
- Use primary external sources and tracked repository evidence; Graphify is
  advisory and must be corroborated.
- Use logical commits and record exact task ranges and review verdicts.
- Use the controlled wrapper, not direct `pre-commit run`, after Task 9.
- Do not mutate runtime Compose, infrastructure, deployment, secrets, remote
  GitHub settings, branch protection, or model-policy values.
- Record actual commands/results and any deviation from the approved plan.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 90 research/audits | User approval of Spec 123 and the 2026-07-11 plan | Canonical 2026-07-05 research/audit packs and 2026-07-07 audit supersession records | Research canonical; audit 2026-07-05 and 2026-07-07 both active | Per-task source ledger, audit rows, supersession mapping, generated matrix, and review verdict | Revert the task's logical commit after preserving verified unique content | No raw web capture, raw logs, credentials, secret values, or environment dumps |
| Stage 00/99 metadata policy | User approval of staged typed metadata | Named governance rules, support contracts, templates, metadata validator/tests | `status` vocabulary enforced; semantic transitions and typed IDs not enforced | Advisory inventory, profile matrix, active-chain migration, changed/new gate, unit tests | Disable blocking invocation and retain advisory report while correcting profiles | Metadata and paths only; no user identity, credential, or secret material |
| QA wrapper | User approval of controlled wrapper | Validation wrapper, tests, QA rules, task template | Direct manual pre-commit prohibited; no approved wrapper | Isolated-worktree wrapper tests and final full-repository evidence | Remove wrapper invocation contract while retaining direct-execution prohibition | Concise hook summary and paths only; no raw hook logs or environment values |
| Provider adapters and CI | User approval of governance/development-harness remediation | Stage 00 provider rules, Claude source adapters, generated Codex/Gemini adapters, existing CI repo-contracts job | Provider surfaces synchronized; no metadata/wrapper instruction | No-drift provider output and existing-job metadata step | Correct canonical source and regenerate; remove only the added CI step if invalid | No model literal change, token, credential, remote setting, or branch-protection mutation |
| Runtime follow-up docs | User approval of audit plus independent follow-up specs/plans | Specs 124-127 and four draft plans | Runtime gaps exist only in audit/research | Implementation-ready gap routing with explicit later approval gates | Keep drafts, revise, or supersede; runtime remains unchanged | No runtime mutation, live diagnostics, secret reads, or deployment action |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-AER-001 | Research metadata, lifecycle, document roles, agent instructions, and vibe coding | doc | Spec 123 / Canonical Research Responsibilities | PLN-AER-001 | Primary-source ledger; LLM Wiki; repo contracts; task review | wiki-curator | Todo |
| T-AER-002 | Revalidate harness, loop, provider, model, and agent-catalog research | doc | Spec 123 / Canonical Research Responsibilities | PLN-AER-002 | Cutoff ledger; provider no-drift; repo contracts; task review | wiki-curator | Todo |
| T-AER-003 | Revalidate workspace, QA, automation, Compose, security, release, and deployment research | doc | Spec 123 / Canonical Research Responsibilities | PLN-AER-003 | Tracked inventory; Compose/hardening; repo contracts; task review | wiki-curator | Todo |
| T-AER-004 | Audit SDLC, document roles, numbering, transitions, frontmatter, templates, and README profiles | doc | Spec 123 / Canonical Audit Categories | PLN-AER-004 | Reproducible counts; audit matrices; repo contracts; task review | doc-writer | Todo |
| T-AER-005 | Audit harness, loops/evals, providers/models, workspace rules, instructions, catalogs, and vibe coding | doc | Spec 123 / Canonical Audit Categories | PLN-AER-005 | Criterion coverage; provider evidence; task review | code-reviewer | Todo |
| T-AER-006 | Audit QA/CI/CD, automation, Compose/infrastructure, security; consolidate audit lifecycle | doc | Spec 123 / Canonical Audit Categories | PLN-AER-006 | One-current-pack scan; audit generators; Compose/hardening; task review | code-reviewer | Todo |
| T-AER-007 | Implement typed metadata profiles, advisory validator, tests, and exhaustive inventory | impl/test | Spec 123 / Typed Document Metadata | PLN-AER-007 | Python unit tests; advisory report; repo contracts; task review | rules-engineer | Todo |
| T-AER-008 | Migrate the approved active chain and enforce metadata for changed/new documents | impl/test | Spec 123 / Metadata Rollout | PLN-AER-008 | Changed-mode tests; before/after inventory; pre-push contract; task review | rules-engineer | Todo |
| T-AER-009 | Implement controlled agent pre-commit wrapper and governance contract | impl/test | Spec 123 / Controlled Pre-commit Wrapper | PLN-AER-009 | Shell tests; syntax/shellcheck; wrapper contract; task review | qa-engineer | Todo |
| T-AER-010 | Synchronize provider adapters and add metadata validation to the existing CI job | impl/test | Spec 123 / Provider Synchronization | PLN-AER-010 | Provider no-drift; workflow checks; repo contracts; task review | ci-cd-engineer | Todo |
| T-AER-011 | Author four independent runtime follow-up specs/plans without runtime mutation | doc | Spec 123 / W5 Runtime Follow-up | PLN-AER-011 | Template/traceability/rollback/approval gates; task review | doc-writer | Todo |
| T-AER-012 | Run full gates, controlled wrapper, whole-branch review, and lifecycle closure | test/eval/doc | Spec 123 / Verification and Success Criteria | PLN-AER-012 | Complete validation bundle; branch review PASS/APPROVED; clean worktree | workflow-supervisor | Todo |

## Phase View

### Phase 1 — Canonical Research

- [ ] T-AER-001 Metadata, lifecycle, instructions, and vibe-coding research
- [ ] T-AER-002 Harness, loop, provider, model, and catalog research
- [ ] T-AER-003 Workspace, QA, automation, Compose, security, and release research

### Phase 2 — Canonical Audit

- [ ] T-AER-004 SDLC and document-contract audit
- [ ] T-AER-005 Harness/provider/agent audit
- [ ] T-AER-006 Quality/runtime-readiness/security audit and pack consolidation

### Phase 3 — Typed Metadata

- [ ] T-AER-007 Profiles, validator, tests, and advisory inventory
- [ ] T-AER-008 Active-chain migration and changed/new enforcement

### Phase 4 — Development Harness

- [ ] T-AER-009 Controlled pre-commit wrapper
- [ ] T-AER-010 Provider and CI synchronization

### Phase 5 — Follow-up and Closure

- [ ] T-AER-011 Runtime follow-up specs/plans
- [ ] T-AER-012 Full verification, review, and closure

## Verification Summary

- **Baseline Commands**:
  - `git diff --check` — PASS
  - `bash scripts/validation/check-doc-traceability.sh` — PASS, `failures=0`
  - `bash scripts/validation/check-doc-implementation-alignment.sh` — PASS, `failures=0`
  - `bash scripts/validation/check-repo-contracts.sh` — PASS, `failures=0`
  - `bash scripts/validation/validate-docker-compose.sh` — PASS, `services_total=5`
  - `bash scripts/hardening/check-all-hardening.sh` — PASS, all eleven tiers
- **Eval Commands**: Added by Tasks 7-10 and recorded with actual results.
- **Full QA Wrapper**: Executed only in Task 12 after wrapper tests and review.
- **Logs / Evidence Location**: This task document, `.superpowers/sdd/progress.md`, task reports, and review packages. Raw logs are not tracked.

## Deviation Notes

- Before execution, the plan's unittest command was normalized to discovery
  mode so `tests/validation/` does not require package marker files. This is a
  command-level correction with no scope or acceptance-criteria change.
- The SDD runtime tool does not expose a per-dispatch model argument. Dispatch
  prompts therefore bind each agent to the repository's Worker or Supervisor
  tier policy, while the platform selects the available concrete model.

## Related Documents

- [Parent specification](../../03.specs/123-agentic-engineering-audit-remediation/spec.md)
- [Parent plan](../plans/2026-07-11-agentic-engineering-audit-remediation.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
