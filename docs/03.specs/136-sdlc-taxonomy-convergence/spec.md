---
status: draft
artifact_id: spec:136-sdlc-taxonomy-convergence
artifact_type: spec
parent_ids:
  - spec:131-document-corpus-lifecycle-migration-foundation
  - spec:134-agent-governance-canonical-convergence
---

# SDLC Taxonomy Convergence Specification

## Overview

This specification defines the convergence of the repository's documentation
taxonomy onto an evidence-based SDLC and spec-driven structure. It is grounded
in an external evidence review of recognized frameworks and current
spec-driven-development implementations, paired with a full measurement of the
implemented corpus.

The external review returned a split verdict. The provider-projection model in
Stage 00 and the Stage 03/Stage 04 separation are sound and current practice.
The stage-based top-level split is nonstandard but not harmful. The
Architecture Requirements Document (ARD) is a local coinage with no external
definition. Date-in-filename is correct for event records and wrong for durable
artifacts.

The internal measurement found one root cause behind six symptoms: the corpus
grows by append and never reclaims. Completed work is never written back into
the durable artifact it came from, terminal documents never leave the active
stages, and validator rules accumulate without retraction. This specification
therefore treats reclamation, not relocation, as the primary change.

Scope covers the taxonomy decision, the archive model, the naming and date
policy, the contract-layer conflicts, the validator enforcement roadmap, the
provider-governance corrections, and the script consolidation. Execution of
those changes belongs to the successor Stage 04 plan and is explicitly outside
this specification.

## Boundaries and Inputs

### In scope

- Taxonomy verdict for `docs/00` through `docs/99` and `scripts/`.
- Lane separation between the product corpus and the governance-meta corpus.
- Archive model redefinition, including a content archive distinct from
  tombstones.
- Artifact-type-differentiated naming, identifier, and date policy.
- Resolution of contract-layer contradictions that currently block coherent
  enforcement.
- A staged validator enforcement roadmap with per-stage exposure estimates.
- Provider-governance corrections and unused-scope disposition.
- Script consolidation criteria.

### Out of scope

- Executing any file move, deletion, rename, or validator edit. This
  specification produces the decision record only.
- Backfilling `artifact_id` and `parent_ids` into the 829 documents that lack
  them. Recorded as a finding; deferred to a separate specification.
- Any change to `infra/`, Compose runtime, secrets, or remote state.
- Pushing to any remote.

### Measured inputs

All figures below were derived from the working tree and are reproducible.

| Subject                             | Measurement                                                                         |
| :---------------------------------- | :---------------------------------------------------------------------------------- |
| Total documents                     | 933 Markdown files, 9,258,584 bytes                                                 |
| Spec directories                    | 57 total: 12 service-domain (001–012), 45 governance-meta (090–134)                 |
| Stage 04 documents                  | 232 files: 101 plans, 130 tasks                                                     |
| Corpus A spec status                | 12 of 12 `active`, 0 terminal                                                       |
| Corpus B spec status                | 3 `active`, 41 `completed`, 1 `superseded`                                          |
| Stage 04 status                     | 7 `active`, 225 `completed`                                                         |
| Terminal documents in active stages | 280 (`completed` 278, `superseded` 2)                                               |
| `artifact_id` coverage              | 104 of 933 tracked records (11%)                                                    |
| Dated filenames                     | 229 of 232 in Stage 04; 0 in every other active stage                               |
| Filename to `artifact_id` mismatch  | 0 — the identifier is derived from the filename                                     |
| `date` frontmatter key              | Absent corpus-wide; `updated` is forbidden in 24 registry positions                 |
| Status vocabulary                   | 755 values, 0 out-of-vocabulary                                                     |
| Broken relative links               | 3, of which 1 is a real defect                                                      |
| SDLC chain completeness             | 11 of 11 infra domains complete                                                     |
| Largest single document             | `docs/00.agent-governance/memory/progress.md`, 1,193,498 bytes, 12.9% of the corpus |
| Validator volume                    | 852,407 bytes across four files                                                     |
| Repository contract baseline        | `failures=4`                                                                        |

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
`docs/99.templates/support/archive-retention-contract.md`, and
`docs/00.agent-governance/rules/documentation-protocol.md`.

## Core Design

### D1 — Lane separation

The product corpus and the governance-meta corpus have different lifespans.
Corpus A specifications are 12 of 12 `active` because a product specification
lives as long as the system it describes. Corpus B specifications are 42 of 45
terminal because a governance change ends when it lands. Holding both in one
lifecycle space is what produced the 280-document terminal backlog.

Stages 01 through 05 remain the product and infrastructure lane, keyed to the 11
`infra/` service domains. Governance-meta work moves to a separate lane, and its
terminal output moves to the content archive defined in D2.

### D2 — Archive model

`docs/98.archive/` currently defines itself as a tombstone stage. It holds 20
documents and has not been exercised since. Meanwhile 280 terminal documents
remain in the active stages because there is no destination that preserves
content.

The archive is therefore split into two roles.

| Role            | Purpose                                                                  | Status value |
| :-------------- | :----------------------------------------------------------------------- | :----------- |
| Tombstone       | Path redirect only; no content                                           | `archived`   |
| Content archive | Full preservation of terminal work, mirroring the source stage structure | `archived`   |

Three rules govern the model.

1. Every archived document leaves a forward pointer at its original location.
   All four external archive patterns reviewed require this; relocation without
   a pointer reproduces the exact link breakage that redirects exist to prevent.
2. Architecture decision records are never moved. Supersession is a status
   change plus a `superseded-by` link, applied in place. This follows Nygard,
   MADR, and Fowler unanimously.
3. Content archive entries retain their date prefix.

Migration volume is 274 documents: 42 terminal Corpus B specifications, 225
completed Stage 04 documents, and 7 superseded Stage 90 references. The result
reduces Stage 04 from 232 to 7 documents and Stage 03 from 57 to 15
directories.

### D3 — Write-back rule

Separation of Stage 03 from Stage 04 is retained. The external review found the
separation defensible and identified the mechanism that makes it work: OpenSpec
pairs a durable specification corpus with ephemeral change records that archive
on completion, and writes results back into the specification first. Böckeler's
2025-10-15 analysis documents the opposite outcome in Spec Kit and Kiro, where
co-located specifications are discarded after implementation.

Separation without write-back produces stale specifications and unbounded
execution sprawl. The measured 231-to-57 ratio is that outcome. This
specification therefore mandates that task completion writes results back into
the parent specification before the task is archived.

### D4 — ARD disposition

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

### D5 — Naming, identifier, and date policy

The user constraint states that dates move from filenames into frontmatter. The
external evidence supports this for durable artifacts and contradicts it for
event records. Both are honored by differentiating on artifact type.

| Target                          | Filename                    | Date location                       |
| :------------------------------ | :-------------------------- | :---------------------------------- |
| `docs/01`, `docs/02`, `docs/03` | Sequential number plus slug | Frontmatter `created` and `updated` |
| `docs/04.execution/tasks/`      | Date prefix retained        | Filename and frontmatter            |
| `docs/98.archive/`              | Date prefix retained        | Filename and frontmatter            |

A task is an event, and its date is part of its identity. A specification is a
state, and a date prefix begins to lie the moment the document is revised.
Renaming to correct it then breaks inbound links. The implemented corpus already
matches this split by accident: all 229 dated filenames are in Stage 04.

Introducing `created` and `updated` requires coordinated edits at 24 registry
positions where `updated` is currently forbidden.

### D6 — Contract-layer conflicts

Two contradictions block coherent enforcement and are resolved before any other
change.

| Conflict                                                                                                                                                                                                                                                                 | Evidence                                                                       | Resolution                                                   |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- | :----------------------------------------------------------- |
| Two competing blocking heading contracts for `docs/05.operations/**`. `documentation-protocol.md:376` mandates `## Policy Scope` for all policies while `check-repo-contracts.sh:641` forbids it for guides; the registry names different headings for the same concepts | `documentation-protocol.md:411-420`, `document-metadata-profiles.yaml:360-380` | Single owner per heading decision; registry is authoritative |
| `archived` is simultaneously a required status and a retired alias, seven lines apart                                                                                                                                                                                    | `documentation-protocol.md:87-88` versus `:94-95`                              | `archived` is valid; the retired-alias sentence is withdrawn |

Additional corrections: `reviewed_at` and `review_cycle` are required by the
policy and runbook profiles and drive 123 findings, yet `frontmatter-contract.md`
never mentions them. Undocumented enforcement is documented or withdrawn.

### D7 — Validator enforcement roadmap

The validator surface is not oversized relative to what it must check; it is
miscalibrated. It blocks regression on roughly 4 percent of documents per commit
and never blocks the standing deficit. Correcting it exposes existing violations
rather than creating new ones.

| Stage | Action                                                                                                                         | Expected exposure                              |
| :---- | :----------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| 1     | Fix vacuous and self-contradictory rules: the `audit` forbidden-heading typo at `document-metadata-profiles.yaml:415`, plus D6 | 0 new findings; rules become capable of firing |
| 2     | Remove the README heading short-circuit at `check-document-metadata.py:2096`                                                   | 159 of 230 READMEs                             |
| 3     | Activate heading enforcement per template role, in batches                                                                     | 546 of 655 typed documents                     |
| 4     | Promote `--mode check-active` to a standing gate                                                                               | 1,275 findings across 414 documents            |

The `audit` role forbids `## Facts and Definitions`, a string carried by zero
audit documents. The heading 34 of 39 audit documents actually carry is
`## Definitions / Facts`, which is the `reference` role's required heading. This
is a string mismatch, not a scoping decision, and the rule has never fired.

Structural remediation accompanies the roadmap. `check-repo-contracts.sh` is
4,065 lines of which 3,576 sit inside 34 Python heredocs and only 421 are shell,
so ShellCheck inspects 10 percent of the file and no Python linter covers the
rest. Roughly 22,000 lines of validator Python are unlinted because
`.pre-commit-config.yaml` declares no `ruff`, `black`, or `mypy` hook.

Glob design is the lever. READMEs classify 230 of 230 correctly and pass 219 of
230 because `readme_profiles` uses 17 narrow explicit path globs. `template_roles`
retrofitted broad directory globs onto a pre-existing corpus and produces the
83.4 percent violation rate. Narrowing globs precedes widening enforcement.

### D8 — Provider governance

The canonical-catalog-to-provider-projection model has the strongest external
support of any decision under review. Corrections are limited to drift.

- `docs/00.agent-governance/agents/agents/` carries a duplicated path segment.
- `providers/claude.md:31-32` claims every Sonnet and Opus adapter emits
  `effort: high`; `doc-writer.md:12` emits `low` and `workflow-supervisor.md:10`
  emits `xhigh`, both correct per `provider-models.yaml`.
- `providers/gemini.md:59-60` names model identifiers that exist nowhere in the
  contract or the adapters.
- 6 of 14 scopes sit outside the agent catalog. `scopes/mobile.md` mandates a
  React Native stack in a repository with no mobile files; `frontend.md`
  mandates a product stack whose only trace is one sandbox.
- Stage 00's sole enforcer exits non-zero on a missing `html5lib` dependency,
  leaving all 106 governance files locally unvalidated.

### D9 — Language policy

The corpus is bimodal and ungoverned: 404 of 933 documents are Korean-dominant.
Stage 01 is 26 of 26 Korean, Stage 00 is 0 of 106, and Stage 03 is split
internally at 21 of 98 with no frontmatter signal. Lane separation resolves this
without a separate mechanism: Corpus A is Korean, Corpus B and Stage 00 are
English.

### D10 — Script consolidation

Consolidation criteria, applied in the successor plan: retire scripts with zero
inbound callers unless a contract pins them; remove duplicate invocation where
`run-local-qa-gates.sh` runs 8 validators twice; externalize embedded Python from
shell heredocs; and externalize embedded data from validator logic where size is
data-driven rather than logic-driven.

### Dead surfaces

| Surface                                                                                     | Measurement                                            | Disposition                                                        |
| :------------------------------------------------------------------------------------------ | :----------------------------------------------------- | :----------------------------------------------------------------- |
| `05.operations/incidents/`, `releases/`                                                     | 0 documents each after 263 operations documents        | Retain scaffold, mark not-yet-exercised                            |
| Templates `incident`, `postmortem`, `release`, `api-spec`, `data-model`, `service`, `tests` | 0 instantiated documents                               | Retain, mark not-yet-exercised in the stage authoring matrix       |
| `2026-06-05-language-policy-*` tasks                                                        | 21 files, 147,461 bytes, 0 real inbound consumers      | Content archive                                                    |
| `audits/2026-07-07-*-audit-pack-update/`                                                    | 6 redirect stubs, 395 lines, all superseded, 0 inbound | Delete; the twin research pack was already removed for this reason |

## Interfaces and Data

The corpus is the data. Three interfaces govern it and are unchanged in kind by
this specification.

| Interface                    | Owner                             | Change                                                     |
| :--------------------------- | :-------------------------------- | :--------------------------------------------------------- |
| Frontmatter profile registry | `document-metadata-profiles.yaml` | Add `created` and `updated`; narrow `template_roles` globs |
| Lifecycle status vocabulary  | `lifecycle-status.md`             | Confirm `archived`; withdraw the retired-alias sentence    |
| Traceability graph           | `artifact_id` and `parent_ids`    | No backfill in this specification                          |

Traceability coverage is 11 percent. The chain the taxonomy claims to enforce
does not exist in machine-readable form for 89 percent of the corpus. This is
recorded as the largest outstanding structural finding and is deliberately not
addressed here, because backfilling identifiers into 829 documents is a larger
undertaking than the taxonomy convergence itself and would obscure it.

## Failure Modes and Guardrails

| Failure mode                                                                                      | Guardrail                                                                     |
| :------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------- |
| Moving 274 documents while contracts contradict each other makes violation attribution impossible | Wave 1 resolves D6 before any movement                                        |
| Archiving without forward pointers breaks inbound links                                           | Pointer creation is part of the same logical commit as the move               |
| Moving ADRs breaks the immutable-decision convention                                              | ADRs are excluded from relocation by rule                                     |
| Widening validator enforcement before narrowing globs surfaces 546 findings at once               | Stage 3 batches by template role, after glob narrowing                        |
| Repairing validators degrades the current baseline                                                | Each wave re-runs `check-repo-contracts.sh` and compares against `failures=4` |
| Counting generated indexes as references makes every document appear referenced                   | `llm-wiki-index.md` emits 1,332 links and is excluded from orphan analysis    |
| Governance-meta work re-accumulates after cleanup                                                 | D3 write-back rule; without it the 231-to-57 ratio returns                    |
| This specification itself adds to the governance-meta corpus it is reducing                       | Accepted; it is a governance change and requires a specification              |

### Wave sequencing

| Wave | Content                                                       | Precondition           |
| :--- | :------------------------------------------------------------ | :--------------------- |
| W1   | Resolve contract conflicts (D6, validator stage 1)            | None; corpus unchanged |
| W2   | Establish archive model and pointer convention (D2)           | W1                     |
| W3   | Migrate 274 documents to the content archive                  | W2                     |
| W4   | ARD vocabulary and ADR/ARD renumbering (D4)                   | W1                     |
| W5   | Naming and date policy, `created`/`updated` introduction (D5) | W1, W4                 |
| W6   | Provider and scope corrections (D8)                           | None                   |
| W7   | Validator enforcement stages 2–4 (D7)                         | W1, W5                 |
| W8   | Script consolidation (D10)                                    | W7                     |

Each wave corresponds to at least one logical-unit commit.

## Verification

| Check                     | Command                                                                      | Acceptance                                                       |
| :------------------------ | :--------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| Repository contracts      | `bash scripts/validation/check-repo-contracts.sh`                            | No regression against the recorded `failures=4` baseline         |
| Changed-document metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed` | Zero violations on changed documents                             |
| Full-corpus metadata      | `python3 scripts/validation/check-document-metadata.py --mode check-active`  | Findings decrease monotonically per wave from the recorded 1,275 |
| Traceability              | `bash scripts/validation/check-doc-traceability.sh`                          | Zero failures                                                    |
| Link integrity            | Relative-link resolution across `docs/**`                                    | Real defects remain at or below the measured 1                   |
| Stage 00 governance       | `python3 scripts/validation/check-agent-governance-contract.py`              | Exits zero once the `html5lib` dependency is resolved            |

Every wave records its command output as Stage 04 evidence. A wave is complete
only when its acceptance row holds and the preceding baseline has not regressed.

## Related Documents

- [Document corpus lifecycle migration foundation](../131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Agent governance canonical convergence](../134-agent-governance-canonical-convergence/spec.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
- [Lifecycle status](../../99.templates/support/lifecycle-status.md)
- [Current project memory](../../00.agent-governance/memory/current.md)
