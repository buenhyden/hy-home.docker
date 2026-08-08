---
status: draft
artifact_id: spec:136-sdlc-taxonomy-convergence
artifact_type: spec
parent_ids:
  - spec:134-agent-governance-canonical-convergence
  - spec:131-document-corpus-lifecycle-migration-foundation
---

# SDLC Taxonomy Convergence Specification

## Overview

This specification defines the convergence of the repository's documentation
taxonomy onto an evidence-based SDLC and spec-driven structure. It is grounded
in an external evidence review of recognized frameworks and current
spec-driven-development implementations, paired with a full measurement of the
implemented corpus.

This is the second revision. The first revision was authored as a decision
record and never left `draft`. A three-track re-measurement of Stage 00,
Stage 05, and the template system falsified two of its factual claims,
completed a third, and surfaced ten findings it did not record. One of its core
decisions was reversed by explicit user direction. The revision is applied in
place because no approved decision existed to preserve, because Stage 00
mandates in-place refactor over parallel copies, and because the first revision
recorded its own guardrail that it "adds to the governance-meta corpus it is
reducing" — a successor specification would repeat that cost.

The external review returned a split verdict. The provider-projection model in
Stage 00 is sound and current practice. The stage-based top-level split is
nonstandard but not harmful. The Architecture Requirements Document (ARD) is a
local coinage with no external definition. Date-in-filename is correct for event
records and wrong for durable artifacts.

The internal measurement found one root cause behind the observed symptoms: the
corpus grows by append and never reclaims. Completed work is never written back
into the durable artifact it came from, terminal documents never leave the
active stages, and validator rules accumulate without retraction. The
re-measurement adds a second root cause the first revision missed: the
enforcement layer is not merely miscalibrated but partially inoperative,
because its heading check matches substrings rather than lines.

This specification therefore treats contract repair as prerequisite to
reclamation, and reclamation as prerequisite to relocation.

## Boundaries and Inputs

### In scope

- Taxonomy verdict for `docs/00` through `docs/99` and `scripts/`.
- Collapse of Stage 04 into Stage 03 by co-location, and the renumbering of
  Stage 05 to Stage 04 that follows from it.
- Archive model redefinition, including a content archive distinct from
  tombstones.
- Artifact-type-differentiated naming, identifier, and date policy.
- Resolution of contract-layer contradictions that currently block coherent
  enforcement, including the substring-matching defect.
- Realignment of the template contract onto the measured corpus vocabulary.
- Provider-governance corrections, rule consolidation, and unused-scope
  disposition.
- Script consolidation criteria.

### Out of scope

- Backfilling `artifact_id` and `parent_ids` into the documents that lack them.
  Recorded as a finding; deferred to a separate specification.
- Any change to Compose service topology, images, secrets, or remote state.
  Renaming a documentation path referenced from an `infra/` annotation is in
  scope; changing what that annotation controls is not.
- Pushing to any remote.
- Adding Diátaxis tutorial or explanation document types. The gap is recorded;
  filling it is new authoring work, not convergence.

### Measured inputs

All figures were re-derived from the working tree during this revision and are
reproducible from the commands recorded in the successor plan. Figures marked
**corrected** replace a value from the first revision.

| Subject                                | Measurement                                                                         |
| :------------------------------------- | :---------------------------------------------------------------------------------- |
| Stage 00 files                         | **corrected** 109 files, 1,633,005 bytes; the first revision omitted `rules/hooks/` |
| Stage 00 byte concentration            | `memory/` is 75.6% of the stage; `progress.md` alone is 73.1%                       |
| `progress.md` share of the docs corpus | **corrected** 10.15%–10.78% depending on corpus boundary, not 12.9%                 |
| Stage 03 spec directories              | **corrected** 59: 41 `completed`, 16 `active`, 1 `superseded`, 1 `draft`            |
| Stage 03 directory composition         | 36 hold `README.md` + `spec.md`; 21 hold `spec.md` only; 2 hold a contract          |
| Stage 04 leaf documents                | 231: 101 plans, 130 tasks — 225 `completed`, 6 `active`                             |
| Spec-to-execution coupling             | 44 of 101 plans and 44 of 130 tasks share a slug with a spec directory              |
| Stage 05 files                         | 263, of which 71 are `README.md` — 192 leaf documents across 77 subjects            |
| Stage 05 subject coverage              | 57 subjects hold a full guide/policy/runbook triplet; 19 are singletons             |
| Stage 05 empty buckets                 | `incidents/` and `releases/` hold 0 leaf documents                                  |
| Template conformance                   | 88 of 631 documents at template target paths satisfy their required headings        |
| Zero-instantiation templates           | **corrected** 9, not 7; `audit` and `agent-design` were unrecorded                  |
| Dated filenames                        | 231, all in Stage 04                                                                |
| Stage 05 rename blast radius           | 597 files, 3,274 occurrences of the literal `05.operations`                         |
| Scopes outside the agent catalog       | 6 of 14, confirming the first revision exactly                                      |
| `agents/agents/` inbound references    | 41 files, including 5 test modules                                                  |

### External evidence boundary

The external review recorded nine evidence gaps. Three constrain this
specification directly and are carried forward as stated limits rather than
resolved claims.

- ISO/IEC/IEEE 12207 is paywalled and was not read. It is cited neither for nor
  against the taxonomy.
- `diataxis.fr` returned HTTP 429 on every attempt. The four-type structure is
  corroborated through Divio; the exact axis wording is unverified.
- No recognized framework addresses separating meta-documentation from product
  documentation. The lane-separation decision is an internal judgement, not an
  externally supported finding.

## Contracts

This specification does not introduce an API, service, or data contract. It
changes documentation contracts, which are owned by Stage 99 support documents
and enforced by Stage 00 validators. The contract changes it mandates are
enumerated in Core Design and must be applied before any corpus movement.

The authoritative registries affected are
`docs/99.templates/support/document-metadata-profiles.yaml`,
`docs/99.templates/support/lifecycle-status.md`,
`docs/99.templates/support/frontmatter-contract.md`,
`docs/99.templates/support/template-selection.md`,
`docs/99.templates/support/archive-retention-contract.md`, and
`docs/00.agent-governance/rules/documentation-protocol.md`.

## Core Design

### D1 — Enforcement repair precedes every other change

The first revision classified the validator surface as miscalibrated. The
re-measurement found a stronger defect: the operations heading check tests
`if literal not in text`, a plain substring match rather than a line-anchored
one. `### Usage Type` therefore satisfies a `## Usage` requirement, and
`### When to Use` satisfies the runbook requirement while simultaneously
appearing on the guides forbidden list.

| Defect                                                         | Location                                    | Effect                                      |
| :------------------------------------------------------------- | :------------------------------------------ | :------------------------------------------ |
| Substring rather than line-anchored heading match              | `check-repo-contracts.sh:665-669`           | Heading contract passes documents vacuously |
| `audit` role forbids a string carried by zero audit documents  | `document-metadata-profiles.yaml:416`       | Rule has never fired                        |
| `archived` is both a required status and a retired alias       | `documentation-protocol.md:88` versus `:95` | Normalization guidance contradicts itself   |
| `reviewed_at` and `review_cycle` enforced but never documented | `frontmatter-contract.md`, 0 mentions       | Undocumented enforcement                    |

The first revision named a fifth conflict that does not exist. It stated that
`documentation-protocol.md:376` mandates `## Policy Scope` for all policies
while `check-repo-contracts.sh:641` forbids it for guides. Line 376 is
path-scoped to `docs/05.operations/policies/` and makes no claim about guides,
and the guides forbidden list is at `:607`, not `:641`. That claim is
withdrawn. The real conflicts are recorded in D2.

Correcting these exposes existing violations rather than creating new ones. No
document movement occurs until they are corrected, because attributing a
violation to a move is impossible while the checker is unsound.

### D2 — The corpus is the contract's evidence

Template conformance is 88 of 631 documents. The first revision treated this as
a corpus deficit. The re-measurement shows the opposite: where the registry and
the corpus disagree, the corpus is consistent and the registry is the outlier.

| Concept         | Registry term                  | Protocol term     | Documents on registry term | Documents on protocol term |
| :-------------- | :----------------------------- | :---------------- | -------------------------: | -------------------------: |
| Policy boundary | `## Scope`                     | `## Policy Scope` |                          1 |                         63 |
| Guide operation | `## Routine Usage`             | `## Usage`        |                          1 |                         65 |
| Runbook entry   | `## Trigger and Preconditions` | `## When to Use`  |                          2 |                         61 |

The measured corpus vocabulary is therefore promoted to canonical and the
registry and templates are corrected to match it. This inverts the first
revision's implied direction and follows from user direction. It resolves the
guide, policy, and runbook conformance figures of 1, 1, and 2 without editing
190 documents.

Nine templates have zero conforming instances. The first revision listed seven;
`audit` and `agent-design` are added. `audit` is the significant case: 34 audit
documents exist and none satisfies the contract, because the required headings
were never the ones audit authors write.

| Template disposition                   | Templates                                                    |
| :------------------------------------- | :----------------------------------------------------------- |
| Retarget to measured corpus vocabulary | `audit`, `guide`, `policy`, `runbook`, `prd`, `ard`, `adr`   |
| Retain, mark not-yet-exercised         | `incident`, `postmortem`, `release`                          |
| Retain, mark not-yet-exercised         | `api-spec`, `data-model`, `service`, `tests`, `agent-design` |

The `reference` role is left untouched. At 36 of 39 conforming it is the only
role whose contract already describes its corpus.

### D3 — Stage 04 collapses into Stage 03 by co-location

The first revision retained the Stage 03 / Stage 04 separation on the strength
of the OpenSpec analogue. User direction reverses this. The decision is recorded
with its cost stated rather than concealed.

Each specification directory becomes the complete unit of durable contract and
execution record.

```text
docs/03.specs/NNN-<slug>/
├── README.md
├── spec.md
├── plan.md
└── task.md
```

The measured execution backlog makes this tractable. Of 231 Stage 04 leaf
documents, 225 are `completed` and archive under D4. Only 6 are `active`, and
they resolve to four subjects. Co-location therefore applies to 6 documents, not 231.

| Active document                                                   | Parent specification | Action                            |
| :---------------------------------------------------------------- | :------------------- | :-------------------------------- |
| `2026-07-26-agent-governance-canonical-convergence` plan and task | spec 134             | Co-locate as `plan.md`, `task.md` |
| `2026-07-28-target-surface-delta-convergence` plan and task       | spec 135             | Co-locate as `plan.md`, `task.md` |
| `2026-08-07-agentic-research-pack-extension` task                 | spec 104             | Co-locate as `task.md`            |
| `2026-03-27-infra-service-optimization-priority-plan`             | none                 | Orphan; disposition in D5         |

The durability risk this incurs is real and is stated. Böckeler's 2025-10-15
analysis records that Kiro, which co-locates, deletes its specifications after
implementation. Co-location without an archive contract reproduces that outcome.
This specification therefore binds co-location to D4: a specification directory
is archived whole, never emptied in place, and never deleted. That pairing —
Spec Kit's shape with OpenSpec's archive-on-completion durability — is the form
the decision takes here.

`docs/04.execution/` is removed once empty.

### D4 — Archive model

`docs/98.archive/` currently defines itself as a tombstone stage. It holds 21
documents and has not been exercised since. Meanwhile 256 terminal documents
remain in the active stages because there is no destination that preserves
content.

The archive is therefore split into two roles.

| Role            | Purpose                                                                  | Status value |
| :-------------- | :----------------------------------------------------------------------- | :----------- |
| Tombstone       | Path redirect only; no content                                           | `archived`   |
| Content archive | Full preservation of terminal work, mirroring the source stage structure | `archived`   |

Three rules govern the model.

1. Relocation preserves reachability, not the original path. Every inbound link
   to a relocated document is rewritten to its archive path in the same logical
   commit as the move, and the source-to-destination mapping is recorded in the
   archive ledger.

   The first revision of this decision required a forward-pointer tombstone at
   the original path instead. That is not implementable.
   `check-document-metadata.py` selects a document's profile from its path
   alone via `infer_artifact_type()`, and line 2549 raises
   `archived-outside-stage-98` whenever `status: archived` appears on a document
   whose path-derived type is not `archive`. A tombstone at
   `docs/03.specs/<slug>/spec.md` therefore cannot carry the status that makes
   it a tombstone, under any frontmatter shape.

   The requirement was also self-contradictory. Leaving 42 tombstones in Stage
   03 keeps that stage at 59 directories, which cannot be reconciled with this
   decision's own stated outcome of 17.

2. Architecture decision records are never moved. Supersession is a status
   change plus a `superseded-by` link, applied in place. This follows Nygard,
   MADR, and Fowler unanimously.

3. Content archive entries retain their date prefix.

Prior recorded dispositions bind this migration. The 2026-07-04 document
restructure audit ruled eleven Stage 03 specifications `evidence-preserve` —
"Kept in place; no archive tombstone" — with reasons recorded per specification:
Stage 90 research and Stage 05 operations still reference them, or they form a
historical audit chain, or their Stage 04 evidence chain remains live. Ten of
those eleven are terminal and would otherwise fall in scope. They are excluded.

Under D3 a terminal specification archives as a directory, carrying its
`plan.md` and `task.md` with it. The archive unit is the directory, not the
file.

### D5 — Write-back rule and orphan disposition

Separation of durable contract from execution record is retained in substance
even though it is no longer expressed by separate stages. OpenSpec pairs a
durable specification corpus with ephemeral change records that archive on
completion, and writes results back into the specification first. Böckeler
documents the opposite outcome in Spec Kit and Kiro, where co-located
specifications are discarded after implementation.

Task completion writes results back into the parent specification before the
directory is archived. Without this rule co-location degrades to Kiro's model.

The measured coupling shows the rule was never enforced: 44 of 101 plans and 44
of 130 tasks share a slug with a specification directory. The remainder are
orphan execution — work that was planned and recorded without a durable contract
to write back into.

| Orphan class                          | Disposition                                                      |
| :------------------------------------ | :--------------------------------------------------------------- |
| Terminal orphans, `status: completed` | Content archive under D4; no specification is retro-created      |
| Active orphans                        | Author the missing parent specification, then co-locate under D3 |

Only one active orphan exists. Retro-creating specifications for 225 terminal
orphans would manufacture contracts for work that has already shipped, and is
explicitly rejected.

### D6 — Stage renumbering

Removing Stage 04 leaves a gap in the stage sequence. User direction selects
renumbering over a reserved gap. `docs/05.operations/` becomes
`docs/04.operations/`, restoring a contiguous `00`–`04` active sequence.

| Blast radius                                 | Count |
| :------------------------------------------- | ----: |
| Files containing the literal `05.operations` |   597 |
| Total occurrences                            | 3,274 |
| Markdown                                     |   569 |
| Shell and Python validators                  |    14 |
| YAML, including Prometheus alert rules       |    13 |
| `.github/CODEOWNERS`                         |     1 |

The rename crosses out of `docs/`. `infra/**/README.md` files and four
`alert_rules.local.*.yml` files carry documentation paths. Those paths are
updated; nothing the alert rules control is changed. Infrastructure validation
runs as part of the same wave for that reason.

The rename executes after all structural movement so that no path is rewritten
twice.

### D7 — ARD disposition

No external basis exists for "Architecture Requirements Document." The only ARD
in circulation is "Agile Requirements Document," which sits above a PRD rather
than beneath it. arc42 places architecture-level requirements in section 10 of
the same document that holds decisions in section 9.

Stage 02 requirements are retitled to arc42 vocabulary as quality requirements
and quality scenarios, which supplies the external definition the current name
lacks. The boundary rules are then codified explicitly in Stage 00: what
qualifies as a Stage 01 requirement, what qualifies as a quality requirement,
and what qualifies as a decision record.

The ADR and ARD numbering series have diverged. Both run 0001–0028 with 25
members but skip different numbers, so the same authentication hardening change
is ARD 0014 and ADR 0017. Number-based cross-referencing is therefore broken and
is realigned as part of this decision. Decision records adopt MADR conventions:
sequential identifier, immutable body, `superseded-by` links, no relocation.

Under D2 the `ard` and `adr` templates are retargeted to the vocabulary their
corpora already use rather than the reverse.

### D8 — Naming, identifier, and date policy

The user constraint states that dates move from filenames into frontmatter. The
external evidence supports this for durable artifacts and contradicts it for
event records. Both are honored by differentiating on artifact type.

| Target                          | Filename                    | Date location                       |
| :------------------------------ | :-------------------------- | :---------------------------------- |
| `docs/01`, `docs/02`, `docs/03` | Sequential number plus slug | Frontmatter `created` and `updated` |
| `docs/98.archive/`              | Date prefix retained        | Filename and frontmatter            |

A task is an event, and its date is part of its identity. A specification is a
state, and a date prefix begins to lie the moment the document is revised.
Renaming to correct it then breaks inbound links. Under D3 the task is no longer
a free-standing dated file but a `task.md` inside a specification directory, so
its identity is carried by the directory and its date moves to frontmatter. The
date prefix survives only in the archive, where the entry is genuinely an event
record of when work terminated.

Two preconditions block this change and are resolved first.

1. No frontmatter field exists to receive the date. `updated` is forbidden in
   every SDLC profile, including `document-metadata-profiles.yaml:492`, `:528`,
   and `:537`. The field is introduced before any filename is changed.
2. The date-in-filename mandate is stated in six places outside the templates:
   `template-selection.md:20`, `:21`, `:27`, and
   `documentation-protocol.md:200`, `:360`, `:384`, `:425`, plus
   `stage-authoring-matrix.md:22`. The templates themselves are already
   date-free and need no change.

### D9 — Stage 00 rule consolidation

Seventeen rule files carry two conflicts and four duplications. Consolidation
covers both, per user direction.

| Class    | Finding                                                           | Evidence                                                            |
| :------- | :---------------------------------------------------------------- | :------------------------------------------------------------------ |
| Conflict | Two mutually exclusive lifecycles, each declared singular         | `agentic.md:74-76` versus `workflows.md:92-93`                      |
| Conflict | Fixture and regression counts disagree; ground truth is 11 and 16 | `quality-standards.md:61-62` versus `postflight-checklist.md:52`    |
| Overlap  | Load order stated three times                                     | `standards.md:13-21`, `quality-standards.md:47`, `agentic.md:50-56` |
| Overlap  | Language policy stated five times                                 | `standards.md:26-28` and four others                                |
| Overlap  | Typed harness loop defined twice                                  | `agentic.md:68-86`, `workflows.md:101-117`                          |
| Overlap  | Eight completion-gate items duplicated                            | `task-checklists.md` versus `postflight-checklist.md`               |

The lifecycle conflict resolves toward `workflows.md`, because
`task-checklists.md:75-77` already binds provider adapters to that formulation
and the `agentic.md` formulation has no downstream consumer.

Two merges follow: `standards.md` into `quality-standards.md`, and
`postflight-checklist.md` into `task-checklists.md`. Seventeen rule files become
fourteen. `bootstrap.md` load order and every inbound cross-reference are
updated in the same logical unit.

### D10 — Provider governance and scope disposition

The canonical-catalog-to-provider-projection model has the strongest external
support of any decision under review. Corrections are limited to drift.

- `providers/claude.md:31-32` claims every Sonnet and Opus adapter emits
  `effort: high`; `doc-writer.md:12` emits `low` and `workflow-supervisor.md:10`
  emits `xhigh`, both correct per `provider-models.yaml`.
- `providers/gemini.md:59-60` names model identifiers that exist nowhere in the
  contract or the adapters.
- Six of fourteen scopes sit outside the agent catalog: `backend`, `entry`,
  `frontend`, `meta`, `mobile`, and `product`. `scopes/mobile.md` mandates a
  React Native stack in a repository with no mobile files; `frontend.md`
  mandates a product stack whose only trace is one sandbox. The structural cause
  is that `persona.md:23-38` routes fourteen personas while the catalog wires
  eight.
- Stage 00's sole enforcer exits non-zero on a missing `html5lib` dependency,
  leaving all 109 governance files locally unvalidated.

The `agents/agents/` duplicated path segment is **retained**. The first revision
recorded it as drift. It is referenced by 41 files including 5 test modules, two
generators, and the generated Codex adapters. Renaming it is a separate change
with its own regression surface and no convergence benefit.

### D11 — Language policy

The corpus is bimodal and ungoverned: 404 of 933 documents are Korean-dominant.
Stage 01 is 26 of 26 Korean, Stage 00 is 0 of 109, and Stage 03 is split
internally with no frontmatter signal. The product and infrastructure corpus is
Korean; Stage 00 and governance-meta specifications are English.

The language ratios in this decision are carried forward from the first revision
and were not re-derived during this one. Only the Stage 00 file count was
corrected. The successor plan re-measures them before acting on this decision.

### D12 — Script consolidation

Consolidation criteria, applied in the successor plan: retire scripts with zero
inbound callers unless a contract pins them; remove duplicate invocation where
`run-local-qa-gates.sh` runs 8 validators twice; externalize embedded Python from
shell heredocs; and externalize embedded data from validator logic where size is
data-driven rather than logic-driven.

`check-repo-contracts.sh` is 4,065 lines of which 3,576 sit inside 34 Python
heredocs and only 421 are shell, so ShellCheck inspects 10 percent of the file
and no Python linter covers the rest. Roughly 22,000 lines of validator Python
are unlinted because `.pre-commit-config.yaml` declares no `ruff`, `black`, or
`mypy` hook.

### Retained scaffolds and recorded gaps

| Surface                                   | Measurement                                          | Disposition                             |
| :---------------------------------------- | :--------------------------------------------------- | :-------------------------------------- |
| `incidents/`, `releases/`                 | 0 leaf documents; both READMEs declare this          | Retain scaffold, mark not-yet-exercised |
| Stage 05 nested `README.md` files         | 71 of 263 files, 27% of the bucket                   | Retain; navigation is not padding       |
| Guide `## Runbook Handoff` boilerplate    | 58 of 66 guides carry a byte-identical sentence      | Recorded; terminal-section only         |
| `document-corpus-migration-contract.yaml` | 21 KB, absent from the support ownership table       | Add to `support/README.md`              |
| Diátaxis tutorial and explanation types   | 0 documents; how-to split across guides and runbooks | Recorded as a gap; out of scope         |
| `2026-06-05-language-policy-*` tasks      | 21 files, 147,461 bytes, 0 real inbound consumers    | Content archive                         |
| `audits/2026-07-07-*-audit-pack-update/`  | 6 redirect stubs, all superseded, 0 inbound          | Delete                                  |

The three-way guide/policy/runbook split is **retained**. Full reads of five
matched triplets measured 15–28 percent cross-member line overlap, concentrated
in reciprocal cross-links rather than shared prose. Each member carries
information the other two do not: ordered procedure, normative obligation, and
failure trigger with rollback. The near-equal bucket counts reflect a genuine
per-service triplet, and the 19 singleton subjects confirm authors did not force
every subject into three.

## Interfaces and Data

The corpus is the data. Three interfaces govern it.

| Interface                    | Owner                             | Change                                                                    |
| :--------------------------- | :-------------------------------- | :------------------------------------------------------------------------ |
| Frontmatter profile registry | `document-metadata-profiles.yaml` | Add `created` and `updated`; retarget heading sets onto corpus vocabulary |
| Lifecycle status vocabulary  | `lifecycle-status.md`             | Confirm `archived`; withdraw the retired-alias sentence                   |
| Traceability graph           | `artifact_id` and `parent_ids`    | No backfill in this specification                                         |

Traceability coverage is 11 percent. The chain the taxonomy claims to enforce
does not exist in machine-readable form for the remainder of the corpus. This is
recorded as the largest outstanding structural finding and is deliberately not
addressed here, because backfilling identifiers is a larger undertaking than the
taxonomy convergence itself and would obscure it.

## Failure Modes and Guardrails

| Failure mode                                                                                      | Guardrail                                                                              |
| :------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------- |
| Moving documents while the heading checker matches substrings makes every result unattributable   | W1 repairs `check-repo-contracts.sh:665-669` before any movement                       |
| Moving 256 documents while contracts contradict each other makes violation attribution impossible | W1 resolves D1 before any movement                                                     |
| Co-location without an archive contract reproduces Kiro's spec-deletion outcome                   | D3 binds co-location to D4; directories archive whole and are never deleted            |
| Relocating without rewriting inbound links breaks them                                            | Link rewriting plus ledger mapping share the move's logical commit                     |
| Moving ADRs breaks the immutable-decision convention                                              | ADRs are excluded from relocation by rule                                              |
| Retargeting templates to the corpus entrenches whatever the corpus got wrong                      | Retargeting applies only where the corpus is internally consistent at 61:1 or better   |
| Renaming Stage 05 twice, before and after structural movement                                     | W5 executes after all movement waves                                                   |
| Renaming Stage 05 silently alters runtime behavior                                                | Only documentation paths change; infrastructure validation runs in the same wave       |
| Repairing validators degrades the current baseline                                                | Each wave re-runs `check-repo-contracts.sh` and compares against the recorded baseline |
| Counting generated indexes as references makes every document appear referenced                   | `llm-wiki-index.md` is excluded from orphan analysis                                   |
| Governance-meta work re-accumulates after cleanup                                                 | D5 write-back rule; without it the orphan-execution ratio returns                      |
| This specification itself adds to the governance-meta corpus it is reducing                       | Revised in place rather than superseded, so the corpus does not grow by one            |

### Wave sequencing

| Wave | Content                                                            | Precondition           |
| :--- | :----------------------------------------------------------------- | :--------------------- |
| W1   | Contract and enforcement repair (D1, D9 conflicts)                 | None; corpus unchanged |
| W2   | Template retargeting onto corpus vocabulary (D2)                   | W1                     |
| W3   | Archive model, link-rewrite convention, 256-document migration (D4) | W2                    |
| W4   | Stage 04 collapse into Stage 03 by co-location (D3, D5)            | W3                     |
| W5   | Stage 05 to Stage 04 renumbering (D6)                              | W4                     |
| W6   | ARD vocabulary and ADR/ARD renumbering (D7)                        | W1                     |
| W7   | Naming and date policy, `created`/`updated` introduction (D8)      | W1, W6                 |
| W8   | Rule consolidation and provider/scope corrections (D9, D10)        | W1                     |
| W9   | Script consolidation (D12)                                         | W8                     |

Each wave corresponds to at least one logical-unit commit.

## Verification

| Check                     | Command                                                                      | Acceptance                                                |
| :------------------------ | :--------------------------------------------------------------------------- | :-------------------------------------------------------- |
| Repository contracts      | `bash scripts/validation/check-repo-contracts.sh`                            | No regression against the baseline recorded at wave start |
| Changed-document metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed` | Zero violations on changed documents                      |
| Full-corpus metadata      | `python3 scripts/validation/check-document-metadata.py --mode check-active`  | Findings decrease monotonically per wave                  |
| Template conformance      | Required-heading match across template target paths                          | Rises from the measured 88 of 631 after W2                |
| Traceability              | `bash scripts/validation/check-doc-traceability.sh`                          | Zero failures                                             |
| Link integrity            | Relative-link resolution across `docs/**`                                    | Zero broken links after each movement wave                |
| Stage 00 governance       | `python3 scripts/validation/check-agent-governance-contract.py`              | Exits zero once the `html5lib` dependency is resolved     |
| Infrastructure            | `bash scripts/validation/validate-docker-compose.sh`                         | No regression; required for W5                            |
| Rename completeness       | Zero remaining occurrences of the literal `05.operations`                    | Required for W5                                           |

Every wave records its command output as execution evidence. A wave is complete
only when its acceptance row holds and the preceding baseline has not regressed.

## Related Documents

- [Document corpus lifecycle migration foundation](../../98.archive/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Agent governance canonical convergence](../134-agent-governance-canonical-convergence/spec.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Template selection](../../99.templates/support/template-selection.md)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
- [Lifecycle status](../../99.templates/support/lifecycle-status.md)
- [Spec-driven development and SDLC reference](../../90.references/research/2026-08-08-agentic-engineering-research-pack/spec-driven-sdlc.md)
- [Current project memory](../../00.agent-governance/memory/current.md)
