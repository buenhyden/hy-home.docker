---
title: "Operations Documents in Role and Domain Folders"
version: "0.2.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "ADR-0057"
parent_ids:
- "AD-0030"
created: "2026-11-06"
---

# ADR-0057: Operations Documents in Role and Domain Folders

## Context

Stage 05 is organized by role first, then by domain. Under
`docs/05.operations/`, the role directories `guides/`, `policies/` and
`runbooks/` each hold numbered domain folders (`01-common` to `15-labs`, for
example `05-databases-and-storage`), and each domain folder has its own
`README.md`. A member's path is `<role>/<NN-domain>/####-<slug>.md`. Incidents
keep their own directory.

### Traceability

This record replaces ADR-0043, deleted in the same change (ADR-0051). ADR-0043
(2026-09-26) moved Stage 05 out of the domain-first catalog
(`catalog/<domain>/####-<subject>/{guide,policy,runbook}.md`, from SPEC-0158 and
MIG-0002) into role-first paths, executed by SPEC-0183. It kept issued IDs (so
`POL-0052` became an Airflow DAG lifecycle policy), made the slug the subject
with a domain prefix for repeated slugs such as `optimization-hardening`, kept
one subject number shared by a subject's role documents, made the operations
validator reject catalog paths, and announced the move to external consumers
through MIG-0005. It rejected keeping the catalog and adding a parallel role
index. Those decisions carry forward. Its flat paths `<role>/####-<slug>.md` and
its removal of domain READMEs are replaced by domain folders with one README
each. No runtime state is claimed.

## Decision Drivers

- A reader looks first by role: understand, control or execute.
- A role directory with over a hundred members needs a second level to stay
  navigable.
- Issued IDs never change.
- One discovery system, not two.

## Options

### Alternatives

- Keep the domain-first catalog: rejected; answering "what may I do" means
  opening every domain.
- Catalog plus a parallel role index: rejected; two discovery systems.
- Flat role directories with one README each: rejected; the role READMEs grow
  long, and domain grouping lives only in prose.
- Role directories with numbered domain folders, one README per domain folder:
  selected.

## Decision

1. A Guide, Policy or Runbook lives at `<role>/<NN-domain>/####-<slug>.md`
   under `docs/05.operations/`. Incident and postmortem paths are unchanged.
2. Every role directory and every domain folder has a `README.md` that lists
   its members.
3. The file number is the document's own artifact number; issued IDs stay.
   One subject number is shared by that subject's role documents, and the same
   slug across role directories names the same subject.
4. Within one role directory a slug is unique; a repeated slug takes a domain
   prefix.
5. The domain catalog is a retired root; a current document that names a
   catalog path is an active-reference violation.

## Consequences

- Positive: a reader finds a document by role, then domain, without a parallel
  index.
- Negative: the role documents of one subject sit in three directories; the
  shared number and slug relate them.
- Negative: each new domain needs a README in every role directory that uses
  it.

### Compliance

`scripts/validation/check-operations-catalog.py`, the Registry taxonomy check,
and `check-document-links.py --mode all` enforce the layout.

### Follow-up

Links from other repositories are fixed by those repositories' owners.

## Related Documents

- [AD-0030 Document lifecycle governance](../descriptions/0030-document-lifecycle-governance.md)
- [Operations README](../../05.operations/README.md)
- [ADR-0051 Summarize-and-delete retirement](0051-summarize-and-delete-retirement.md)
