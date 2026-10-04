---
title: "Documentation Protocol"
version: "3.2.1"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
---

# Documentation Protocol

## Authority

The Stage 99 registry is the only machine authority for paths, profiles,
required sections, lifecycle values, and identifier relations. agent governance owns
authoring behavior and `scripts/` owns executable validation.

## Document Boundaries

- Stage 01 owns long-lived solution-independent requirements.
- Stage 02 owns current architecture descriptions and durable decisions.
- Stage 03 owns a change behavior contract, technical approach, plan, Tasks,
  and executable interface contracts.
- Stage 05 owns operator guidance, policies, runbooks, and incidents.
- Stage 90 owns non-normative research, audits, and reference data.
- Stage 98 owns four capture classes for frozen units and two route
  dispositions that hold no body; current assessment and availability are separate.
- Stage 99 owns profiles, schemas, and copyable templates.

Do not create parallel PRD, SRS, interface-requirement, design, tests, release,
progress, or handoff authorities when the canonical package already owns the
content. Root `DESIGN.md` remains UI and design-system authority only.

### Entry point for documents outside `docs/`

Outside `docs/`, README navigation and directory-purpose routes are allowed.
Do not link to individual numbered-stage documents or depend on them for current
agent instructions. State the current rule in its canonical governance or fact
owner and route readers through an appropriate README. An artifact ID, plain
path, or former approval is not a substitute for that current rule.

`leaf.docs-traceability` enforces deterministic link findings through the
`entrypoint` mode of `check-document-links.py`, reading tracked Markdown plus
`llms.txt`. It normalizes relative and absolute paths, this repository's GitHub
blob/raw URLs, percent encoding, case, separators and anchors, including
reference Markdown, HTML, wiki and fenced clickable forms. It does not infer
semantic authority from prose. Review current authority dependence separately:
literal output-path examples, negative test controls and dated historical
provenance may remain when they do not direct current behavior. A code fence
alone does not exempt a clickable stage-document route.

Machine access is narrowly scoped: document-governance validators consume the
Stage 99 registry and schemas to validate profiles and lifecycle; approved
stage authoring reads the selected registered template to create that document;
the Compose validator reads its named profile-vocabulary machine section to
validate selections; `scripts/hardening/check-all-hardening.sh` reads the exact
security Requirement input to assert its architecture trace link. These are
validation data reads, not imports of agent instructions.
These exceptions identify kind, consumer, necessity and
scope; they grant no stage-wide link exemption or policy authority. Any new
machine input must establish the same four facts at its owning consumer.

Reading governing Requirements, Architecture, the approved Spec and current
Task during authorized execution remains required by bootstrap. Such scoped
reads, investigation, and docs-internal traceability are not outside-docs
instruction dependencies. Links inside `docs/` keep their existing rules;
[Links into Stage 98](#links-into-stage-98) governs archive citations.

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
   because its shape belongs to the runtime that reads it. A canonical native
   skill uses top-level `name` and `description` plus `metadata` containing its
   common and governance fields. Its skill-local invocation control permits only
   explicit invocation. Stage 99 defines both shapes; native discovery does not
   change policy ownership or role permissions.
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
    A single Task status belongs in frontmatter. A multi-item receipt keeps its
    existing acceptance-criterion/work-unit identity and uses the Registry's
    optional Status column; it does not create a second progress ledger. Record
    an optional lifecycle event only for an observed direct registered edge and
    same-Task evidence. Structural records do not authenticate approval.
15. Validate metadata, links, and stage-specific contracts before completion.
16. Keep a fenced command block runnable: every repository path it names must be
    a path a reader can open. Where a block's paths illustrate a rule or a shape
    rather than naming a file — an anti-pattern example, a `git check-ignore`
    probe, a deliberately absent search pattern — say so inside the block with
    `# doc-paths: illustrative`, so the exemption is visible to the reader
    instead of hidden in a predicate. `leaf.docs-traceability` enforces this
    through the `commands` mode of `check-document-links.py`. Operator-created
    files under `secrets/` and preserved bodies under `docs/98.archive/` are
    outside the check: the first are untracked by design and the second are
    supposed to name what the tree has since dropped.

### Document language

The Registry `language` field of a document's profile decides the language of
its prose. The profiles follow one priority order:

1. Every tracked `README.md` is Korean, whatever its path or profile. This
   includes the READMEs under `.agents/`, the provider directories, Stage 90
   packages, Stage 99, and the Stage 98 index. The generated provider READMEs
   are written in Korean through their renderer template, although they
   declare no `language` and are not judged. A frozen Stage 98 body keeps the
   language it was written in.
2. Every other document under `docs/05.operations/` is Korean.
3. Every other document under `docs/` that declares a language is English.

Canonical governance sources under `.agents/`, the authored native provider
documents, and the Stage 99 registry, schema, and template sources stay
English, except for their `README.md` files. A template source is English, but
its author prompt names the language of the document it produces, which is the
language of the target profile. Stage 98 records, template sources, and
generated runtime adapters declare no language and are not judged.

Structure tokens keep their original form in every language: required headings,
identifiers, paths, command text, metadata keys, environment variables, profile
and status values, tool names, and code samples. Korean first does not mean
Hangul only. Byte-preserved historical text, quotations, and external originals
are not translated.

The check judges the ratio of Hangul to Latin letters after it removes
frontmatter, fenced blocks, HTML comments, headings, inline code, link targets,
URLs, and path or `ID-####` tokens. A structure token it cannot recognize, such
as an unquoted metadata key, still counts as Latin letters; that is one of the
heuristic's limits. The thresholds live in
`scripts/lib/document_governance/language.py`. This is a script heuristic: it
cannot judge meaning, and a text too short to measure is not judged. Correct a
false result by recalibrating the thresholds with evidence, never with a
per-path exception. The `language` mode of `check-document-links.py` judges
every document whose profile declares a language, and the metadata body
contract applies the same judgment to each changed document. Conversational responses are not artifacts and
follow [output style](output-style.md).

### README navigation

A README whose directory holds at least one subdirectory and no direct files,
apart from itself and placeholders such as `.gitkeep`, is a folder router. Within its own directory,
a folder router links only a direct child directory or that child's
`README.md`. It does not list documents inside a child, in a table, list, HTML,
collapsed block, generated block, or a fenced tree that names files. A README
whose directory holds direct files is a collection README: it indexes those
files, and a deeper link it carries is a citation that this rule does not limit.
In any README, a link whose label ends in `/` resolves to that folder or to its
`README.md`. A link outside the README's own directory is a citation, and the
citation rules in this protocol apply to it. The `navigation` mode of
`check-document-links.py` enforces this rule.

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
  redefine agent governance rules governing agents.
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
| [Spec Kit](https://github.com/github/spec-kit) | partial | Stage 03 clarify, Spec, Plan, Tasks, analyze, implement, verify flow in [SDLC](sdlc.md); retain individual Task records |
| [Diataxis](https://diataxis.fr/) | partial | Guide reader purpose; do not create parallel stage categories |
| [C4](https://c4model.com/) | partial | Description diagram choice and communication checks; code-level diagrams are not a default requirement |
| [ADR](https://adr.github.io/) | adopted | one significant decision, alternatives, consequences, and explicit supersession |
| [arc42](https://arc42.org/) | partial | proportionate context, structure, flow, deployment, quality, and risk views in registered Description sections |
| [Google SRE incident management](https://sre.google/resources/practices-and-processes/incident-management-guide/) | partial | factual Incident coordination and blameless Postmortem follow-through; no implied live-response authority |

### Gap-to-Stage Routing

| Gap Type | Owner | Rule |
| --- | --- | --- |
| Governance behavior | `.agents/` | Change canonical policy, role, skill, or provider facts first. |
| Reusable routing knowledge | `.agents/knowledge/` | Record verified surface-to-owner routing with its provenance and refresh trigger. |
| Reusable prompt contract | `.agents/prompts/` | Record required inputs, output contract, prohibitions, and failure handling. |
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

### Stage 98 dispositions

Stage 98 retains what the active stages no longer carry, in six dispositions.
Each disposition owns a directory that is created by the change that first uses
it, so a disposition with no record yet has no directory. The families are two
kinds, and the kind decides what a directory holds and whether a current
document may cite it.

A **retention class** records why a whole document or package left its current
stage, under the profile that governed it then. A governed document that is no
longer current leaves Stages 01, 02, 03, 05, 90, and 99 and is captured in the
class that matches what happened to it. Availability is a separate judgment:
`retained` keeps the immutable whole body in the current tree; approved
`git-history-only` keeps its catalog provenance and recoverable Git source
without a current payload or compatibility copy. Disposition requires its own
authorization.

| Class | Captured scope | Must name | Citable from an active stage |
| --- | --- | --- | --- |
| `completed/` | Work that finished and landed | What it promoted | yes |
| `superseded/` | Content a newer current authority replaced | The document that replaced it | no; cite its successor |
| `retired/` | A rule or scope withdrawn with no successor | Why it was withdrawn | no |
| `resolved/` | A closed Incident bundle and published Postmortem | Closure evidence and the current corrective-work owner | yes, as historical evidence |

A **route disposition** holds no body. It names a route for a consumer outside
this repository, so a current document cites the current route and never the
record that names it.

| Family | Holds | Must name | Citable from an active stage |
| --- | --- | --- | --- |
| `tombstones/` | Nothing | The retired route, its successor or absence, and the reason | no |
| `migrations/` | Nothing | The moved scope and its current owner, as `MIG-####` | no |

Citability is the repository's explicit use policy, enforced by the Registry's
ordered rules; a directory name alone does not establish authority. Captured
completion or incident resolution remains historical evidence. Current rules
cite their current owner.

What no Stage 98 record carries, in any family, is a second recovery ledger: no
redirect, path ledger, self-designed body digest, branch SHA, or recovery
commit. The catalog's Retention Envelope names the source Git object once;
normal Git history remains the recovery mechanism for frozen content. Existing
Task Commit Ledgers are original execution evidence and remain unchanged; they
are not duplicate Archive recovery ledgers.

#### Links into Stage 98

Links between documents inside `docs/` keep their existing contracts. Resolve
path, profile, and preservation unit first; then apply current assessment and
availability restrictions, route-record restrictions, source-profile and capture
class permissions, current-owner or historical-context checks, and link integrity,
in that order. `withdrawn`, `invalidated`, and `git-history-only` units cannot be
ordinary direct payload targets, even from an Incident or Postmortem. Cite the
current assessment, erratum, or Archive index instead. `superseded` assessment
routes current authority to its successor.

The Archive index and catalog provide historical discovery. Current documents
may cite retained `completed/` and `resolved/` bodies as historical evidence;
`operation/incident` and `operation/postmortem` may also cite other retained
classes as evidence subject to the earlier restrictions. `tombstones/` and
`migrations/` remain closed to every ordinary source profile because they hold
routes, not bodies. Frozen-body links are interpreted at the captured source
commit and original path, never repaired against today's tree. Current catalog
and assessment links still use current link checks. A historical broken target
is an observation or erratum, not permission to rewrite its source.

#### Current assessment and Git-history-only availability

The existing Retention Catalog owns optional current assessment rows, at most
one per unit. The capture envelope remains immutable. Assessment values are
`unreviewed`, `usable`, `superseded`, `withdrawn`, and `invalidated`; availability
is independently `retained` or `git-history-only`. No row means
`unreviewed` and `retained`, never implicit approval or usability. Do not seed
empty rows. A real reassessment records its decision, reason, actual date,
retention hold, and conditional current owner; `superseded` requires a real
successor. Previous judgments remain in Git history. Do not delete an assessment
to regain the default, or restore `invalidated` to `usable` without evidence.

Removing a retained unit requires a separately current unit/action/date-scoped
authorization from the trusted operator route, reassessment, no hold, completed
current-consumer cutover, reachable source history with recoverable objects, and
complete unit absence. The pinned Task revision is an immutable structural record
of the original completed disposition and its scope; it is not a trusted approval
source. An existing ID, a proposed ADR, an approver name, an archive
authorization record, or a validator result alone proves no current
authorization. A later lifecycle change does not rewrite or invalidate the
historical record valid at its original revision, but missing, mismatched, or
revoked current authorization blocks a pending or new removal. Automatic
authentication and revocation enforcement are unsupported unless separately
observed through a native provider capability. Partial deletion, renaming,
rewriting, and deletion of the capture row are rejected. Keep the catalog and
capture envelope and route discovery to them, not a missing payload. Restoration
is a separately explained recovery into a current owner, not silent resurrection
of frozen authority.

`git-history-only` means that the current tree supplies no payload; it makes no
claim about purging Git history, clones, forks, or caches. `purged` is not a
registered availability value. Secret exposure follows separately authorized
credential revocation and security response, not ordinary archival deletion.
Tests of removal use isolated Git fixtures and grant no permission to remove
real records. A sealed Tombstone or Migration keeps its original form.

### Retention by status

The Registry owns each profile's entry state, transition edges, and terminal
states. Apply that lifecycle before disposition; do not infer permission from
age or a folder count. Completed packages and superseded documents move to their
registered frozen archive routes, and withdrawn ones move to `retired/`. Do not
record completion or supersession as a withdrawal.

Before package completion, apply the [completion checklist](task-checklists.md#before-completion).
Record final evidence while the package is still editable. All-files checks
retain their explicit approval and controlled-wrapper requirements. A completed
Spec may wait in Stage 03 when its Plan is completed and every Task is completed
or validly cancelled. Its completion receipt must cover every numbered Spec
criterion and Plan work unit before disposition. Waiting is neither active work
nor disposition approval; the Stage 03 index routes to the package without a
second status ledger. A later authorized move preserves the prepared source
object, including the original Task evidence.

Stage 03 occupancy is a package judgment using the Registry's Spec, Plan, and
Task terminal sets. In an unfinished package, completed Tasks and validly
cancelled Tasks may remain; a terminal Plan may not. A cancelled Task records
nonempty `reason` and `approved_by`, a valid `approved_at` date, and `criteria`.
Each criterion names a Spec acceptance number and exactly one of another
non-cancelled Task in the package (`reassigned_to`) or a nonempty withdrawal
reason (`withdrawn`). An empty list means no assigned criterion. Withdrawal
never exempts a criterion still present in the Spec from PASS evidence.
A cancelled or superseded Spec keeps no package members in active Stage 03.
Standalone documents keep their per-document disposition rule. No rule here
renames lifecycle statuses or applies a union of terminal sets to other stages.
Stage 03 may be empty when no package remains, including no waiting package.

### Retirement preconditions

Retire a package or a standalone document only when all of these hold.

1. Its status is terminal: `completed`, `cancelled`, `superseded`, or `retired`.
2. Every still-current obligation, decision, structure, or procedure it owns is
   written to its canonical agent governance, 01, 02, or 05 owner.
3. Every inbound consumer is updated in the same logical change.
4. Preserve the original body in the matching Stage 98 disposition route.
   Withdrawal also records exactly one withdrawal record for the preserved unit:
   a sealed Tombstone paired with `retired/`, or a Retention Catalog row.
   Completion and supersession are never recorded as a withdrawal.

A package is never retired because it is old, because a count was exceeded, or
because nothing currently links to it. Missing inbound links are a defect to
investigate, not permission to delete.

Record the authoring obligations and consumer cutover in the current Task's
promotion receipt. A withdrawal's Retention Catalog row carries the withdrawal
reason, and a sealed Tombstone that already carries it in `Reason` keeps it.
Verification compares each unit against the single source commit/path in its
capture envelope. Captures already present at cutover
`be949f338056ee05ca139ea72403576aa18f21d8` retain their legacy comparison:
member set, Git modes, body bytes, and only the registered lifecycle-field
allowances. Older rows without provable identity remain explicit verification
limits rather than retroactive identity claims. The explicitly registered ADR-0036 bootstrap capture alone also
uses that narrow legacy metadata transition. Every other new capture preserves
the complete raw Git blob bytes, modes, and member set exactly, including
frontmatter. Prepare closure, promotion, and links at the original path before
freezing; without an authorized commit boundary, report the prepared result
rather than inventing a source commit. Never reformat legacy bodies or envelopes.

Validate the selected worktree, index, or commit explicitly. Retained-unit
history detects deletion of both a unit and its catalog row. A recorded SHA is
not reachability: missing history or objects is an unverifiable result, not
success. Raw object identity and checkout representation are separate checks;
attributes, encoding, and line-ending conversions can change the latter. Report
an unsupported checkout representation separately, execute no external filters,
and never renormalize frozen records. Resource bounds protect the checker and
never authorize deletion. Unsupported gitlinks or unavailable external large
objects remain explicit recovery limits.

Age may trigger a disposition review. It never triggers a deletion.

### Tombstone scope

One Tombstone records one retired route, never one per member. It names the
retired route, its successor or absence, and the reason, holds no body, and
carries no recovery commit. Because it records a route for an outside consumer
rather than a withdrawal, it may name the route of a record in any retention
class. A sealed Tombstone keeps the form it was written in, including its
recovery commit and its pairing with a `retired/` body, and that pairing is the
withdrawal record of the unit it pairs with.

A Tombstone lives under `docs/98.archive/tombstones/<stage>/`, mirroring the
namespace of the document it retires, and the change that writes a stage's
first Tombstone creates that namespace. A missing namespace is a namespace to
create, never a reason to remove a document without a withdrawal record.

### Divergent branch package handoff

This rule applies only to an explicitly approved integration of divergent,
committed lineages when the same source identity is already an immutable
completed archive Spec record. It does not permit ordinary removal of a
nonterminal package.

Preserve the source packet's original status and bytes unchanged, and copy the
full packet to `docs/98.archive/superseded/<original-path>`. The target current
in-progress Task carries the integration receipt in
`branch_integration_receipts`: the exact source commit, path, and identity plus
a receipt for the distinct active integration owner. That active package owns
the integration receipt and acceptance mapping. Before its atomic completion,
every still-current obligation and inbound consumer is cut over to its canonical
agent governance, 01, 02, or 05 owner.

There is exactly one carrier state. After target atomic completion and
preservation, the matching Task under
`docs/98.archive/completed/<target-package>/` is the durable carrier. Its
receipt remains unchanged across the move; the archived Task is frozen evidence,
not current policy.

This handoff creates no Tombstone or new identity, does not reopen a terminal
package, and never treats Git-only deletion or an allowlist as sufficient
evidence. Machine guards verify the full source tree against the superseded
mirror, the exact source commit/path/identity, the existing immutable completed
same-ID Spec record, and the distinct target.

### Implementation coverage

Every capability implemented in this workspace has one Stage 01 Requirement
owner for its obligation and one Stage 02 Description or ADR owner for its
structure and durable decision. Retiring a Stage 03 package never removes that
coverage: the package's implemented outcome moves to those owners before the
package is retired.

## Related Documents

- [Stage authoring matrix](stage-authoring-matrix.md)
- Stage 99 registry (`docs/99.templates/registry.json`)
- [SDLC](sdlc.md)
- [Task checklists](task-checklists.md)
- [Documentation index](../../docs/README.md)
