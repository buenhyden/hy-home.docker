---
status: active
artifact_id: task:2026-07-15-agent-governance-harness-convergence
artifact_type: task
parent_ids:
  - plan:2026-07-15-agent-governance-harness-convergence
---

# Task: Agent Governance Harness Convergence

## Overview

This Task is the durable execution ledger for Spec 132 and its six-unit Plan.
It records approved boundaries, fresh-agent assignments, RED/GREEN results,
independent reviews, logical commits, controlled all-files evidence, generated
freshness, deviations, and final closure. It does not restate the design.

Execution occurs on branch `codex/agent-governance-harness-convergence` in the
linked worktree `.worktrees/agent-governance-harness-convergence`. Planning is
complete; implementation evidence is `not_run` until each command is actually
executed.

## Inputs

- Spec: `docs/03.specs/132-agent-governance-harness-convergence/spec.md`
- Plan:
  `docs/04.execution/plans/2026-07-15-agent-governance-harness-convergence.md`
- Approved planning baseline: `6cde68dc`
- Work units: `T-AGHC-001` through `T-AGHC-006`
- Canonical governance: `docs/00.agent-governance/`
- Canonical audit:
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md`
- Controlled QA owner:
  `scripts/validation/run-agent-precommit-all-files.sh`

## Goals and Non-goals

Goals:

- make Stage 00 the machine-enforced owner of artifact, catalog, provider,
  model, path-authority, harness, and loop semantics;
- normalize root, governance, and provider surfaces by artifact/native schema;
- converge the canonical role/function catalog and provider projections;
- add tested semantic loops, QA selection, CI enforcement, and dated evidence;
- close with independent task and branch reviews, logical commits, controlled
  all-files QA, and a clean worktree.

Non-goals:

- user-global provider configuration, credentials, secrets, or entitlement;
- runtime Compose, infrastructure, deployment, release, or remote GitHub
  mutation;
- wholesale `agency-agents` intake or an always-on orchestrator;
- floating/preview model defaults or unobserved provider-runtime claims;
- merge to `main`, push, PR creation, or worktree deletion without a later
  explicit instruction.

## Scope and Change Boundaries

Allowed authored paths:

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`;
- `.agents/**`, `.claude/**`, `.codex/**`, new `.gemini/**`;
- `.github/CODEOWNERS`, `.github/PULL_REQUEST_TEMPLATE.md`,
  `.github/labeler.yml`, `.github/workflows/ci-quality.yml`, and no unrelated
  GitHub surface or workflow;
- `docs/00.agent-governance/**`;
- Spec 132, this Plan, this Task, and existing Stage 03/04 routing;
- directly affected Stage 90 canonical research, audit, data, indexes, and
  generated inventory;
- directly affected active Stage 05 policy/runbook owner references for the
  retired LLM Wiki role, without broader operations-corpus normalization;
- directly affected Stage 99 metadata profile/frontmatter support only;
- coupled operations/validation/knowledge scripts, script routing, focused
  tests, and `.pre-commit-config.yaml`.

Forbidden paths/actions:

- user-global `.claude`, `.codex`, or `.gemini` configuration;
- credentials, tokens, auth files, private keys, shell history, raw logs, or
  secret values;
- Compose service definitions, infrastructure runtime, deployment runtime,
  release/promotion, and remote GitHub resources;
- unrelated Stage 01 through Stage 99 corpus rewrites;
- direct `pre-commit run --all-files`, `--no-verify`, history rewriting, or
  destructive Git cleanup.

Compose impact: none.

Security impact: least-privilege agent, hook, sandbox, CI, and evidence
hardening only. No identity, secret-store, network, or runtime security-resource
change.

Operations impact: repository governance and quality automation only. No
service, incident, release, deployment, or on-call behavior changes.

Runtime impact: provider project configuration and read-only CI/QA definitions
only. Provider-global and application/runtime configuration are excluded.

## Approval Evidence

Approval source:

- The user approved a staged canonical convergence and explicitly included
  `.gemini/**`.
- The user approved capability-gap-only use of `agency-agents`.
- The user approved official current model revalidation as of 2026-07-15 KST,
  with stable/preview/deprecated/entitlement separation and no moving latest.
- The user approved type-specific metadata, the controlled all-files wrapper,
  and governance/development harness priority.
- The user approved Spec 132 and repeatedly approved continued implementation.
- The user selected Subagent-Driven execution.

Protected surfaces:

- Stage 00 contracts/governance, provider adapters/hooks, QA/CI, CODEOWNERS,
  Stage 99 integration, and canonical audit evidence may change within this
  Plan.
- Provider-global settings, credentials, runtime/deployment surfaces, remote
  GitHub state, and unrelated documents remain protected.

Approval boundary:

- Local authored/generated changes, tests, local commits, and read-only
  validation are authorized.
- Runtime, remote, credential, push, PR, merge, and worktree-deletion actions
  are not authorized by this Task.

Rollback or recovery:

- Revert logical task commits in reverse dependency order.
- Regenerate only outputs owned by the reverted task.
- Never use `git reset --hard`, rewrite history, or remove unrelated user work.

Redaction boundary:

- Evidence records commands, exit states, stable finding codes, bounded paths,
  counts, hashes of approved generated evidence, commit identities, and review
  verdicts.
- Evidence never records raw logs, provider prompt payloads containing private
  data, token values, credentials, auth files, shell history, or secrets.

## Work Breakdown

| Work unit | Responsibility | State |
| --- | --- | --- |
| T-AGHC-001 | Typed contracts and contract-only validator | Not run |
| T-AGHC-002 | Metadata, authority, root shims, and governance normalization | Not run |
| T-AGHC-003 | Agent/function catalog and canonical skill source | Not run |
| T-AGHC-004 | Provider-native adapters and dated model policy | Not run |
| T-AGHC-005 | Harness loops, semantic eval, local QA, and CI | Not run |
| T-AGHC-006 | Reference/audit/evidence reconciliation and closure | Not run |

## Work Log

| Date | Work unit | Agent role | Result |
| --- | --- | --- | --- |
| 2026-07-15 | Planning | Controller | Approved Spec 132 activated; Plan and this execution ledger authored. |
| 2026-07-15 | Planning review | Read-only discovery agents | Exact metadata, provider, CI/eval/audit integration maps requested; findings incorporated before the planning commit. |
| 2026-07-15 | Planning lifecycle routing | Controller | Added this Plan as the exact new active consumer of five promoted Foundation sources: progress, the Stage 03 index, both Stage 04 indexes, and the frontmatter contract. Regenerated the canonical summary without changing dispositions, verdicts, enforcement, or other rows. |

Implementation rows are appended only after the relevant agent finishes work.

## Verification Evidence

Planning verification:

| Command | Expected | Actual | State |
| --- | --- | --- | --- |
| changed metadata against `6cde68dc` | zero violations | selected 9; violations 0; legacy exceptions 0; transition overrides 0 | Pass |
| promoted/impacted lifecycle | zero violations | promoted 0; impacted selected 202 with 0 violations and the configured Task-directory budget warning | Pass |
| document traceability | zero failures | 46 catalog pairs; failures 0 | Pass |
| documentation alignment | zero failures | 653 stage docs; 5,204 local links; 141 operations docs; failures 0 | Pass |
| repository contracts | `failures=0` | `failures=0` | Pass |
| generated index/coverage/inventory checks | fresh | index 1,309 paths; coverage 1,308 safe paths; inventory 911 records / 2,160 advisory findings | Pass |
| staged diff hygiene and scoped pre-commit | no failures | `git diff --cached --check` clean; all applicable scoped hooks passed | Pass |

Per-task focused evidence and the final full ladder are appended with exact
commands, exit states, bounded counts, and observed results. A planned command
is never recorded as a pass.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command: not run. Task 6 will record the exact current CLI
invocation after checking the wrapper help and contract.

Allowed prefixes: not run. The final list must be limited to the approved root
shims, provider/compatibility trees, Stage 00, coupled Stage 03/04/90/99 paths,
validation/operations/knowledge scripts, focused tests, CI workflow,
CODEOWNERS, and `.pre-commit-config.yaml`.

Exit status: not run.

Snapshot result: not run.

Observation boundary: clean linked worktree, sanitized summary only, no raw
logs or secret-bearing data.

Observed path sets: not run.

Disposition: pending Task 6.

## Review Evidence

Planning implementation review verdict: controller self-review PASS. Tasks 1
through 6 remain not run.

Planning specification/plan review verdict: independent read-only reviewer
PASS with Critical 0, Important 0, and Minor 0 after three correction rounds.
Tasks 1 through 6 and the whole branch remain not run.

Quality review verdict: not run for Tasks 1 through 6 or the whole branch.

Planning findings and disposition: fixed provider skill discovery, Gemini
`PreCompress`, wrapper clean-state ordering, staged aggregate-validator
migration, exact path boundaries, CODEOWNERS identity, micro-step granularity,
closure verification, and narrow wrapper allowlists. No planning finding is
open. Future Critical and Important findings must be resolved and re-reviewed
before a task closes. Minor findings are either fixed or explicitly deferred
with owner, reason, and destination.

## Commit Ledger

| Logical unit | Planned commit | Identity | Validation |
| --- | --- | --- | --- |
| Planning | `docs(plan): plan agent governance harness convergence` | pending | pending |
| T-AGHC-001 | `feat(governance): add typed agent governance contracts` | pending | pending |
| T-AGHC-002 | `refactor(governance): normalize agent authority and metadata` | pending | pending |
| T-AGHC-003 | `refactor(agents): converge role and function catalogs` | pending | pending |
| T-AGHC-004 | `feat(providers): generate native agent adapters` | pending | pending |
| T-AGHC-005 | `feat(harness): enforce agent loops and semantic gates` | pending | pending |
| T-AGHC-006 | `docs(governance): reconcile agent harness evidence` | pending | pending |
| Controlled QA evidence | `docs(governance): record controlled agent QA evidence` | pending | pending |
| Closure | `docs(execution): close agent governance convergence` | pending | pending |

Material review remediations receive separate rows rather than being folded
into unrelated commits.

## Deferred and Blocked Items

Deferred by design:

- Provider runtime acceptance or entitlement that cannot be observed locally
  remains `needs_revalidation`.
- Preview, deprecated, invitation-only, and exceptional models remain
  non-default catalog entries.
- Runtime Compose, infrastructure, deployment, release, security-resource, and
  remote GitHub changes require independent approved follow-up work.
- Product-discovery agent intake remains deferred until recurring demand and a
  representative evaluation exist.

Blocked items: none at planning time.

Deferral destination: the applicable provider registry entry, canonical audit
recommendation, or separately approved Stage 03/04 chain. No deferred item is
silently treated as complete.

## Related Documents

- [Spec 132](../../03.specs/132-agent-governance-harness-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-15-agent-governance-harness-convergence.md)
- [Stage 00 Governance](../../00.agent-governance/README.md)
- [Canonical Agentic Audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Canonical Agentic Research](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Task Template](../../99.templates/templates/sdlc/task.template.md)
