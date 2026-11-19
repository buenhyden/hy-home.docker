---
title: "Operations Documents in Role and Domain Folders"
version: "0.3.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "ADR-0057"
parent_ids:
- "AD-0030"
created: "2026-11-06"
---

# ADR-0057: Operations Documents in Role and Domain Folders

## Context

### Problem and Drivers

Stage 05 is organized by role first, then by domain. Under
`docs/05.operations/`, the role directories `guides/`, `policies/` and
`runbooks/` each hold numbered domain folders (`01-common` to `15-labs`, for
example `05-databases-and-storage`), and each domain folder has its own
`README.md`. A member's path is `<role>/<NN-domain>/####-<slug>.md`. Incidents
keep their own directory.

- A reader looks first by role: understand, control or execute.
- A role directory with over a hundred members needs a second level to stay
  navigable.
- Issued IDs never change.
- One discovery system, not two.

#### Sources

No runtime state is claimed.

- [AD-0030 Document lifecycle governance](../01.descriptions/0030-document-lifecycle-governance.md)
- [Operations README](../../../05.operations/README.md)
- [ADR-0051 Summarize-and-delete retirement](0051-summarize-and-delete-retirement.md)

### Decision Scope

This decision covers the paths of Guides, Policies and Runbooks under
`docs/05.operations/`. Incident and postmortem paths are unchanged, and links
from other repositories are outside it.

## Options

### Considered Options

- Keep the domain-first catalog: rejected; answering "what may I do" means
  opening every domain.
- Catalog plus a parallel role index: rejected; two discovery systems.
- Flat role directories with one README each: rejected; the role READMEs grow
  long, and domain grouping lives only in prose.
- Role directories with numbered domain folders, one README per domain folder:
  selected.

### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep the domain-first catalog | The ADR records no benefit for this option. | Answering "what may I do" means opening every domain. | Rejected; answering "what may I do" means opening every domain. |
| Catalog plus a parallel role index | The ADR records no benefit for this option. | Two discovery systems. | Rejected; one discovery system is required, not two. |
| Flat role directories with one README each | The ADR records no benefit for this option. | The role READMEs grow long, and domain grouping lives only in prose. | Rejected; the role READMEs grow long, and domain grouping lives only in prose. |
| Role directories with numbered domain folders, one README per domain folder | A reader finds a document by role, then domain, without a parallel index. | The role documents of one subject sit in three directories related only by the shared number and slug, and each new domain needs a README in every role directory that uses it. | Selected; a reader looks first by role, a role directory with over a hundred members needs a second level, and issued IDs never change. |

- Negative: the role documents of one subject sit in three directories; the
  shared number and slug relate them.
- Negative: each new domain needs a README in every role directory that uses
  it.

## Decision

### Chosen Option

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

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval
record is linked. Effective from 2026-11-06.

#### Supersession

This record replaces ADR-0043, deleted in the same change (ADR-0051); ADR-0043
is historical and non-authoritative. ADR-0043
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
each.

## Consequences

### Impacts

- Positive: a reader finds a document by role, then domain, without a parallel
  index.

### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

Links from other repositories are fixed by those repositories' owners.

#### Compliance

`scripts/validation/check-operations-catalog.py`, the Registry taxonomy check,
and `check-document-links.py --mode all` enforce the layout.
