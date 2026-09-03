---
title: Documentation Protocol
version: 1.0.0
type: governance/policy
status: active
owner: "@buenhyden"
---

# Documentation Protocol

## Authority

The Stage 99 registry is the only machine authority for paths, profiles,
required sections, lifecycle values, and identifier relations. Stage 00 owns
authoring behavior and `scripts/` owns executable validation.

## Document Boundaries

- Stage 01 owns long-lived solution-independent requirements.
- Stage 02 owns current architecture descriptions and durable decisions.
- Stage 03 owns a change behavior contract, technical approach, plan, Tasks,
  and executable interface contracts.
- Stage 05 owns operator guidance, policies, runbooks, and incidents.
- Stage 90 owns non-normative research, audits, and reference data.
- Stage 98 owns minimal migration and tombstone navigation; Git stores history.
- Stage 99 owns profiles, schemas, and copyable templates.

Do not create parallel PRD, SRS, interface-requirement, design, tests, release,
progress, or handoff authorities when the canonical package already owns the
content. Root `DESIGN.md` remains UI and design-system authority only.

## Authoring Rules

1. Select the registry profile before creating or moving a document.
2. Use four-digit numbered slugs where the profile requires an identity.
3. Keep dates in frontmatter; the incident year directory is the only path exception.
4. Store incident packets only at `docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md` and `docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md`.
5. Link canonical IDs in full and never reuse an issued ID.
6. Give a member document its container identity plus that container's own
   internal sequence, so the same member number may recur under two containers.
   The registry's `artifact_id_pattern` states the exact shape per profile.
7. Name a Stage 90 package member `m####-<slug>.md`; a Stage 03 Task keeps its
   `tsk-####-<slug>.md` name and an incident packet keeps `inc-####-<slug>/`.
8. Give a tombstone the retired document's identity under a `tomb-` prefix
   instead of allocating a new number.
9. Declare the frontmatter its registry profile requires, in the registry's
   `common.frontmatter_order`. The registry owns which keys a profile requires
   and permits; `contracts/frontmatter.schema.json` owns their value shapes.
   The reasons behind that envelope are the part this policy owns. `type`
   carries the `family/kind` document role, so a reader learns a document's
   family without resolving its path. `title` never repeats the artifact
   identity, because the identity is already a field. A new document starts its
   `version` at `1.0.0`, so a first revision is distinguishable from an unset
   value. `layer` names the owning stage without its numeric prefix and is
   omitted wherever the canonical path already states the authority. A profile
   without an identity declares no `artifact_id` and never invents one. A
   provider-owned runtime projection is exempt from this envelope entirely,
   because its shape belongs to the runtime that reads it.
10. Title a Stage 03 Spec as `<Subject> Specification`. The subject names what
    the change contracts, not the document class, so `Technical`, `Capability`,
    and other class words do not appear in it.
11. Keep a Stage 03 package to a bounded change. A package that describes a
    steady state belongs to the Stage 02 Description and Stage 05 subjects that
    own that state, and is retired to them.
12. Keep Stage 01 solution-independent. A requirement that names a specific
    middleware chain, container flag, volume path, or script is an
    implementation contract; it belongs to the Stage 03 Spec or Stage 05 policy
    that owns the implementation.
13. Update cross-links in the same logical change.
14. Record execution evidence in the co-located Stage 03 Task.
15. Validate metadata, links, and stage-specific contracts before completion.

Governance and internal technical authority is written in English. User-facing
guidance may follow the audience language when its template permits it.

Historical quotations retained in current Markdown must be a contiguous explicit
blockquote beginning `> Historical evidence (not current authority; source: Git history):`.
Keep source context with the quotation. It records an earlier observation or
decision, never a current instruction. Current obligations remain outside the
quote and must use current owners; a historical heading alone grants no exception.
For machine-consumed historical tables, place
`<!-- Historical evidence table (not current authority; source: Git history). -->`
immediately before the table header and separator. Only that contiguous table is
evidence; surrounding instructions remain current and validated normally.

### Gap-to-Stage Routing

| Gap Type | Owner | Rule |
| --- | --- | --- |
| Governance behavior | `docs/00.agent-governance/` | Change canonical policy, role, skill, or provider facts first. |
| Long-lived need | `docs/01.requirements/` | Record solution-independent requirements and acceptance. |
| Structure or durable decision | `docs/02.architecture/` | Update a description or ADR. |
| Change contract | `docs/03.specs/` | Update the bounded Spec Package. |
| Implementation sequencing | `docs/03.specs/####-<slug>/plan.md` | Record the approved implementation order. |
| Implementation evidence | `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` | Record result, deviation, and validation evidence. |
| Operator knowledge | `docs/05.operations/` | Update the applicable guide, policy, runbook, or incident. |
| External evidence | `docs/90.references/` | Preserve non-normative research, audit, or data. |
| Historical recovery | Git history; Stage 98 is non-authoritative | Recover prior content without creating a current authoring route. |
| Shape or lifecycle | `docs/99.templates/` | Change the registry, schema, or copyable template. |
| Protected or ambiguous change | `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` Task/audit gap first | Stop mutation and bind approval, scope, and recovery first. |

## Document Retention and Retirement

Retention follows lifecycle and ownership. Age and document count are never
retention criteria. A document is retained while it owns current behavior,
structure, decision, or procedure. It is retired when its status is terminal
and its still-current meaning has moved to a canonical owner.

### Retention by status

| Status | Stage 03 Spec Package | Stage 01 / Stage 02 document |
| --- | --- | --- |
| `draft` | keep every member | keep |
| `active` | keep every member | keep |
| `completed` | keep `spec.md`; mark `plan.md` and Tasks `completed` first, then remove them in a following change | not reachable in the `living` lifecycle |
| `superseded` | keep `spec.md` with `superseded_by`; execution members may be removed | keep with `superseded_by` |
| `retired` | remove the package and record one Tombstone | remove and record one Tombstone |

### Retirement preconditions

Retire a package or a standalone document only when all of these hold.

1. Its status is terminal: `completed`, `cancelled`, `superseded`, or `retired`.
2. Every still-current obligation, decision, structure, or procedure it owns is
   written to its canonical Stage 00, 01, 02, or 05 owner.
3. Every inbound consumer is updated in the same logical change.
4. One Stage 98 Tombstone records the retirement.

A package is never retired because it is old, because a count was exceeded, or
because nothing currently links to it. Missing inbound links are a defect to
investigate, not permission to delete.

Preconditions 1 to 3 are authoring obligations and are recorded in the
Tombstone's `Reason`. Precondition 4 is the enforced one: the comparison base
of a change is its branch point, so a package that is `active` there can never
be observed as terminal by the same change that retires it. The Tombstone is
therefore the tracked evidence that the other three were met.

Age may trigger a disposition review. It never triggers a deletion.

### Tombstone scope

One Tombstone records one retired package or one retired standalone document,
never one per member. It carries the retired path, the replacement or `none`,
the reason, and the recovery commit. Git stores the content; the Tombstone is
the tracked pointer that keeps the content findable.

A Tombstone lives under `docs/98.archive/tombstones/<stage>/`, mirroring the
namespace of the document it retires. Every stage that can retire a document has
one. A missing namespace is a namespace to create, never a reason to remove a
document without its Tombstone.

### Implementation coverage

Every capability implemented in this workspace has one Stage 01 Requirement
owner for its obligation and one Stage 02 Description or ADR owner for its
structure and durable decision. Retiring a Stage 03 package never removes that
coverage: the package's implemented outcome moves to those owners before the
package is retired.

## Related Documents

- [Stage authoring matrix](stage-authoring-matrix.md)
- [Stage 99 registry](../../99.templates/registry.json)
- [SDLC](../sdlc.md)
- [Task checklists](task-checklists.md)
