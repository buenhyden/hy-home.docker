---
title: "Stale Fact Convergence Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0176"
parent_ids:
- "REQ-0024"
- "REQ-0025"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0033"
created: "2026-09-07"
---

# Stale Fact Convergence Specification

## Overview

A repository-wide audit compared what the tracked documents assert against what
the tracked implementation does. Every registered gate passed while it ran, and
the audit still found four independent clusters of statements that the
implementation contradicts. That combination is the finding, not an accident:
the registered checks prove that a document exists, carries its profile, and
resolves its links, and none of them reads what a sentence claims.

The largest cluster is one retired model preserved in thirty-nine documents.
SPEC-0156 and SPEC-0171 converged Compose activation from "comment an `include`
line to disable a file" onto "include every file unconditionally and let
profiles select". The root `docker-compose.yml` carries the new model. The
documents that describe it still carry the old one, and they name specific
services as commented-out and optional that the root file includes.

The second cluster is the preservation-owner chain. `REQ-0026`, `AD-0030`, and
accepted `ADR-0031` state that a completed package preserves its Spec alone and
removes Plan and Task as transient carriers. The canonical policy, the
executable guard, and four preserved packages in the archive all keep every
document. `ADR-0033` was written as the successor for exactly this and has
waited at `proposed`.

The third cluster is position recorded by branch name. Two active Spec packages
name `codex/0173-agent-governance-home` as their current baseline. That branch
was retired into `main` and no longer exists, and `main` has advanced forty-five
commits past the commit those documents call current.

The fourth cluster is three isolated counting and routing errors: the Stage 02
index counts twenty-six ADRs where twenty-eight exist, the canonical repository
map restates a bootstrap load order that predates two canonical categories, and
the Stage 03 behavior contract of SPEC-0173 describes a fixture directory its own
Task emptied.

This package converges all four on the implementation rather than changing the
implementation to match the prose. Where a current-authority document is wrong,
its owner is corrected. Where a dated observation is wrong, it is left alone and
the correction is recorded beside it.

## Boundaries and Inputs

- Position is recorded from Git rather than by branch name, because a short
  branch retired at integration is dead before the next reader arrives. A
  resuming session reads `git rev-parse --abbrev-ref HEAD` for the branch,
  `git rev-parse HEAD` for the commit, and
  `git log --oneline origin/main..HEAD` for what is not yet on the remote. The
  durable facts are that `main` is the integration target and that the Task's
  Commit Ledger lists every commit this package produced.
- Audit baseline: local `main` at
  `e37b2dbcd877f6fbbf32205fd4f5e83680630dc9`, clean worktree, six commits ahead
  of `origin/main` at `d890b862e310b519802a1e837089b87a2b27cdf7`.
- Lifecycle budget, measured rather than assumed. The transition check reads
  `previous_status` from the merge base with `origin/main`, so a document present
  there admits exactly one transition on this branch and a document absent from
  it admits none. Every transition this package needs is one step from that base,
  except its own three new documents, which are therefore created at their
  initial statuses and advance only after the remote carries them.
- In scope, stated as the complete set of surfaces this package changes:
  - The thirty-nine documents under `infra/**`, `docs/05.operations/catalog/**`,
    and `docs/02.architecture/descriptions/` that describe a Compose file as a
    commented, optional, or standalone root include.
  - `infra/README.md`, whose Compose inventory snapshot carries both wrong counts
    and the retired four-state status vocabulary.
  - `infra/04-data/lake-and-object/minio/README.md`, which forbids describing
    `docker-compose.cluster.yaml` as part of the root include that contains it.
  - `docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md`,
    whose system scope counts files SPEC-0171 deleted.
  - The `include:` comment block in the root `docker-compose.yml`.
  - `docs/01.requirements/0026-document-retention-and-retirement.md` and
    `docs/02.architecture/descriptions/0030-document-lifecycle-governance.md`,
    whose retention clauses move to the accepted successor's model.
  - `docs/02.architecture/decisions/0033-full-spec-package-preservation.md`,
    which transitions to `accepted`, and
    `docs/98.archive/superseded/02.architecture/decisions/0031-preserved-archive-record.md`, whose
    accepted body is preserved unchanged under `docs/98.archive/superseded/`.
  - `docs/02.architecture/README.md` and
    `docs/02.architecture/decisions/README.md` for the resulting index facts.
  - `.agents/knowledge/repository-map.md` and
    `.agents/knowledge/verification-surface-map.md`.
  - `docs/03.specs/0173-governance-qa-surface-convergence/spec.md` and `plan.md`,
    for baseline position and one behavior-contract sentence.
  - `docs/03.specs/0175-governance-knowledge-and-prompt-surface/spec.md`,
    `plan.md`, and `tasks/tsk-0001-knowledge-and-prompt-surface.md`, which reach
    their terminal statuses and move to `docs/98.archive/completed/`.
  - `docs/README.md` and `docs/03.specs/README.md` for the affected index rows.
  - The generated LLM Wiki outputs under `docs/90.references/data/`, regenerated
    by the registered generator and never hand-edited.
- Out of scope and explicitly unchanged: the root `include:` list itself, any
  Compose service, profile, image, or network value, every validator and gate,
  `docs/99.templates/registry.json`, the Provider Registry, every role and skill
  identity, and the frozen bodies already under `docs/98.archive/`.
- SPEC-0173 remains active and blocked. Its Rulings forbid a new policy, Spec,
  Plan, or Task inside that package, so this work takes its own package. This
  package corrects two stale sentences in SPEC-0173's own documents and closes
  the retention-owner promotion SPEC-0173 declared as an open dependency; it does
  not complete SPEC-0173 and does not touch its Task evidence.
- Authorization: local edits, local commits on this branch, and local
  integration into `main`. Push, pull request, remote reference change,
  deployment, live service action, secret values, and global installation remain
  unauthorized. Pushing to `main` is additionally blocked by a registered hook
  and is not attempted by any other route.

## Behavior Contract

1. No tracked current-authority document describes a Compose file under `infra/`
   as commented out of, optional in, or absent from the root `include:` list
   while that file appears in it uncommented.
2. Documents that need to express conditional activation say that the root file
   includes every Compose file unconditionally and that the selected profile
   decides which services resolve, which is the model
   `docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md`
   owns.
3. Every count of Compose files, service directories, and root `include:` entries
   in a current document equals what the tracked tree holds.
4. The retention owner chain states one preservation unit. `REQ-0026`,
   `AD-0030`, and the accepted decision agree with
   `.agents/governance/documentation-protocol.md` and with the guard in
   `scripts/lib/document_governance/spec_packages.py` that a preserved package
   keeps its Spec, its Plan, and every Task.
5. `ADR-0031` keeps its accepted body byte-identical under
   `docs/98.archive/superseded/`, carries reciprocal supersession metadata with
   `ADR-0033`, and is not edited to agree with the later contract.
6. No package already preserved under `docs/98.archive/completed/` gains a
   retroactively authored Plan or Task. The scope each package was preserved with
   remains the historical fact.
7. The Stage 02 index states the number of Architecture Descriptions and
   Architecture Decisions the directory actually holds, and its structure block
   names the highest identifier present in each.
8. `.agents/knowledge/repository-map.md` states the canonical load order that
   `.agents/governance/bootstrap.md` owns, including when to read
   `.agents/knowledge/` and `.agents/prompts/`.
9. A knowledge member's provenance names, for each source it transcribes, the
   commit at which that source was read.
10. No active Spec package records its current position as a branch name that Git
    does not resolve, and no active Spec package names a superseded commit as the
    current baseline.
11. SPEC-0175 reaches `completed` across its Spec, Plan, and Task in one result
    tree, its three bodies move to
    `docs/98.archive/completed/03.specs/0175-governance-knowledge-and-prompt-surface/`,
    and the Stage 03 index describes it as preserved rather than active.
12. SPEC-0173's behavior contract does not describe `tests/fixtures/` as holding
    current synthetic input, and its acceptance criteria are otherwise unchanged.
13. Every generated output affected by these edits is regenerated by its
    registered generator, and its freshness check passes on the staged tree.
14. `python3 scripts/validation/run-ci-gate.py --profile changed` exits 0 on the
    final path set, and the document metadata, link, corpus lifecycle, and
    Spec-package checks report zero violations.

## Technical Approach

The corrections are applied at their owners and never by adding a second
statement beside a wrong one.

For the Compose cluster, one sentence pattern replaces another. The retired
pattern asserts a file's include state; the replacement asserts the profile that
selects the service, because that is what now decides whether it runs. Where a
document listed a four-state include vocabulary, the vocabulary is removed rather
than renamed, since the states it distinguished no longer exist.

For the retention chain, the promotion follows the sequence SPEC-0173's Plan
declared. `ADR-0033` transitions `proposed` to `accepted`. In the same result
tree, `ADR-0031` transitions `accepted` to `superseded`, its body moves unchanged
to `docs/98.archive/superseded/`, and the two decisions gain reciprocal
`supersedes` and `superseded_by` metadata. `REQ-0026` and `AD-0030` then lose the
transient-carrier clauses and state the preservation unit the accepted decision
owns. No frozen archive body is touched, and no already-preserved package is
back-filled.

For position, the two active packages adopt what SPEC-0175's Task already
concluded for itself: the branch name is removed and the three Git commands that
read position replace it. A commit hash stays where it names a dated event and is
replaced where it claimed to be current.

For SPEC-0175's completion, the three documents transition and move in one
change together with the Stage 03 index row, because a terminal status inside an
active stage is what the corpus check rejects and moving one member while its
siblings stay is what the retention guard rejects.

## Interfaces and Data

No executable interface changes. The public validation entrypoints, the provider
projection interface, the registered generators, and the Stage 99 contracts are
inputs to this package and are not modified by it.

The only machine-read structures this package writes are document frontmatter
fields already owned by the Stage 99 registry: `status`, `updated`, `version`,
`supersedes`, and `superseded_by`.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| --- | --- |
| A correction edits a frozen archive body to agree with the current contract | Frozen bodies are read-only; the corpus and archive checks fail on any byte change, and `ADR-0031`'s preserved body is compared before and after the move |
| A dated observation is rewritten to look current | Stage 90 and Task work-log entries keep their measurement and date; a later fact is recorded as a later entry |
| A Compose sentence is corrected by guessing the profile | Each replacement reads the `profiles:` value from the service's own Compose file rather than from any prose |
| A count is corrected by arithmetic on the old number | Each count is re-measured from the tracked tree at edit time and the command is recorded |
| More than one lifecycle transition per document is attempted on this branch | The transition budget is measured against the merge base first, and a document needing a second transition is left where it stands with the reason recorded |
| The retention promotion silently widens into a policy rewrite | `.agents/governance/documentation-protocol.md` already carries the accepted model and is not edited by this package |
| SPEC-0173 is advanced or completed as a side effect | This package changes two stale sentences in SPEC-0173 and nothing else in it; its blocked aggregate and Task evidence are untouched |
| A generated output is hand-edited | Generated outputs are produced only by their registered generator and their freshness check is run after staging |

## Acceptance Contract

1. Zero tracked current-authority documents assert a commented, optional, or
   absent root include for a Compose file the root `include:` list contains.
2. `infra/README.md` states the measured file, directory, and include counts and
   carries no four-state include vocabulary.
3. `docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md`
   counts only files that exist and does not describe SPEC-0171 as pending.
4. The root `docker-compose.yml` comment describes the sibling-pair resolution as
   completed rather than owned by an open package.
5. `ADR-0033` is `accepted` and `ADR-0031` is `superseded`, each carrying the
   reciprocal metadata of the other.
6. `ADR-0031`'s preserved body under `docs/98.archive/superseded/` is
   byte-identical to its pre-move body except for the frontmatter fields the
   transition owns, and the comparison is recorded.
7. `REQ-0026` and `AD-0030` state the full-package preservation unit and retain
   no transient Plan/Task removal clause.
8. `docs/02.architecture/README.md` routes to the per-directory indexes and the
   tracked file list as the count authority, in the same terms
   `decisions/README.md` already uses, and its structure block names `0030-` and
   `0034-` as the highest identifiers.
9. `.agents/knowledge/repository-map.md` step 3 names `.agents/knowledge/` and
   `.agents/prompts/` with the same conditions `bootstrap.md` states.
10. `.agents/knowledge/verification-surface-map.md` names the commit at which
    each transcribed source was read, and the two commits differ where the
    sources were read at different times.
11. Neither active Spec package contains `codex/0173-agent-governance-home` in a
    current-position statement, and each states how position is read from Git.
12. SPEC-0173's Spec no longer describes `tests/fixtures/` as current, and
    `git diff` shows no other change to its acceptance criteria.
13. SPEC-0175's Spec, Plan, and Task are `completed` and present under
    `docs/98.archive/completed/03.specs/0175-governance-knowledge-and-prompt-surface/`,
    with no member left under `docs/03.specs/`.
14. `docs/03.specs/README.md` describes SPEC-0175 as preserved and lists
    SPEC-0176 as the active package.
15. `docs/README.md` does not claim co-located Plan and Task evidence for a
    preserved package that holds only a Spec.
16. Every registered generated output touched by this package is fresh on the
    staged tree, proven by its own freshness check.
17. `python3 scripts/validation/run-ci-gate.py --profile changed` exits 0 on the
    final path set, with the command, path set, and exit code recorded.
18. An independent exact-diff review of the whole package reports no finding
    outside the current authorization, and every accepted finding is corrected
    before completion.

## Traceability

| Governing document | Relation |
| --- | --- |
| [REQ-0024 Agent Governance Standardization](../../01.requirements/0024-agent-governance-standardization.md) | Owns the canonical governance surface the knowledge corrections serve |
| [REQ-0025 Operational Readiness Closure](../../01.requirements/0025-operational-readiness-closure.md) | Owns the operational documentation accuracy the Compose corrections serve |
| [REQ-0026 Document Retention and Retirement](../../01.requirements/0026-document-retention-and-retirement.md) | Amended by this package to the accepted preservation unit |
| [AD-0027 Agent Governance Canonical Adapter](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md) | Owns the canonical/adapter boundary the load-order correction restates |
| [AD-0030 Document Lifecycle Governance](../../02.architecture/descriptions/0030-document-lifecycle-governance.md) | Amended by this package to the accepted preservation unit |
| [ADR-0033 Full Spec Package Preservation](../../02.architecture/decisions/0033-full-spec-package-preservation.md) | Accepted by this package as the durable decision owner |
| [ADR-0031 Archive as Preserved Record](../../98.archive/superseded/02.architecture/decisions/0031-preserved-archive-record.md) | Superseded and preserved by this package |
| [SPEC-0173 Governance and QA Surface Convergence](../0173-governance-qa-surface-convergence/spec.md) | Declared the retention-owner promotion this package performs; otherwise untouched |
| [SPEC-0175 Governance Knowledge and Prompt Surface](../0175-governance-knowledge-and-prompt-surface/spec.md) | Completed and preserved by this package |
| [POL-0078 Compose Profile Vocabulary](../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) | Owns the profile model the Compose corrections converge on |

## Open Questions

- SPEC-0173's aggregate remains blocked on the actual PostgreSQL operating and
  image leaf. This package closes its retention-owner dependency and does not
  change that blocker.
- The three new documents of this package cannot transition on the branch that
  creates them, because the transition check reads the merge base with
  `origin/main`. Whether they advance depends on the remote carrying them, which
  no authorization here grants.

## Operational Impact

No runtime, service, image, network, profile, secret, permission, model, hook, or
gate behavior changes. Every edit is to a document or a comment. The one
structural change is the move of four bodies inside `docs/`: SPEC-0175's three
members to `completed/` and `ADR-0031` to `superseded/`.
