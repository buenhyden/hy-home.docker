---
status: active
artifact_id: audit:agentic-engineering-implementation:frontmatter-template-readme
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
reviewed_at: 2026-07-12
review_cycle: per-remediation-task
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md -->

# Reference: Frontmatter, Template, and README Implementation Audit

## Overview

This reference records the current implementation state of document
frontmatter, type profiles, templates, lifecycle meaning, README exceptions,
and generated-document ownership. It reassesses all DML criteria after
T-AER-008 and T-AER-012 while separating changed/new enforcement from the
advisory historical-corpus inventory.

## Purpose

Document the implemented typed-metadata contract and its enforcement boundary
without presenting the advisory historical inventory as a completed corpus-wide
migration.

## Repository Role

Stage 00 and Stage 99 remain the active contract owners. This report is an
advisory Stage 90 audit. The Stage 99 metadata profiles and
`check-document-metadata.py` enable typed keys and semantic checks for migrated
and changed/new documents; they do not rewrite historical frontmatter or turn
the full advisory inventory into a blocking gate.

## Scope

### In Scope

- Top-frontmatter syntax, allowed status values, and legacy key signals
- Artifact-type semantics, direct parents, supersession, freshness, and transitions
- README and generated-document exceptions
- Current typed profiles, validator enforcement, and advisory inventory boundary

### Out of Scope

- Further schema/profile expansion or historical-corpus migration
- Treating current filesystem paths or modification times as lifecycle evidence
- Hand-editing generator-owned outputs

## Definitions / Facts

- **Syntactically valid** means a non-README target-stage leaf has top YAML
  frontmatter with one allowed status word.
- **Semantically correct** means the value and keys fit the inferred artifact
  type, current role, parents, replacement, review evidence, and transition history.
- **Type-inappropriate key** is a key present where its profile forbids it;
  the pre-remediation generic-key scan is historical context, while current
  profile enforcement is defined by the Stage 99 metadata profiles.
- **README exception** means role is normally derived from path, heading, and
  folder-index behavior rather than copied leaf lifecycle metadata.

## Historical Syntax Baseline and Current Semantic Boundary

The pre-remediation syntax results were reproduced at baseline
`e4c92fa1e0e4e59af20efa9f1fcb104e3a8698eb` on 2026-07-11.

| Check | Result | Syntax conclusion | Semantic limitation |
| --- | --- | --- | --- |
| `git ls-files 'docs/**/*.md' \| wc -l` | 872 | Current docs-only corpus scope is reproducible. | It is not the same scope as the dated repo-wide 930/948 snapshots. |
| Allowed-status `rg -l` over Stage 01/02/03/04/05/90/98 | 635 | Exact Task 4 command result. | Body examples can match `rg`; top-frontmatter parsing is the authoritative breakdown. |
| Top-frontmatter parse for Stage 01/02/03/04/05/90/98 | 366 active, 240 completed, 9 superseded, 20 archived; total 635 | Every one of 598 non-README leaves has an allowed top status; 37 READMEs also carry status. | Valid vocabulary does not prove currentness or a legal transition. |
| README inventory in the brief's Stage 01-05/90/98/99 scope | 140 total; 37 with status and 103 without | No README has copied `status: draft`. | No explicit consumer/profile matrix currently explains each status-bearing README. |
| Pre-remediation proposed and legacy key scan | 0 occurrences of `artifact_id`, `artifact_type`, `parent_ids`, `supersedes`, `reviewed_at`, `review_cycle`, `type`, `owner`, `updated`, `links`, `document_type`, or `template_type` at column 1 under `docs` | This is preserved dated baseline evidence, not current implementation state. | Current migrated documents and profiles now use the typed keys. |
| Generated metadata | 6 tracked Stage 90 outputs have generator-owned `generated_by` plus generator-emitted `status: active` | Generator ownership is explicit for these outputs. | Freshness comes from canonical generator check/write modes, not human status edits. |
| Superseded documents | 9 | Manual review found a current replacement route in every body. | No validator prevents a future replacement-free supersession or proves direction/transition history. |
| Top fence in `docs/**/*.md` | 778/872 | Frontmatter is common. | The 94 without a top fence include profiles where lifecycle metadata is not required; absence alone is not a defect. |

The 2026-07-03 report's 930 tracked Markdown / 745 top-frontmatter / 185
missing snapshot and the 2026-07-04 report's 948 / 764 / 184 snapshot remain
dated repo-wide evidence. They are not current implementation counts.

The Spec 129 foundation is later current-state evidence, not a rewrite of those
snapshots. The registry now classifies all 231 tracked READMEs through 17
non-overlapping profiles and fails closed on zero or multiple matches; the 37
status-bearing READMEs in the preserved audit baseline still await the next
migration wave. Frontmatter and multiple-parent order are deterministic
serialization only, never semantic priority. Release now has a distinct profile,
checker route, copyable template, selection route, and Stage 05 index, while no
Release event record exists.

T-AER-008 implemented machine-readable profiles, a deterministic manifest and
checker, active-chain migration, changed/new blocking selection, transition
overrides, and focused tests. T-AER-012 then hardened deletion, identity-change,
explicit-base decoding, and referential-integrity behavior. The generated full
inventory remains advisory for historical findings; only the safe changed/new
and impacted-dependent selection is blocking.

## Audit Criterion Records

| Criterion ID | External criterion | Workspace evidence | Implementation state | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DML-01 | Give every migrated leaf a stable identifier independent of path and heading. | T-AER-008 migrated the approved active chain to unique `artifact_id` values; the deterministic manifest rejects duplicates, and T-AER-012 covers rename and identity-change impact. | Implemented | 3 | Retain | Stage 99 metadata profiles and checker owner | Retain manifest, duplicate-ID, rename, and identity-change tests for migrated/changed documents. | Run focused metadata tests and changed/new checks from T-AER-008/012. | High for the enforced scope; no full historical-corpus migration claim. |
| DML-02 | Apply required/optional/forbidden metadata through artifact-type profiles, not one universal key list. | `document-metadata-profiles.yaml` defines machine-readable required, optional, and forbidden keys by inferred artifact type, including README, generated, governance, template, archive, and unsupported exceptions. | Implemented | 3 | Retain | Stage 99 metadata profiles | Retain profile-specific validation and fixtures instead of introducing a universal key list. | Run the metadata profile unit suite and changed/new checker. | High. |
| DML-03 | Record only direct upstream artifact IDs as resolvable parents, with deterministic multiple-parent handling. | Migrated documents use `parent_ids`; the checker builds a deterministic ID manifest and enforces resolvable direct parents, permitted roots, serialization order, self-reference, and cycles. Serialization follows registry type precedence and artifact ID only to stabilize presentation; list position never assigns semantic priority. T-AER-012 hardens impacted dependents across deletion and identity changes. | Implemented | 3 | Retain | Metadata checker and stage owners | Retain relation, serialization, and referential-integrity fixtures for current, staged, and explicit-base changes without adding priority semantics. | T-AER-008/012 focused tests plus Spec 129 parent-order fixtures and changed/new validation. | High for migrated/changed and impacted-dependent scope. |
| DML-04 | Express replacement explicitly and preserve supersession direction. | Typed profiles support `supersedes`; the checker resolves replacement IDs and validates lifecycle/type direction, while human replacement links remain readable. | Implemented | 3 | Retain | Metadata checker and Stage 04 owner | Retain replacement-direction, missing-target, and dependent-impact fixtures. | Metadata semantic tests and T-AER-012 referential-integrity checks. | High for typed changed/new scope. |
| DML-05 | Make `reviewed_at` and `review_cycle` type-dependent evidence-backed freshness fields. | Stage 99 profiles require, allow, or forbid `reviewed_at` and `review_cycle` by artifact type; changed/new validation checks values without using filesystem mtime as review proof. | Implemented | 3 | Retain | Artifact owners and Stage 99 profiles | Retain type-specific freshness validation; keep historical inventory findings advisory. | Profile tests and changed/new checker from T-AER-008. | High for enforced changed/new scope. |
| DML-06 | Keep PRD/Spec, ARD/ADR, dated Plan/Task, and tier numbering type-specific and separate from lifecycle identity. | All scanned PRD/ARD/ADR/Spec-folder/Plan/Task names conform; the typed `artifact_id` layer is separately validated without suffix unification. | Implemented | 3 automated/enforced for naming | Retain | Documentation protocol | Preserve type-specific naming and separate stable identity. | Reproducible filename scans, metadata checks, and repository contracts. | High. |
| DML-07 | Enforce forward transitions and keep superseded terminal and archived Stage 98-only after rollout. | The metadata contract separates status vocabulary from transitions, validates prior/current state for selected changes, keeps terminal states terminal, and restricts archived artifacts to Stage 98. | Implemented | 3 | Retain | Stage 99 lifecycle contract and checker owner | Retain forward, terminal, superseded, and archived-path fixtures. | Focused transition tests and changed/new validation from T-AER-008/012. | High for enforced changes. |
| DML-08 | Require approval, reason, previous state, and explicit override for reverse transitions. | The checker rejects reverse transitions unless the Stage 04-approved override input identifies the path, previous state, current state, reason, and approval evidence; T-AER-012 reclosure used four explicit overrides. | Implemented | 3 | Retain | Stage 04 task owner and metadata checker | Retain negative/positive override fixtures and require scoped task evidence. | T-AER-008 transition tests and T-AER-012 four-override validation. | High. |
| DML-09 | Derive README role from its profile unless a real metadata consumer is declared. | The registry defines 17 non-overlapping README profiles and the checker classifies all 231 tracked READMEs exactly once, keeps frontmatter absent by default, and exposes declared-consumer behavior. The preserved 37 status-bearing README baseline has not yet been migrated or individually reconciled. | Partial | 3 for classification; 2 for corpus adoption | Improve | Documentation protocol and README contract owners | Retain fail-closed exact-one profile selection and consumer fixtures; classify the 37 status-bearing files in the next approved README wave without bulk deletion or addition. | README profile/consumer unit tests, tracked-path coverage, and later migration manifest review. | High for the implemented foundation; Medium for individual legacy consumer intent. |
| DML-10 | Keep generated metadata and content generator-owned and freshness-checked. | Six outputs declare `generated_by`; canonical scripts provide write/check modes and repo contracts check freshness. | Implemented | 3 automated/enforced | Retain | Generator/script owner | Keep metadata emitted by generators; add no human typed keys outside generator changes. | Generator declarations, write/check commands, clean regenerated diff. | High. |
| DML-11 | Validate semantic profiles, relations, transitions, and replacements in addition to YAML syntax/vocabulary. | `check-document-metadata.py` parses typed profiles, builds the manifest, validates relations/replacements/lifecycle/freshness, emits the advisory inventory, and blocks safe changed/new plus impacted-dependent violations. | Implemented | 3 | Retain | Metadata checker owner | Retain focused semantic tests and repository-contract integration. | T-AER-008/012 metadata suites, inventory freshness, and changed/new checks. | High. |
| DML-12 | Keep Incident, Postmortem, Runbook, and Release as distinct type profiles. | Incident, Postmortem, Runbook, and Release have distinct registry profiles and checker routes. Release also has a copyable template, selection route, and Stage 05 index; no Release event record exists, and none is required merely to prove profile separation. | Implemented | 3 | Retain | Stage 99 registry/template and Stage 05 release owners | Retain distinct profile/template fixtures; create Incident, Postmortem, or Release leaves only from qualifying event evidence. | Metadata profile tests, all-template instantiation tests, Release route checks, and event-leaf inventory. | High. |
| DML-13 | Preserve stable criterion rows and evidence rather than a composite score. | Spec 123 defines ten fields; the canonical reports use one complete row per criterion, and the shared generator/parser emits all 161 unique rows from eleven criterion reports. | Implemented | 3 | Retain | Canonical audit pack owner | Keep row-level evidence canonical and generated matrix freshness enforced. | Run both audit scripts in check mode and confirm 11 reports / 161 unique rows. | High. |
| DML-14 | Roll out advisory-first, review false positives, then block changed/new documents only. | The deterministic full-corpus inventory remains advisory, while T-AER-008 migrated the approved active chain and enabled blocking changed/new selection; T-AER-012 added impacted-dependent referential-integrity hardening without promoting unrelated historical findings. | Implemented | 3 | Retain | Metadata program and checker owners | Retain advisory inventory plus changed/new and impacted-dependent blocking boundaries. | Inventory write/check, focused tests, and T-AER-008/012 task evidence. | High; full historical-corpus migration remains intentionally unclaimed. |

## Syntax Compliance Versus Semantic Correctness

| Surface | Syntax result | Current semantic result |
| --- | --- | --- |
| Leaf lifecycle status | The dated syntax baseline remains preserved; current typed profiles validate allowed status by artifact role. | Implemented for migrated/changed documents, including transition and explicit reverse-override rules; historical inventory findings remain advisory. |
| Supersession | Typed `supersedes` relations and terminal lifecycle rules are available. | Implemented for typed changed/new scope with replacement resolution/direction and referential-integrity impact checks. |
| Templates | Changed and normalized target documents retain mapped heading/literal checks. | Typed changed/new metadata additionally validates profile, identity, parents, freshness, and lifecycle; body truth still requires review. |
| README | The preserved baseline's mixed use conforms to the default exception better than a universal leaf rule; no draft copy was found. | Partial corpus adoption: exact-one profile classification and declared-consumer semantics are implemented for all tracked READMEs, while the 37 status-bearing baseline awaits migration review. |
| Generated outputs | Six current outputs are generator-owned and freshness-checked. | Implemented when regenerated canonically; human edits cannot establish freshness. |
| Generic keys | Typed keys are profile-governed and legacy duplicate-purpose keys are globally forbidden. | Implemented for the checker scope; advisory findings do not rewrite historical files. |

## Implemented Semantic Inventory and Enforcement Boundary

The advisory inventory produces one deterministic row per tracked target
document without printing secret values or raw body content. Each row records:

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

The report is stable across repeated runs, summarizes counts by profile and
finding, keeps per-row evidence, and changes no document automatically. The
blocking checker selects migrated/changed documents and impacted dependents;
unrelated historical findings remain advisory.

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
