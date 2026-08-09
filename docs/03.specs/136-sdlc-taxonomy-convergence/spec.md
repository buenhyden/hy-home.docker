---
status: draft
artifact_id: spec:136-sdlc-taxonomy-convergence
artifact_type: spec
parent_ids:
  - spec:134-agent-governance-canonical-convergence
  - spec:131-document-corpus-lifecycle-migration-foundation
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
- Operations is organized by domain and subject rather than by parallel
  guides, policies, and runbooks roots.
- Every date-based documentation path moves to a stable ID and slug. Dates are
  metadata, not path identity.
- docs/98.archive becomes the single documentation archive.
- Legacy, deprecated, dormant, duplicate, and one-time script surfaces do not
  remain in the completed repository.

The status remains draft until the user reviews this written specification.
The design decisions themselves were approved in four staged reviews on
2026-08-09.

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
6. Make Operations discoverable by the system or service being operated.
7. Replace date-based paths with stable identifiers while preserving dates in
   frontmatter.
8. Consolidate or delete duplicate, conflicting, legacy, deprecated, dormant,
   and one-time scripts and validators.
9. Align local, hook, and CI validation around the same typed gate graph.
10. Preserve the history of every move, merge, replacement, and deletion
    through Git provenance and a migration ledger.

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
    ├── prd-<id>-<slug>.md
    ├── srs-<id>-<slug>.md
    └── interface-<id>-<slug>.md

PRD owns the problem, user value, scope, product requirements, and acceptance
criteria.

SRS is optional. It owns system or software behavior, quality requirements,
external dependencies, and constraints when that detail would overload the
PRD.

Interface Requirement is optional. It owns participants, direction, exchanged
information semantics, constraints, compatibility expectations, and failure
expectations. Implemented schemas belong with the Spec under contracts.

Internal requirement identifiers are:

- PRD-001-R001 and PRD-001-AC001
- SRS-001-R001
- IFR-001-R001

Unresolved product choices remain in Stage 01 and do not move into
architecture.

## Architecture Contract

Stage 02 is:

    docs/02.architecture/
    ├── README.md
    ├── descriptions/
    │   └── ad-<id>-<slug>.md
    └── decisions/
        └── adr-<id>-<slug>.md

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
    └── spec-<id>-<capability>/
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
The parallel guides, policies, and runbooks roots are removed.

    docs/05.operations/
    ├── README.md
    ├── 00-workspace/
    ├── 01-gateway/
    ├── 02-auth/
    ├── 03-security/
    ├── 04-data/
    ├── 05-messaging/
    ├── 06-observability/
    ├── 07-workflow/
    ├── 08-ai/
    ├── 09-tooling/
    ├── 10-communication/
    ├── 11-laboratory/
    ├── 12-infra-net/
    ├── incidents/
    └── releases/

Each domain directly contains stable operation subjects:

    06-observability/
    ├── README.md
    └── ops-<id>-prometheus/
        ├── guide.md
        ├── policy.md
        └── runbook.md

Only required roles exist for a subject:

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

Domain README files and the Stage 05 README are the only Operations indexes.
Subject README files are not created. Empty or redundant domains may merge
after content analysis, but the existing domain meaning is preserved unless
the migration ledger records an approved consolidation.

Incident and Release identities are stable:

    incidents/inc-<id>-<slug>/incident.md
    incidents/inc-<id>-<slug>/postmortem.md
    releases/rel-<id>-<slug>/release.md

## Stable Identity and Date Contract

Every new and existing documentation path uses a stable ID and slug. Date
prefixes and year partition directories are prohibited.

Canonical identities include:

- prd-001, srs-001, interface-001;
- ad-0001, adr-0001;
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
- year/artifact partitions.

This applies to Stages 01, 02, 03, 05, 90, and 98, including every existing
dated Plan, Task, research pack, audit record, release, incident, archive
packet, and migration record.

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
path-to-ID agreement, and absence of dated documentation paths.

This specification remains at its legacy path and uses the legacy colon-form
identifier only for the design-review commit. During the Stage 03 identity
migration it moves to docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md,
its artifact_id becomes spec-0136, and its parent_ids migrate atomically. This
avoids applying one isolated taxonomy change before its validators and inbound
references exist.

## Archive Contract

docs/98.archive is the single documentation archive. The root archive
directory is removed after its tracked content is classified and migrated.

    docs/98.archive/
    ├── README.md
    ├── changes/
    │   └── chg-<id>-<slug>/
    │       ├── plan.md
    │       └── task.md
    ├── tombstones/
    │   ├── 01.requirements/
    │   ├── 02.architecture/
    │   ├── 03.specs/
    │   └── 05.operations/
    └── migrations/
        └── mig-<id>-sdlc-taxonomy-convergence.md

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
- reason.

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

## Validation and CI Contract

The Pull Request required aggregate includes:

- document contract;
- metadata and stable path identity;
- lifecycle and archive integrity;
- cross-link and traceability;
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

Validation dependencies are reproducible and pinned. The current html5lib
dependency failure is resolved through the approved validation environment,
not by bypassing provider or governance checks.

Generated outputs have one registered owner and freshness command. Every
generator defaults to non-mutating check behavior.

## Stage 00 Convergence

Stage 00 is retained as the canonical AI-agent governance control plane and is
reconciled in place:

- typed path authority replaces conflicting prose ownership;
- language policy is owned once by document role;
- provider overlays point to typed model and capability contracts;
- date and path rules point to the Stage 99 contract;
- load order, lifecycle, workflow, and completion checklists are consolidated;
- unused frontend, mobile, backend, product, entry, and meta scopes are removed
  or converted to explicit conditional capability profiles;
- provider model versions and function counts are regenerated from typed
  sources;
- workspace memory points to the active convergence Task during implementation
  and to the durable Spec after completion.

Workspace-wide rules apply to each agent through its declared role,
permissions, mandatory reviewers, and provider adapter. Providers do not own
independent SDLC variants.

## Migration Data Flow

The migration follows this dependency order:

    Authority and typed contracts
      -> templates and validators
      -> Stage 01 and Stage 02 identities
      -> Stage 03 and Stage 04 co-location
      -> Stage 05 subject-first organization
      -> Stage 90 and Stage 98 stable identities
      -> scripts consolidation
      -> CI and local gate alignment
      -> cross-link, index, memory, and generated-output repair

Every path move uses Git-aware rename where possible. All inbound references
and the migration ledger change in the same logical commit. No redirect file is
left behind.

If a migration unit cannot pass its scoped gates, no later unit consumes its
new structure. Recovery uses a normal revert commit or a corrective commit;
destructive history rewriting is not required.

## Logical Commit Boundaries

The implementation uses these logical commits:

1. Approve the SDLC taxonomy convergence specification.
2. Establish canonical SDLC and authority contracts.
3. Replace ARD with Architecture Description templates and profiles.
4. Migrate Requirement and Architecture stable identities.
5. Co-locate Spec, Plan, and Task artifacts.
6. Reorganize Operations by domain and subject.
7. Consolidate Archive and migrate stable identities.
8. Add the script manifest and shared governance libraries.
9. Consolidate document and generated-artifact validators.
10. Remove duplicate, one-time, and compatibility tooling.
11. Align local and remote policy gates.
12. Repair references, indexes, memory, and the migration ledger.
13. Complete governance-corpus regression verification.

A commit may split further if required to remain reviewable, but unrelated
units are not combined.

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
- Stable ID uniqueness and path-to-frontmatter agreement.
- Rejection of date-prefixed files and year partition directories.
- Architecture Description acceptance and ARD rejection.
- Operations subject-folder role selection.
- Archive provenance and active-link prohibition.
- Script manifest coverage and consumer validation.

### Migration tests

- Old-to-new path map is complete and collision-free.
- Every moved path preserves Git provenance.
- Every deleted active reference has a current replacement or is removed.
- No active document points into Stage 98.
- No Stage 04 path remains.
- No parallel Operations role root remains.
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
5. Operations content is grouped by domain and stable operation subject.
6. No documentation path uses a date prefix or year partition for identity.
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
16. All required final gates pass without grandfathered migration debt.

## Related Documents

- [Stage 00 bootstrap](../../00.agent-governance/rules/bootstrap.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [SDLC document contract](../../99.templates/support/sdlc-document-contract.md)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
- [Parent Spec 134](../134-agent-governance-canonical-convergence/spec.md)
