---
title: "Operations Role Layout Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0183"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-09-26"
---

# Operations Role Layout Specification

## Overview

Replace the domain-first Stage 05 catalog
(`docs/05.operations/catalog/<domain>/####-<subject>/{guide,policy,runbook}.md`) <!-- retired-route-record -->
with a role-first layer that a person operating this workspace reads by
purpose: `guides/` for stable operating context, `policies/` for approval,
security, and exception boundaries, `runbooks/` for executable command flows,
and `incidents/` for event facts with their postmortems. The owner requested
this change on 2026-09-26 and named the catalog taxonomy the replaced
contract; [ADR-0043](../../02.architecture/decisions/0043-operations-role-layout.md)
records the decision. The change is documentation and validation only. It
authorizes no service, data, credential, network, or remote action.

## Boundaries and Inputs

Inputs are the current Stage 05 tree (225 role documents, 13 domain READMEs,
the catalog README, the root and incident READMEs, one incident), the Stage 99
Registry, the operations validator
(`scripts/lib/document_governance/operations_catalog.py`), the link, taxonomy,
archive, and manifest validators and their tests, and every active consumer
of a catalog path found by `git grep` at baseline `0deb430ea`.

In scope:

- Registry path patterns, identity relation, README registration, and the
  removal of the `operations-domain-readme` profile and its template.
- The move of every role document, the role indexes that replace the domain
  READMEs, and every inbound and outbound link and path mention on active
  surfaces.
- The operations validator, the archive tombstone identity derivation, and
  their regression tests.
- The confirmed stale statements named in the request: the missing LLM Wiki
  generator in `scripts/README.md` and the dated "no incident" note in the
  incidents README.
- A route disposition (MIG-0005) for consumers outside this repository.

Out of scope: Stage 98 frozen bodies and sealed records, which keep the paths
they were written with; the gate identifier `leaf.operations-catalog`, its
entrypoint name, and CI required-check names; the CouchDB `NODENAME` and
`lab_net` aliases; the state of `inc-2026-0002`; and any runtime or remote
action, including push and pull request.

## Behavior Contract

1. Stage 05 holds exactly `README.md`, `guides/`, `policies/`, `runbooks/`,
   and `incidents/`. Each role directory holds a `README.md` index and
   `####-<slug>.md` members only.
2. A member's file number is its artifact number: `guides/0051-x.md` carries
   `GDE-0051`. Every existing `GDE`, `POL`, and `RUN` identifier is kept; no
   identifier is issued or renumbered by the move.
3. A subject is its slug. The same slug in two role directories names the same
   subject, so sibling Guide, Policy, and Runbook stay related without a
   shared directory. A slug is unique within one role directory.
4. Each role index lists every member once, grouped by domain. Domain is an
   index classification, not a path segment.
5. No active document or automation names `docs/05.operations/catalog/` as a <!-- retired-route-record -->
   current route. The validator rejects such a mention outside Stage 98,
   Stage 90, Stage 03 execution bodies, and tests, and rejects a
   reintroduced `catalog/` directory.
6. The incident and postmortem contract is unchanged.

## Technical Approach

The move is one closed dependency set and lands in one commit: Registry
patterns, the validator, tests, the moved documents, their links, and every
consumer change together, so no intermediate commit leaves a document outside
its registered profile. Characterization tests are written first against the
new contract and observed failing on the old tree. Content corrections that
do not depend on the move land as separate commits.

`identity_relation` becomes `direct`, which the taxonomy validator already
enforces as file number equal to artifact number. Seven generic
`optimization-hardening` subjects take their domain word as a slug prefix so
that the slug stays a readable, unique subject name. The service inventory
binds a Guide to its Policy and Runbook by slug instead of by directory.

## Interfaces and Data

- Registry: `guide`, `policy`, and `runbook` path patterns and relation;
  `readme` additional paths; removal of `operations-domain-readme` and the
  `operation/domain-readme` template role; `migration` identity space.
- Validator codes kept: the existing finding codes. New or reinterpreted:
  `retired-root-present` for `catalog`, `role-path-invalid`,
  `role-slug-duplicate`, `role-index-membership-invalid`, and
  `active-operations-reference-invalid` for catalog routes.
- `tombstone_identity()` derives `tomb-GDE|POL|RUN-####` from a role path.

## Failure Modes and Guardrails

- A missed consumer leaves a broken link: `check-document-links.py --mode all`
  and the active-reference scan must both pass before commit.
- A renumbered identifier would break inbound `parent_ids`: the taxonomy
  check compares file and artifact numbers, and the move script aborts on a
  collision before writing.
- A frozen record rewritten to the new path would falsify history: Stage 98
  bodies, sealed Tombstones, and Migrations are excluded from rewriting.
- A path-only rewrite could corrupt a regression fixture that must keep the
  old path to prove rejection: fixtures are edited by hand, not by the move
  script.

## Acceptance Contract

1. The Registry registers role-first paths with `direct` identity, the three
   role READMEs as `common/readme`, and no `operations-domain-readme` profile
   or template; registry tests pass.
2. All 225 role documents live at their mapped role path with unchanged
   artifact identifiers and bodies apart from link targets; the catalog tree
   and its fourteen READMEs are gone.
3. Each role README lists its members exactly once, grouped by domain, and
   the Stage 05 README routes to the three role indexes and incidents.
4. `check-operations-catalog.py` passes on the new tree, and new regression
   tests prove it fails on a reintroduced catalog path, a number that differs
   from the artifact number, a duplicate slug, an unindexed member, and an
   active catalog mention.
5. `check-document-links.py --mode all` passes and no active surface names a
   catalog route; remaining mentions are classified as frozen, sealed,
   Stage 90 evidence, or rejection fixtures.
6. `scripts/README.md` names no missing generator or removed document, and
   the incidents README lists the current incident instead of the dated
   absence note.
7. MIG-0005 records the moved scope and current owner for outside consumers.
8. The changed and full CI gate profiles pass locally, or each failure is
   recorded with its baseline status.

## Traceability

- Requirement: [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- Architecture: [AD-0030](../../02.architecture/descriptions/0030-document-lifecycle-governance.md),
  [ADR-0043](../../02.architecture/decisions/0043-operations-role-layout.md)
- Plan: [plan.md](plan.md); Task: [TSK-0001](tasks/tsk-0001-operations-role-layout.md)

## Open Questions

None blocking. Live verification of `inc-2026-0002` and link updates in other
repositories are handoff items recorded in the Task.

## Operational Impact

Operators and agents find documents by role instead of by domain. Links from
other repositories to catalog paths stop resolving; MIG-0005 names the new
scope and the Task lists the observed outside references. No runtime
behavior changes.
