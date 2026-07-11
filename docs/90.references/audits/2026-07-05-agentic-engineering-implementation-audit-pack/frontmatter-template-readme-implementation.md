---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md -->

# Reference: Frontmatter, Template, and README Implementation Audit

## Overview

This reference records the 2026-07-11 pre-remediation state of document
frontmatter, type profiles, templates, lifecycle meaning, README exceptions,
and generated-document ownership. It assesses all DML criteria from the
canonical Task 1 research and separates parseable syntax from semantic truth.

## Purpose

Provide Tasks 7 and 8 with a reproducible baseline and explicit semantic
inventory requirements before typed metadata or changed/new enforcement is
implemented.

## Repository Role

Stage 00 and Stage 99 remain the active contract owners. This report is an
advisory Stage 90 audit. It does not enable `artifact_id`, `artifact_type`,
`parent_ids`, `supersedes`, `reviewed_at`, or `review_cycle`; it does not
rewrite historical frontmatter or change any lifecycle state.

## Scope

### In Scope

- Top-frontmatter syntax, allowed status values, and legacy key signals
- Artifact-type semantics, direct parents, supersession, freshness, and transitions
- README and generated-document exceptions
- Current template/validator enforcement and Task 7/8 inventory requirements

### Out of Scope

- Schema, profile, parser, test, template, validator, or corpus remediation
- Treating current filesystem paths or modification times as lifecycle evidence
- Hand-editing generator-owned outputs

## Definitions / Facts

- **Syntactically valid** means a non-README target-stage leaf has top YAML
  frontmatter with one allowed status word.
- **Semantically correct** means the value and keys fit the inferred artifact
  type, current role, parents, replacement, review evidence, and transition history.
- **Type-inappropriate key** is a key present where its profile forbids it;
  absence from the current generic-key scan does not prove future typed profiles.
- **README exception** means role is normally derived from path, heading, and
  folder-index behavior rather than copied leaf lifecycle metadata.

## Reproducible Syntax Snapshot

All current results were reproduced at baseline
`e4c92fa1e0e4e59af20efa9f1fcb104e3a8698eb` on 2026-07-11.

| Check | Result | Syntax conclusion | Semantic limitation |
| --- | --- | --- | --- |
| `git ls-files 'docs/**/*.md' \| wc -l` | 872 | Current docs-only corpus scope is reproducible. | It is not the same scope as the dated repo-wide 930/948 snapshots. |
| Allowed-status `rg -l` over Stage 01/02/03/04/05/90/98 | 635 | Exact Task 4 command result. | Body examples can match `rg`; top-frontmatter parsing is the authoritative breakdown. |
| Top-frontmatter parse for Stage 01/02/03/04/05/90/98 | 366 active, 240 completed, 9 superseded, 20 archived; total 635 | Every one of 598 non-README leaves has an allowed top status; 37 READMEs also carry status. | Valid vocabulary does not prove currentness or a legal transition. |
| README inventory in the brief's Stage 01-05/90/98/99 scope | 140 total; 37 with status and 103 without | No README has copied `status: draft`. | No explicit consumer/profile matrix currently explains each status-bearing README. |
| Proposed and legacy key scan | 0 occurrences of `artifact_id`, `artifact_type`, `parent_ids`, `supersedes`, `reviewed_at`, `review_cycle`, `type`, `owner`, `updated`, `links`, `document_type`, or `template_type` at column 1 under `docs` | No current proposed-key partial rollout or generic duplicate-purpose key signal. | A zero text match is not type inference, parent resolution, freshness, or transition validation. |
| Generated metadata | 6 tracked Stage 90 outputs have generator-owned `generated_by` plus generator-emitted `status: active` | Generator ownership is explicit for these outputs. | Freshness comes from canonical generator check/write modes, not human status edits. |
| Superseded documents | 9 | Manual review found a current replacement route in every body. | No validator prevents a future replacement-free supersession or proves direction/transition history. |
| Top fence in `docs/**/*.md` | 778/872 | Frontmatter is common. | The 94 without a top fence include profiles where lifecycle metadata is not required; absence alone is not a defect. |

The 2026-07-03 report's 930 tracked Markdown / 745 top-frontmatter / 185
missing snapshot and the 2026-07-04 report's 948 / 764 / 184 snapshot remain
dated repo-wide evidence. They are not current implementation counts.

## Audit Criterion Records

| Criterion ID | External criterion | Workspace evidence | Implementation state | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DML-01 | Give every migrated leaf a stable identifier independent of path and heading. | No `artifact_id` exists; identity is currently path/number based. | Missing | 0 absent | Add | Stage 99 metadata profiles | Candidate deterministic manifest, duplicate-ID check, and rename fixture. | Current key scan; later manifest tests. | High. |
| DML-02 | Apply required/optional/forbidden metadata through artifact-type profiles, not one universal key list. | Path-derived roles and template mappings exist, but no machine-readable typed profile matrix exists. | Partial | 1 documented | Add | Stage 99 metadata profiles | Add one profile per supported type, including README/generated exceptions and N/A rules. | Stage 99 contract review; later profile tests. | High. |
| DML-03 | Record only direct upstream artifact IDs as resolvable parents, with deterministic multiple-parent handling. | Human `Related Documents` and traceability checks exist; no `parent_ids`, ID resolver, permitted-root rule, missing-parent diagnostic, or cycle check exists. | Partial | 2 partially applied through links | Add | Metadata validator and stage owners | Candidate manifest resolution, allowed-root checks, deterministic ordering, and cycle fixtures. | Link-signal inventory and traceability scope now; parser tests later. | High. |
| DML-04 | Express replacement explicitly and preserve supersession direction. | Nine current superseded docs all point to replacements in their bodies; no `supersedes` key or semantic validator exists. | Partial | 1 documented/manual | Add | Stage owner plus Stage 04 task | Validate replacement IDs, old/new state coherence, and direction; retain human replacement link. | Manual superseded-body scan; later replacement fixtures. | High. |
| DML-05 | Make `reviewed_at` and `review_cycle` type-dependent evidence-backed freshness fields. | Neither key exists. Body maintenance sections express cadence on many references, policies, and runbooks, but no common review-evidence validator exists. | Partial | 1 documented/manual | Improve | Artifact owner and Stage 99 profiles | Add only to freshness-managed types; require review result/evidence, not mtime. | Key scan and maintenance-section review; later profile fixtures. | High for absence; Medium for which individual artifacts need cadence. |
| DML-06 | Keep PRD/Spec, ARD/ADR, dated Plan/Task, and tier numbering type-specific and separate from lifecycle identity. | All scanned PRD/ARD/ADR/Spec-folder/Plan/Task names conform; no stable identity layer exists. | Implemented | 3 automated/enforced for naming | Retain | Documentation protocol | Preserve naming; introduce identity without suffix unification. | Reproducible filename scans and repository contracts. | High. |
| DML-07 | Enforce forward transitions and keep superseded terminal and archived Stage 98-only after rollout. | Vocabulary/path rules exist; current 20 archived statuses are Stage 98-only and 9 superseded bodies have replacements. Transition history is not checked. | Partial | 1 documented | Add | Stage 99 lifecycle contract | Add before/after transition fixtures and terminal-state validation in staged rollout. | Current status/path scan; later transition tests. | High. |
| DML-08 | Require approval, reason, previous state, and explicit override for reverse transitions. | Stage 04 evidence can record approvals, but no reverse-transition representation or validator exists. | Missing | 0 absent | Add | Stage 04 task owner | Add override input/evidence contract and negative fixtures; never infer approval from a valid word. | Contract review now; tests later. | High. |
| DML-09 | Derive README role from its profile unless a real metadata consumer is declared. | 140 scoped READMEs; 37 status-bearing and 103 status-free; no copied `status: draft`; current contracts allow profile exceptions. | Partial | 2 documented/profile-dependent | Improve | Documentation protocol owner | Add explicit README profile inference and consumer exception tests; do not bulk-delete or add status. | Path/top-frontmatter inventory and README template review. | High for counts; Medium for individual consumer intent. |
| DML-10 | Keep generated metadata and content generator-owned and freshness-checked. | Six outputs declare `generated_by`; canonical scripts provide write/check modes and repo contracts check freshness. | Implemented | 3 automated/enforced | Retain | Generator/script owner | Keep metadata emitted by generators; add no human typed keys outside generator changes. | Generator declarations, write/check commands, clean regenerated diff. | High. |
| DML-11 | Validate semantic profiles, relations, transitions, and replacements in addition to YAML syntax/vocabulary. | Repository contracts parse headings/frontmatter and enforce templates/links, but no typed semantic metadata parser exists. | Missing | 0 absent for the proposed semantics | Add | Metadata validator owner | Task 7 parser/profile/manifest/transition tests; advisory report first. | Validator source review and current checks; later unit suite. | High. |
| DML-12 | Keep Incident, Postmortem, Runbook, and Release as distinct type profiles. | Incident/Postmortem/Runbook templates or roles are distinct; 61 Runbooks exist and zero event-driven incident leaves exist. Release is only changelog communication plus manual runbook; no Release profile/record exists. | Partial | 2 partially applied | Add | Stage 05 and release owners | Add distinct typed profiles; do not conflate event absence with failure or runbook execution with a Release record. | Template/path/release-surface inventory. | High. |
| DML-13 | Preserve stable criterion rows and evidence rather than a composite score. | Spec 123 defines ten fields; the canonical reports use one complete row per criterion, and Task 6 generates all 161 unique rows from eleven criterion reports. | Implemented | 3 | Retain | Canonical audit pack owner | Keep row-level evidence canonical and generated matrix freshness enforced. | Run both audit scripts in check mode and confirm 11 reports / 161 unique rows. | High. |
| DML-14 | Roll out advisory-first, review false positives, then block changed/new documents only. | Spec 123 and the plan mandate advisory-first rollout; current historical corpus is not typed and no blocking metadata validator exists yet. | Partial | 1 approved/documented | Improve | Metadata program owner | Task 7 generates advisory inventory/tests; Task 8 migrates the approved chain and adds changed/new enforcement. | Approved spec/plan and later task evidence. | High. |

## Syntax Compliance Versus Semantic Correctness

| Surface | Syntax result | Semantic result before remediation |
| --- | --- | --- |
| Leaf lifecycle status | Complete for all 598 Stage 01/02/03/04/05/90/98 non-README leaves. | Partial: staleness, transition history, reverse approval, and entry/exit completion are not machine-validated. |
| Supersession | Allowed vocabulary and current bodies are manually coherent for all nine cases. | Partial: replacement resolution/direction and terminal transitions are not enforced. |
| Templates | Changed and normalized target documents have mapped heading/literal checks. | Partial: template shape cannot prove correct role choice, necessary parents, current facts, or valid N/A. |
| README | Current mixed use conforms to the default exception better than a universal leaf rule; no draft copy was found. | Partial: no explicit typed consumer matrix classifies the 37 status-bearing indexes. |
| Generated outputs | Six current outputs are generator-owned and freshness-checked. | Implemented when regenerated canonically; human edits cannot establish freshness. |
| Generic keys | No current duplicate-purpose key signal. | Not evidence that the proposed typed keys are implemented or semantically valid. |

## Required Task 7/8 Semantic Inventory

The advisory inventory must produce one deterministic row per tracked target
document without printing secret values or raw body content. At minimum, each
row needs:

| Field | Required behavior |
| --- | --- |
| Path and inferred profile | Infer PRD, ARD, ADR, Spec/support contract, Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, Release, Reference, Audit, Archive, README, generated, or explicit unsupported profile. |
| Frontmatter parse result | Distinguish missing fence, malformed YAML, duplicate key, allowed syntax, and profile-semantic error. |
| Identity | Report missing, valid, or duplicate `artifact_id`; resolve through a deterministic manifest. |
| Relations | Resolve direct `parent_ids` and `supersedes`; report missing target, wrong root/type, nondeterministic order, self-reference, and cycle. |
| Lifecycle | Report current status, profile-allowed states, stale-active signal, replacement-free supersession, archived-outside-Stage-98, and transition-evidence availability. |
| Freshness | Report whether review fields are required/optional/forbidden and whether evidence-backed dates/cadence exist; never use mtime as proof. |
| README/generated exception | Record profile reason and consumer/generator owner; flag copied leaf keys or human edits to generator-owned fields. |
| Type-inappropriate keys | Evaluate required/optional/forbidden per profile, including generic `type`, `owner`, `updated`, `links`, `document_type`, and `template_type`. |
| Enforcement disposition | Advisory-only, migration candidate, changed/new blocking candidate, generated exception, README exception, justified N/A, or separately approved historical cleanup. |

The report must be stable across repeated runs, summarize counts by profile and
finding, keep per-row evidence, and avoid changing any document automatically.
Task 8 may block only the approved migrated chain and changed/new documents
after false-positive review.

## Source Rules

- Current counts come from tracked files at the stated baseline.
- Graphify's `30df271a` report is stale and advisory; it was not used as proof.
- The DML criteria come from primary-source-backed Task 1 research, but active
  schema ownership remains Stage 00/99 and approved Stage 04 work.
- Historical 930/948 counts remain dated evidence with their original scopes.

## Sources

- [Document metadata and lifecycle criteria](../../research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md) - DML-01 through DML-14
- [SDLC document roles](../../research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md) - artifact-type boundaries
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - current key/profile and README/generated rules
- [Lifecycle status](../../../99.templates/support/lifecycle-status.md) - current status vocabulary and replacement requirement
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - target-stage status, template, and numbering rules
- [Reference template](../../../99.templates/templates/common/reference.template.md) - active report profile
- [2026-07-03 frontmatter inventory](../2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md) - dated syntax baseline
- [2026-07-04 frontmatter profile inventory](../2026-07-04-document-restructure-audit-contract-archive/frontmatter-profile-inventory.md) - dated profile baseline

## Maintenance

- **Owner**: Documentation Specialist / Metadata program owner
- **Review Cadence**: Reproduce before metadata profile, validator, or changed/new enforcement changes
- **Update Trigger**: Frontmatter, template, README, generator, identity, relation, freshness, or lifecycle semantics change

## Related Documents

- [Audit pack README](./README.md)
- [SDLC and document-contract audit](./sdlc-document-contracts-implementation.md)
- [SDLC quality and formatting summary](./sdlc-quality-formatting-implementation.md)
- [Implementation overview](./implementation-overview.md)
- [Spec 123](../../../03.specs/123-agentic-engineering-audit-remediation/spec.md)
