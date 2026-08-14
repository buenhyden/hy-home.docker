---
status: draft
artifact_id: reference:agentic-engineering-research:document-metadata-lifecycle
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-14
review_cycle: on-source-change
---

# Reference: Document Metadata and Lifecycle

## Overview

Document lifecycle in this workspace is a typed application-profile system,
not a universal frontmatter convention. The Stage 99 registry binds a path and
role to required/optional/forbidden keys, direct-parent types, headings,
template, lifecycle values, transition rules, and explicit exceptions.
Human-readable contracts explain intent; the metadata checker interprets the
machine contract.

This analysis was re-derived at HEAD `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`
(2026-08-14), superseding the Task 5 baseline
`0445a17860ac27f6bf5ff1f9a8ffcde32bc4f2ee` previously cited. It separates
current-path counts, frontmatter states, typed migration depth, template
sources, generated outputs, README exceptions, and archive tombstones so none
is mistaken for another.

## Purpose

Explain how identity, type, parents, supersession, freshness, status, templates,
validation, migration exceptions, archive provenance, and retention signals
work together. Identify which parts are executable today and which remain
unexercised or legacy-partial without proposing changes to the contracts.

## Repository Role

This Stage 90 reference is advisory. The sole machine-readable owner is
`docs/99.templates/support/document-metadata-profiles.yaml`; exact transition
and exception behavior is enforced by
`scripts/validation/check-document-metadata.py`. Stage 00 governs approval and
authoring, Stage 99 owns template/profile semantics, Stage 04 records evidence,
and Stage 98 preserves tombstones. This document cannot authorize a metadata
change, lifecycle transition, corpus migration, archive action, or generated
refresh.

## Scope

### In scope

- Typed frontmatter roles and direct relation semantics.
- Current lifecycle vocabulary and transition boundary.
- Current active/archive/template measurements and legacy migration limits.
- README, governance, generated, template-source, and archive exceptions.
- Retention review signals and archive provenance boundaries.

### Out of scope

- Editing the registry, templates, validators, corpus, archive, or generators.
- Inferring metadata from naming resemblance or copying arrays from this leaf.
- Bulk normalization, reverse transitions, deletion, or archive promotion.
- Treating a freshness date, status, graph edge, or generated index as proof of
  current runtime behavior.

## Definitions / Facts

### Application-profile model

| Concern               | Canonical representation                                                      | Meaning and boundary                                                                                                                            |
| --------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Identity              | `artifact_id`                                                                 | Stable typed identity across links and approved moves; a filename/number alone is not a cross-stage key.                                        |
| Role                  | `artifact_type`                                                               | Selects one registered profile such as PRD, ADR, Spec, Task, Policy, Release, Reference, or Archive. Generic `type` aliases are forbidden.      |
| Direct parents        | `parent_ids`                                                                  | Evidence-backed direct upstream artifacts admitted by the child profile. Ordering is deterministic presentation, not priority or approval rank. |
| Replacement direction | `supersedes`                                                                  | Optional typed relation from current artifact to replaced identity where the profile admits it. It does not erase history.                      |
| Freshness             | `reviewed_at`, `review_cycle`                                                 | Profile-specific review evidence, not universal fields and not automatic truth.                                                                 |
| Lifecycle             | `status`                                                                      | Document-state vocabulary; body/event state remains separate for Incident and other operational records.                                        |
| Generation            | `generated_by`                                                                | Identifies a canonical generator where admitted; does not replace required lifecycle state or permit hand editing.                              |
| Archive provenance    | `archived_from`, `archived_on`, disposition, commit/blob, preservation fields | Exact source identity and recovery evidence for a tombstone; the removed body is not current guidance.                                          |

Every new target must resolve to exactly one profile and one mapped template.
Zero matches, overlapping matches, an unsupported path, or an unclear role is
blocking ambiguity. The author must not choose the nearest-looking profile or
manufacture a parent to satisfy a field.

### Current measured state

The following counts exclude `README.md` unless stated otherwise and were
derived from current canonical paths after the 2026-08-08 archive migration.
Re-verified directly with `find`/`grep` at the 2026-08-14 boundary: the Stage
01-05 and Stage 04 totals are now two leaves higher than the Task 5 baseline,
and the `draft` bucket that previously held 2 leaves is empty. Both movements
trace to the same cause: this deepening effort's own governing Task,
`docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md`
(`status: active`), is itself a Stage 04 leaf and entered the corpus already
`active`. The draft/completed split moves whenever any Task's own status
moves, including this pack's.

| Population                              | Count and state                                       | Typed-depth interpretation                                                                                                                                                                                                                                                                                                                |
| --------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 01-05 non-README leaves           | 533: 298 `active`, 235 `completed`, 0 `draft`         | All have lifecycle status, but many predate typed `artifact_id`/`artifact_type` migration. The `draft` bucket is transiently empty.                                                                                                                                                                                                       |
| PRD / ARD / ADR role paths              | 25 / 25 / 25                                          | Only one leaf in each family currently exposes its typed role; path counts and typed counts must not be conflated.                                                                                                                                                                                                                        |
| Parent Specs                            | 28 current, 32 archived                               | Current and archived Spec populations coexist; archive zero is obsolete.                                                                                                                                                                                                                                                                  |
| Stage 04 role paths                     | 103 Plans, 133 Tasks                                  | 16 Plans and 20 Tasks currently expose typed `artifact_type`; remaining legacy leaves retain changed-file exception constraints.                                                                                                                                                                                                          |
| Stage 05 role paths                     | 66 Guides, 64 Policies, 62 Runbooks                   | Current typed role coverage is 1 Guide, 1 Policy, and 2 Runbooks; current path remains the role evidence for legacy leaves.                                                                                                                                                                                                               |
| Incident / Postmortem / Release targets | 0 / 0 / 0                                             | Profiles/templates exist but no real target has exercised them. Unchanged since 2026-08-08; re-confirmed twice now.                                                                                                                                                                                                                       |
| Stage 98 non-README leaves              | 52, all `archived`                                    | 32 expose `artifact_type: archive`; 20 are legacy tombstones. Stage 98 total Markdown is 69 including navigation.                                                                                                                                                                                                                         |
| Stage 99 non-README Markdown            | 35                                                    | 24 declare template-source `status: draft`; support contracts are governance inputs rather than copyable lifecycle targets.                                                                                                                                                                                                               |
| Registered profile catalog              | 21 `profiles:` entries, 17 `readme_profiles:` entries | Directly re-counted from the registry's top-level keys: `prd, ard, adr, spec, plan, task, guide, policy, runbook, incident, postmortem, release, reference, audit, readme, repo-support, generated, template-source, governance, archive, unsupported` — 12 human SDLC roles plus 9 non-lifecycle governance/navigation/archive profiles. |

The historical corpus is intentionally not bulk-rewritten. A changed legacy
leaf outside the approved migration set may use the checker's legacy exception
only if it existed at the selected base, had no typed migration keys before or
after, and introduces no parser, forbidden-key, transition, or new typed-profile
error. New documents can never use that exception.

### SDLC profile differences

This table summarizes semantic differences; it does not replace the registry's
exact arrays or validation algorithm.

| Profile    | Required freshness                               | Direct-parent boundary                                                   | Notable lifecycle/relation rule                                         |
| ---------- | ------------------------------------------------ | ------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| PRD        | None                                             | Root; empty allowed                                                      | Product root may be draft/active/completed/superseded.                  |
| ARD        | None                                             | PRD                                                                      | Non-empty parent required.                                              |
| ADR        | None                                             | PRD or ARD                                                               | Preserve decision history; supersession is directional.                 |
| Spec       | None required; freshness optional                | PRD, ARD, ADR, Spec, or Archive                                          | Parent required; focused child contracts remain Spec family.            |
| Plan       | None                                             | PRD, ARD, ADR, Spec, or Archive                                          | Prospective artifact; parent required.                                  |
| Task       | None                                             | Spec, Plan, Task, or Archive                                             | Evidence artifact; parent required and historical results preserved.    |
| Guide      | Optional                                         | Spec, Plan, Task, or Policy                                              | Parent required; usage context links controls/procedures.               |
| Policy     | `reviewed_at` and `review_cycle` required        | PRD, ARD, ADR, Spec, Plan, or Task                                       | Periodically reviewed operational control.                              |
| Runbook    | `reviewed_at` and `review_cycle` required        | Spec, Plan, Task, Guide, Policy, or Archive                              | Periodically reviewed executable procedure.                             |
| Incident   | None                                             | Runbook; empty allowed                                                   | May be root if no verified Runbook parent; event state belongs in body. |
| Postmortem | `reviewed_at` required; `review_cycle` forbidden | Incident only                                                            | Strict child of paired Incident; reviewed learning is dated once.       |
| Release    | `reviewed_at` optional; `review_cycle` forbidden | Spec, Plan, or Task                                                      | Must be backed by a real release event; not deployment/runtime proof.   |
| Reference  | Both optional                                    | PRD/ARD/ADR/Spec/Plan/Task/Guide/Policy/Runbook/Reference; empty allowed | Advisory support role; cannot become policy or execution evidence.      |

The three research leaves in this pack set both reference freshness keys as a
pack convention. The reference profile permits but does not require them.

### Lifecycle states and transitions

| Status       | Human meaning                                                                       | Machine boundary                                                                |
| ------------ | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `draft`      | In-progress target or template source; not accepted current truth.                  | Ordinary forward transition is to `active`.                                     |
| `active`     | Current contract, guidance, reference, or working evidence.                         | May transition to `completed` or `superseded`.                                  |
| `completed`  | Finished execution/historical-but-valid evidence retained in its owning stage.      | May transition to `superseded`; age alone does not archive it.                  |
| `superseded` | Replaced artifact retained in the active chain with replacement direction/evidence. | Terminal in the common graph.                                                   |
| `archived`   | Stage 98/root archive tombstone after removal from the current chain.               | Archive-profile terminal state, not a status to assign to an active-stage leaf. |

```text
draft -> active -> completed -> superseded
                  \----------> superseded

archive requires a separately approved manifest/provenance path;
it is not an ordinary age-based status hop from the active chain
```

Reverse transitions require explicit scoped Stage 04 override evidence and
checker acceptance. Prose, an old timestamp, formatting cleanup, a copied
template, or an advisory review signal cannot authorize an exception.

### Template and heading lifecycle

- The registry maps each role to one copyable source, target glob, required and
  conditional headings, forbidden headings, and artifact profile.
- A template source stays `status: draft` because it is a form, not because a
  copied target must be draft. Authors replace every registered placeholder.
- Plan forbids execution-evidence headings; Task requires observed evidence and
  review/commit/deferral sections. This is a semantic separation, not style.
- Incident forbids root-cause/postmortem content; Postmortem forbids current
  response state. Guide, Policy, and Runbook likewise have disjoint procedure
  and control boundaries.
- Reference requires source-backed facts and forbids audit Findings; Stage 90
  still needs an explicit repository-role boundary in this pack.

### README, governance, generated, and native exceptions

README profiles are selected by path and consumer, not by copying the common
README template. Frontmatter is absent by default; only a matched profile with
a real consumer admits the registered keys. Governance, provider-runtime,
generated, template-source, and native-platform surfaces have consumer-specific
contracts and must not receive ordinary lifecycle metadata for visual uniformity.

Generated output is refreshed only through its canonical generator and checked
for deterministic freshness. A generated graph/index can describe relationships
but cannot create them, authorize archive, or override tracked owners. Graphify
is particularly limited here because its report predates the current baseline.

### Archive and retention boundary

Two exact archive profiles share semantic `artifact_type: archive`:

- `sdlc-archive` owns `docs/98.archive/**`, requires direct-parent/provenance
  metadata, and conditionally admits replacement or immutable-snapshot fields.
- `content-archive` owns root `archive/**`, forbids SDLC parents, replacement,
  and snapshot fields, and uses its own template.

Git history is the default preservation route. An immutable snapshot requires
the exact evidence-preserve conditions and confidentiality checks. Secret,
credential, token, key, auth, shell-history, or raw-log payloads are not
committed as archive evidence.

Review-age signals (`draft_days: 30`, `active_days: 90`, and
`completed_execution_days: 180`) request human review only. Directory budgets
(`warning_at: 100`, `block_new_leaf_at: 150`) drive navigation/partition review,
not automatic moves. Archive/deletion still requires an approved manifest,
consumer/replacement proof, provenance, preservation, rollback, and independent
specification and quality reviews.

### Enforcement boundary

1. Resolve target path and role against the registry.
2. Instantiate the mapped template and deterministic frontmatter order.
3. Record only evidence-backed direct parents and lifecycle state.
4. Run `check-document-metadata.py --mode check-changed` against an explicit
   safe base and the exact changed targets.
5. Run applicable traceability and repository-contract checks.
6. Record results, deviations, transition overrides, and review in the Stage 04
   Task; a passing local checker proves only that local contract at that revision.

Remote CI required-check configuration, provider enforcement, runtime state,
and archive/deployment outcomes remain separate observations.

### Checker modes and the transition-override mechanism

`scripts/validation/check-document-metadata.py` (5,630 lines) is a single
interpreter with four `--mode` values, re-read directly this revision rather
than assumed from its one cited invocation:

| Mode              | What it validates                                                                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `report`          | Full-corpus profile/field/relation audit without failing the run; a survey mode.                                                                   |
| `check-changed`   | The exact changed-path set against an explicit `--base-ref`; the enforcement-gate mode named above and in the companion role/lifecycle references. |
| `check-active`    | Currently-active-family documents only, independent of what changed in a given diff.                                                               |
| `check-contracts` | Registry/contract self-consistency, independent of any target document set.                                                                        |

The "Reverse transitions require explicit scoped Stage 04 override evidence
and checker acceptance" claim elsewhere in this reference has a concrete
mechanism: `--transition-override-file` accepts a YAML file whose only
top-level key is `transition_overrides` (a non-empty list); the checker
raises `ProfileError` if either constraint is violated. This flag is
rejected outright — `"configuration-error: --transition-override-file
requires --mode check-changed"` — under any other mode. An override is
therefore always both an explicit file (not an inline flag or prose
assertion) and always scoped to the one mode that already requires an exact
base ref and changed-path set; there is no path to an override under
`report`, `check-active`, or `check-contracts`.

## Scope Implications

| Scope          | Application and disposition                                                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Agents must resolve one profile/template, preserve deterministic metadata and evidence, and stop rather than invent relations or transitions.       |
| `architecture` | ARD/ADR identity and supersession preserve constraints/decision history consumed by Specs; metadata never replaces architectural review.            |
| `backend`      | Parent/child Spec relations can type API, data, service, and test contracts; runtime behavior still needs implementation and validation evidence.   |
| `common`       | Shared Markdown/style rules coexist with consumer-specific profiles; uniform appearance is not authority to normalize metadata.                     |
| `docs`         | Owns profile/template selection, link/heading validation, language boundaries, archive routing, and changed/new enforcement.                        |
| `entry`        | Gateway documents follow the same typed chain; path/parent validity does not prove deployed routing.                                                |
| `frontend`     | UI Specs/Tasks/Guides use their actual profiles; screenshots and generated assets cannot supply missing identity, parent, or verification evidence. |
| `infra`        | Compose/config paths are implementation evidence, not lifecycle profiles; typed docs must link but cannot claim runtime acceptance.                 |
| `meta`         | Registry/checker are the machine owners; changes require explicit approval, tests, migration impact analysis, and no copied schema in Stage 90.     |
| `mobile`       | No current mobile chain exists; future documents must use admitted profiles and device/runtime evidence without adding ad hoc types.                |
| `ops`          | Policy/Runbook freshness, Incident/Postmortem parent rules, and Release event boundaries are role-specific and currently partly unexercised.        |
| `product`      | PRD is a root profile and human approval owner; metadata completeness cannot infer stakeholder acceptance.                                          |
| `qa`           | Checker results, traceability, exact-range reviews, and skipped-check reasons belong in Task evidence; historical exception counts remain explicit. |
| `security`     | Archive and evidence metadata must remain redacted and provenance-safe; no profile authorizes secret/private payloads or protected mutation.        |

## Sources

| Source                                                                                                                         | Accessed   | Class                        | Use and verification state                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------ | ---------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)                                       | 2026-08-08 | External fixed vocabulary    | Identifier/type/relation comparison only; no schema adoption.                                                             |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/)                                                                                    | 2026-08-08 | External fixed standard      | Provenance/revision comparison only; workspace registry remains canonical.                                                |
| [RFC 8288 Web Linking](https://www.rfc-editor.org/rfc/rfc8288)                                                                 | 2026-08-08 | External fixed standard      | Relation semantics comparison; no repository profile adoption.                                                            |
| [Michael Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | 2026-08-08 | External fixed article       | HTTP 200; preserved/superseded ADR history comparison.                                                                    |
| [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/)                                               | 2026-08-08 | External fixed publication   | HTTP 200; reviewed learning supports the Postmortem freshness boundary.                                                   |
| [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)                                         | 2026-08-08 | Workspace tracked            | Canonical routing, template-first, language, and changed/new enforcement boundary.                                        |
| [Metadata profiles](../../../99.templates/support/document-metadata-profiles.yaml)                                             | 2026-08-14 | Workspace tracked            | Re-read to confirm 21 profiles / 17 README profiles at current HEAD.                                                      |
| [Lifecycle status](../../../99.templates/support/lifecycle-status.md)                                                          | 2026-08-08 | Workspace tracked            | Human lifecycle vocabulary and interpretation boundary.                                                                   |
| [SDLC document contract](../../../99.templates/support/sdlc-document-contract.md)                                              | 2026-08-08 | Workspace tracked            | Human role, relation, feedback, and release boundary.                                                                     |
| [Common document contract](../../../99.templates/support/common-document-contract.md)                                          | 2026-08-08 | Workspace tracked            | Reference/audit/archive/generated/governance ownership.                                                                   |
| [Archive and retention contract](../../../99.templates/support/archive-retention-contract.md)                                  | 2026-08-08 | Workspace tracked            | Provenance, confidentiality, review signals, and directory budgets.                                                       |
| [Metadata checker](../../../../scripts/validation/check-document-metadata.py)                                                  | 2026-08-14 | Workspace tracked executable | 5,630-line script re-read directly; confirmed 4 `--mode` values and the `--transition-override-file` schema/mode-binding. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                    | 2026-08-08 | Workspace stale/advisory     | Built from `f8a72211`; no uncorroborated graph inference used.                                                            |

## Maintenance

Re-measure after profile, template, checker, lifecycle, corpus-migration,
archive, README, generator, or stage-topology changes. Keep current-path,
frontmatter-status, typed-migration, and archive counts separate. The first real
Incident, Postmortem, or Release must trigger a focused review of its previously
unexercised template/profile without changing historical evidence by analogy.

## Related Documents

- [Verification and validation](./verification-validation.md)
- [Spec-driven SDLC](./spec-driven-sdlc.md)
- [SDLC document roles](./sdlc-document-roles.md)
- [Workspace baseline](./workspace-baseline.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
