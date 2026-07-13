---
status: active
artifact_id: spec:130-template-contract-system-canonicalization
artifact_type: spec
parent_ids:
  - spec:129-document-contract-canonicalization
---

# Template Contract System Canonicalization Technical Specification

## Overview

This specification defines the registry-first, staged canonicalization of the
workspace template system. It turns the metadata foundation established by
Spec 129 into a consistent separation between machine contracts, human
contracts and governance, copyable template forms, executable validation, and
preservation-oriented consumer migration.

The immediate implementation owns Stage 99, its direct Stage 00 and validator
fallout, and the already typed document chain. The remaining active,
operational, historical, archive, and generated corpus is routed into bounded
follow-up batches with independent validation. This prevents a template cleanup
from rewriting execution history or inventing review evidence.

## Current Evidence

The approved design is based on tracked source, the canonical implementation
audit, and read-only corpus inspection as of 2026-07-13 KST.

- Stage 99 contains 44 tracked files: one root catalog, 11 support files, and
  32 files under templates.
- Twenty-three copyable Markdown template sources exist. Twenty-one contain
  non-copyable Rules blocks even though the current contract assigns rules to
  support.
- Twenty typed template sources are registered. All currently use the
  registry presentation order and no registered template contains a legacy
  frontmatter key.
- The Stage 01 through Stage 05 typed-family corpus contains 527 leaf
  documents. Seventeen are fully typed; 510 remain advisory migration debt.
- The untyped debt is not caused by generic legacy keys. No tracked target uses
  type, document_type, template_type, owner, updated, or links as a legacy
  frontmatter key in the inspected corpus.
- The remaining untyped corpus includes 280 active, 229 completed, and one
  superseded document. Historical execution bodies therefore require evidence
  preservation rather than mechanical restyling.
- All 229 tracked README files classify into exactly one of 17 profiles. A
  repository-wide README rewrite is neither necessary nor authorized here.
- The common README template is a 435-line mixture of copyable form, selection
  rules, snippets, lifecycle guidance, and governance.
- The generic Task and Harness Task templates target the same Stage 04 path
  family and the same task artifact type without a deterministic role boundary.
- Audit has a distinct registry and human role but no distinct copyable
  template. Current routing incorrectly reuses the Reference template.
- The Release template is registered but absent from the required-template
  inventory in the repository contract checker.
- The Stage 00 memory template mirror duplicates the Stage 99 source.

Graphify output was built from commit f8a72211 and is stale relative to the
approved baseline a42f70b4. It is navigation-only evidence for this work;
completion claims use tracked source, Stage 00 and Stage 99 contracts, stage
documents, validators, tests, and Git evidence.

## Strategic Boundaries & Non-goals

### Goals

- Make the metadata registry and validator the sole exact machine contract.
- Keep human role, lifecycle, selection, and governance rules in named Stage 99
  support owners.
- Reduce copyable templates to frontmatter and body forms that are safe to
  instantiate.
- Define deterministic template roles, target matchers, parent relationships,
  body-section envelopes, and placeholder rules.
- Preserve the existing common lifecycle vocabulary while keeping document
  workflow state and incident response state semantically separate.
- Reconcile PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident,
  Postmortem, Release, Reference, Audit, Archive, README, governance, and
  machine-readable contract forms.
- Establish a traceable, iterative Stage 01 through Stage 05 authoring and
  feedback flow.
- Apply the new system to the fully typed chain and direct fallout before
  routing the remaining corpus into evidence-safe batches.
- Maintain logical commits and independent implementation, specification, and
  quality reviews for every implementation task.

### Non-goals

- Do not rewrite all 527 Stage 01 through Stage 05 leaves in one branch.
- Do not rewrite 229 README files solely for visual uniformity.
- Do not create Incident, Postmortem, or Release records without a real event.
- Do not infer review dates, test dates, parent identities, approvals, runtime
  state, or release outcomes.
- Do not change Docker Compose, infrastructure runtime, secrets, deployments,
  remote GitHub configuration, or user-global provider settings.
- Do not restyle completed Plans, Tasks, Incidents, Releases, or audit results
  in a way that changes their historical meaning.
- Do not create a separate Vault/content typed family when the tracked corpus
  has no qualifying leaf documents.
- Do not use frontmatter order to imply semantic priority.

## Boundaries and Inputs

- [Spec 129: Document Contract Canonicalization](../129-document-contract-canonicalization/spec.md)
- [Agent Governance PRD](../../01.requirements/024-agent-governance-standardization.md)
- [Agent Governance ARD](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- [ADR-0027: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Stage 99 template system](../../99.templates/README.md)

## External Source Basis

External sources inform the local design; they do not define the repository's
exact type names, directory numbers, status enum, or frontmatter schema.

| Official or primary source | Local design consequence |
| --- | --- |
| [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) | Separate information-item purpose and content requirements from local template presentation and lifecycle governance. |
| [YAML 1.2.2](https://yaml.org/spec/1.2.2/) | Reject duplicate mapping keys and treat key order as presentation rather than semantics. |
| [GitHub Docs YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter) | Validate consumer-specific metadata with an explicit schema instead of one universal key set. |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | Keep requirements, constraints, acceptance criteria, provenance, and verification traceable in the PRD role. |
| [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) | Give ARDs explicit stakeholders, concerns, boundaries, viewpoints, models, constraints, and requirement links. |
| [MADR](https://adr.github.io/madr/) | Keep one decision per ADR and distinguish context, options, outcome, consequences, and confirmation. |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Separate what and why, technical design, execution planning, tasks, implementation, and cross-artifact analysis. |
| [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html) | Treat the numbered stages as iterative gates rather than a fixed waterfall. |
| [NASA SWE-052](https://swehb.nasa.gov/spaces/7150/pages/16450285/SWE-052%2B-%2BBidirectional%2BTraceability%2BBetween%2BHigher%2BLevel%2BRequirements%2Band%2BSoftware%2BRequirements) | Maintain stable identities, bidirectional links, orphan detection, and change-impact traceability. |
| [ISO/IEC/IEEE 26514:2022](https://www.iso.org/standard/77451.html) and [Kubernetes content types](https://kubernetes.io/docs/contribute/style/page-content-types/) | Separate explanatory usage guidance, task procedures, tutorials, and reference facts by purpose. |
| [NIST security policy definition](https://csrc.nist.gov/glossary/term/security_policy) | Keep Policy focused on required or prohibited controls and exception authority, not command sequences. |
| [Google SRE On-call](https://sre.google/workbook/on-call/) and [Emergency Response](https://sre.google/sre-book/emergency-response/) | Require triggers, prerequisites, tested procedures, verification, rollback, escalation, and automation handoff in Runbooks. |
| [NIST SP 800-61r3](https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations) | Keep Incident response records distinct from retrospective learning. |
| [Google SRE Postmortem Culture](https://sre.google/workbook/postmortem-culture/) | Require factual, blameless analysis and owned, tracked follow-up actions. |
| [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) | Treat a Release record as evidence for a real version, tag or commit, artifacts, validation, approvals, and outcome. |
| [SLSA v1.2 provenance](https://slsa.dev/spec/v1.2/provenance) | Record task evidence with command, tool, commit, result, and evidence location without claiming SLSA conformance. |

## Contracts

The following contracts define one owner for each machine rule, human rule,
copyable form, lifecycle transition, and validation behavior. They also define
the preservation boundary for current and historical consumers.

## Canonical Ownership Model

| Surface | Sole responsibility |
| --- | --- |
| document-metadata-profiles.yaml | Exact profiles, key sets, types, enum values, parent rules, lifecycle transitions, serialization order, README profiles, template roles, target matchers, and body-section envelopes. |
| Metadata and repository validators | Executable interpretation of the registry and fail-closed diagnostics. |
| frontmatter-contract.md | Human interpretation of frontmatter and serialization boundaries. |
| sdlc-document-contract.md | Human roles and traceability rules for SDLC and operations documents. |
| common-document-contract.md | Human roles for Reference, Audit, Archive, governance, generated output, template sources, repo support, and native surfaces. |
| readme-profile-contract.md | README profile selection, heading envelopes, metadata consumers, and local-content boundary. |
| template-contract.md | Structural requirements for copyable template sources and instantiated targets. |
| template-selection.md | Purpose-to-template and target-path routing. |
| lifecycle-status.md | Human lifecycle interpretation; exact transitions remain registry-owned. |
| template-governance.md | Creation, review, approval, replacement, migration, destructive change, and commit governance. |
| external-source-rationale.md | Verified external source rationale and local interpretation. |
| templates | Copyable forms only. |
| Stage 99 README files | Catalog and routing only. |

No detailed shared rule may be copied into a catalog README or template source.
Templates may contain required placeholders and topic-specific section prompts,
but they may not contain selection rules, lifecycle algorithms, path policy,
authoring-language policy, or migration governance.

## Frontmatter Contract

The common lifecycle vocabulary remains:

- draft
- active
- completed
- superseded
- archived

The canonical presentation order remains:

1. status
2. artifact_id
3. artifact_type
4. parent_ids
5. supersedes
6. reviewed_at
7. review_cycle
8. generated_by
9. archived_from
10. archived_on
11. archive_reason
12. current_replacement

Each profile continues to define its exact subset. Generic type,
document_type, template_type, owner, updated, and links keys remain forbidden
where no real consumer exists.

The following interpretation rules apply:

- artifact_type describes the document role, never the template source.
- parent_ids contains direct upstream identities with set-like meaning.
- Parent serialization is deterministic and does not assign approval rank,
  chronology, dependency strength, or semantic priority.
- supersedes appears only for a proven replacement relationship.
- reviewed_at and review_cycle appear only where the profile and actual review
  evidence justify them.
- Template-source draft status does not determine an instantiated target's
  lifecycle.
- Typed leaf template sources carry the target profile keys with registered
  placeholders. The README source carries source-only draft metadata that is
  removed unless the selected README profile permits a consumed field.
- Governance Memory and Progress forms carry layer: agentic and source draft
  status so their instantiated targets match the governance consumer contract
  without gaining artifact identity keys.
- The Archive source retains the documented draft-source exception while an
  instantiated tombstone must use archived status and complete provenance.
- Task row state, incident response state, release event state, and common
  document lifecycle are distinct dimensions. They remain in role-specific
  body sections unless a later approved consumer contract requires a key.
- Spec child roles retain artifact_type spec and are derived from exact target
  paths. No duplicate template_type field is introduced.
- Governance and repository-native documents use their real consumer contract
  rather than receiving SDLC metadata for visual consistency.

## Interfaces and Data

The registry will add exact machine-readable template-role and body-envelope
data. Each role defines:

- canonical source path;
- target path matcher;
- target artifact profile;
- required, conditional, and forbidden headings;
- valid parent relationships;
- placeholder forms;
- source and target validation behavior.

Ambiguous role matches fail closed. Conditional headings do not become required
merely because they exist in a template. A target may omit a conditional
section only when the concern is genuinely inapplicable.

Each Markdown template contains only:

1. profile-compatible frontmatter placeholders;
2. one H1;
3. role-specific body sections;
4. explicit replacement placeholders;
5. one Related Documents section.

Template sources will not contain Rules blocks, target numbering policy,
language policy, fixed-depth link examples, selection guidance, lifecycle
algorithms, migration instructions, or executable-looking sample commands.
Instantiated documents fail validation if they retain unresolved placeholders,
template instructions, or template-only comments.

The executable repository gate no longer requires Target comments. It rejects
template-only Target comments on newly introduced target content while
preserving base-existing body deficits until the bounded direct-consumer
migration in Task 7. This validator unit removes the transitional comments
from Spec 130 and its active Plan and Task atomically with retiring the old
shell-owned requirement.

Machine-readable OpenAPI, GraphQL, and Protobuf templates use explicit
unresolved tokens instead of valid-looking Example names, example.com hosts,
JWT values, or plausible fields. Their syntax and replacement contract are
validated without adding Markdown frontmatter.

## Core Design

The core design applies the canonical ownership and metadata contracts through
role-specific template consolidation, iterative stage gates, executable
validation, and dependency-ordered migration waves.

## Template Consolidation Decisions

### README

The common README template becomes one bounded base form with Overview,
Audience, Scope, Structure, How to Work in This Area, and Related Documents.
The 17 path profiles and their allowed variations remain in the registry and
README contract. The current rulebook, snippet library, lifecycle guidance,
script policy, traceability policy, and agent guardrails are removed from the
copyable source.

The six template-tree catalog README files that do not satisfy the registered
template-catalog heading envelope will be corrected without adding shared
governance prose.

### Audit and Reference

Audit receives a distinct audit.template.md because it owns criteria, scope,
evidence, findings, severity or priority, comparison, and disposition.
Reference retains stable facts, definitions, sources, maintenance, and
supporting context. Stage 00 and Stage 99 routing will no longer map audits to
the Reference form.

### Task and Harness Task

The duplicate Harness Task template is removed. Its unique protected-surface,
approval, validation, secret, Compose, operations, rollback, and evidence
concerns become conditional sections of the one Task form. Authoring rules and
suggested document-type lists move to support governance.

### Governance Memory

The duplicate Stage 00 memory template mirror is removed. All consumers link
to the Stage 99 memory template. Governance metadata wording is reconciled with
the registry and current consumer behavior.

### Depth-safe Links

Reference and Archive forms stop publishing fixed-depth relative examples for
arbitrarily deep targets. Related Documents uses explicit target-relative
placeholders that must be resolved at instantiation.

## Stage 01 Through Stage 03 Contract

The numbered stages are traceable gates with feedback, not a fixed waterfall.
Within the existing lifecycle, active means reviewed and currently effective.

### PRD

PRD owns the problem, stakeholders, value, scope, requirements, constraints,
acceptance criteria, success measures, provenance, and verification intent.
Requirement identities live in the body and remain stable across downstream
links. PRDs may have no parent.

### ARD

ARD owns the system of interest, stakeholders, concerns, boundaries, quality
attributes, viewpoints and views, data and infrastructure context, constraints,
and requirement traceability. Overview and Summary are consolidated. Individual
architecture choices remain in ADRs.

### ADR

ADR owns one significant decision. Its body distinguishes context and drivers,
considered options, the decision, consequences, and confirmation. A later ADR
uses supersedes rather than rewriting the old decision.

### Spec and Children

Spec owns implementable contracts, core design, interfaces, failure modes,
guardrails, and verification. Verification commands and acceptance meaning are
one coherent section rather than duplicated Verification and Success Criteria
sections.

API, Agent, Data, Service, and Test child documents own separately reviewable
details. When a child exists, the parent retains only a summary, ownership
boundary, and link. Exact child roles are derived from target paths while their
artifact type remains spec.

Before execution, validation checks parent relationships, cross-artifact
consistency, orphaned requirements, and unresolved decisions.

## Stage 04 Execution Contract

Plan is prospective. It converts an active Spec into implementation sequence,
scope, dependencies, verification strategy, risk controls, rollback, and
completion criteria.

Task is evidentiary. It records what was attempted, changed, approved,
validated, reviewed, committed, deferred, failed, or blocked. Its conditional
harness evidence includes:

- allowed and forbidden paths;
- protected-surface approval;
- Compose, security, operations, and runtime impact;
- validator and test commands with results;
- controlled agent pre-commit wrapper evidence;
- implementation review, specification review, and quality review;
- logical commit ledger;
- unresolved findings and follow-up routing.

Plan expectations do not substitute for Task execution evidence. The Task
template removes Suggested Types and similar authoring-rule sections.

## Stage 05 Operations Contract

### Guide

Guide explains usage context and routine operation. Routine task steps are
allowed, but incident recovery, rollback, and escalation procedures belong in a
Runbook.

### Policy

Policy defines required and prohibited controls, scope, exception authority,
verification intent, and review cadence. It does not own product-specific
command sequences.

### Runbook

Runbook defines trigger, prerequisites, safety conditions, ordered steps,
expected results, verification, evidence, one rollback or recovery section,
and escalation. Repeated deterministic procedures are automation candidates;
the Runbook keeps invocation, judgment, and recovery boundaries.

Actual test evidence is recorded in a Verification Record with environment,
command or procedure, result, and evidence location. reviewed_at does not
pretend to be a last-tested timestamp.

### Incident

Incident records impact, severity, leadership, timeline, actions, current
response state, evidence, mitigation, resolution, and handoff. Because an
incident can occur before a Runbook exists, an empty parent list is allowed.
Applicable Runbooks are linked when available.

### Postmortem

Postmortem directly parents the Incident and owns factual, blameless root cause
and contributing-factor analysis, lessons, reviewed action items, owners,
priority, tracking identities, prevention, and feedback to requirements,
architecture, specifications, policies, and Runbooks.

### Release

Release records a real event only. It requires parent Spec, Plan, or Task
evidence and records immutable identity, version or tag and commit, artifacts,
validation, approvals, compatibility, rollout, rollback, outcome, and known
issues. A readiness checklist, changelog entry, successful build, or template
does not manufacture a Release record.

## Feedback and Traceability

The primary forward path is:

PRD to ARD and ADR to Spec and child contracts to Plan and Task evidence to
Release and operations.

Operations provides explicit feedback:

- incidents and postmortems can create or revise requirements;
- findings can supersede architecture decisions;
- operational evidence can revise Specs and tests;
- repeated procedure failures can revise Policy and Runbook;
- release outcomes can create follow-up Plans and Tasks.

Relationships are linked in both upstream and downstream owners. Requirements
are referenced by stable identity rather than copied into a separate matrix as
competing truth.

## Immediate Implementation Boundary

This branch implements:

- Stage 99 registry and support reconciliation;
- copyable Markdown and machine-readable template normalization;
- the Audit template and Task consolidation;
- Stage 00 memory mirror removal and direct reference repair;
- six template catalog README corrections;
- template-role, body-envelope, target-matcher, placeholder, README heading,
  Release inventory, and machine-template validation;
- preservation-oriented review of the 17 fully typed Spec, Plan, and Task
  documents and only the direct changes required by the new contracts;
- source rationale and canonical inventory refresh;
- this Spec, its Plan and Task, and explicit follow-up batch routing.

This branch does not infer new content merely to make an old document resemble
a template. Topic-specific body changes require evidence and an approved edit
boundary.

Task 6 implementation is **In Review**. The executable body and machine-template
contracts, changed-target gate, and Python-owned shell delegation are locally
verified; independent specification and quality reviews have not yet run.

## Follow-up Migration Batches

| Batch | Scope | Rule |
| --- | ---: | --- |
| A | 89 active PRD, ARD, ADR, Spec, and Plan documents | Establish the parent graph first, then migrate by complete design chain. |
| B | 66 Guides, 64 Policies, and 61 Runbooks | Migrate by operations domain; review metadata requires actual review evidence. |
| C | 229 completed and one superseded document | Preserve bodies and dated evidence; apply only minimum metadata and cross-link repair. |
| D | Five Archive tombstones with provenance deficits | Confirm origin, reason, date, and replacement before editing. |
| E | Six generated documents | Refresh through the canonical generator only. |

README files remain profile-driven. Only directly affected catalogs and links
change here.

## Verification

The implementation adds or extends checks for:

- duplicate, forbidden, missing, mistyped, or misordered frontmatter keys;
- invalid artifact types, values, transitions, direct parent types, or orphan
  parent identities;
- ambiguous or missing template-role matches;
- required, conditional, and forbidden body headings;
- unresolved placeholders, copied authoring instructions, and template-only
  comments in targets;
- valid-looking unresolved values in machine-readable templates;
- stale references to removed templates and mirrors;
- template-catalog README heading envelopes;
- required-template inventory completeness, including Release;
- generated inventory drift;
- cross-stage traceability and documentation-to-implementation alignment.

Conditional section absence, preserved historical structure, and unapproved
follow-up batches remain advisory. A missing review date or parent identity is
reported; it is never guessed.

## Failure Modes and Guardrails

At minimum, implementation evidence includes:

- metadata validator unit and integration tests;
- repository contract checks;
- document traceability and implementation-alignment checks;
- YAML, OpenAPI, GraphQL, and Protobuf syntax or fixture validation as
  applicable;
- reference search and broken-link review after deletions or moves;
- generated inventory refresh and check mode;
- diff hygiene and independent per-task reviews;
- graphify update after code changes when the CLI is available.

The final all-files gate uses only
scripts/validation/run-agent-precommit-all-files.sh from a clean isolated
worktree. Agents must not invoke pre-commit run --all-files directly. The Task
records the wrapper command, allowed prefixes, exit status, before and after
path sets, hook-managed changes, and disposition.

## Subagent-Driven Implementation

Implementation runs in an isolated worktree on a codex-prefixed branch. Seven
logical tasks are executed sequentially:

1. Registry and support contracts.
2. Common, README, and governance templates.
3. Stage 01 through Stage 03 templates.
4. Stage 04 Plan and Task system.
5. Stage 05 operations templates.
6. Validators, tests, and QA contracts.
7. Fully typed chain, direct fallout, generated evidence, and follow-up batch
   plans.

Each task receives a fresh implementation agent. A separate specification
review agent checks the completed work before a separate quality review agent.
Review findings are fixed and re-reviewed before the logical task commit. A
fresh final reviewer audits the entire branch before closure.

## Rollback

- Revert logical commits in reverse dependency order.
- Restore validator behavior before restoring template sources that depend on
  it.
- Restore deleted mirror or specialized template paths only together with
  their references and ownership contracts; do not leave two canonical owners.
- Regenerate derived inventory after any registry rollback.
- Do not roll back by rewriting historical evidence or inventing replacement
  records.
- If the controlled pre-commit wrapper changes files outside approved prefixes,
  stop, preserve the evidence, and inspect the unexpected paths before any
  cleanup.

## Success Criteria & Verification Plan

- SC-TCS-001: Every Stage 99 support concern has one named canonical owner.
- SC-TCS-002: Every copyable template is form-only and has one deterministic
  role or explicit catalog exception.
- SC-TCS-003: No template or target contains a legacy generic metadata key.
- SC-TCS-004: Audit and Reference have distinct roles and copyable forms.
- SC-TCS-005: Generic Task and Harness Task no longer compete for the same
  target.
- SC-TCS-006: README profiles remain exact-one and template catalogs satisfy
  their registered heading envelope.
- SC-TCS-007: ARD, Spec, Runbook, Incident, and Postmortem duplicate-purpose
  sections are consolidated without losing role-specific evidence.
- SC-TCS-008: Stage 01 through Stage 05 forward and feedback traceability is
  represented in contracts, templates, and validator fixtures.
- SC-TCS-009: The 17 fully typed direct consumers remain valid without broad
  historical body rewrites.
- SC-TCS-010: The remaining corpus is represented by bounded, reproducible
  migration batches.
- SC-TCS-011: Repository contract, metadata, traceability, alignment, template,
  and relevant syntax tests pass.
- SC-TCS-012: The controlled final QA wrapper passes from a clean isolated
  worktree with Task evidence and no unexpected path changes.
- SC-TCS-013: Independent per-task and whole-branch reviews report no unresolved
  blocking finding.
- SC-TCS-014: No runtime, secret, deployment, remote GitHub, or global provider
  state changes.

## Related Documents

- [Spec 129: Document Contract Canonicalization](../129-document-contract-canonicalization/spec.md)
- [Agent Governance PRD](../../01.requirements/024-agent-governance-standardization.md)
- [Agent Governance ARD](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- [ADR-0027: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Stage 99 template system](../../99.templates/README.md)
- [Metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Template contract](../../99.templates/support/template-contract.md)
- [Template governance](../../99.templates/support/template-governance.md)
- [SDLC document contract](../../99.templates/support/sdlc-document-contract.md)
- [Common document contract](../../99.templates/support/common-document-contract.md)
