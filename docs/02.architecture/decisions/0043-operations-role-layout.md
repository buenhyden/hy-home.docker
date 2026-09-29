---
title: "Operations Role Layout"
version: "0.1.2"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0043"
parent_ids:
- "AD-0030"
created: "2026-09-26"
---

# ADR-0043: Operations Role Layout

## Context

On 2026-08-13, SPEC-0158 and MIG-0002 converged Stage 05 into a domain-first
catalog. Documents live at
`docs/05.operations/catalog/<domain>/####-<subject>/{guide,policy,runbook}.md`, <!-- retired-route-record -->
and 13 domain READMEs plus the catalog README own discovery. The operations
validator from that time rejects the `guides/`, `policies/`, `runbooks/` paths
as a "retired root."

On 2026-09-26 the owner redefined Stage 05 as a people-centered layer for
safely operating the current workspace. A person first looks for a document by
asking "do I need to understand, do I need to know what is allowed, or do I
need a command to run." In the catalog structure, answering that same
question requires opening all 13 domains, and pressure to fill all three
roles builds up per subject folder.

Facts at baseline `0deb430ea`:

- 225 role documents (77 Guide, 75 Policy, 73 Runbook), 13 domain READMEs.
- Every `GDE`/`POL`/`RUN` number matches its subject folder number, with one
  exception: `0051-airflow-dag-lifecycle/policy.md` is `POL-0052`, a result of
  MIG-0002's merge.
- The `optimization-hardening` slug repeats across 7 domains.

## Decision Drivers

- People look first by role (understand, control, execute).
- Do not change issued IDs (documentation protocol authoring rule 5).
- Do not run two discovery systems in parallel.
- Do not rewrite Stage 98 frozen bodies and sealed records.

## Options Considered

1. **Keep the catalog**: No change cost, but leaves a structure the owner has
   explicitly said conflicts with the goal.
2. **Keep the catalog and add a per-role index**: Two discovery systems run in
   parallel permanently, exactly the state the README prohibits by banning
   "publishing a parallel per-role index."
3. **Switch to role-first paths (adopted)**: `guides/`, `policies/`,
   `runbooks/`, `incidents/` own the role, and domain remains an index
   classification.

## Decision

- Path: under `docs/05.operations/`, `guides/####-<slug>.md`,
  `policies/####-<slug>.md`, `runbooks/####-<slug>.md`. Incident and
  Postmortem paths are unchanged.
- The file number is the document's own artifact number
  (`identity_relation: direct`). Existing IDs stay as they are, so `POL-0052`
  becomes `policies/0052-airflow-dag-lifecycle.md`.
- The subject is the slug. The same slug across role directories points to the
  same subject, and within one role directory the slug is unique. The
  repeated `optimization-hardening` gets a domain word prefixed (for example,
  `data-optimization-hardening`).
- New subject numbers continue to be issued one per subject, as now, shared by
  that subject's role documents.
- Each role directory's `README.md` groups and lists its members by domain
  once. `catalog/`, the domain READMEs, and the `operations-domain-readme`
  profile and template are removed. No Stage 98 preserved document uses that
  profile, so no historical-only profile is kept.
- The operations validator treats `catalog` as a retired root and rejects any
  current document's mention of a catalog path as an active-reference
  violation.
- For external repository consumers, MIG-0005 announces the move's scope and
  current owner.

## Consequences

- Positive: People find documents directly by role. There is no structural
  reason to create empty documents just to fill a role.
- Negative: The three documents for one subject no longer sit in one folder.
  The matching slug across role indexes shows that relationship.
- Catalog links from other repositories break. This repository hands that off
  without fixing it.
- Stage 98 records and MIG-0002 continue to carry the catalog path as
  historical fact.

## Traceability

- Parent architecture: [AD-0030](../descriptions/0030-document-lifecycle-governance.md)
- Superseded structural decision: SPEC-0158 and MIG-0002's catalog convergence
  (Stage 98 preserved record)
- Execution: [SPEC-0183](../../03.specs/0183-operations-role-layout/spec.md)

## Compliance

`scripts/validation/check-operations-catalog.py`, the Registry's taxonomy
check, and `check-document-links.py --mode all` enforce this decision.

## Follow-up

- `inc-2026-0002` is unrelated to this decision. It was resolved on owner
  evidence (SPEC-0183 Task W13), and its postmortem is published.
- Fixing links in other repositories is performed by each repository's owner.
