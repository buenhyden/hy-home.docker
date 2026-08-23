---
profile_id: spec
status: superseded
artifact_id: SPEC-0136
artifact_type: spec
parent_ids:
  - SPEC-0131
  - SPEC-0134
superseded_by: SPEC-0153
created: 2026-08-07
updated: 2026-08-21
---
# SDLC Taxonomy and Agent Governance Convergence Specification

## Overview

This specification defines the approved target design for the repository
documentation lifecycle, spec-driven development flow, AI-agent governance,
operations corpus, archive policy, templates, validators, and scripts.

It replaces the earlier draft decisions in this file. In particular:

- Operations remains Stage 05. It is not renumbered to Stage 04.
- Stage 04 execution artifacts move into their owning Stage 03 capability.
- Architecture Requirements Document is replaced by Architecture Description.
- Operations keeps current operational knowledge in a domain-classified
  catalog and groups it by reviewed subject rather than by parallel guides,
  policies, and runbooks roots.
- Every date-based documentation path moves to a stable ID and slug. Dates are
  metadata, not path identity.
- docs/98.archive becomes the single documentation archive.
- Legacy, deprecated, dormant, duplicate, and one-time script surfaces do not
  remain in the completed repository.

The user approved the original written specification after four staged design
reviews on 2026-08-09 and approved this revised design after six staged
reviews on 2026-08-13. The revised design adds the Operations catalog
container, role-and-purpose consolidation, four-digit internal requirement
identities, stricter per-agent governance, and one-owner validator rules. The
specification is active and its implementation is governed by the related
Plan after that Plan is reconciled to this revision.

## Boundaries and Inputs

The governed inputs are the tracked documentation corpus, Stage 00 and Stage 99
contracts, script and workflow entrypoints, current validator results, Git
provenance, and the external evidence listed below. The change boundary covers
repository documentation and governance implementation only; Runtime and
remote state remain outside it.

## Goals

The convergence must:

1. Establish one coherent SDLC taxonomy from requirements through operations.
2. Keep durable product truth separate from temporary execution state.
3. Co-locate Spec, Plan, and Task by capability without losing completed
   execution evidence.
4. Give every policy topic one canonical typed owner.
5. Replace ambiguous architecture-requirements terminology with externally
   recognized Architecture Description terminology.
6. Make current Operations knowledge discoverable through one domain-classified
   catalog while keeping incidents and releases as separate event records.
7. Replace date-based paths with stable identifiers while preserving dates in
   frontmatter.
8. Consolidate or delete duplicate, conflicting, legacy, deprecated, dormant,
   and one-time scripts and validators.
9. Align local, hook, and CI validation around the same typed gate graph.
10. Preserve the history of every move, merge, replacement, and deletion
    through Git provenance and a migration ledger.
11. Review SDLC terms and every template role for necessity, semantic fit, and
    one-owner enforcement before applying the rule to the corpus.
12. Publish one coherent AI-agent governance system with typed per-agent
    authority, scope, inputs, procedure, outputs, gates, and provider-specific
    projections generated from the canonical owner.
13. Review every Operations subject name and merge or delete role documents
    and subjects that do not own a distinct operational purpose.

## Convergence and Conflict Resolution

The active typed owners in this specification supersede contradictory earlier
documents, rules, validators, scripts, and generated projections. Resolution
uses this order:

1. identify the one canonical typed owner and the workspace purpose it serves;
2. merge unique, still-valid semantics into that owner;
3. update all active consumers and tests atomically;
4. delete the conflicting, duplicate, obsolete, or compatibility predecessor;
5. preserve only Git/migration provenance, never a live compatibility path.

When correction and retention conflict, deletion of the superseded rule is the
default after its valid semantics and consumers have moved. A passing legacy
validator does not justify retaining contradictory rules. Validators for the
same policy topic must share one implementation or be reduced to distinct,
non-overlapping modes under one owner.

## Non-Goals

- This work does not change Compose service topology, deployed runtime state,
  images, networks, secrets, volumes, or remote systems.
- It does not introduce empty documentation categories merely to mirror an
  external framework.
- It does not preserve compatibility paths after their consumers have moved.
- It does not treat a passing schema check as proof that the document corpus
  conforms.
- It does not weaken a validator to accept an inconsistent migration.

## External Evidence and Limits

The target is an internal repository convention informed by standards and
official practices. No cited source mandates the repository's numeric folder
names.

| Source | Supported use in this design |
| :-- | :-- |
| ISO/IEC/IEEE 15289:2019 | Lifecycle information items may be selected, combined, or subdivided to fit an organization's lifecycle model. |
| ISO/IEC/IEEE 29148:2018 | Requirements engineering and requirements information items justify a distinct requirements authority. |
| ISO/IEC/IEEE 42010:2022 | Architecture Description, stakeholder concerns, viewpoints, views, and models justify the Stage 02 vocabulary. |
| NIST SP 800-218 SSDF 1.1 | Security practices and evidence must integrate into the chosen SDLC rather than form an unrelated lifecycle. |
| NIST AI RMF 1.0 | Govern is cross-cutting; agent governance is a control plane, not a serial delivery stage. |
| GitHub Spec Kit | Specification, plan, tasks, and implementation form a practical spec-driven flow. |
| OpenSpec | Completed changes write back into durable specifications. |
| MADR | Architecture decisions use stable sequential identities and supersession links. |
| Google SRE guidance | Runbooks, incident records, postmortems, and corrective actions have different operational roles. |
| Diátaxis | Content purpose should be explicit, but empty classification buckets should not be created. |
| DCMI Metadata Terms | Created, modified, issued, and related dates belong in structured metadata. |

Primary references:

- https://www.iso.org/standard/74909.html
- https://www.iso.org/standard/72089.html
- https://www.iso.org/standard/74393.html
- https://csrc.nist.gov/pubs/sp/800/218/final
- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- https://github.com/github/spec-kit
- https://github.com/Fission-AI/OpenSpec
- https://adr.github.io/madr/
- https://sre.google/workbook/postmortem-culture/
- https://diataxis.fr/start-here/
- https://www.dublincore.org/specifications/dublin-core/dcmi-terms/

## Current-State Evidence

The following measurements were corroborated against tracked files at
78b60974164ff5427ba8c64aaf3ecde4a7faf41a. The Graphify report was stale and
was used only as advisory context.

| Surface | Current state |
| :-- | :-- |
| Stage 00 | 109 files; authority, language, provider, date, load-order, and persona rules conflict |
| Stage 01 | 25 PRDs plus README; no SRS or Interface Requirement profile |
| Stage 02 | 25 architecture-requirements documents, 25 ADRs, and 3 READMEs |
| Stage 03 | 27 Spec directories; 22 redundant child READMEs |
| Stage 04 | 102 dated Plans and 130 dated Tasks |
| Stage 05 | 263 Markdown files; 66 guides, 64 policies, 62 runbooks, and 71 READMEs |
| Stage 90 | 92 Markdown files plus 5 other artifacts; several dated research paths |
| Stage 98 | 52 tombstones, including 32 complete Specs incorrectly treated as tombstones |
| Stage 99 | 27 template sources; only 300 of 600 measured instances conform |
| scripts | 63 tracked files, including 39 Shell and 20 Python files, totaling about 53,748 lines |

Focused traceability currently passes 46 fixed pairs, but broader alignment
fails on 184 links. Of those, 182 are active documents linking directly to
archived material. Active metadata validation reports 1,276 violations across
303 documents. Promoted lifecycle validation reports 25 findings, and 20
legacy tombstones lack complete provenance.

These failures are migration inputs. They are not accepted as permanent
baselines.

## Contracts

This specification changes repository-local documentation, script, archive,
agent-governance, and validation contracts. It introduces no network API or
Runtime service contract. Contract authority and precedence are defined below;
the existing typed registries change before dependent corpus movement.

## Authority Model

Each policy topic has exactly one canonical owner:

| Topic | Canonical owner |
| :-- | :-- |
| Agent roles, authority, approvals, provider projection | Stage 00 typed governance contracts |
| Document types, paths, frontmatter, headings, lifecycle | Stage 99 typed document contracts |
| Script ownership, mutation, consumers, disposition, tests | scripts/manifest.yaml |
| Gate IDs, ordering, environment, and timeout | .github/workflow-contract.yml |
| Current product behavior | Stage 01 through Stage 05 artifacts according to role |

Human-readable documents point to these owners and do not copy complete rule
sets. When two surfaces disagree, typed path authority wins. Ambiguous
ownership, conflicting policy, unsafe paths, or missing approvals fail closed.

Rules Engineer owns Stage 00 policy. Doc Writer contributes documentation but
does not own Stage 00 policy. Hook Developer owns provider rendering and hook
adapters. Mandatory reviewers remain declared in the typed governance
contract.

## Core Design

The target design is the combination of the following taxonomy, artifact-role,
stable-identity, archive, template, script, and gate contracts. A downstream
section may specialize an upstream contract but may not silently override it.

## Target Repository Taxonomy

The final top-level documentation structure is:

    docs/
    ├── 00.agent-governance/
    ├── 01.requirements/
    ├── 02.architecture/
    │   ├── descriptions/
    │   └── decisions/
    ├── 03.specs/
    ├── 05.operations/
    │   ├── catalog/
    │   ├── incidents/
    │   └── releases/
    ├── 90.references/
    ├── 98.archive/
    └── 99.templates/
    scripts/

docs/04.execution is removed after active Plan and Task artifacts are
co-located and completed artifacts are archived.

Stage 00 and scripts are cross-cutting control planes. They are not sequential
SDLC phases.

## Requirements Contract

Stage 01 is flat:

    docs/01.requirements/
    ├── README.md
    └── ####-<slug>.md

Each Requirement Package owns the problem, user value, scope, functional and
non-functional requirements, optional solution-independent interface
requirements, acceptance criteria, dependencies, and constraints. Implemented
schemas belong with the Spec under contracts.

Package-qualified requirement identifiers use four digits. Current declared
examples are:

- `REQ-0001-FR-0001`
- `REQ-0003-NFR-0005`
- `REQ-####-IF-####` only after a package/kind allocation is issued

Acceptance items reference their matching FR IDs and do not allocate separate
acceptance identities.

Unresolved product choices remain in Stage 01 and do not move into
architecture.

## Architecture Contract

Stage 02 is:

    docs/02.architecture/
    ├── README.md
    ├── descriptions/
    │   └── ad-####-<slug>.md
    └── decisions/
        └── adr-####-<slug>.md

Architecture Description owns:

- stakeholders and concerns;
- system boundaries and context;
- viewpoints, views, and component allocation;
- data and control flow;
- quality attributes and quality scenarios;
- security, reliability, and operability architecture;
- requirement disposition;
- links to decisions and implementation specifications.

ADR owns one material choice, alternatives, rationale, consequences, and
supersession.

Architecture Requirements Document, ARD, artifact_type ard, and the
02.architecture/requirements path are removed. They do not receive redirect
files or compatibility profiles.

Direct lineage is:

- SRS to PRD;
- Interface Requirement to PRD or SRS;
- Architecture Description to applicable requirements;
- ADR to Architecture Description;
- Spec to Architecture Description and applicable ADRs.

## Spec-Driven Execution Contract

Each capability is a complete active work unit:

    docs/03.specs/
    ├── README.md
    └── spec-####-<capability>/
        ├── spec.md
        ├── plan.md
        ├── task.md
        └── contracts/

Only spec.md is mandatory. plan.md and task.md exist only while an approved
change is active. contracts is optional and contains machine-readable API,
schema, protocol, or similar implementation contracts.

Capability child README files are removed. spec.md owns the capability
description.

Role boundaries:

- Spec is durable current behavior.
- Plan is the prospective implementation strategy for one approved change.
- Task is work decomposition, state, validation results, and evidence.
- One capability has at most one active change packet.

Completion is atomic:

1. Task validation finishes.
2. Implemented behavior writes back into spec.md.
3. Operator-visible changes update Stage 05.
4. Plan and Task move together into one Stage 98 change packet.
5. plan.md and task.md leave the active capability directory.

A Spec remains active while its capability exists. It is not archived merely
because an implementation task completed.

## Operations Contract

Stage 05 remains Stage 05 and becomes the single integrated Operations root.
The parallel guides, policies, and runbooks roots are removed. Current
operational knowledge is classified under one catalog container; incidents
and releases are event records and therefore remain outside that catalog.

    docs/05.operations/
    ├── README.md
    ├── catalog/
    │   ├── README.md
    │   ├── 00-workspace/
    │   ├── 01-gateway/
    │   ├── 02-auth/
    │   ├── 03-security/
    │   ├── 04-data/
    │   ├── 05-messaging/
    │   ├── 06-observability/
    │   ├── 07-workflow/
    │   ├── 08-ai/
    │   ├── 09-tooling/
    │   ├── 10-communication/
    │   ├── 11-laboratory/
    │   └── 12-infra-net/
    ├── incidents/
    └── releases/

`catalog/` is the canonical current Operations corpus, not a link collection
or reference archive. Each domain directly contains reviewed stable operation
subjects:

    catalog/06-observability/
    ├── README.md
    └── 0045-prometheus/
        ├── guide.md
        ├── policy.md
        └── runbook.md

Only required roles exist for a subject, and each role appears at most once:

| Role | Sole responsibility |
| :-- | :-- |
| Guide | Purpose, concepts, normal use, and non-destructive checks |
| Policy | Mandatory and prohibited behavior, controls, exceptions, verification, and review cadence |
| Runbook | Trigger, prerequisites, safety, ordered commands, expected observations, stop conditions, validation, recovery, and escalation |
| Incident | Occurrence, impact, response timeline, and current state |
| Postmortem | Root cause, contributing factors, learning, follow-up owner, and due condition |
| Release | Scope, evidence, known risk, promotion result, and rollback condition |

Guide Runbook Handoff is conditional on a sibling Runbook. Runbook Automation
Handoff is conditional on real automation. Policy does not copy procedures.
Runbook does not invent unimplemented design. A design gap routes back to the
owning Requirement, Architecture Description, ADR, or Spec.

The Stage 05 README, catalog README, domain READMEs, incidents README, and
releases README are the only Operations indexes. Subject README files are not
created. Empty or redundant domains may merge after content analysis, but the
existing domain meaning is preserved unless the migration ledger records an
approved consolidation.

Subject paths use this role-neutral form:

    docs/05.operations/catalog/<domain>/ops-####-<operational-subject>/

The slug names the managed object or independent operational capability. It
does not contain `guide`, `policy`, `runbook`, `document`, or `manual`; a date,
version, or state; a redundant domain name; repeated tokens; or generic
`basics`/`setup` wording without an independent operational boundary.

Two subjects merge only when all of these are true:

1. they govern the same managed object or operational capability;
2. they have the same operational owner and control boundary;
3. they have materially the same trigger, verification result, and recovery
   boundary; and
4. neither owns an independent review cadence or execution-evidence boundary.

The canonical subject is the one directly consumed by current implementation,
automation, or Runbooks; otherwise the most complete role boundary wins, then
the older stable ID. A new ID is created only when no existing subject can
truthfully own the merged content. Cross-domain duplication has one owner in
the domain that holds operational responsibility. Workspace-wide harness and
repository operations belong only to `catalog/00-workspace/`.

For every approved merge, unique valid semantics move to the correct Guide,
Policy, or Runbook; duplicated prose, empty sections, and template residue are
deleted; active consumers move atomically; and the predecessor subject or role
file is removed. Similar names alone never authorize a merge, and no deprecated
or redirect document remains.

Incident and Release identities are stable:

    docs/05.operations/incidents/<year>/inc-####-<slug>/incident.md
    docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md
    docs/05.operations/releases/rel-####-<slug>/release.md

Incident and Postmortem records link affected catalog subjects through typed
relationships such as `affected_ops_ids`; they are never stored under a single
domain merely because one system was involved.

## Stable Identity and Date Contract

Every new and existing documentation path uses a stable ID and slug. Stable
document identifiers use exactly four decimal digits. Date prefixes and year
partition directories are prohibited except for the required Incident
containment directory described below.

Canonical identities include:

- REQ-0001;
- AD-0001, ADR-0001;
- spec-0136;
- ops-0001, guide-0001, policy-0001, runbook-0001;
- inc-0001, postmortem-0001, rel-0001;
- chg-0001, mig-0001, ref-0001.

README.md and role filenames such as spec.md, plan.md, task.md, guide.md,
policy.md, runbook.md, incident.md, postmortem.md, and release.md inherit stable
path identity from their parent directory and retain their own artifact_id.

The following path shapes are invalid:

- YYYY-MM-DD-slug.md;
- YYYY-MM-DD-slug/;
- year/artifact partitions other than
  `docs/05.operations/incidents/<year>/inc-####-<slug>/`.

This applies to Stages 01, 02, 03, 05, 90, and 98, including every existing
dated Plan, Task, research pack, audit record, release, incident, archive
packet, and migration record. The Incident year is event containment metadata,
not artifact identity; the stable Incident ID remains `inc-####`.

Immutable provenance values are not canonical current paths. Fields such as
`archived_from`, a predecessor ID, an original dated path, a source commit and
blob, or a commit-pinned manifest value preserve their exact historical bytes.
Validators must distinguish these values from live routes and may not rewrite
them merely to satisfy current path syntax.

Common frontmatter includes:

- status;
- artifact_id;
- artifact_type;
- parent_ids;
- created;
- updated.

created is immutable. updated changes only for semantic changes. Additional
typed dates are:

| Type | Additional fields |
| :-- | :-- |
| Plan and Task | completed_at |
| Guide, Policy, Runbook | reviewed_at, next_review_at |
| Incident | occurred_at, resolved_at |
| Postmortem | reviewed_at |
| Release | released_at |
| Change packet and Tombstone | archived_at |
| Migration | completed_at |
| Reference evidence | observed_at when applicable |

Dates use ISO 8601. Event timelines may include timestamps in their body; path
identity never uses them.

The validator enforces global artifact_id uniqueness, type-specific ID shape,
path-to-ID agreement, four-digit internal requirement and acceptance-criterion
identities, and absence of dated documentation paths. Distinct artifact roles
may reuse a numeric sequence only when their complete artifact IDs remain
globally unique.

## Archive Contract

docs/98.archive is the single documentation archive. The root archive
directory is removed after its tracked content is classified and migrated.

    docs/98.archive/
    ├── README.md
    ├── changes/
    │   └── chg-####-<slug>/
    │       ├── plan.md
    │       └── task.md
    ├── tombstones/
    │   ├── 01.requirements/
    │   ├── 02.architecture/
    │   ├── 03.specs/
    │   └── 05.operations/
    └── migrations/
        └── mig-####-sdlc-taxonomy-convergence.md

Change packets retain the completed Plan and Task body. Tombstones are concise
provenance records and do not reproduce removed bodies.

Required tombstone fields are:

- artifact_id;
- artifact_type tombstone;
- archived_from;
- archived_at;
- archived_commit;
- archived_blob;
- replacement when one exists;
- reason.

Active documents never link directly to Stage 98. Consumers move to the
current replacement before archival. Historical lookup uses the migration
ledger and Git provenance.

The 32 complete Specs currently under docs/98.archive/03.specs are
reclassified. A current capability returns to Stage 03; a genuinely retired
capability becomes a concise tombstone.

The migration ledger records every moved, merged, replaced, and deleted path:

- legacy_path;
- stable_path;
- artifact_id;
- action;
- replacement;
- source_commit;
- source_blob;
- canonical role and owner;
- unique semantics preserved by an approved merge;
- duplicate or template-residue semantics removed;
- affected active consumers;
- verification evidence;
- reason.

An Operations merge is not executable until its ledger row names the canonical
subject, target role files, and consumer migration. The ledger preserves
historical identity and Git proof; it does not preserve a live compatibility
copy of the removed body.

## Template Contract

Stage 99 contains the following SDLC templates:

    docs/99.templates/templates/sdlc/
    ├── prd.template.md
    ├── srs.template.md
    ├── interface-requirement.template.md
    ├── architecture-description.template.md
    ├── adr.template.md
    ├── spec.template.md
    ├── plan.template.md
    └── task.template.md

ard.template.md is renamed in Git to architecture-description.template.md and
then all ARD contracts are removed. SRS and Interface Requirement profiles are
added.

Operations templates become subject-folder aware. Conditional sibling
sections do not generate placeholder boilerplate. Incident, Postmortem, and
Release templates use stable IDs and typed event metadata.

Template selection, frontmatter, lifecycle, path, archive, and metadata
profiles change atomically. A template rule is not promoted until positive and
negative fixtures prove its path, headings, lifecycle, and frontmatter
behavior.

Each document role has exactly one canonical template. A generic template does
not replace a role's required semantics. When two templates own the same role
question, unique valid fields move to the canonical template and the duplicate
is deleted. Existing documents do not justify weakening a template: the
document's role is reviewed first, then it is corrected, moved, merged, or
deleted. Guide Runbook Handoff, Runbook Automation Handoff, Incident
Postmortem routing, and similar sibling sections appear only when the related
artifact or implemented automation exists.

## Script Governance Contract

scripts/manifest.yaml becomes the complete machine-readable inventory for all
tracked files below scripts.

Each record contains:

- path;
- kind;
- authority;
- lifecycle;
- mutation;
- consumers;
- disposition;
- successor;
- tests.

During migration, disposition may be retain, rewrite, merge, or delete. A live
manifest record always describes a currently tracked file. The completed
manifest therefore contains maintained files only. A file selected for deletion
and its disposition evidence move to the migration ledger in the same commit
that removes its final consumer and live manifest record. Legacy, deprecated,
dormant, and compatibility-wrapper states are not final states.

Every tracked script file appears exactly once. Every executable has one
canonical owner, declared mutation behavior, at least one consumer, and a
verification path.

Generators default to check mode. Repository changes require explicit
--write. Runtime-changing operations require explicit invocation and a
Runbook.

The implementation performs these directed consolidations:

| Current surface | Required disposition |
| :-- | :-- |
| LLM Wiki index and coverage Shell generators | Merge their duplicated source-selection and classification engine; remove old files after consumer migration |
| Document traceability and implementation-alignment Shell validators | Share one document-graph library and one mode-driven Python CLI |
| Metadata and lifecycle Python validators | Share frontmatter, path, Git provenance, and migration parsing while retaining role-specific CLIs |
| Generated artifact checks | Register owners and outputs once and execute one aggregate freshness gate |
| check-repo-contracts.sh | Move typed rules to their owners, replace residual invariants with a focused validator, and delete the 4,056-line Shell policy engine |
| recommend-qa-gates.sh | Merge selection into the typed gate runner |
| report-provider-hook-parity.sh | Merge reporting into provider rendering |
| patch-graphify-post-commit.sh | Move the filter into canonical hook generation and delete the after-install patch |
| post-tool-validate.sh | Reduce to a non-mutating typed gate dispatcher |
| Rehearsals with dated Task paths | Replace paths with stable artifact IDs; retain only if a current Runbook and test consume them |
| Consumerless reports, recommendations, and rehearsals | Merge useful behavior or evidence into the canonical owner, then delete |
| Dormant lifecycle modes | Give them a current consumer and test or remove them |

The typed gate CLI, local QA runner, CI pre-commit runner, controlled agent
all-files runner, metadata CLI, lifecycle CLI, provider sync wrapper, and
provider renderer are retained by default because they have distinct current
roles. The manifest audit may still delete one if its consumers and tests do
not justify it.

One-time migration utilities are not tracked. Their durable output is the
migration ledger and validated corpus. __pycache__, temporary evidence, and
generated intermediates do not remain in the final tree.

## Validator Ownership Contract

The repository does not converge on one policy monolith. It converges on one
typed owner and one implementation for each validation topic:

| Topic | Typed owner | Focused execution surface |
| :-- | :-- | :-- |
| Document identity, path, and frontmatter | Stage 99 metadata profiles and taxonomy library | `check-document-metadata.py` |
| Lifecycle, archive, and migration provenance | Stage 98/99 lifecycle and archive contracts | `check-document-corpus-lifecycle.py` |
| Links, lineage, and traceability | Shared document graph library | explicit modes of `check-document-links.py` |
| Operations catalog and role duplication | Operations role/profile contract | `check-operations-catalog.py` |
| Agent governance and provider parity | Stage 00 typed contracts | agent-governance validator and renderer |
| Script ownership and mutation | `scripts/manifest.yaml` | `check-script-manifest.py` |
| Gate selection and ordering | workflow contract registry | `run-ci-gate.py` |

`scripts/lib/document_governance/` owns shared taxonomy, frontmatter, Git
provenance, migration, link-graph, and finding primitives. CLIs import those
libraries and never dynamically import one another. Metadata, lifecycle,
links, and Operations checks retain distinct policy responsibilities even when
they share parsing and evidence code.

The Operations validator fails closed on catalog/domain/subject shapes,
four-digit identities, role cardinality, forbidden role roots and subject
READMEs, role-specific headings and fields, duplicated role content, duplicate
subject candidates, Incident/Release topology, stale consumers, and migration
source/target provenance. Similarity findings are review inputs only; deletion
requires an approved typed migration disposition.

`check-repo-contracts.sh` is decomposed by inventorying its rules, moving each
still-valid rule to its typed owner and focused validator, migrating every
consumer to registered gate IDs, proving the former detection behavior with
positive and negative mutations, and deleting the Shell monolith with its last
consumer. A legacy pass does not authorize retaining a conflicting rule.

## Validation and CI Contract

The Pull Request required aggregate includes:

- document contract;
- metadata and stable path identity;
- lifecycle and archive integrity;
- cross-link and traceability;
- Operations catalog topology and semantic-role integrity;
- template conformance;
- governance authority;
- provider surface freshness;
- generated artifact freshness;
- script manifest integrity.

Pull Requests compare against the PR base SHA. Push validation compares against
the push-before SHA. HEAD~1 is not an acceptable default for a multi-commit
change.

Local and CI profiles use the same gate IDs and leaf implementations. The
controlled all-files pre-commit wrapper is a formatter and hook safety layer;
it is not represented as full repository validation.

The typed contract selects a focused validator, and the workflow registry
routes that same CLI and arguments to local, pre-commit, controlled-agent, and
CI execution. CI-only weakening and local-only exceptions are prohibited.
Transition allowances require an exact source commit, legacy path, successor,
owner Task, and expiry condition; final convergence has zero allowances.

Validation dependencies are reproducible and pinned. The current html5lib
dependency failure is resolved through the approved validation environment,
not by bypassing provider or governance checks.

Generated outputs have one registered owner and freshness command. Every
generator defaults to non-mutating check behavior.

## Stage 00 Convergence

Stage 00 is retained as the sole canonical AI-agent governance control plane.
`agent-catalog.yaml`, `governance-artifacts.yaml`, and
`provider-models.yaml` own typed identities, artifacts, and provider/model
facts; human rules and provider adapters point to them rather than copying
their complete values.

Each active agent has exactly one contract containing its stable identity,
single responsibility, allowed and forbidden scopes, inputs and preconditions,
procedure, outputs and handoff, mandatory gates, mutation boundary, escalation
conditions, allowed functions/skills, provider routing, and canonical owner.
Agent and function counts are outcomes of this review, not fixed targets.

Agents with the same purpose, scope, inputs, outputs, and gates merge. A role
that is only a procedure of another agent becomes a function or skill. A
separate agent remains only when it owns an independent approval, security,
review, or mutation boundary. A consumerless or unprojectable agent is reviewed
for removal; deprecated agents do not remain after their valid behavior moves.

Rules Engineer owns Stage 00 policy. Domain implementation and operations
agents own their technical outputs. Doc Writer contributes structure and
language but does not own another role's policy or design decision. Hook
Developer owns deterministic provider/hook projection but not the source
policy. Implementers never supply their own final independent approval.

The provider surfaces `.claude/`, `.codex/`, `.gemini/`, and `.agents/` are
thin generated or validated adapters. Their agent/function sets and provider
models derive from Stage 00 typed contracts. They may adapt provider syntax and
runtime mechanics but may not redefine SDLC, workflow, completion, role,
language, template, or model policy. Drift fails closed.

Stage 00 keeps one load order, one workflow, and one completion contract.
Requirements, Architecture, Spec, Plan, Task, Operations, and Incident work
select typed agents and reviewers through those contracts. Unused scopes and
duplicated provider prose are removed rather than retained as compatibility
policy.

`memory/current.md` is a bounded verified handoff, not policy authority.
Memory that conflicts with the current Spec, Task, typed contract, or live Git
state is corrected or deleted. Dated external observations move to stable
Stage 90 evidence, and notes already promoted to active rules are consolidated
or removed.

## Migration Data Flow

The migration follows this dependency order:

    Authority and typed contracts
      -> templates and validators
      -> Stage 01 and Stage 02 identities
      -> Stage 03 and Stage 04 co-location
      -> Operations catalog migration manifest
      -> Stage 05 structural move under catalog
      -> Stage 05 subject naming and semantic-role consolidation
      -> Stage 90 and Stage 98 stable identities
      -> scripts consolidation
      -> CI and local gate alignment
      -> cross-link, index, memory, and generated-output repair

Every path move uses Git-aware rename where possible. All inbound references
and the migration ledger change in the same logical commit. No redirect file is
left behind.

Operations structural movement and semantic consolidation are separate review
units. The structural unit moves domains under `catalog/` without redesigning
their bodies. The semantic units review subject names and roles by bounded
domain groups: workspace/gateway/auth/security; data/messaging/observability;
workflow/AI/tooling; communication/laboratory/infra-net; then
incidents/releases/root indexes. Each group passes its own manifest, metadata,
Operations, link, archive-consumer, provenance, diff, and independent-review
gates before commit.

If a migration unit cannot pass its scoped gates, no later unit consumes its
new structure. Recovery uses a normal revert commit or a corrective commit;
destructive history rewriting is not required.

## Logical Commit Boundaries

The remaining implementation uses these logical commit boundaries after the
already completed earlier convergence commits:

1. Approve this revised SDLC and Operations catalog design.
2. Complete the shared document-validation libraries and focused link CLI.
3. Normalize four-digit identities and Incident routing.
4. Register the complete Operations catalog/subject migration manifest.
5. Move Operations domains under `catalog/` without semantic rewriting.
6. Converge Operations subject names and roles by each bounded domain group.
7. Align Incident, Release, catalog, and root indexes and templates.
8. Remove the policy monolith, duplicate validators, and one-time scripts.
9. Align local, hook, controlled-agent, and CI gates.
10. Repair current links, generated evidence, indexes, and governance Memory.
11. Remove transition allowances and complete regression verification.

A domain group may split further if required to remain reviewable, but
structural moves, semantic mergers, and unrelated policy changes are not
combined.

## Interfaces and Data

The primary data interfaces are typed frontmatter, artifact IDs, parent_ids,
the migration ledger, the script manifest, generated-output ownership records,
and the workflow gate graph. They are versioned repository files. Validators
consume them without inferring canonical policy from prose. Migration writes
change only through explicitly approved document and script paths.

## Failure Modes and Guardrails

- Conflicting typed owners, ambiguous path classification, or duplicate
  artifact IDs fail closed.
- A path move without complete inbound-link and migration-ledger coverage does
  not proceed.
- An Operations merge based only on textual similarity does not proceed; all
  four ownership, trigger, evidence, and cadence criteria must be proven.
- A role file is not deleted until its unique valid semantics have moved to a
  canonical Guide, Policy, or Runbook and active consumers have followed it.
- A deleted script without a successor or proven absence of consumers does not
  proceed.
- A generator that mutates in check mode fails validation.
- A Runbook command without implemented behavior, observable expectations, and
  recovery guidance is rejected.
- A migration unit that fails its scoped gates remains isolated from later
  units and is corrected or reverted through normal Git history.

## Verification

### Contract tests

- Positive and negative fixtures for every document profile.
- Stable four-digit ID uniqueness, internal requirement identity width, and
  path-to-frontmatter agreement.
- Rejection of date-prefixed files and year partition directories except the
  exact Incident containment route.
- Architecture Description acceptance and ARD rejection.
- Operations catalog/domain/subject topology and role selection.
- Operations role duplication and subject-merge candidate detection, with
  mutation tests proving that similarity alone cannot authorize deletion.
- AI-agent owner, scope, handoff, gate, provider projection, and duplicate-role
  enforcement.
- Archive provenance and active-link prohibition.
- Script manifest coverage and consumer validation.

### Migration tests

- Old-to-new path map is complete and collision-free.
- Every moved path preserves Git provenance.
- Every deleted active reference has a current replacement or is removed.
- No active document points into Stage 98.
- No Stage 04 path remains.
- No parallel Operations role root remains.
- Every active Operations domain is under `docs/05.operations/catalog/`.
- No approved Operations predecessor or redundant role file retains an active
  consumer after its canonical merge.
- No root archive path remains.

### Gate tests

- Local and CI resolve identical leaf gate IDs.
- PR and push base selection covers every commit in the change range.
- Missing dependency, missing owner, unknown document type, ambiguous path, or
  stale generated output fails closed.
- Check mode does not modify the working tree.
- Explicit write mode changes only registered outputs.

### Final repository verification

- Relevant unit and integration tests pass.
- Document metadata, lifecycle, archive, cross-link, traceability, template,
  governance, provider, generated-output, and script-manifest gates pass.
- Git diff has no whitespace errors.
- Git status contains no temporary or generated residue.
- Graphify is regenerated only after tracked source validation passes and its
  report is treated as advisory if health remains degraded.

## Acceptance Criteria

The work is complete only when:

1. The approved top-level taxonomy exists and docs/04.execution is absent.
2. Stage 02 uses descriptions and Architecture Description exclusively.
3. Stage 03 co-locates active Spec, Plan, and Task by capability.
4. Stage 05 has no guides, policies, or runbooks parallel roots.
5. Current Operations content is grouped under
   `docs/05.operations/catalog/<domain>/ops-####-<subject>/`; incidents and
   releases are catalog siblings rather than domains.
6. No documentation path uses a date prefix or a year partition for identity;
   the sole year containment exception is
   `docs/05.operations/incidents/<year>/inc-####-<slug>/`.
7. Dates remain in typed frontmatter and event timelines where applicable.
8. docs/98.archive is the only documentation archive.
9. Active documents do not link to archived tombstones or change packets.
10. Stage 99 templates and metadata profiles match the new taxonomy.
11. Stage 00 contains one non-conflicting SDLC and agent-governance authority
    model.
12. Every tracked script has a manifest disposition, owner, consumer,
    mutation profile, and test.
13. Duplicate and one-time scripts are merged or deleted, not deprecated.
14. Typed validators have one rule owner and local/CI execution parity.
15. The migration ledger accounts for every modified, merged, moved,
    replaced, and deleted legacy path.
16. Every document identity uses a four-digit numeric component, including
    existing Requirement Packages and internal requirement identities;
    acceptance items reference their matching FR IDs, and Incident packets use
    the required year partition.
17. Every Operations subject name and retained role file owns a distinct
    reviewed operational purpose; approved duplicates are merged and removed.
18. Every active agent has one typed owner, responsibility, scope, handoff,
    gate, and provider projection, with duplicate or consumerless roles
    consolidated or deleted.
19. All required final gates pass without grandfathered migration debt.

## Related Documents

- [Stage 00 bootstrap](../../00.agent-governance/policies/bootstrap.md)
- [Stage authoring matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [SDLC document contract](../../99.templates/support/sdlc-document-contract.md)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
- [Parent Spec 134](../0134-agent-governance-canonical-convergence/spec.md)

## Behavior Contract

The behaviors and invariants already specified above remain the package behavior contract.

## Technical Approach

The implementation and component design recorded above remain the technical approach.

## Acceptance Contract

The verification and success conditions above remain the acceptance contract.

## Traceability

The requirement, architecture, operations, and evidence links above provide traceability.
