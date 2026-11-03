---
title: "Documentation Protocol"
version: "3.7.1"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
---

# Documentation Protocol

## Overview

Keep one document authority per role and preserve truthful provenance throughout authoring and retirement.

## Scope

Current authored documents, registered machine inputs, and retained historical units.

## Rules

### Authority

The Stage 99 registry is the only machine authority for paths, profiles,
required sections, lifecycle values, and identifier relations. agent governance owns
authoring behavior and `scripts/` owns executable validation.

### Document Boundaries

- Stage 01 owns long-lived solution-independent requirements.
- Stage 02 owns current architecture descriptions and durable decisions.
- Stage 03 owns a change behavior contract, technical approach, plan, Tasks,
  and executable interface contracts.
- Stage 05 owns operator guidance, policies, runbooks, and incidents.
- Stage 90 owns non-normative research, audits, and reference data.
- Stage 98 owns only the README describing the disposition scheme; it holds no
  records, and retired numbers live in the Registry.
- Stage 99 owns profiles, schemas, and copyable templates.

Do not create parallel PRD, SRS, interface-requirement, design, tests, release,
progress, or handoff authorities when the canonical package already owns the
content. Root `DESIGN.md` remains UI and design-system authority only.

#### Entry point for documents outside `docs/`

Inside `docs/`, a document may link to Stage 99 templates and Stage 05
operations documents for their shape or procedure; anything else it relies on
is written in the document itself rather than replaced by a link.

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
[Document Retention and Retirement](#document-retention-and-retirement) governs
retired identities.

### Authoring Rules

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
    [SDLC](sdlc.md#sequence) owns the meaning of execution state, Evidence,
    Criterion Acceptance and archive readiness; the Registry owns their shapes
    and vocabulary. Record an optional lifecycle event only for an observed
    direct registered edge and same-Task evidence. A Plan has one Spec parent
    and a Task has one Plan parent where their Registry profiles require it.
    Structural records do not authenticate approval, review, or execution.

15. Keep a fenced command block runnable: every repository path it names must be
    a path a reader can open. Where a block's paths illustrate a rule or a shape
    rather than naming a file — an anti-pattern example, a `git check-ignore`
    probe, a deliberately absent search pattern — say so inside the block with
    `# doc-paths: illustrative`, so the exemption is visible to the reader
    instead of hidden in a predicate. `leaf.docs-traceability` enforces this
    through the `commands` mode of `check-document-links.py`. Operator-created
    files under `secrets/` are outside the check because they are untracked by
    design. So is the body of a terminal Task: it is immutable execution
    evidence that may name a script a later change retired. The exemption keys
    on the Registry path profile, so only a file at a registered Task path with
    a terminal Task status qualifies; a `type: sdlc/task` frontmatter elsewhere
    does not.

#### Document language

The Registry `language` field of a document's profile decides the language of
its prose. The profiles follow one priority order:

1. Every tracked `README.md` is Korean, whatever its path or profile. This
   includes the READMEs under `.agents/`, the provider directories, Stage 90
   packages, Stage 99, and the Stage 98 index. The generated provider READMEs
   are written in Korean through their renderer template, although they
   declare no `language` and are not judged.
2. Every other document under `docs/05.operations/` is Korean.
3. Every other document under `docs/` that declares a language is English.
4. Every non-README governance, hook, role, skill, knowledge, and prompt
   document under `.agents/`, and the authored `.claude/provider.md` and
   `.codex/provider.md`, is English.

A template's author prompt names its profile's language. Native keys,
required headings, commands, code, quotations, and external originals keep
their original syntax. The current authoring language is not applied back
to template sources or generated runtime adapters.

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

#### README navigation

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

#### Role-Specific Authoring

- A Requirement Package combines PRD, SRS, and implementation-independent
  interface perspectives. A Description owns current structure; an ADR owns one
  consequential choice. Preserve accepted decisions and use explicit
  supersession when the choice changes.
- Use the Description core for architecture views: context and scope
  in `Scope`, building blocks in `Structure`, runtime interaction and topology
  in `Runtime and Deployment`, and quality scenarios and risks in
  `Quality and Risks`. Add registered optional content only when it helps the
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
  a tracking ID or link, and a verification condition, with no imposed
  completion deadline; link their execution owner instead of leaving untracked
  checkboxes. A published postmortem keeps the columns it was written with.
- Research records source-backed claims and limitations; Audit records criteria
  and dated observations; Data records schema, provenance, consumers, and
  refresh ownership. State evidence limitations and freshness triggers where
  applicable. Registered generators own generated outputs, whose freshness is
  verified without turning evidence into current policy.

#### Release Evidence Boundary

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
deployment actions wait for their exact target under
[Approval boundaries](approval-boundaries.md).

#### Reference Framework Adoption

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

#### Gap-to-Stage Routing

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
| Historical recovery | Version history and the owner's Traceability; non-authoritative for current rules | Read a removed body at the revision that last carried it; summarize still-current meaning into its current owner. |
| Shape or lifecycle | `docs/99.templates/` | Change the registry, schema, or copyable template. |
| Protected or ambiguous change | `docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` Task/audit gap first | Stop mutation and bind approval, scope, and recovery first. |

### Document Retention and Retirement

Retirement is a disposition inside the current approved Task, never a new Spec
project of its own, and a closed Spec gets no new standing verification
pipeline. Retention follows lifecycle and ownership. Age and document count are
never retention criteria. A document is retained while it owns current
behavior, structure, decision, or procedure. It is retired when its status is
terminal and its still-current meaning has moved to a canonical owner.

A retired document is summarized and deleted, not preserved. Its still-current
meaning goes to the Traceability section of the owning Stage 01 requirement or
Stage 02 description or decision, and the original file is removed. Version
history is the record of the removed body. Stage 98 (`docs/98.archive/`) holds
no records: only its README remains, describing the disposition scheme. No gate
validates Stage 98, and the README is checked like any other README.

Retired artifact numbers live in the Registry. Each top-level identity space
keeps `reserved_history`, the sorted list of numbers that no current document
carries; a reserved number is never issued again. Stage 01 numbering is dense,
so a Requirement gap is legitimate exactly when its number is reserved, and a
Stage 03 package removal is recorded exactly when its Spec number is reserved.

Current documents do not link into `docs/98.archive/` and do not name a retired
identity in `parent_ids`, `supersedes`, or `superseded_by`. A retired identity
may still appear in prose where it explains lineage.

#### Retention by status

The Registry owns each profile's entry state, transition edges, and terminal
states. Apply that lifecycle before disposition; do not infer permission from
age or a folder count. Do not record completion or supersession as a
withdrawal. Before a package becomes ready for removal, apply the
[completion checklist](task-checklists.md#before-completion) and record final
evidence while the package is still editable.

Stage 03 occupancy is a package judgment using the Registry's Spec, Plan, and
Task terminal sets. In an unfinished package, completed Tasks and validly
cancelled Tasks may remain; a terminal Plan may not. A cancelled Task records
nonempty `reason`, an actual `authorization_ref`, and `criteria_disposition`.
Each item names a Spec acceptance `criterion` and exactly one of another
non-cancelled Task in the package (`successor`) or an actual approved scope
withdrawal reference (`withdrawal_ref`). An empty list means no assigned criterion. Withdrawal
never exempts a criterion still present in the Spec from PASS evidence; only a
Criterion Acceptance `not-required` decision closes a criterion without PASS.
A cancelled or superseded Spec keeps no package members in active Stage 03.
Standalone documents keep their per-document disposition rule. No rule here
renames lifecycle statuses or applies a union of terminal sets to other stages.
Stage 03 may be empty when no package remains.

#### Retirement preconditions

Retire a package or a standalone document only when all of these hold.

1. Its profile/status pair is eligible in the Registry's
   `archive_retention.disposition_entry_statuses` map. Lifecycle terminality and
   disposition eligibility are separate: neither one grants an automatic
   removal.
2. Every still-current obligation, decision, structure, or procedure it owns is
   written to its canonical agent governance, 01, 02, or 05 owner, and its
   lineage is summarized in that owner's Traceability.
3. Every inbound consumer is updated in the same logical change.
4. Its artifact number is added to the Registry `reserved_history` of its
   identity space in the same change.

A package is never retired because it is old, because a count was exceeded, or
because nothing currently links to it. Missing inbound links are a defect to
investigate, not permission to delete. Record the summary map and consumer
cutover in the current Task. Age may trigger a disposition review. It never
triggers a deletion.

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Verification

 1. Validate metadata, links, and stage-specific contracts before completion.

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
