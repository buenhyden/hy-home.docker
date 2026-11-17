---
title: "Documentation Protocol"
version: "7.3.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# Documentation Protocol

## Purpose and Scope

### Objective

Keep one document authority per role and preserve truthful provenance throughout authoring and retirement.

#### Authority

This policy is the canonical owner of document authority, authoring, and retirement under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Current authored documents, registered machine inputs, and retained historical units.

#### Exclusions

A provider-owned runtime projection is exempt from the metadata envelope. Operator-created files under `secrets/` and the body of a terminal Task at a registered Task path are outside the fenced-path check of `check-document-links.py`.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| DOCUMENTATION-PROTOCOL-R1 | Always | Required: treat the Stage 99 registry as the only machine authority for paths, profiles, required sections, lifecycle values and identifier relations; governance owns authoring behavior and `scripts/` owns validation | none | none |
| DOCUMENTATION-PROTOCOL-R2 | Creating or changing a document in a stage | Required: keep each stage to its owned content (01 requirements, 02 architecture, 03 change contract, 05 operations, 90 evidence, 98 README only, 99 templates) | none | none |
| DOCUMENTATION-PROTOCOL-R3 | Canonical package already owns the content | Forbidden: creating parallel PRD, SRS, interface-requirement, design, tests, release, progress or handoff authorities | none | none |
| DOCUMENTATION-PROTOCOL-R4 | Always | Required: root `DESIGN.md` remains UI and design-system authority only | none | none |
| DOCUMENTATION-PROTOCOL-R5 | Document inside `docs/` | Allowed: link to Stage 99 templates and Stage 05 operations documents for their shape or procedure | none | none |
| DOCUMENTATION-PROTOCOL-R6 | Document inside `docs/` relies on anything else | Required: write it in the document itself rather than replace it with a link | none | none |
| DOCUMENTATION-PROTOCOL-R7 | Document outside `docs/` | Allowed: README navigation and directory-purpose routes | none | none |
| DOCUMENTATION-PROTOCOL-R8 | Document outside `docs/` | Forbidden: link to individual numbered-stage documents or depend on them for current agent instructions | `leaf.docs-traceability` via the `entrypoint` mode of `check-document-links.py` for link findings; manual review for authority dependence | none |
| DOCUMENTATION-PROTOCOL-R9 | Document outside `docs/` | Required: state the current rule in its canonical governance or fact owner and route readers through an appropriate README | manual | none |
| DOCUMENTATION-PROTOCOL-R10 | Document outside `docs/` | Forbidden: using an artifact ID, plain path or former approval as a substitute for the current rule | none | none |
| DOCUMENTATION-PROTOCOL-R11 | Stage 99 data or a machine input is read | Allowed: narrow validation data reads by the listed consumers (document-governance validators, approved stage authoring, Compose validator, `compose_start.py`, security hardening check) | none | none |
| DOCUMENTATION-PROTOCOL-R12 | Adding a new machine input | Required: establish kind, consumer, necessity and scope at its owning consumer | none | none |
| DOCUMENTATION-PROTOCOL-R13 | A machine access exception applies | Forbidden: treating it as a stage-wide link exemption or policy authority | none | none |
| DOCUMENTATION-PROTOCOL-R14 | Authorized execution | Required: read governing Requirements, Architecture, the approved Spec and current Task as bootstrap requires | none | none |
| DOCUMENTATION-PROTOCOL-R15 | Any link in a governed document | Required: give each link one type (`normative`, `evidence`, `historical`, `navigation`), using no other title; the author assigns and the reviewer confirms | `check-document-links.py --mode alignment` for the title being one of four types; manual review for type choice | none |
| DOCUMENTATION-PROTOCOL-R16 | Any link in a governed document | Required: point each link forward from the document that writes it | none | none |
| DOCUMENTATION-PROTOCOL-R17 | Any link in a governed document | Forbidden: asking the link target to write a link back | none | none |
| DOCUMENTATION-PROTOCOL-R18 | A required link | Required: resolve | `check-document-links.py` (link resolves) | none |
| DOCUMENTATION-PROTOCOL-R19 | Evidence link whose target may later be deleted | Required: use a commit-pinned `https://` URL whose path holds a 40-character commit, or a commit and path in plain text | `check-document-links.py --mode alignment` for a titled `evidence` link being commit-pinned | none |
| DOCUMENTATION-PROTOCOL-R20 | Before a document is deleted or moved | Required: sort inbound consumers by link type and handle each per the table; the reviewer confirms the sorting | manual | none |
| DOCUMENTATION-PROTOCOL-R21 | Governed document | Required: use relative Markdown links | none | none |
| DOCUMENTATION-PROTOCOL-R22 | Recording a document relation | Required: write the relation only on the side the Writer column names | Writer checks: `check-document-links.py` for links, `check-document-metadata.py` for `parent_ids` and `supersedes`, `check-document-corpus-lifecycle.py` for Evidence rows; manual review for prose writers and Promotion | none |
| DOCUMENTATION-PROTOCOL-R23 | Recording a document relation | Forbidden: keeping a manual reverse-state table | none | none |
| DOCUMENTATION-PROTOCOL-R24 | Frontmatter `owner` | Required: name an accountable person, not a related document | none | none |
| DOCUMENTATION-PROTOCOL-R25 | Retained reverse field | Required: keep `superseded_by` as the single reciprocal successor of `supersedes` | none | none |
| DOCUMENTATION-PROTOCOL-R26 | Registry `common` section | Required: bind `link_types`, `link_profiles` and `document_relations`, each relation `owner` naming its check or owning policy | Registry validator rejects a missing contract, undeclared writer key, link type or relation, nonexistent owner path and invalid retained reverse field | none |
| DOCUMENTATION-PROTOCOL-R27 | Creating or moving a document | Required: select the registry profile first | none | none |
| DOCUMENTATION-PROTOCOL-R28 | Profile requires an identity | Required: use four-digit numbered slugs | none | none |
| DOCUMENTATION-PROTOCOL-R29 | Always | Required: keep dates in frontmatter, with the incident year directory the only path exception | none | none |
| DOCUMENTATION-PROTOCOL-R30 | Storing incident packets | Required: store only at `docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md` and `postmortem.md` | none | none |
| DOCUMENTATION-PROTOCOL-R31 | Linking an artifact ID | Required: link canonical IDs in full | none | none |
| DOCUMENTATION-PROTOCOL-R32 | Issuing an artifact ID | Forbidden: reusing an issued ID | none | none |
| DOCUMENTATION-PROTOCOL-R33 | Member document | Required: give it its container identity plus the container's own internal sequence, in the registry `artifact_id_pattern` shape | none | none |
| DOCUMENTATION-PROTOCOL-R34 | Naming a member | Required: name a Stage 90 member `m####-<slug>.md`, keep Task `tsk-####-<slug>.md` and incident `inc-####-<slug>/` | none | none |
| DOCUMENTATION-PROTOCOL-R35 | A document is retired | Required: record its number in its identity space Registry `reserved_history` | none | none |
| DOCUMENTATION-PROTOCOL-R36 | Authored Markdown profile | Required: declare the profile frontmatter in `common.frontmatter_order`, starting `title`, `version`, `type`, `status`, `owner`, `updated`, scalars double-quoted, profile fields after; `title` never repeats the artifact identity; no `artifact_id` for a profile without identity; `layer` omitted where the path states authority | none | none |
| DOCUMENTATION-PROTOCOL-R37 | New document | Required: start `version` at `0.1.0` | none | none |
| DOCUMENTATION-PROTOCOL-R38 | Changed document | Required: give `version` higher numeric precedence than the same path at the merge base | `check-document-metadata.py --mode check-changed` reports `version-unchanged` and `version-downgrade`; increment choice by review | none |
| DOCUMENTATION-PROTOCOL-R39 | Edit confined to `status`, `updated`, `reviewed_at`, `next_review_at` | Allowed: no new version | none | none |
| DOCUMENTATION-PROTOCOL-R40 | Artifact number, baseline or reset, Task completion or PR merge | Forbidden: treating it as a version event that sets or resets a `version` | none | none |
| DOCUMENTATION-PROTOCOL-R41 | Provider-owned runtime projection | Allowed: exemption from the frontmatter envelope | none | none |
| DOCUMENTATION-PROTOCOL-R42 | Canonical native skill | Required: use top-level `name` and `description` plus `metadata` with common and governance fields, with explicit-invocation-only control | none | none |
| DOCUMENTATION-PROTOCOL-R43 | Stage 01 to 03 profile | Forbidden: carrying `supersedes` or `superseded_by` | none | none |
| DOCUMENTATION-PROTOCOL-R44 | Stage 01 to 03 successor | Required: record the replaced substance in its Traceability and delete the predecessor with its number reserved | none | none |
| DOCUMENTATION-PROTOCOL-R45 | Other profiles | Required: keep multiple predecessors in `supersedes` and one reciprocal successor in `superseded_by` | none | none |
| DOCUMENTATION-PROTOCOL-R46 | Registry-required root | Required: record `parent_ids: []` as root identity | none | none |
| DOCUMENTATION-PROTOCOL-R47 | Titling a Stage 03 Spec | Required: title it `<Subject> Specification` without class words such as `Technical` or `Capability` | none | none |
| DOCUMENTATION-PROTOCOL-R48 | Stage 03 package | Required: keep it to a bounded change; a steady-state description belongs to Stage 02 and Stage 05 and is retired to them | none | none |
| DOCUMENTATION-PROTOCOL-R49 | Stage 01 requirement | Required: keep it solution-independent; implementation contracts belong to the Stage 03 Spec or Stage 05 policy | none | none |
| DOCUMENTATION-PROTOCOL-R50 | Always | Required: update cross-links in the same logical change | none | none |
| DOCUMENTATION-PROTOCOL-R51 | Recording execution evidence | Required: record it in the co-located Stage 03 Task; a Plan has one Spec parent and a Task one Plan parent where profiles require | none | none |
| DOCUMENTATION-PROTOCOL-R52 | Optional lifecycle event | Allowed: record it only for an observed direct registered edge with same-Task evidence | none | none |
| DOCUMENTATION-PROTOCOL-R53 | Fenced command block | Required: name only repository paths a reader can open | `leaf.docs-traceability` through the `commands` mode of `check-document-links.py` | none |
| DOCUMENTATION-PROTOCOL-R54 | Block paths illustrate a rule or shape | Allowed: mark the block `# doc-paths: illustrative` | none | none |
| DOCUMENTATION-PROTOCOL-R55 | Operator-created `secrets/` files or terminal Task body at a registered Task path | Allowed: exempt from the fenced command path check | none | none |
| DOCUMENTATION-PROTOCOL-R56 | Authoring prose in a document | Required: write prose in the language of the Registry profile (README Korean; folder `AGENTS.md` English; other `docs/05.operations/` Korean; other `docs/` English; non-README `.agents/` and provider documents English) | `language` mode of `check-document-links.py`; metadata body contract for changed documents | none |
| DOCUMENTATION-PROTOCOL-R57 | Any language | Required: keep structure tokens (headings, identifiers, paths, commands, metadata keys, environment variables, profile and status values, tool names, code) in original form | none | none |
| DOCUMENTATION-PROTOCOL-R58 | Byte-preserved historical text, quotations, external originals | Allowed: remain untranslated | none | none |
| DOCUMENTATION-PROTOCOL-R59 | False language-check result | Required: recalibrate thresholds with evidence | none | none |
| DOCUMENTATION-PROTOCOL-R60 | False language-check result | Forbidden: a per-path exception | none | none |
| DOCUMENTATION-PROTOCOL-R61 | Conversational responses | Required: follow output style | none | none |
| DOCUMENTATION-PROTOCOL-R62 | README directory with a subdirectory and no direct files | Required: a folder router links only a direct child directory or its `README.md` | `navigation` mode of `check-document-links.py` | none |
| DOCUMENTATION-PROTOCOL-R63 | Folder router | Forbidden: listing documents inside a child in any form | `navigation` mode of `check-document-links.py` | none |
| DOCUMENTATION-PROTOCOL-R64 | README directory with direct files | Required: a collection README indexes its direct files | `navigation` mode of `check-document-links.py` | none |
| DOCUMENTATION-PROTOCOL-R65 | A link outside the README directory | Allowed: treat it as a citation under the citation rules | none | none |
| DOCUMENTATION-PROTOCOL-R66 | Folder with README or `AGENTS.md` | Required: write README for people and `AGENTS.md` for agents without repeating each other | none | none |
| DOCUMENTATION-PROTOCOL-R67 | Deciding a folder guide | Required: carry `README.md` and `AGENTS.md` together only where folder-specific agent rules exist; other folders carry `README.md` only | none | none |
| DOCUMENTATION-PROTOCOL-R68 | Adding a folder guide | Required: add its path to Registry `folder-agent-guide` `path_pattern` or `additional_paths`, the only list | A test keeps tracked guides equal to that list | none |
| DOCUMENTATION-PROTOCOL-R69 | Root `AGENTS.md` and `CLAUDE.md` | Required: stay the entry shims, not folder guides | none | none |
| DOCUMENTATION-PROTOCOL-R70 | Folder whose only agent rule is not handling a secret value | Required: keep `README.md` only | none | none |
| DOCUMENTATION-PROTOCOL-R71 | Folder `AGENTS.md` | Required: follow the `common/agent-guide` template (Scope, Required Policies, Workflow, Verification and Safety); Required Checks name only registered commands | none | none |
| DOCUMENTATION-PROTOCOL-R72 | Folder `AGENTS.md` | Forbidden: copying a policy body; the owner wins when summary and owner disagree | none | none |
| DOCUMENTATION-PROTOCOL-R73 | Folder carries `AGENTS.md` | Required: carry a generated `CLAUDE.md` shim holding only the renderer marker, a heading and `@AGENTS.md` | `provider_surface_renderer.py` writes, checks and retires each shim | none |
| DOCUMENTATION-PROTOCOL-R74 | Generated `CLAUDE.md` shim | Forbidden: editing it by hand | none | none |
| DOCUMENTATION-PROTOCOL-R75 | README | Forbidden: an `AI Agent Guidance` section or other agent-directed instructions; point to the folder `AGENTS.md` | none | none |
| DOCUMENTATION-PROTOCOL-R76 | Historical quotation in current Markdown | Required: use the contiguous `> Historical evidence (not current authority; source: Git history):` blockquote, or the evidence table marker for machine-consumed tables; keep source context and current obligations outside the quote | none | none |
| DOCUMENTATION-PROTOCOL-R77 | Role moves to the common form | Required: use `COMMON-DOC-FORM-1` H2 and H3 sections, moving all of the role's documents in one change | Registry-declared `required_sections` order checked by the validator | none |
| DOCUMENTATION-PROTOCOL-R78 | Role has moved | Forbidden: old form, or a section body that is only TODO, TBD, N/A or `-`; an inapplicable section says why | none | none |
| DOCUMENTATION-PROTOCOL-R79 | Product difference from the common form | Required: record it as an Exception under quality standards with condition, scope, reason, end or review condition and verification | manual | none |
| DOCUMENTATION-PROTOCOL-R80 | Requirement Package | Required: write an interface need as a functional requirement and a quality need | none | none |
| DOCUMENTATION-PROTOCOL-R81 | Requirement Package | Forbidden: a separate interface section or `IF` child identity | none | none |
| DOCUMENTATION-PROTOCOL-R82 | Preserving decisions | Required: preserve accepted decisions and use explicit supersession when the choice changes | none | none |
| DOCUMENTATION-PROTOCOL-R83 | Architecture views | Required: use the Description core mapping (`Scope`, `Structure`, `Runtime and Deployment`, `Quality and Risks`) | none | none |
| DOCUMENTATION-PROTOCOL-R84 | Architecture views | Allowed: add registered optional content only when it helps the reader | none | none |
| DOCUMENTATION-PROTOCOL-R85 | Architecture views | Forbidden: imposing an empty full architecture framework | none | none |
| DOCUMENTATION-PROTOCOL-R86 | System-level Description | Allowed: consider system context, container, component, dynamic and deployment diagrams as useful | none | none |
| DOCUMENTATION-PROTOCOL-R87 | A diagram | Required: identify title, scope, audience, legend, element responsibilities and labeled relationships, and keep editable source | none | none |
| DOCUMENTATION-PROTOCOL-R88 | Guide | Required: state its primary reader need and include prerequisites, outcome, checks and troubleshooting; hand repeatable procedures to a Runbook | none | none |
| DOCUMENTATION-PROTOCOL-R89 | Operations Policy | Required: own obligations, prohibitions, exceptions, accountable owners, enforcement and review cadence | none | none |
| DOCUMENTATION-PROTOCOL-R90 | Operations Policy | Forbidden: owning command sequences or redefining agent governance rules | none | none |
| DOCUMENTATION-PROTOCOL-R91 | Runbook | Required: state trigger, prerequisites, approval and safety boundaries, blast radius, ordered actions, expected signals, verification, recovery, escalation and evidence handoff | none | none |
| DOCUMENTATION-PROTOCOL-R92 | Runbook | Forbidden: copying a past execution result into a reusable instruction | none | none |
| DOCUMENTATION-PROTOCOL-R93 | Guide, Operations Policy or Runbook changes | Required: update the document in the same change and carry `next_review_at` at most 180 days after `updated` | Missing or over-interval `next_review_at` rejected; stale until `reviewed_at` on or after a passed date | none |
| DOCUMENTATION-PROTOCOL-R94 | README or Architecture Description | Forbidden: carrying a review date | none | none |
| DOCUMENTATION-PROTOCOL-R95 | Incident | Required: record impact, severity, affected service, coordination, timeline, hypotheses, mitigation and next action; distinguish observation from unconfirmed cause; use ISO 8601 timestamps with UTC offset | none | none |
| DOCUMENTATION-PROTOCOL-R96 | Postmortem | Required: separate confirmed causes, enabling conditions, uncertainty, detection/response and learning from facts, in blameless language | none | none |
| DOCUMENTATION-PROTOCOL-R97 | Postmortem corrective action | Required: name an owner, completion condition and evidence with tracking ID or link and check, linking the execution owner | none | none |
| DOCUMENTATION-PROTOCOL-R98 | Postmortem corrective action | Forbidden: an imposed completion deadline or untracked checkboxes | none | none |
| DOCUMENTATION-PROTOCOL-R99 | Research, Audit, Data | Required: record source-backed claims and limitations, criteria and dated observations, schema, provenance, consumers and refresh ownership, with evidence limitations and freshness triggers | none | none |
| DOCUMENTATION-PROTOCOL-R100 | Versioned object | Required: author each version once and use one SemVer parser and comparator (`scripts/lib/document_governance/semver.py`) | none | none |
| DOCUMENTATION-PROTOCOL-R101 | Document or contract version | Required: exactly `MAJOR.MINOR.PATCH` with no prerelease or build metadata | none | none |
| DOCUMENTATION-PROTOCOL-R102 | Changed versioned object | Required: higher precedence than its base; equal is `version-unchanged`, lower `version-downgrade`, missing `version-missing` | `check-document-metadata.py --mode check-changed` | none |
| DOCUMENTATION-PROTOCOL-R103 | Release publication | Required: apply the version rule against the highest published release or tag; refuse equal precedence to a published release, tag or CHANGELOG entry | `scripts/operations/release.py` | none |
| DOCUMENTATION-PROTOCOL-R104 | Release publication | Forbidden: a backport (a version below the highest published release or tag) | `scripts/operations/release.py` | none |
| DOCUMENTATION-PROTOCOL-R105 | Product version row | Required: a changed `version` is a valid SemVer value not lower than the merge base | `check-document-metadata.py --mode check-changed` (`version-malformed`, `version-downgrade`) | none |
| DOCUMENTATION-PROTOCOL-R106 | Other version rows | Required: review a changed value against the Compatibility surface | manual | none |
| DOCUMENTATION-PROTOCOL-R107 | Product version | Required: rise only with its own product's change; a documentation change raises no other object's version | none | none |
| DOCUMENTATION-PROTOCOL-R108 | Versioned document or contract change | Required: review against prior valid producers and consumers (keys, sections, columns, relations, states, meaning, diagnostics, output shape) | manual | none |
| DOCUMENTATION-PROTOCOL-R109 | Choosing an increment | Required: MAJOR when a prior producer or consumer breaks, MINOR for a compatible addition, PATCH for a consumer-preserving correction, same for `0.x` | none | none |
| DOCUMENTATION-PROTOCOL-R110 | Proposed revision | Required: apply the increment rules before submitting for approval; an approval limited to lifecycle metadata keeps the version | none | none |
| DOCUMENTATION-PROTOCOL-R111 | Versioned change | Required: record the affected consumer and compatibility evidence in the current Task | none | none |
| DOCUMENTATION-PROTOCOL-R112 | Release readiness or deployment evidence | Required: keep release facts with the Release Runbook, current Task, CHANGELOG, tag and CI result; link version, commit, CHANGELOG entry and observed tag or CI result when they exist | none | none |
| DOCUMENTATION-PROTOCOL-R113 | External release evidence unavailable | Required: record it explicitly | none | none |
| DOCUMENTATION-PROTOCOL-R114 | Local readiness or a Runbook | Forbidden: treating it as proof that deployment occurred | none | none |
| DOCUMENTATION-PROTOCOL-R115 | Documentation roles | Forbidden: registering a Release Record profile, template or generator under any name | Registry validator rejects profile or template role carrying a `release` name token, section, frontmatter or purpose match; generator checked by review | none |
| DOCUMENTATION-PROTOCOL-R116 | Remote release or deployment action | Required: wait for its exact target under Approval boundaries | none | none |
| DOCUMENTATION-PROTOCOL-R117 | Adopting an external framework | Allowed: use Spec Kit, Diataxis, C4, ADR, arc42 and Google SRE as informing sources at the stated adoption level | none | none |
| DOCUMENTATION-PROTOCOL-R118 | Adopting an external framework | Forbidden: replacing stage taxonomy or machine contracts with it | none | none |
| DOCUMENTATION-PROTOCOL-R119 | A documentation gap is found | Required: route it to its owner by gap type per the Gap-to-Stage Routing table | none | none |
| DOCUMENTATION-PROTOCOL-R120 | Protected or ambiguous change | Required: stop mutation and bind approval, scope and recovery in a Task first | none | none |
| DOCUMENTATION-PROTOCOL-R121 | Historical recovery | Required: read a removed body at the revision that last carried it and summarize still-current meaning into its owner | none | none |
| DOCUMENTATION-PROTOCOL-R122 | Retiring a document | Required: treat retirement as a disposition inside the current approved Task | none | none |
| DOCUMENTATION-PROTOCOL-R123 | Retiring a document | Forbidden: creating a new Spec project for retirement or a standing verification pipeline for a closed Spec | none | none |
| DOCUMENTATION-PROTOCOL-R124 | Deciding retention | Required: retain while the document owns current behavior, structure, decision or procedure; retire when terminal or replaced with its meaning moved to an owner | none | none |
| DOCUMENTATION-PROTOCOL-R125 | Deciding retention | Forbidden: using age or document count as a retention criterion | none | none |
| DOCUMENTATION-PROTOCOL-R126 | Operational data, backups, shared agent memory | Forbidden: deleting them under this section; they keep their owners' retention | none | none |
| DOCUMENTATION-PROTOCOL-R127 | Retired document | Required: summarize its still-current meaning into its owner, delete the file, and keep Stage 98 to its README | none | none |
| DOCUMENTATION-PROTOCOL-R128 | Retired artifact number | Required: keep it in the identity space `reserved_history`, which no current document carries | Registry allocation check rejects dropping a reserved number | none |
| DOCUMENTATION-PROTOCOL-R129 | Retired artifact number | Forbidden: issuing a reserved number again | none | none |
| DOCUMENTATION-PROTOCOL-R130 | Current document | Forbidden: linking into `docs/98.archive/` or naming a retired identity in `parent_ids`, `supersedes` or `superseded_by` | none | none |
| DOCUMENTATION-PROTOCOL-R131 | Retired identity | Allowed: appear in prose to explain lineage | none | none |
| DOCUMENTATION-PROTOCOL-R132 | Applying disposition | Required: apply the Registry lifecycle first and the completion checklist before a package is ready for removal, recording final evidence while editable | none | none |
| DOCUMENTATION-PROTOCOL-R133 | Applying disposition | Forbidden: inferring permission from age or folder count, or recording completion or supersession as a withdrawal | none | none |
| DOCUMENTATION-PROTOCOL-R134 | Stage 03 package ready for removal review and approved | Required: delete it once the meaning current documents depend on sits in its owner; join its Spec number to `reserved_history` and turn current links into plain text | manual | none |
| DOCUMENTATION-PROTOCOL-R135 | Stage 03 package has a non-terminal Task | Required: keep the package with its completed Tasks | none | none |
| DOCUMENTATION-PROTOCOL-R136 | Link from a terminal Task into a package deleted later | Allowed: leave it unrepaired; link alignment excuses it under the Registry reservation conditions | none | none |
| DOCUMENTATION-PROTOCOL-R137 | Non-terminal document links a retired package | Required: turn the link into plain text naming the retired identity | none | none |
| DOCUMENTATION-PROTOCOL-R138 | Unfinished Stage 03 package | Allowed: keep completed Tasks and validly cancelled Tasks | none | none |
| DOCUMENTATION-PROTOCOL-R139 | Unfinished Stage 03 package | Forbidden: keeping a terminal Plan | none | none |
| DOCUMENTATION-PROTOCOL-R140 | Cancelled Task | Required: record `reason`, `authorization_ref` and `criteria_disposition` naming a Spec `criterion` and one of `successor` or `withdrawal_ref` | none | none |
| DOCUMENTATION-PROTOCOL-R141 | Criterion still present in the Spec | Forbidden: exempting it from PASS evidence by withdrawal; only a Criterion Acceptance `not-required` decision closes it without PASS | none | none |
| DOCUMENTATION-PROTOCOL-R142 | Cancelled Spec | Forbidden: keeping package members in active Stage 03 | none | none |
| DOCUMENTATION-PROTOCOL-R143 | Incident and Postmortem records | Forbidden: retiring them; they stay in place after closure | Registry validator rejects any status on a profile with an Incident or Postmortem lifecycle | none |
| DOCUMENTATION-PROTOCOL-R144 | Registry disposition entry | Required: list only statuses its profile lifecycle can reach | Registry validator rejects an unreachable status | none |
| DOCUMENTATION-PROTOCOL-R145 | Retiring a package or standalone document | Required: profile/status pair eligible in `archive_retention.disposition_entry_statuses`, or an ADR or Description replaced in the same change | none | none |
| DOCUMENTATION-PROTOCOL-R146 | Retiring a package or standalone document | Required: write every still-current obligation, decision, structure or procedure to its canonical owner and summarize lineage in that owner's Traceability | none | none |
| DOCUMENTATION-PROTOCOL-R147 | Retiring a package or standalone document | Required: update every inbound consumer in the same logical change | none | none |
| DOCUMENTATION-PROTOCOL-R148 | Retiring a package or standalone document | Required: add its artifact number to the identity space `reserved_history` in the same change | none | none |
| DOCUMENTATION-PROTOCOL-R149 | Retiring a package or standalone document | Required: record in a surviving Task the last commit and path carrying each removed body, reachable from `main` | manual record, stated as not a gate | none |
| DOCUMENTATION-PROTOCOL-R150 | Retiring a package or standalone document | Forbidden: retiring because it is old, a count was exceeded or nothing links to it; missing inbound links are a defect to investigate | none | none |
| DOCUMENTATION-PROTOCOL-R151 | Retiring a package or standalone document | Required: record the summary map and consumer cutover in the current Task | none | none |
| DOCUMENTATION-PROTOCOL-R152 | Disposition review | Allowed: age may trigger a review, never a deletion | none | none |
| DOCUMENTATION-PROTOCOL-R153 | Capability implemented in this workspace | Required: keep one Stage 01 Requirement owner and one Stage 02 Description or ADR owner, moving the package outcome to them before retirement | none | none |

#### Authority

The Stage 99 registry is the only machine authority for paths, profiles,
required sections, lifecycle values, and identifier relations. agent governance owns
authoring behavior and `scripts/` owns executable validation.

#### Document Boundaries

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
the Compose validator and `scripts/lib/ops/compose_start.py` read the
profile-vocabulary machine section of policy 0078 to validate selections (including `scripts/lib/document_governance/operations_catalog.py`, reached through `check-operations-catalog.py` and `scripts/operations/lab.py`); `scripts/hardening/check-all-hardening.sh` reads the exact
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

#### Link types and document relations

Every link in a governed document has one of four types, and every link points
forward from the document that writes it. A link never asks its target to
write a link back. The author assigns the type and the reviewer confirms it.
An inline link's title carries the type, such as
`[Run](https://github.com/<owner>/<repo>/blob/<commit>/<path> "evidence")`; an
untitled link is a Normative or Navigation link, so existing links keep their
meaning without a title. The title is one of `normative`, `evidence`,
`historical` or `navigation`, and no other title is used.

| Type | Required | Authority | Pinned version | When the target is removed or moved |
| --- | --- | --- | --- | --- |
| Normative | Yes | The target governs the linked meaning | Current target | Update the consumer in the same change |
| Evidence | Yes | None: it supports a claim | A revision or content hash | Keep the pinned reference |
| Historical | No | None: it explains lineage | A revision | Turn the link into plain text |
| Navigation | Yes | None: it routes a reader | Current target | Update the consumer in the same change |

A required link must resolve. An evidence link whose target may later be
deleted uses a revision-addressed form, such as a commit-pinned repository URL
or a commit and path in plain text, because a relative link to a deleted file
cannot stay resolved. A link titled `evidence` is a commit-pinned `https://`
URL, whose path holds a 40-character commit. Before a document is deleted or moved, the author sorts
its inbound consumers by link type and handles each as the last column says,
and the reviewer confirms that sorting. Vault wiki links are a separate
profile and are not typed this way. The Vault owner converts them outside this
repository, which has no wiki converter. A governed document uses relative
Markdown links.

Seven relations connect documents, one per meaning of the shared contract;
none stands in for another. Each one has a relation ID, one direction and its
writers. A writer is a frontmatter key or link type, scoped to one profile as
`profile:ref` where the same key means different things in different
profiles, or a registered H3 named `profile:H2/H3`. The last column names the
check for each kind of writer, not for the relation as a whole.

| Relation | ID | Direction | Writer | Check that validates the writer |
| --- | --- | --- | --- | --- |
| Authority | `rel.authority` | Consumer to owner | Normative links | `check-document-links.py`: the link resolves |
| Structural Ownership | `rel.structural-ownership` | Child to parent | `parent_ids` of a Plan, Task, data model contract, research or audit member, and postmortem | `check-document-metadata.py`: `parent_ids` are valid |
| Constraint | `rel.constraint` | Change to constraint | `parent_ids` of a Requirements package, Architecture description, ADR and Spec; Spec `Owning Requirements` as prose | `check-document-metadata.py` for `parent_ids`; the prose is checked by review |
| Traceability | `rel.traceability` | Record to source | Task `Results` rows and a Task's evidence links; `parent_ids` of research, audit, data, guide, runbook, operations policy, incident and generated documents | `check-document-corpus-lifecycle.py` for Evidence rows; `check-document-links.py` for links; `check-document-metadata.py` for `parent_ids` |
| Promotion | `rel.promotion` | Plan to target owner | Plan `Durable Meaning` and `Owner and Receipt` | None: the reviewer applies the [SDLC](sdlc.md#sequence) promotion rule |
| Supersession | `rel.supersession` | Successor to predecessor | Frontmatter `supersedes`; ADR `Traceability` / `Supersession` | `check-document-metadata.py` for the key; the section is checked by review |
| Change Impact | `rel.change-impact` | Owner to consumer | None: derived from Authority, Constraint and Structural Ownership | `check-document-links.py --impact` reports it; the reviewer decides which consumers change |

The frontmatter `owner` names an accountable person, not a related document,
and historical and navigation links carry no relation; their link types above
still govern them. A `Traceability` section heading in a Stage 01 to 03
document holds that document's basis and supersession records; it is a
section name, not the `rel.traceability` relation.

Only the side the Writer column names records a relation, and no document
keeps a manual reverse-state table. Reverse lookups, such as the children of a
parent or the consumers of an owner, and Change Impact are derived from those records when a document is removed or
moved: `check-document-links.py --impact <path>` reports the documents whose
`parent_ids` or `supersedes` name it, the documents with an untitled or
`normative` link to it (a folder link reaching its README), and the
transitive closure over the first and third; it fails on nothing it finds,
exits 2 when the path is not a current document and 1 on unreadable input. An untitled link may be navigation, so the
reviewer still decides which consumers the change affects. The one retained reverse
field is `superseded_by`, the single reciprocal successor of `supersedes`, as
[Authoring Rules](#authoring-rules) item 9 keeps it. Making it an array
requires a coordinated graph and lineage contract change. A Registry
`template_roles[*].consumer_paths` list is not a document relation: it is the
TemplateDefinition enumeration of the consumers found for that role, a
`test_registry` test requires each entry to be a tracked file, and whether
each still reads the role is checked by review.

The Registry `common` section binds these definitions as `link_types`,
`link_profiles` and `document_relations`, and each relation's `owner` names
the check in the last column, or the policy that owns the rule where there is
none. The schema
pins every relation ID and direction and every link-type and link-profile
value; writers, owners and retained reverse fields are checked by the
validator below, not pinned. The Registry validator also rejects a
missing contract, a writer that names an undeclared frontmatter key, link type
or relation, a profile or key a scoped writer does not have, or an unregistered
profile H3, a relation derived from itself,
an owner path that does not exist, and a retained reverse field that is not a frontmatter key. The
checkers enforce that links resolve, that metadata keys and `parent_ids` are
valid, that this Registry binding is valid, and, in
`check-document-links.py --mode alignment`, that a link title is one of the
four types and that a link titled `evidence` is commit-pinned. Whether an
untitled link is Normative or Navigation, and whether an author chose the
right type, stay a review. The link checker runs in the local profile;
its hosted CI route is not wired yet. Existing links are not retyped by this rule.

#### Authoring Rules

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
8. Record a retired document's number in its identity space's Registry
   `reserved_history`, as [Document Retention and Retirement](#document-retention-and-retirement)
   sets out.
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
   `version` at `0.1.0`. Choose the increment under
   [Version objects](#version-objects). A changed document's
   `version` has higher numeric precedence than the same path at the merge
   base: `check-document-metadata.py --mode check-changed` reports
   `version-unchanged` for equal precedence and `version-downgrade` for lower
   precedence. A new document, a document without a valid `version` on either
   side, a path Git does not show at the merge base (a rename is never
   guessed) and a path whose content is the base content are not compared. An
   edit confined to the lifecycle keys `status`, `updated`, `reviewed_at` and
   `next_review_at` is no content change, so it needs no new version. Which
   increment a change needs is left to review.
   Lifecycle status is independent of this content version. An artifact
   number, a numbering baseline or its reset, a Task completion and a pull
   request merge are not version events; none of them sets or resets a
   `version`. `layer` names the
   owning stage without its numeric prefix and is omitted wherever the canonical
   path already states the authority. A profile
   without an identity declares no `artifact_id` and never invents one. A
   provider-owned runtime projection is exempt from this envelope entirely,
   because its shape belongs to the runtime that reads it. A canonical native
   skill uses top-level `name` and `description` plus `metadata` containing its
   common and governance fields. Its skill-local invocation control permits only
   explicit invocation. Stage 99 defines both shapes; native discovery does not
   change policy ownership or role permissions.
   Stage 01 to 03 profiles carry no `supersedes` or `superseded_by`, and their
   statuses follow the [SDLC](sdlc.md#sequence): a successor records the
   replaced substance in its Traceability and the predecessor is deleted with
   its number reserved. Other profiles keep the lineage graph of
   multiple predecessors in `supersedes` and one reciprocal successor in
   `superseded_by`; changing that singular successor to an array requires a
   coordinated graph and lineage contract change. A Registry-required root `parent_ids: []` records
   root identity and is not optional placeholder metadata.
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
   packages, Stage 99, and the Stage 98 README. The generated provider READMEs
   are written in Korean through their renderer template, although they
   declare no `language` and are not judged.
2. Every folder `AGENTS.md` is English, wherever it sits, including under
   `docs/05.operations/`.
3. Every other document under `docs/05.operations/` is Korean.
4. Every other document under `docs/` that declares a language is English.
5. Every non-README governance, hook, role, skill, knowledge, and prompt
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
`check-document-links.py` enforces this rule. A folder `AGENTS.md` does not
count as a direct file, so it leaves a folder router a router.

#### README and AGENTS.md

A `README.md` is written for people: what the folder is for, what it holds,
and how to find or use it. A folder `AGENTS.md` is written for AI agents: the
working rules an agent follows when it changes a file in that folder, routed to
the canonical owners that decide them. Neither repeats the other.

A folder carries `README.md` and `AGENTS.md` together only when an agent
changing files there needs folder-specific working rules that no single
canonical owner already routes: a stage with its own templates, identities and
lifecycle, a surface with protected or generated files, or registered checks
that the folder owns. Every other folder carries `README.md` only. The Registry
`folder-agent-guide` profile's `path_pattern` and `additional_paths` are the
only list of folders that carry a guide; adding one means adding its path
there, and a test keeps the tracked guides equal to that list. Root `AGENTS.md` and
`CLAUDE.md` stay the entry shims that [bootstrap](bootstrap.md) defines and are
not folder guides. A folder whose only agent rule is "never handle a secret
value", such as `secrets/`, keeps `README.md` only, because
[approval boundaries](approval-boundaries.md) already owns that rule.

A folder `AGENTS.md` follows the Stage 99 `common/agent-guide` template, the
common AGENTS form: Scope, Required Policies, Workflow, Verification and
Safety, each with the H3 sections the Registry declares. Canonical Sources
name the `.agents/` policies, roles, skills, prompts and hook rules, and the
`.claude/` and `.codex/` adapters and hooks that apply to the folder. Required
Checks name only registered commands that exist. The guide routes and summarizes; it never copies a policy body, and
when a summary and its owner disagree, the owner wins and the guide is
corrected. Its rank and when an agent reads it are set by
[bootstrap](bootstrap.md#authority-and-precedence); it grants no tool, path,
permission or approval.
A folder that carries `AGENTS.md` also carries a generated `CLAUDE.md` whose
only content is the renderer marker, a heading and the import `@AGENTS.md`.
Claude Code
reads a folder `CLAUDE.md` but not a folder `AGENTS.md` below root `CLAUDE.md`,
so the import is how the guide reaches it.
`scripts/operations/provider_surface_renderer.py` writes, checks and retires
each shim with its guide. The shim adds no rule and is never edited by hand.
A README does not carry an
`AI Agent Guidance` section or other agent-directed instructions; it points to
its folder `AGENTS.md` instead.

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

- Each common role moves to one form, the H2 and H3 sections of
  `COMMON-DOC-FORM-1` 1.0.0; different roles are never forced into one form.
  The Registry declares each profile's sections (`required_sections`,
  `optional_sections`, `required_subsections`, `optional_subsections`), and
  the validator checks the order of required sections and subsections only.
  A role moves in one change that covers all of its current documents,
  completed and approved ones included, and keeps their existing procedures,
  commands and evidence in the matching section. From then on the old form is
  rejected for that role, as is a section body that is only TODO, TBD, N/A or
  `-`; an inapplicable section says why. A role not yet moved keeps its
  `SDLC-COMMON-r10-local-v1` H2 sections until it moves. A role has moved
  when its Registry profile declares `required_subsections`. A product difference from the form
  is an Exception under [quality standards](quality-standards.md), with its
  approved condition, scope, reason, end or review condition and verification.
- A Requirement Package combines PRD, SRS, and implementation-independent
  interface perspectives. An interface need is written as a functional
  requirement and a quality need under Quality Requirements; no separate
  interface section or `IF` child identity is issued. A Description owns current structure; an ADR owns one
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
- A Guide, Operations Policy or Runbook stays current by event: a change to
  the service, pin, command or procedure it describes updates it in the same
  change. It also carries `next_review_at`, the date its next review is due,
  at most 180 days after `updated`, the owner's decision of 2026-11-14. A
  `next_review_at` that has passed makes it stale until a `reviewed_at` on or
  after it, and a missing date or one beyond the interval is rejected. A README
  is navigation, kept current by the link and navigation checks, and carries no
  review date. An Architecture Description records authority only (`draft`,
  `in-review`, `approved`) and is kept current by event with its parent
  Requirement and Spec, so it carries no review date either.
- An Incident records observed impact, severity, affected service, coordination,
  timeline, hypotheses, mitigation, and the next responsible action. Put
  severity and service details in the body unless the Registry declares a
  metadata field. Distinguish observation from unconfirmed cause. Use ISO 8601
  timestamps with explicit UTC offset consistently throughout the packet.
- A Postmortem follows stabilization and, in the core postmortem role's
  Facts, Causes and Actions sections, separates the confirmed causes and the
  conditions that allowed them, what stays uncertain, detection/response, and
  learning from the incident's factual record. Use blameless language. Each
  corrective action in the Owners and Checks table names an owner, a completion
  condition, and evidence that carries its tracking ID or link and its check,
  with no imposed completion deadline; link their execution owner instead of
  leaving untracked checkboxes. A published postmortem keeps its recorded facts
  and rows; only the change that binds its role to the core moves them to the
  core columns.
- Research records source-backed claims and limitations; Audit records criteria
  and dated observations; Data records schema, provenance, consumers, and
  refresh ownership. State evidence limitations and freshness triggers where
  applicable. Registered generators own generated outputs, whose freshness is
  verified without turning evidence into current policy.

#### Version objects

Each version below has one authored value; every other place reads it. A
SemVer value is a SemVer 2.0.0 string: `MAJOR.MINOR.PATCH`, with no `v`
prefix and no leading zeros, optionally followed by a prerelease (`-rc.1`) and
build metadata (`+build.7`). A numeric prerelease identifier has no leading
zero. Precedence ignores build metadata and puts a prerelease below its
release, and is never compared as text or a number. A document or contract
version (the document content, new document start, common form and
vocabulary contract rows) is a numeric value: exactly `MAJOR.MINOR.PATCH`
with no prerelease or build metadata, as the shared vocabulary and decision
Q03 set; the Stage 99 schemas reject anything else. Product and release
versions keep full SemVer values. One parser and comparator
serves every consumer: `scripts/lib/document_governance/semver.py`
(`compare_semver`, `version_change_code`, `check_version_change`), imported by
`scripts/operations/release.py` and by the document `version` check, neither
of which keeps a copy. The one change rule is that a changed object's version
has higher precedence than its base: equal precedence is `version-unchanged`,
lower is `version-downgrade`, and a missing side is `version-missing`. Release
publication applies it to the highest published release or tag, refuses a
version of equal precedence to a published release, tag or CHANGELOG entry, and
allows no backport: a version below the highest published release or tag is
always refused. The document check applies it as the Document content row
states. A product version row is checked in the same `check-changed` run, by
its `version` field only: a changed value must be a valid SemVer value not
lower than the merge base (`version-malformed`, `version-downgrade`), and an
unchanged value with other edits to the file is allowed, because the product
releases on its own cadence. The other rows have no gate that compares a
changed value; their change is reviewed against the Compatibility surface.

The Canonical source column is the one authored place; the Producer writes it,
and the Compatibility surface is what its consumers depend on, so a change
there decides the increment. A product version rises only with its own
product's change; a documentation change raises no other object's version.

For a versioned document or contract, review the proposed change against the
prior valid producers and consumers. Include required keys, sections, table
columns, relations, lifecycle states, meaning, diagnostics and output shape
when they are part of the contract.

- **MAJOR** when a prior valid producer or consumer breaks. Reset MINOR and
  PATCH to zero. Moving all consumers together still requires a MAJOR increase
  if the old interface breaks.
- **MINOR** for a compatible addition. Reset PATCH to zero.
- **PATCH** for a correction that preserves the consumer contract.

The same rules apply to `0.x` versions. Apply them to the proposed
content before submitting that revision for approval. Record the owner's
approval of that revision through the document's lifecycle. An
approval limited to lifecycle metadata keeps the content version.

Record the affected consumer and the compatibility evidence in the current
Task. An accepted contract change receives its own revision. A new
observation follows the document content rule, and a lifecycle-only edit
follows the lifecycle exception.

The numeric grammar is authored in `semver.py`. The standalone Stage 99
schemas mirror it for schema consumers. The Registry regression checks
the copies against the Python grammar, including rejection of a final newline.

| Object ID | Version field | Current value | Rule | Canonical source | Producer | Consumers | Compatibility surface | Deploy unit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `document-content` | frontmatter `version` | per document | Numeric value; the rule above, checked by `check-document-metadata.py --mode check-changed` | The document's own frontmatter | The document's writer | `contracts/document-frontmatter.schema.json`, metadata validator | The keys, sections, tables, states and link directions its profile's consumers read | The document |
| `new-document-start` | Registry `common.template_initial_version` | `0.1.0` | Numeric value | `docs/99.templates/registry.json` | Stage 99 owner | Profile schema, template checks | The first version a new document carries | The Registry |
| `common-form-contract` | Registry `common.common_form_contract.contract_version` | `1.0.0` | Numeric version; `contract_id` holds `COMMON-DOC-FORM-1` separately | `docs/99.templates/registry.json` | Stage 99 owner, adopting the shared contract | `template_definition.py` | The common H1, H2 and H3 form and the empty-section rule | The shared contract, adopted per workspace |
| `role-design-contract` | Registry `common.role_design_contract.contract_version` | `4.0.0` | Numeric version; `contract_id` holds `workspace-document-role-design`, and `source_sha256` and `schema_sha256` pin the tracked core and its schema | `docs/99.templates/contracts/document-role-design.json` | Stage 99 owner, adopting the shared core on the owner's decision of 2026-11-17 | `template_definition.py`, `check-document-metadata.py --mode check-contracts` | The H2, H3, requiredness and table columns of each template role that declares `core_role` | The shared core, adopted per workspace |
| `legacy-form-contract` | Registry `common.contract_version` | `1.0.0` | Numeric version; `common.contract_id` holds the existing legacy identity | `docs/99.templates/registry.json` | Stage 99 owner | `template_definition.py` | The legacy form for roles without common subsections | The Registry |
| `template-definition-projection` | Stage 99 projection schema | `2.0.0` | Major change for the split output fields | `docs/99.templates/contracts/template-definition.schema.json` | Stage 99 owner | `template_definition.py`, body validator | The projected role definition, including the identity and version fields | Stage 99 template definitions |
| `vocabulary-contract` | Registry `common.vocabulary_contract.version` | `3.0.1` | Numeric value; the first adoption, from package label `v14.5`, is 1.0.0, by the owner's decision recorded in SPEC-0212 TSK-0064; the owner approved adopting the shared 3.0.1 on 2026-11-15 (SPEC-0212 TSK-0068), and `source_label` names the adopted source | `docs/99.templates/registry.json` | Glossary owner | Glossary `Contract Version` column, `vocabulary_contract_findings` | The common Term IDs, names, order and meanings | The shared contract, adopted per workspace |
| `registry-serialization` | Registry `schema_version` | `2` | Integer format epoch; the profile schema pins the current epoch and Git revisions use their committed schema | `docs/99.templates/registry.json` | Stage 99 owner | Profile schema, `registry.py` | The JSON structure the profile schema and `registry.py` read | The Registry |
| `product-release` | release version, tagged as `v` plus the version, and CHANGELOG | per release | SemVer, checked by `scripts/operations/release.py` against the published releases and tags; the `v` belongs to the tag, not the value; no backport | `CHANGELOG.md` dated heading, then the tag | The release workflow, through `release.py` | Release Runbook and the release workflow | The repository's published release | One tagged release |
| `product-opsflow-smtp` | `version` in `package.json` | `0.1.0` | SemVer value, checked by `check-document-metadata.py --mode check-changed`; `package-lock.json` mirrors it | `infra/07-workflow/n8n/workloads/manifest-outbox-notifier/nodes/OpsflowSmtp/package.json` | The node package's maintainer | npm, `package-lock.json` | The n8n node's parameters, credentials and outputs | The n8n community node package |
| `product-hermes-publisher` | `version` in `pyproject.toml` | `1.0.0` | SemVer value, checked by `check-document-metadata.py --mode check-changed` | `infra/07-workflow/n8n/workloads/hermes-blog-ingestion/pyproject.toml` | The workload's maintainer | The Python build backend; installation reads only `requirements.lock` | The publisher's command line and the payloads it reads and writes | The hermes-blog-ingestion workload |
| `product-storybook-nextjs` | `version` in `package.json` | `0.1.0` | SemVer value, checked by `check-document-metadata.py --mode check-changed` | `projects/storybook/nextjs/package.json` | The Storybook app's maintainer | npm, `package-lock.json` | The Storybook app's build outputs and exported design artifacts | The Storybook Next.js app |
| `product-storybook-ui` | `version` in `package.json` | `0.2.0` | SemVer value, checked by `check-document-metadata.py --mode check-changed` | `projects/storybook/nextjs/packages/ui/package.json` | The UI package's maintainer | The Storybook app's workspace dependency | The exported components, props and design tokens | The `@hy-home/storybook-ui` workspace package |

Not versions: `common.contract_id` and other contract identifiers, the
`lifecycle_generation` counter, artifact numbers and identity-space
baselines, and input-package labels such as `v14.7`. A Task completion, a
merge or a Q-07 renumbering changes none of the values above.

#### Release Evidence Boundary

The repository uses `external-release-evidence`: the Release Runbook owns the
repeatable readiness procedure; the current Task owns a particular execution's
approval, checks, outcome, and recovery evidence. Link its Spec and affected
Operations documents, exact version/commit, CHANGELOG entry, and observed tag or
CI result when those exist. Record unavailable external evidence explicitly.
CHANGELOG summarizes user changes; a tag or CI result proves only its observed
event. Neither local readiness nor a Runbook proves deployment occurred.

Release is not a document role. Do not register a Release Record profile,
template or generator under any name; release facts stay with the owners
above. The Registry validator rejects a profile whose ID, type, template ID
or path patterns, or a template role whose ID or source, has a `release` or
`releases` name token. It also rejects a profile whose section or subsection
names or frontmatter values carry that token or at least three of the retired
Release shape's groups (artifacts, rollout or rollback, approvals, outcome),
and a template role whose purpose, responsibility or applicability does, so a
role for release records is rejected under any ID, type or template. A generator is checked
by review. This
removes no GitHub Release, tag, CHANGELOG entry or release workflow. Remote release and
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

#### Document Retention and Retirement

Retirement is a disposition inside the current approved Task, never a new Spec
project of its own, and a closed Spec gets no new standing verification
pipeline. Retention follows lifecycle and ownership. Age and document count are
never retention criteria. A document is retained while it owns current
behavior, structure, decision, or procedure. It is retired when its status is
terminal, or it is replaced as the retirement preconditions allow, and its
still-current meaning has moved to a canonical owner.
These rules govern development documents only. Operational data and backups
keep the retention their Stage 05 owners set, and shared agent memory keeps
the retention rules of the
[environment constraints](environment-constraints.md); neither is deleted
under this section.

A retired document is summarized and deleted, not preserved. Its still-current
meaning goes to its canonical agent governance, Stage 01, 02 or 05 owner, as
the [retirement preconditions](#retirement-preconditions) require, and the
original file is removed. Version
history is the record of the removed body. Stage 98 (`docs/98.archive/`) holds
no records: only its README remains, describing the disposition scheme. Its
checks are listed in the
[quality standards](quality-standards.md#3-reliability-baseline).

Retired artifact numbers live in the Registry. Each top-level identity space
keeps `reserved_history`, the sorted list of numbers that no current document
carries; a reserved number is never issued again, and the allocation check
rejects dropping one. Stage 01 numbering is dense,
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

A Stage 03 package is deleted when it is
[ready for removal review](sdlc.md#sequence) and its removal is approved, once
the meaning a current document still depends on sits in its owner; the
[SDLC](sdlc.md#sequence) owns readiness and batch approval. Its Spec number joins the Registry `reserved_history`, current links to it become
plain text, and version history keeps the body. A package with any
non-terminal Task stays, with its completed Tasks. A terminal Task body stays
immutable while its package exists, so a link it holds into a package deleted
later is not repaired; link alignment excuses exactly that link, from a
terminal Task at a registered Task path into a numbered Spec, data, research
or audit package whose number the checked root's Registry reserves in that
package's identity space. A non-terminal document turns such a link into
plain text that names the retired identity. From lifecycle generation 7 the loader reads
the generation 5 and 6 migration proofs from the last generation 6 revision,
not the working tree, so a package that carried one is retired like any other.

Stage 03 occupancy is a package judgment using the Registry's Spec, Plan, and
Task terminal sets. In an unfinished package, completed Tasks and validly
cancelled Tasks may remain; a terminal Plan may not. A cancelled Task records
nonempty `reason`, an actual `authorization_ref`, and `criteria_disposition`.
Each item names a Spec acceptance `criterion` and exactly one of another
non-cancelled Task in the package (`successor`) or an actual approved scope
withdrawal reference (`withdrawal_ref`). An empty list means no assigned criterion. Withdrawal
never exempts a criterion still present in the Spec from PASS evidence; only a
Criterion Acceptance `not-required` decision closes a criterion without PASS.
A cancelled Spec keeps no package members in active Stage 03.
Standalone documents keep their per-document disposition rule. Incident and
Postmortem records never retire: they are permanent operational history and
stay in place after closure, whatever their age, and no disposition status
admits them to retirement. A Registry disposition entry that lists a status
its profile's lifecycle cannot reach is a defect, not a retirement path. An
empty entry admits no status. The Registry validator rejects an unreachable
status, and any status on a profile with an Incident or Postmortem lifecycle.
No rule here renames lifecycle statuses or applies a union of terminal sets to
other stages.
Stage 03 may be empty when no package remains.

#### Retirement preconditions

Retire a package or a standalone document only when all of these hold.

1. Its profile/status pair is eligible in the Registry's
   `archive_retention.disposition_entry_statuses` map, or it is an ADR or
   Architecture Description whose replacing ADR or Description, carrying its
   summary, lands in the same change. Lifecycle terminality and
   disposition eligibility are separate: neither one grants an automatic
   removal.
2. Every still-current obligation, decision, structure, or procedure it owns is
   written to its canonical agent governance, 01, 02, or 05 owner, and its
   lineage is summarized in that owner's Traceability.
3. Every inbound consumer is updated in the same logical change.
4. Its artifact number is added to the Registry `reserved_history` of its
   identity space in the same change.
5. The removing change records, in a Task that survives it, the last commit
   and path that carry each removed body, and that the commit is reachable
   from `main`. A body that exists only as uncommitted work, only in the
   reflog, only on an unmerged or squash-dropped branch, or not at all in a
   shallow clone blocks that removal, as does a recorded hold. After merge, the
   same Task restores each body from that commit and compares its bytes. A
   body stored through Git LFS or a submodule is recovered as its payload or
   submodule commit, not its pointer or gitlink, and an unrecoverable payload
   or submodule commit blocks that removal. This is a manual record, not a
   gate.

A package is never retired because it is old, because a count was exceeded, or
because nothing currently links to it. Missing inbound links are a defect to
investigate, not permission to delete. Record the summary map and consumer
cutover in the current Task. Age may trigger a disposition review. It never
triggers a deletion.

#### Implementation coverage

Every capability implemented in this workspace has one Stage 01 Requirement
owner for its obligation and one Stage 02 Description or ADR owner for its
structure and durable decision. Retiring a Stage 03 package never removes that
coverage: the package's implemented outcome moves to those owners before the
package is retired.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

- `python scripts/validation/check-document-metadata.py --mode check-active`
- `python scripts/validation/check-document-links.py --mode all` (links, entry
  points, fenced command paths, navigation, language)
- Stage checks selected by the
  [change-type verification matrix](quality-standards.md#5-change-type-verification-matrix).

### Limits

Named checks cover metadata, links, entry points, fenced command paths, navigation, language and the Registry validator; the remaining rules rest on review, owner approval or manual records.

- Authority: no named check or manual only (R1-R4).
- Entry points: no named check or manual only (R5-R7, R9-R14).
- Links: no named check or manual only (R16-R17, R20-R21, R23-R25).
- Authoring: no named check or manual only (R27-R37, R39-R52, R54-R55).
- Language: no named check or manual only (R57-R61).
- Readme: no named check or manual only (R65-R67, R69-R72, R74-R76).
- Roles: no named check or manual only (R78-R92, R94-R99).
- Versions: no named check or manual only (R100-R101, R106-R111).
- Release: no named check or manual only (R112-R114, R116).
- Frameworks: no named check or manual only (R117-R118).
- Routing: no named check or manual only (R119-R121).
- Retention: no named check or manual only (R122-R127, R129-R142, R145-R148, R150-R153).
- Partly named, with a review or manual remainder: R8, R15, R22, R38, R93, R115, R149.
- Link type choice for an untitled link and the author's type choice are a review; the link checker runs in the local profile and its hosted CI route is not wired yet.
- Authority dependence of outside-docs text on stage documents is not inferred by `check-document-links.py` and is reviewed separately.
- The Promotion relation has no check, and the Spec `Owning Requirements` prose and ADR `Supersession` section are checked by review.
- Which version increment a change needs is left to review, and version rows other than the product version have no gate that compares a changed value.
- The language check is a heuristic: it cannot judge meaning and does not judge text too short to measure.
- Retirement preconditions 2 to 5 are a manual record, not a gate.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [SDLC](sdlc.md)
- [Task checklists](task-checklists.md)
- [Documentation index](../../docs/README.md)
- [Stage authoring matrix](stage-authoring-matrix.md)
- Stage 99 registry (`docs/99.templates/registry.json`)
