---
profile_id: spec
status: draft
artifact_id: SPEC-0158
artifact_type: spec
parent_ids: [REQ-0024, REQ-0025, ADR-0029, SPEC-0157]
created: 2026-08-31
updated: 2026-08-31
---

# Document Governance Lifecycle Convergence Specification

## Overview

The repository's registered document gates pass while semantic and lifecycle
drift remains in the corpus. At the design baseline, the selected stage roots
contain 588 tracked Markdown files. The largest active Plan has 19,023 lines,
the three completed Stage 98 Migrations have 19,878 lines combined, active
Stage 90 material still presents retired Stage 04 and predecessor paths as
current in places, and several Spec Packages have parent and child lifecycle
states that cannot all be true at once.

SPEC-0157 also has implementation commits while its Spec and Plan are `draft`
and it has no Task. This specification therefore starts by restoring an honest
SPEC-0157 chain, then converges the current corpus by lifecycle rather than by
directory. Canonical owners are repaired before non-normative evidence is
retired, compressed, or removed. Git remains the recovery boundary; Stage 98
does not become a copy of deleted bodies.

The convergence reduces authority and validation machinery. It creates no new
top-level stage, public suite, public gate profile, document lifecycle, audit
pack, progress document, or compatibility redirect.

## Boundaries and Inputs

### In Scope

- `docs/00.agent-governance/`, `docs/01.requirements/`,
  `docs/02.architecture/`, `docs/03.specs/`, `docs/05.operations/`,
  `docs/90.references/`, `docs/98.archive/`, and `docs/99.templates/`.
- Work in progress whose state affects those stages, beginning with SPEC-0157.
- Stage indexes, metadata, lifecycle, traceability, templates, generated
  provider adapters, and recovery records affected by a disposition.
- Registered document and governance validators, their focused tests, and the
  manifest or workflow routing needed to remove duplicate ownership.
- Fixtures and Git provenance logic that currently validate retired document
  bodies or pin branch and corpus state.

### Out of Scope

- Runtime mutation, deployment, remote systems, secrets, credentials, or live
  infrastructure validation.
- Product or service behavior changes unrelated to document truth.
- Changing the six public suite responsibilities fixed by ADR-0029.
- Creating a replacement taxonomy, a new lifecycle vocabulary, or a second
  provider-independent policy source.
- Preserving obsolete text merely because it is historical.

### Authoritative Inputs

- REQ-0024, Agent Governance Standardization.
- REQ-0025, Operational Readiness Closure.
- ADR-0029, Workspace Governance Authority.
- Stage 00 bootstrap, SDLC, documentation, approval, workflow, and authoring
  policies.
- Stage 99 Registry, schemas, and registered templates.
- The current script manifest and workflow contract.
- Git-tracked consumers, current branch state, and regular-blob recovery
  evidence measured at execution time.

## Behavior Contract

### Authority and Disposition

Every tracked target is covered exactly once by an ordered Task-local
disposition rule:

- `keep`: the artifact is current, uniquely owned, and consumed;
- `rewrite`: the owner is correct but its current text is not;
- `consolidate`: unique current content moves into one canonical owner;
- `supersede`: useful point-in-time evidence remains explicitly non-current;
- `delete`: no current authority, consumer, or preservation need remains;
- `tombstone`: a deleted stable path needs a minimal recovery pointer.

These values are execution decisions, not document lifecycle statuses. A
verified `keep` cohort may be covered by one deterministic profile or path rule;
every non-`keep` target is listed by path. The Task records the rule, covered
count, exceptions, current owner, consumers, disposition, replacement, recovery
evidence, and review. The rules and exceptions must cover the measured target
set without overlap or omission. Missing or ambiguous evidence blocks mutation.

### Stage Responsibilities

- Stage 00 is the sole provider-neutral AI-agent policy, role, skill, provider
  boundary, and SDLC authority.
- Stage 01 owns current solution-independent requirements. Substantively
  duplicate packages converge on one owner.
- Stage 02 owns current architecture descriptions and the durable ADR log.
  Superseded ADRs remain in that log.
- Stage 03 keeps current capability Specs and honest change packets. Completed
  or cancelled execution bodies do not remain active guidance.
- Stage 05 keeps procedures for current operational subjects. Duplicate
  procedures converge on one subject owner.
- Stage 90 keeps non-normative evidence only when provenance and a current
  consumer justify it. Stale observations are shortened and superseded or are
  deleted.
- Stage 98 keeps minimal migration and tombstone recovery navigation. It stores
  no deleted body, snapshot, raw Task ledger, or duplicate digest.
- Stage 99 is the sole machine authority for document paths, profiles,
  identifiers, sections, lifecycle, traceability shapes, and copy templates.
  Provider Registry ownership of runtime projection paths is a separate,
  narrower namespace and does not compete with this document-path authority.

### SDLC State

- An active Task has active Spec and Plan parents.
- A terminal or superseded parent has no active child.
- A completed Plan has only terminal Tasks.
- A current capability Spec may remain active without a Plan or Task.
- A change-packet Spec becomes terminal when its results have been written to
  current owners and its recovery boundary is known.
- Existing non-conforming work is recorded as discovered and revalidated; it
  is never described as retroactively approved.

### Agent Responsibility

- The user or operator grants approval.
- `workflow-supervisor` coordinates scope, order, handoff, and stop conditions
  without becoming the default writer.
- `doc-writer` edits approved canonical documentation.
- The actual Task owner records its own execution evidence.
- `qa-engineer` owns deterministic validator, fixture, and test changes.
- `eval-engineer` verifies evidence and evaluations but does not impersonate
  the evidence author.
- `rules-engineer` gives an independent governance verdict; that verdict is
  not user approval.
- `code-reviewer` independently reviews the exact diff and acceptance evidence.
- `hook-developer`, `ci-cd-engineer`, and `security-auditor` participate only
  when their protected surfaces change.

### Validation Ownership

The public suite names and the public `changed` and `full` profiles remain
stable. Within that interface:

- Stage 99 Registry owns document validity;
- `scripts/manifest.yaml` owns validator inventory and suite membership;
- `.github/workflow-contract.yml` owns CI routing and execution context;
- each validator owns its domain predicate;
- the current Task owns observed results.

No Task-numbered immutable inventory may restate the manifest.

## Technical Approach

### Wave 0: Restore SPEC-0157

Measure the commits and remaining work on the SPEC-0157 branch. Transition its
Spec and Plan through the registered lifecycle, create a current Task, and
record earlier commits as implementation discovered and revalidated at the
current revision. Do not claim prior approval. Because changed-document
validation compares merge-base endpoints, land the legal SPEC-0157 activation
and implementation while its Spec remains `active`, then close it from an
updated base where `active -> completed` is a legal endpoint. Complete or
explicitly defer the remaining bounded work, run the full gate, and close the
packet before corpus convergence implementation begins. Do not bypass the
merge boundary with a transition override.

### Wave 1: Classify the Corpus

Re-derive the tracked target set and create the complete disposition rule set in
the current Task. Cover unchanged cohorts by deterministic rule and list every
non-`keep` target explicitly. Measure profile, lifecycle, authority, consumers,
duplicate purpose, retired-path literals, generated provenance, Gate and fixture
references, commit pins, and recovery. Mutation begins only after the rules and
exceptions cover the target set exactly once and every destructive disposition
has passed recovery and review checks.

### Wave 2: Converge Canonical Owners

Repair Stage 00 and Stage 99 boundaries first. Then update the affected Stage
01, Stage 02, and Stage 05 owners. Clarify that Stage 99 paths are document
paths and provider-registry paths are runtime projection paths. Separate
workflow coordination, mutation, evidence writing, evaluation, review, and
human approval in the existing role and provider contracts. Regenerate
registered provider adapters only after their canonical inputs are correct.

### Wave 3: Normalize SDLC Packages

Classify Stage 03 packages as current capability contracts or bounded change
packets. Reconcile actual work and lifecycle status, including the known
SPEC-0136, SPEC-0154, SPEC-0155, and SPEC-0157 inconsistencies. Reassess stale
active Tasks in SPEC-0102, SPEC-0123, SPEC-0134, and SPEC-0135 against current
consumers and branch evidence. Compress or remove obsolete execution detail
only after its current outcome and recovery have been captured.

### Wave 4: Reduce Evidence and Archive

Retain Stage 90 sources only when their provenance and current consumer remain
useful. Remove current-sounding predecessor taxonomy from retained evidence.
Reduce completed Stage 98 Migrations to concise versions of all registered
required sections: Purpose, Authority Change, Path Mapping, Recovery, Approval,
and Traceability. Retain only required metadata and evidence needed to preserve
Migration 0003 as the structural disposition and recovery boundary. Add a
Tombstone only for a stable retired path that still needs recovery navigation.
Never create a body copy or redirect.

### Wave 5: Simplify Gates, Fixtures, and SHA Tracking

Derive validator inventory from the script manifest and remove duplicate
immutable inventories. Preserve the six public suites and the `changed|full`
profiles. Merge lifecycle and Operations modes only after consumer and
equivalence proof; retain Stage 98 recovery validation.

Document-contract tests use three fixture forms only: a current contract
derived from the Registry, a one-field mutation, and a temporary-Git recovery
case. They do not resurrect deleted documents from a fixed workspace commit,
copy full historical bodies, or pin fixture and corpus counts.

Allow commit identifiers only for supply-chain pins, minimal Stage 98 recovery,
actual logical implementation commits recorded in the current Task, and a
bounded transition fallback proven to have a live recovery consumer. Remove
branch-tip equality, expected design or implementation SHA chains, persistent
blob or diff digest ledgers, historical byte equality, and test-only workspace
commit pins. This does not remove an ephemeral digest comparison required by
the shared-worktree concurrency policy; that comparison is not retained as a
document lineage control.

### Wave 6: Verify and Close

Run focused checks with each change, then the complete document, governance,
Operations, provider-parity, unit-test, and full CI profiles. Obtain independent
policy and exact-diff review. Write current outcomes back to canonical owners,
close terminal packets, and remove temporary or verbose execution material once
its registered recovery is proven.

## Interfaces and Data

| Interface | Contract after convergence |
| :--- | :--- |
| Stage 99 Registry | Sole machine source for document contracts and allocation |
| Provider Registry | Typed runtime routing, model, permission, hook, and projection data under Stage 00 policy |
| Stage authoring matrix | One writer, validator, and independent-review mapping per stage |
| Script manifest | Sole validator inventory and suite membership |
| Workflow contract | Public profile and CI execution routing |
| Disposition rule set | Task-local complete coverage rules plus explicit non-`keep` paths; never a lifecycle registry or corpus copy |
| Migration | Minimal path mapping and recovery evidence; no execution body |
| Tombstone | Minimal stable retired-path recovery pointer |
| Fixture | Current generated contract, one-field mutation, or temporary-Git recovery case |

Generated provider adapters may consume Stage 00 sources and provider routing
data but may not define policy, roles, lifecycle, templates, model intent, or
completion. Consumerless generated rules or workflows projections are removed;
retained projections receive an explicit canonical-source mapping.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| :--- | :--- |
| A useful historical source is deleted as merely old | Require provenance, current-consumer, replacement, recovery, and review decisions separately |
| Historical evidence remains active guidance | Supersede and shorten it or delete it; active owners never defer to Stage 90 |
| SPEC-0157 is presented as previously approved | Record the anomaly and current revalidation; preserve the real transition order |
| A Task disposition becomes a new lifecycle | Keep disposition values local to execution; validate document status against Stage 99 only |
| Stage 98 reduction breaks recovery | Prove every retained `commit:path` resolves to a regular Git blob before mutation |
| Gate reduction drops a live guarantee | Search every registered and direct consumer, add the replacement test, then remove the old path |
| Fixture cleanup removes a real domain oracle | Limit this reduction to document-contract history fixtures; retain agent-output and supply-chain oracles |
| Provider projection becomes a policy source | Correct canonical inputs first, generate through the registered renderer, and verify parity |
| A role grants approval it cannot own | Separate human approval, policy verdict, evidence evaluation, and mutation permissions |
| SHA reduction weakens concurrent-worktree safety | Retain policy-required ephemeral digest comparison but never persist it as lineage evidence |
| A public suite responsibility must change | Stop and require a separate ADR rather than expanding this specification |
| Concurrent or dirty state makes ownership unclear | Stop the Wave, preserve the state, and reclassify before editing |

## Acceptance Contract

1. Ordered Task-local rules and exceptions cover every tracked target at the
   execution baseline exactly once. Every non-`keep` path is explicit and has
   owner, consumer, replacement, recovery, and review evidence; unchanged
   cohorts are not copied into a path-by-path audit pack.
2. Active documents contain no retired Stage 04, predecessor support, rules,
   memory, agent, Spec-path, or template path presented as current procedure.
3. No two active Requirement, Architecture Description, Spec, Operations, or
   governance documents own the same purpose or rule.
4. Active Task, Plan, and Spec states are mutually consistent, and only actual
   work in progress remains active.
5. SPEC-0157 is normalized without retroactive approval and passes its full
   completion gate before SPEC-0158 implementation.
6. Stage 90 retained evidence has provenance and a current consumer; stale
   observations are explicitly superseded and concise or are deleted.
7. Stage 98 contains no deleted body, snapshot, raw execution ledger, or
   duplicate digest, and every recovery tuple resolves to a regular Git blob.
8. Stage 99 Registry and templates contain no parallel or unused document
   authority, and every retained template has a registered target role.
9. The six public suites and `changed|full` profiles remain stable, every
   manifest validator executes exactly once in `full`, and no Task-numbered
   immutable validator inventory remains.
10. Document-contract tests contain no fixed-workspace historical document
    resurrection, fixture-count pin, corpus-count pin, or count-bearing test
    name.
11. Active Plans contain no branch-tip equality, expected SHA lineage,
    persistent blob or diff digest ledger, or historical byte-equality control.
    Only approved recovery, supply-chain, actual Task commit evidence, and
    policy-required ephemeral concurrency checks remain.
12. Workflow coordinator, writer, evidence author, evaluator, governance
    reviewer, exact-diff reviewer, and human approver responsibilities are
    distinct in canonical Stage 00 and provider routing.
13. Stage 99 document-path authority and Provider Registry runtime-projection
    authority are explicitly disjoint; renderer and hook inventories are
    derived from their declared owner rather than a second code constant.
14. Generated provider adapters are byte-for-byte fresh and define no policy.
15. Metadata active and contract checks, document graph, document lifecycle and
    recovery, agent-governance repository checks, Operations complete, focused
    unit tests, provider parity, `git diff --check`, and the full CI profile all
    pass.
16. No runtime, remote, deployment, secret, or infrastructure state is changed.

## Traceability

| Parent | Coverage |
| :--- | :--- |
| REQ-0024 | Canonical AI-agent governance, role separation, provider projection boundaries, and current Stage terminology |
| REQ-0025 | Approved Spec/Plan/Task sequence, targeted and full validation, independent review, recovery, and honest completion |
| ADR-0029 | Stage 00/99 authority split, six public suites, Task evidence, Stage 90 non-authority, and Stage 98 recovery boundary |
| SPEC-0157 | Script and test ownership, reachable validation, current fixtures, derived census, and bounded Git-history behavior |

## Operational Impact

This specification changes tracked documentation, validation, tests, and
generated provider adapters only. It performs no deployment, restart, remote
mutation, credential access, secret inspection, or runtime recovery. Any
discovered runtime discrepancy is recorded as a separate deferred owner rather
than inferred from documentation.

## Related Documents

- [Agent Governance Standardization Requirement](../../01.requirements/0024-agent-governance-standardization.md)
- [Operational Readiness Closure Requirement](../../01.requirements/0025-operational-readiness-closure.md)
- [Workspace Governance Authority ADR](../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [Script Surface Ownership Convergence](../0157-script-surface-ownership-convergence/spec.md)
- [SDLC](../../00.agent-governance/sdlc.md)
- [Stage Authoring Matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Stage 99 Registry](../../99.templates/registry.json)
- [Stage 98 Archive](../../98.archive/README.md)
