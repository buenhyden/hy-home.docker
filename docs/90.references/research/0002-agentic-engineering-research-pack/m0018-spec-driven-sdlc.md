---
title: "Reference: Spec-Driven Development and SDLC"
type: references/research-member
layer: reference
status: active
owner: "@buenhyden"
artifact_id: RES-0002-m0018
parent_ids: [RES-0002]
created: 2026-08-23
updated: 2026-08-30
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Reference: Spec-Driven Development and SDLC

## Overview

Spec-driven development in this workspace is a traceable engineering lifecycle,
not the installation of a particular AI tool. Product intent, architecture,
technical contracts, prospective execution, observed execution, and operations
evidence remain separate artifacts with named owners. Implementation is
acceptable only when the applicable contract, change boundary, validation,
review, and evidence chain agree.

This analysis re-measured the current tree at HEAD `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`
(2026-08-14, branch `docs/agentic-research-pack-deepening`). It does not reuse
the predecessor pack's `59 specs / 0 archived specs` figure. The stale Graphify
report was used only as a navigation aid and every relationship below was
corroborated against tracked Stage 00, Stage 01-05, Stage 98, and Stage 99
sources, re-derived with `find`/`rg` rather than trusted from the prior
revision of this leaf.

## Purpose

Define REQ-06 and REQ-09: the workspace's spec-driven concepts, lifecycle,
traceability, gates, feedback, ownership, evidence, and enforcement boundaries.
The companion role reference owns document-by-document distinctions, while the
metadata reference owns profile and state semantics.

## Repository Role

This is advisory Stage 90 research. It explains current tracked contracts and
external comparisons; it does not approve a requirement, choose architecture,
authorize implementation, establish policy, execute a release, prove runtime
state, or change any Stage 00/99 contract. Canonical authority remains in the
stage matrix, documentation protocol, typed metadata registry, lifecycle
contracts, active Spec/Plan/Task chain, implementation, and validation evidence.

## Scope

### In scope

- The current Stage 01-05 lifecycle and Stage 90/98/99 support boundaries.
- Entry and exit evidence, feedback routing, validation, review, and ownership.
- Spec-driven tool comparison at immutable upstream revisions.
- Current active/archive counts and lifecycle-state distribution.

### Out of scope

- Adopting ISO, IETF, NIST, Spec Kit, OpenSpec, or another external method.
- Changing templates, metadata profiles, lifecycle transitions, stages, or archives.
- Starting services, observing private runtime state, or mutating remote controls.
- Treating a tracked workflow, tag, Release record, or Stage 90 statement as
  deployment/runtime proof.

## Definitions / Facts

### Working definition

Spec-driven development is the practice of making an explicit, reviewable
contract the controlling input to implementation and keeping bidirectional
traceability among intent, decisions, design, work, validation, and outcomes.
The contract must be specific enough to reject an implementation, not merely
describe it after the fact. In this workspace, that principle spans more than a
single `spec.md`: PRD, ARD/ADR, Spec and child contracts, Plan, Task evidence,
and Operations each own a different question.

The lifecycle is iterative rather than a one-way waterfall. A failed check,
incident, postmortem, release outcome, vulnerability, or verified drift routes
back to the earliest canonical owner whose truth must change. The downstream
artifact links the correction; it does not copy the upstream contract and
become a competing source of truth.

### Current corpus measurement

Counts below exclude `README.md` navigation files. They are path and parsed
frontmatter measurements, not claims that every legacy leaf has completed typed
metadata migration. Re-verified at the 2026-08-14 boundary with `find`/`rg`
against HEAD `ece3eda9c3e1a60`: the leaf-count is now two higher than the prior
source-refresh baseline, and the `draft` bucket that previously held 2 leaves
is now empty. Both movements trace to the cause the prior revision of this
leaf predicted: this deepening effort's own governing Task,
`docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md`
(`status: active`, `artifact_type: task`), is itself a Stage 04 leaf, and it
entered the corpus already `active` rather than `draft`. This analysis's own
evidence trail is therefore part of the population it measures and will move
again the next time any Task in the corpus changes `status`.

**Superseded 2026-08-19; read this table as a dated snapshot, not as current state.** A seat measured it against the working tree and the figures below are falsified by the taxonomy convergence, which moved Stage 04 evidence into `docs/03.specs/spec-*/task.md` and grew `docs/98.archive`. Re-derived at the review tree: `ls docs/03.specs/*/spec.md | wc -l` returns **32** against a stated 28; `find docs/98.archive -name '*.md' | wc -l` returns **275**, of which 274 carry `status: archived`, against a stated 52; `find docs/04.execution -name '*.md' | wc -l` returns **7** against stated Plan 103 and Task 133; and the registry's `profiles:` key has **23** children against a stated 21. The identical defect in the sibling leaf `document-metadata-lifecycle.md` was marked on 2026-08-19 and this one was missed. Any current figure must be re-derived with the commands above.

| Surface                            | Current measured result                                                                       | Interpretation                                                                                                                                                                                                                                                                                       |
| ---------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 01-05 lifecycle leaves       | 533                                                                                           | 25 requirements, 50 architecture, 30 Spec-stage, 236 execution, and 192 operations leaves.                                                                                                                                                                                                           |
| Lifecycle statuses in those leaves | 298 `active`, 235 `completed`, 0 `draft`                                                      | Status exists across the measured active-stage corpus; `completed` remains durable evidence, not archive. The `draft` bucket is transiently empty, not structurally forbidden.                                                                                                                       |
| Current parent Specs               | 28 `docs/03.specs/*/spec.md`                                                                  | Replaces the predecessor's stale active-Spec count; unchanged since 2026-08-11.                                                                                                                                                                                                                      |
| Archived parent Specs              | 32 `docs/98.archive/**/spec.md`                                                               | Archive is populated after the 2026-08-08 migration; zero is false.                                                                                                                                                                                                                                  |
| Stage 98 non-README leaves         | 52, all `status: archived`                                                                    | Includes 32 typed archive leaves and 20 legacy tombstones without `artifact_type`; path/profile evidence and typed-field evidence must remain distinct.                                                                                                                                              |
| Stage 99 Markdown                  | 43 total, 35 non-README                                                                       | Template/support corpus; 24 non-README sources declare `status: draft`, while support contracts are governance sources rather than copied target artifacts.                                                                                                                                          |
| Current role paths                 | PRD 25; ARD 25; ADR 25; Plan 103; Task 133; Guide 66; Policy 64; Runbook 62                   | Role counts are derived from canonical paths. Legacy `artifact_type` coverage is incomplete and cannot replace path measurement. Task moved 132 -> 133 for the same reason the leaf-count and draft bucket moved.                                                                                    |
| Typed `artifact_type` coverage     | PRD 1/25; ARD 1/25; ADR 1/25; Plan 16/103; Task 20/133; Guide 1/66; Policy 1/64; Runbook 2/62 | Directly re-counted via `grep -l 'artifact_type: <role>'` per family. Typed migration remains shallow outside Plan/Task; a path match is not a typed-field match.                                                                                                                                    |
| Metadata-profile catalog           | 21 profiles under `profiles:`; 17 `readme_profiles:` entries                                  | `prd, ard, adr, spec, plan, task, guide, policy, runbook, incident, postmortem, release, reference, audit, readme, repo-support, generated, template-source, governance, archive, unsupported`. Nine of the 21 sit outside the twelve human-named SDLC roles the companion role reference documents. |
| Event roles                        | Incident 0; Postmortem 0; Release 0                                                           | Registered templates/profiles are not proof that an event occurred or that the contracts have been exercised by a real target.                                                                                                                                                                       |

The measured status total is deliberately not called an "active document"
count: `active`, `completed`, and `draft` are different lifecycle states, yet
all 533 leaves still reside in current Stage 01-05 paths. Likewise, Stage 98
tombstones preserve provenance and are not current guidance. The
metadata-profile catalog row is a fresh re-derivation this revision adds: the
registry's typed surface (21 profiles) is materially larger than the
lifecycle-document surface this pack narrates in prose (12 roles), because the
registry also types non-lifecycle governance surfaces such as README
variants, generated outputs, template sources, and archive tombstones. Do not
read "21 profiles" as "21 SDLC document roles"; the extra nine exist to type
things this workspace produces but does not treat as spec-driven-lifecycle
artifacts.

### Lifecycle and gates

```text
stakeholder intent
  -> PRD
  -> ARD + decision-specific ADRs
  -> parent Spec + focused child contracts
  -> prospective Plan
  -> Task implementation/validation/review evidence
  -> Operations and evidenced Release events
  -> feedback to the earliest owner that must change
```

| Transition                                        | Entry evidence                                                                 | Owner and exit evidence                                                                                            | Gate and failure route                                                                                                    |
| ------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Intent -> PRD                                     | Stakeholder problem, users, value, constraints, and verified current state     | Product owner; numbered PRD with testable requirements, scope, success criteria, and links                         | Human approval plus template/metadata/repository checks; ambiguity returns to intent.                                     |
| PRD -> ARD/ADR                                    | Approved intent and current architecture constraints                           | System Architect; enduring boundaries/quality attributes plus one ADR per significant choice                       | Architecture review and traceability; infeasibility returns to PRD, while a changed decision creates/supersedes an ADR.   |
| ARD/ADR -> Spec                                   | Approved upstream constraints and applicable implementation evidence           | Engineering owner; implementable behavior, interfaces, failure modes, verification, and optional focused contracts | Spec and contract checks; gaps return to the earliest requirement/architecture owner.                                     |
| Spec -> Plan                                      | Stable technical contract and known dependencies                               | Engineering/Project Lead; prospective sequence, risk, intended checks, rollback, and completion criteria           | Plan review and traceability; no executed-result claim belongs here.                                                      |
| Plan -> Task evidence                             | Approved scope, authority, baseline, dependencies, and approvals               | Implementer/QA; actual changes, commands/results, impact, reviews, commits, deferrals, and blockers                | Focused checks and independent review; failure returns to Task implementation or an earlier contract.                     |
| Task -> Operations/Release                        | Completed implementation evidence and operator/release impact                  | Operations/Release owner; changed guidance/control/procedure or a real release-event record                        | Runtime-specific checks and event evidence; a document, tag, changelog, or CI definition alone does not prove deployment. |
| Incident/Postmortem/QA/Security -> earliest owner | Observed impact, reviewed learning, failed validation, vulnerability, or drift | Owner selected by gap-to-stage routing; corrected PRD/ARD/ADR/Spec/Plan/Task/Operations artifact                   | Re-run the applicable gate and retain the causal evidence; Stage 90 analysis cannot close the loop.                       |

### Traceability model

Traceability has four distinct forms that must agree:

1. `artifact_id`, `artifact_type`, `parent_ids`, and `supersedes` encode typed
   identity and direct relations where the target profile admits them.
2. Human `Related Documents` links explain the broader upstream/downstream
   context; they are not a substitute for direct typed parents.
3. Requirement IDs, acceptance criteria, verification cases, Task evidence,
   and commit identities connect intended behavior to observed results.
4. Runtime or remote claims require an authorized observation of the named
   target and time. Tracked files prove definitions/configuration only.

Broken or ambiguous traceability fails closed. An author must not invent a
parent, infer priority from `parent_ids` order, or copy a requirement into a
later artifact merely to make a check pass.

### Enforcement layers

| Layer                                     | What it establishes                                                                                   | What it cannot establish                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Stage and role contracts                  | Canonical question, path, owner, template, consumer, and evidence duty                                | That a target followed the contract or was approved.                                       |
| Metadata registry and checker             | Profile match, fields, relations, headings, lifecycle transitions, and changed/new blocking semantics | Product correctness, runtime state, or remote enforcement.                                 |
| Specs and child contracts                 | Implementable behavior and verification criteria                                                      | That implementation or tests passed.                                                       |
| Plans and Tasks                           | Intended work versus observed work/evidence                                                           | That a remote CI rule, provider, deployment, or service executed unless directly observed. |
| Focused validation and independent review | Reproducible local results and a bounded verdict over an exact range                                  | Universal correctness beyond the reviewed inputs and environment.                          |
| CI/workflow configuration                 | A tracked automation definition                                                                       | A successful run, required-check configuration, branch protection, or production outcome.  |
| Release/operations evidence               | A bounded event or operating contract                                                                 | Deployment/runtime proof outside the separately evidenced chain.                           |

Two named scripts implement the traceability/alignment slice of this table
and were re-read directly this revision rather than assumed from their names.
`check-doc-traceability.sh` (90 lines) is **not** requirement-ID or
artifact-graph tracing; it checks reciprocal README links between
`docs/04.execution/` and `docs/05.operations/`, priority-Plan links to the
operations policy catalog/index, and that catalog `OPER`/`RUN` targets exist —
a link-literal check, not a `parent_ids`/requirement-ID verifier.
`check-doc-implementation-alignment.sh` (261 lines, inline Python) walks
active Stage 01-05 Markdown, extracts referenced repository paths, and
confirms each resolves against a fixed prefix/file allowlist (`docs/`,
`infra/`, `scripts/`, `.github/`, `.claude/`, `.codex/`, `secrets/`,
`projects/`, `tests/`, named root files) — it catches a doc citing a path no
longer in the tree, not whether the cited path's content matches the doc's
claim about it. Neither performs end-to-end requirement-to-commit tracing;
both are narrower verifiers this repository composes with the metadata
checker and human review to approximate full traceability.

### External implementations and standards boundary

| Source                                                                                                                     | Verified observation                                                                                                                                                                                                                                                                                                                                            | Workspace disposition                                                                                                                                                                                                                                                                                                                                                                              |
| -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub Spec Kit, re-pinned `83883a2ebad7e7de667fd00381b100d597faf846` (2026-08-14; was `684b3d8e0` on 2026-08-08)          | The flow grew from four phases to ten named phases/commands: `constitution` (governing principles; new first step), `specify`, `clarify`, `plan`, `tasks`, `analyze`, `checklist`, `taskstoissues` (new: converts tasks to GitHub Issues), `implement`, and `converge` (new: assesses codebase against spec/plan/tasks and appends remaining work).             | Its new `constitution` prefix and `converge` drift-detection step echo functions this workspace already separates into other owners (Stage 00 governance; QA/security drift routing). Still a comparative harness; this workspace's PRD/architecture prefixes, durable Task evidence, operations, archive, and feedback owners remain unadopted-but-analogous.                                     |
| Fission-AI OpenSpec, re-pinned `2826b8889e5223a9a8095d4428b60b56597e1020` (2026-08-14; was `e50bd0983d` on 2026-08-08)     | Core artifact structure is unchanged (`proposal.md`, `specs/`, `design.md`, `tasks.md`, archived to `openspec/changes/archive/<date>-<name>/`), now fronted by slash commands `/opsx:explore` (new: pre-proposal exploration), `/opsx:propose`, `/opsx:apply`, and `/opsx:archive`, with tool-specific aliases for Cursor/Amazon Q/Codex.                       | The live-Spec/in-flight-change split and new pre-proposal explore step resemble this workspace's Spec-stability-before-Plan and clarification norms; paths, commands, and archive semantics remain unadopted.                                                                                                                                                                                      |
| ISO/IEC/IEEE 12207:2026                                                                                                    | Public catalog says it covers conception through retirement and permits concurrent, iterative, recursive, and incremental application without requiring one lifecycle model.                                                                                                                                                                                    | Catalog/abstract comparison only. Purchased full text was not accessed and is **UNVERIFIED**; no conformance claim is made. Not re-fetched this revision: `iso.org` is a known HTTP-403 host for automated retrieval, so the claim needs revalidation by a browser-capable reviewer, not another automated attempt.                                                                                |
| ISO/IEC/IEEE 29148:2018 and 42010:2022                                                                                     | Public catalogs describe requirements-engineering information items and architecture descriptions.                                                                                                                                                                                                                                                              | Context for PRD/architecture analysis only. Purchased full text was not accessed and is **UNVERIFIED**; same `iso.org` 403 condition applies.                                                                                                                                                                                                                                                      |
| RFC Editor                                                                                                                 | Official home and archive for RFCs, including Standards and Best Current Practices.                                                                                                                                                                                                                                                                             | Example of a governed publication series, not a template or lifecycle owner for this repository.                                                                                                                                                                                                                                                                                                   |
| Landscape survey (MarkTechPost, Augment Code, Glukhov, Daniliants — secondary/aggregator sources, 2026-05 through 2026-08) | By 2026, GitHub Spec Kit, AWS Kiro, Cursor, OpenSpec, BMAD, and Tessl each ship a distinct spec-driven flavor; Kiro is described as lightest (three Markdown files, IDE-native), Spec Kit as most customizable but heaviest (most artifacts per feature, CLI-driven), and Tessl as a language-agnostic "tiles" framework layered onto any MCP-compatible agent. | **Landscape context only — External mutable, lower confidence than the primary-vendor rows above.** Third-party comparison articles, not vendor documentation; not cross-verified against each tool's own repository. Cited only to show this workspace's multi-artifact, stage-gated approach sits at the heavier/more-durable end of a real 2026 tool spectrum, not to endorse or rank any tool. |

### Feedback and evidence rules

- A validation failure changes Task evidence first; revise a Spec only when the
  failure demonstrates that the technical contract is wrong or incomplete.
- An incident owns live event state. A Postmortem owns reviewed causal learning
  and preventive actions after stabilization.
- A vulnerability can route to Policy, ADR, Spec, Plan, Task, Runbook, or all of
  them through links, but each fact has one earliest canonical owner.
- A Release record requires actual event evidence and remains distinct from
  deployment/runtime proof. Release notes, SemVer, a tag, a successful build,
  and readiness evidence each prove only their own fact.
- A reference, audit, graph, generated index, or template may inform work but
  cannot authorize a lifecycle transition or protected mutation.

### Carried source-evidence claims

Source-evidence claims carried forward from the superseded 2026-07-05
research pack on 2026-08-19. Each states what the upstream evidence supports
and, where it matters more, what it does not.

- **Two standards status claims carry unreconciled provenance.** The 29148:2018 and 42010:2022 status claims retain earlier retrieval provenance and were not re-verified on the date stated beside them. Carried as the contradiction rather than as either claim, because choosing one silently discards the other provenance.

## Scope Implications

| Scope          | Application and disposition                                                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `agentic`      | Agents must load the applicable contract, preserve stage ownership, use bounded loops, record evidence, and stop on missing authority; automation does not collapse lifecycle roles. |
| `architecture` | Architecture constraints belong in ARDs and significant choices in ADRs before Specs consume them; runtime architecture remains separately evidenced.                                |
| `backend`      | API, data, failure, and service behavior requires a parent Spec and focused contracts/tests where complexity warrants them.                                                          |
| `common`       | Shared standards and review conventions support every gate but cannot create a parallel lifecycle or bypass canonical owners.                                                        |
| `docs`         | Owns template-first authoring, metadata/link validation, archive boundaries, and Stage 90 advisory framing; Stage 01-99 writes still require explicit scope.                         |
| `entry`        | Gateway changes route through requirements, architecture, Spec, Task, and operations evidence with explicit runtime/rollback boundaries.                                             |
| `frontend`     | UI behavior, accessibility, state, and browser evidence follow the same Spec-to-Task chain; generated UI is not accepted from screenshots or prompts alone.                          |
| `infra`        | Compose and infrastructure definitions are implementation evidence and require Spec, validation, rollback, and operations handoff; they are not the SDLC owner.                      |
| `meta`         | The registry, templates, validators, and taxonomy encode lifecycle semantics; changes require their own approved metadata/docs chain rather than edits in this reference.            |
| `mobile`       | No current mobile implementation is established; any future work needs an approved product/architecture/Spec chain plus device-specific evidence.                                    |
| `ops`          | Owns guides, policies, runbooks, incidents, postmortems, and releases; event evidence feeds upstream owners without turning operations prose into product intent.                    |
| `product`      | Human stakeholders own intent, value, scope, requirements, and acceptance; an agent or external tool cannot infer approval.                                                          |
| `qa`           | Owns verification strategy, focused evidence, failure routing, and independent quality review; a passing local check is bounded to its command/environment.                          |
| `security`     | Security requirements, decisions, controls, tests, incidents, and remediation remain traceable with least privilege, redaction, and approval boundaries.                             |

## Sources

| Source                                                                                                                                                   | Accessed   | Class                        | Use and verification state                                                                                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [GitHub Spec Kit documentation](https://github.github.com/spec-kit/)                                                                                     | 2026-08-08 | External mutable             | HTTP 200; current phase flow and artifact handoff.                                                                                                       |
| [GitHub Spec Kit immutable tree, re-pinned](https://github.com/github/spec-kit/tree/83883a2ebad7e7de667fd00381b100d597faf846)                            | 2026-08-14 | External fixed               | `git ls-remote` HEAD re-pin (moved from `684b3d8e0`); ten-phase flow read from raw README at this commit.                                                |
| [OpenSpec immutable README, re-pinned](https://raw.githubusercontent.com/Fission-AI/OpenSpec/2826b8889e5223a9a8095d4428b60b56597e1020/README.md)         | 2026-08-14 | External fixed               | `git ls-remote` HEAD re-pin (moved from `e50bd0983d`); slash-command workflow read at this commit.                                                       |
| [Landscape survey articles](https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/) | 2026-08-14 | External mutable, secondary  | Aggregator comparison of Spec Kit/Kiro/OpenSpec/Tessl/BMAD; landscape context only, not primary vendor evidence.                                         |
| [ISO/IEC/IEEE 12207:2026 catalog](https://www.iso.org/standard/90219.html)                                                                               | 2026-08-08 | External catalog             | Public status/abstract accessible; purchased standard text **UNVERIFIED**. Not re-fetched 2026-08-14: `iso.org` returns HTTP 403 to automated retrieval. |
| [ISO/IEC/IEEE 29148:2018 catalog](https://www.iso.org/standard/72089.html)                                                                               | 2026-08-08 | External catalog             | Public status/abstract accessible; purchased standard text **UNVERIFIED**.                                                                               |
| [ISO/IEC/IEEE 42010:2022 catalog](https://www.iso.org/standard/74393.html)                                                                               | 2026-08-08 | External catalog             | Public status/abstract accessible; purchased standard text **UNVERIFIED**.                                                                               |
| [RFC Editor](https://www.rfc-editor.org/)                                                                                                                | 2026-08-08 | External mutable catalog     | HTTP 200; official RFC series and publication classes only.                                                                                              |
| [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)                                                                                   | 2026-08-08 | External fixed               | HTTP 200; April 2025 final CSF 2.0 incident-response profile. Rev. 2 is superseded and not used.                                                         |
| [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/)                                                                         | 2026-08-08 | External fixed publication   | HTTP 200; learning, triggers, blamelessness, review, and preventive actions.                                                                             |
| [Stage authoring matrix](../../../00.agent-governance/policies/stage-authoring-matrix.md)                                                                   | 2026-08-08 | Workspace tracked            | Canonical stage purposes, inputs, templates, and done criteria at Task 5 baseline.                                                                       |
| SDLC document contract (retired path: `../../../99.templates/support/sdlc-document-contract.md`)                                                                        | 2026-08-08 | Workspace tracked            | Human lifecycle and feedback boundary.                                                                                                                   |
| Metadata profiles (retired path: `../../../99.templates/support/document-metadata-profiles.yaml`)                                                                       | 2026-08-14 | Workspace tracked            | Re-read to confirm 21 profiles / 17 README profiles at current HEAD.                                                                                     |
| [Document traceability checker](../../../../scripts/validation/check-doc-traceability.sh)                                                                | 2026-08-14 | Workspace tracked executable | 90-line script re-read directly; scope confirmed as README-link and catalog-target checks, not requirement-ID tracing.                                   |
| [Implementation alignment checker](../../../../scripts/validation/check-doc-implementation-alignment.sh)                                                 | 2026-08-14 | Workspace tracked executable | 261-line inline-Python script re-read directly; scope confirmed as path-reference resolution against an allowlist.                                       |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                                              | 2026-08-08 | Workspace stale/advisory     | Built from `f8a72211`; all used claims corroborated against current tracked sources.                                                                     |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Relate agent work to a durable Spec and Task. | Inspect the current Spec package. | No agent execution is proved. |
| architecture | applies | Keep architecture intent in its typed owner. | Check the current Stage 03 Spec/Plan/Task route before a decision. | Tool phases do not assign architecture authority. |
| common | applies | Preserve approved handoff and capture rules. | Review the scoped diff. | Advisory comparison only. |
| docs | applies | Use Spec/Plan/Task roles when documenting work. | Check frontmatter and links. | No workflow adoption is implied. |
| infra | applies | Connect infrastructure change intent to its Spec/Plan/Task owner. | Check the scoped package and infrastructure owner. | No runtime evidence. |
| ops | applies | Feed operational incidents and learning back to their owner. | Confirm catalog or incident-packet path. | No operation is inferred. |
| qa | applies | Capture checks against the Task. | Inspect recorded check evidence. | A record is not a green suite. |
| security | applies | Retain approval and source boundaries. | Review cited local sources. | No control effectiveness is evaluated. |

## Maintenance

Re-measure counts and re-open mutable sources when stages, templates, metadata
profiles, lifecycle/archive contracts, validator behavior, Spec Kit, OpenSpec,
or official standard status changes. Keep current-path counts separate from
typed-metadata coverage and never infer runtime, remote, release, or deployment
outcomes from tracked documentation alone. Re-pin Spec Kit and OpenSpec at
their current HEAD on each future revision: both moved substantially between
2026-08-08 and 2026-08-14 (four phases to ten for Spec Kit; a new explore
command for OpenSpec), so treating either pin as durable across a longer gap
would understate real upstream drift.

## Related Documents

- [Verification and validation](./m0019-verification-validation.md)
- [SDLC document roles](./m0016-sdlc-document-roles.md)
- [Document metadata lifecycle](./m0006-document-metadata-lifecycle.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
