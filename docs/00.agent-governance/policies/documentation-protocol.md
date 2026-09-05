---
title: "Documentation Protocol"
version: "2.1.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
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
- Stage 98 owns frozen preserved bodies plus minimal migration and tombstone
  records; Git proves the preserved source and supplies recovery history.
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
   instead of issuing a new artifact identity. Its numbered filename still
   uses the Registry's separate monotonic `tombstone` allocation.
9. Declare the frontmatter its registry profile requires, in the registry's
   `common.frontmatter_order`. The registry owns which keys a profile requires
   and permits; `contracts/document-frontmatter.schema.json` owns their value shapes.
   Every authored Markdown profile begins with `title`, `version`, `type`,
   `status`, `owner`, and `updated` in that exact order. String, date,
   version, and identifier scalars are double-quoted. Profile-specific fields
   follow the common six in Registry order.
   The reasons behind that envelope are the part this policy owns. `type`
   carries the `family/kind` document role, so a reader learns a document's
   family without resolving its path. `title` never repeats the artifact
   identity, because the identity is already a field. A new document starts its
   `version` at `0.1.0`; approval of its first stable contract promotes it to
   `1.0.0`. Patch, minor, and major increments communicate compatible correction,
   compatible meaning growth, and incompatible contract change respectively.
   Lifecycle status is independent of this content version. `layer` names the
   owning stage without its numeric prefix and is omitted wherever the canonical
   path already states the authority. A profile
   without an identity declares no `artifact_id` and never invents one. A
   provider-owned runtime projection is exempt from this envelope entirely,
   because its shape belongs to the runtime that reads it.
   The existing lineage graph permits multiple predecessors in `supersedes`
   and one reciprocal successor in `superseded_by`. Preserve that singular
   successor contract; changing it to an array requires a coordinated graph and
   lineage contract change. A Registry-required root `parent_ids: []` records
   structural root identity and is not optional placeholder metadata.
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

### Role-Specific Authoring

- A Requirement Package combines PRD, SRS, and implementation-independent
  interface perspectives. A Description owns current structure; an ADR owns one
  consequential choice. Preserve accepted decisions and use explicit
  supersession when the choice changes.
- Use existing Description sections for architecture views: context and scope
  in `System Boundaries`, building blocks in `Components`, runtime interaction
  in `Data Flow`, topology in `Deployment View`, and quality scenarios in
  `Quality Attributes`. Add registered optional content only when it helps the
  reader; do not impose an empty full architecture framework.
- Consider system context and container diagrams for system-level Descriptions.
  Use component detail only when useful, dynamic diagrams for interactions, and
  deployment diagrams for environment topology. A diagram identifies its title,
  scope, audience, legend, element responsibilities, and labeled relationships.
  Keep editable diagram source; a generated image alone is not the authority.
- A Guide states its primary reader need: tutorial, how-to, technical reference,
  or explanation. Include prerequisites, intended outcome, checks, and relevant
  troubleshooting within its registered sections. Hand off repeatable operator
  procedures to an actual Runbook. Diataxis technical reference is a reader
  purpose, not the Stage 90 evidence family.
- An Operations Policy owns obligations, prohibitions, exceptions, accountable
  owners, enforcement, and review cadence. It does not own command sequences or
  redefine Stage 00 rules governing agents.
- A Runbook states its trigger, prerequisites, approval and safety boundaries,
  blast radius, ordered actions, expected signals, verification, recovery,
  escalation, and evidence handoff. Place these in its registered sections;
  do not copy a past execution result into a reusable instruction.
- An Incident records observed impact, severity, affected service, coordination,
  timeline, hypotheses, mitigation, and the next responsible action. Put
  severity and service details in the body unless the Registry declares a
  metadata field. Distinguish observation from unconfirmed cause. Use ISO 8601
  timestamps with explicit UTC offset consistently throughout the packet.
- A Postmortem follows stabilization and separates confirmed root cause,
  contributing factors, detection/response, and learning from the incident's
  factual record. Use blameless language. Corrective actions identify an owner,
  due date, tracking ID or link, and verification condition; link their execution
  owner instead of leaving untracked checkboxes.
- Research records source-backed claims and limitations; Audit records criteria
  and dated observations; Data records schema, provenance, consumers, and
  refresh ownership. State evidence limitations and freshness triggers where
  applicable. Registered generators own generated outputs, whose freshness is
  verified without turning evidence into current policy.

### Release Evidence Boundary

The repository uses `external-release-evidence`: the Release Runbook owns the
repeatable readiness procedure; the current Task owns a particular execution's
approval, checks, outcome, and recovery evidence. Link its Spec and affected
Operations documents, exact version/commit, CHANGELOG entry, and observed tag or
CI result when those exist. Record unavailable external evidence explicitly.
CHANGELOG summarizes user changes; a tag or CI result proves only its observed
event. Neither local readiness nor a Runbook proves deployment occurred.

There is no separate Release Record profile. Add one only if a distinct audit
consumer requires it, through an approved ADR and a coordinated Registry change.
Do not change an existing accepted decision silently. Remote release and
deployment actions require separate authorization.

### Reference Framework Adoption

These sources inform the rules above; they do not replace stage taxonomy or
machine contracts. Templates use concise repository-specific forms, not copies
of external templates.

| Framework | Adoption | Location and limit |
| --- | --- | --- |
| [Spec Kit](https://github.com/github/spec-kit) | partial | Stage 03 clarify, Spec, Plan, Tasks, analyze, implement, verify flow in [SDLC](../sdlc.md); retain individual Task records |
| [Diataxis](https://diataxis.fr/) | partial | Guide reader purpose; do not create parallel stage categories |
| [C4](https://c4model.com/) | partial | Description diagram choice and communication checks; code-level diagrams are not a default requirement |
| [ADR](https://adr.github.io/) | adopted | one significant decision, alternatives, consequences, and explicit supersession |
| [arc42](https://arc42.org/) | partial | proportionate context, structure, flow, deployment, quality, and risk views in registered Description sections |
| [Google SRE incident management](https://sre.google/resources/practices-and-processes/incident-management-guide/) | partial | factual Incident coordination and blameless Postmortem follow-through; no implied live-response authority |

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
| Historical recovery | `docs/98.archive/`; non-authoritative for current rules | Read prior content as a preserved record without creating a current authoring route. |
| Shape or lifecycle | `docs/99.templates/` | Change the registry, schema, or copyable template. |
| Protected or ambiguous change | `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` Task/audit gap first | Stop mutation and bind approval, scope, and recovery first. |

## Document Retention and Retirement

Retention follows lifecycle and ownership. Age and document count are never
retention criteria. A document is retained while it owns current behavior,
structure, decision, or procedure. It is retired when its status is terminal
and its still-current meaning has moved to a canonical owner.

### Retention by status

The Registry owns each profile's entry state, transition edges, and terminal
states. Apply that lifecycle before disposition; do not infer permission from
age or a folder count. Completed packages and superseded documents move to their
registered frozen archive routes. Withdrawal uses `retired/` with a Tombstone.
Do not record completion or supersession as a withdrawal.

Before package completion, apply the [completion checklist](task-checklists.md#before-completion).
An all-files run requires its explicit approval and Git-visible, non-ignored
Task-owned state, and uses only the controlled wrapper. It binds its evidence to
a Task under `docs/03.specs/`, and completion preserves
that Task under `docs/98.archive/completed/`, where it is a frozen record that
must not take new evidence.

An active stage may hold no package at all. Stage 03 is empty exactly when no
change is in flight, which is a state to reach rather than avoid. A registered
index still governs the packages preservation moved, so index membership counts
a preserved member by the path it was moved from.

### Retirement preconditions

Retire a package or a standalone document only when all of these hold.

1. Its status is terminal: `completed`, `cancelled`, `superseded`, or `retired`.
2. Every still-current obligation, decision, structure, or procedure it owns is
   written to its canonical Stage 00, 01, 02, or 05 owner.
3. Every inbound consumer is updated in the same logical change.
4. Preserve the original body in the matching Stage 98 disposition route.
   Withdrawal additionally requires one Tombstone paired with `retired/`;
   completion and supersession do not require a Tombstone.

A package is never retired because it is old, because a count was exceeded, or
because nothing currently links to it. Missing inbound links are a defect to
investigate, not permission to delete.

Record the authoring obligations and consumer cutover in the current Task's
promotion receipt. For withdrawal, the Tombstone's `Reason` also records the
disposition rationale. Verification must compare preserved bytes with their
recorded source without rewriting the frozen body to manufacture a later status.

Age may trigger a disposition review. It never triggers a deletion.

### Tombstone scope

One Tombstone records one retired package or one retired standalone document,
never one per member. It carries the retired path, the replacement or `none`,
the reason, and the recovery commit. The matching Stage 98 preserved copy stores
the frozen body; Git proves its source and provides recovery history. The
Tombstone is the tracked disposition record that keeps the content findable.

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
