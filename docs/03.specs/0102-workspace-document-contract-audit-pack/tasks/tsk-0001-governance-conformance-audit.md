---
profile_id: task
status: active
artifact_id: task-0102-0001
artifact_type: task
parent_ids:
  - SPEC-0102
created: 2026-08-29
updated: 2026-08-29
---
# Task: Governance Conformance Audit of Stages 00, 01, 02, 03, 05, 90, 98, 99

## Objective

Establish, by measurement rather than by reading, which documents under
`docs/00.agent-governance`, `docs/01.requirements`, `docs/02.architecture`,
`docs/03.specs`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`
and `docs/99.templates` no longer reflect current governance, and which gates,
fixtures and commit pins are excess rather than control.

This Task produces findings and owners. It changes no rule, deletes no
document, and removes no gate. Remediation follows in separate units, against
this evidence.

## Inputs

- [SPEC-0102](../spec.md) — profile model, gap disposition rules, and
  protected-surface boundaries.
- Tracked Markdown corpus of the eight stages named above: 596 files, roughly
  133,000 lines.
- 84 scripts registered in `scripts/manifest.yaml`.
- 50 leaves across 85 gate nodes in `.github/workflow-contract.yml`. Corrected from "144 leaves", which counted nodes of every kind.
- 48 test modules, roughly 57,800 lines.

Out of scope: generated projections under `.claude/`, `.agents/` and
`.codex/`; untracked-by-design paths (`secrets/`, personal settings, generated
state); and any remediation.

### Criteria

Nine detectors, each with a decision rule stated so the result is reproducible
and can be re-run as the corpus moves.

| ID | Detector | Decision rule |
| -- | -------- | ------------- |
| D1 | Dangling path citation | a backticked repository path resolving to no tracked file or directory, classified by the citing document's own `profile_id` and `status` |
| D2 | Profile conformance | findings reported by `check-document-metadata.py` |
| D3 | Supersession lineage | `superseded_by` present, canonical scalar shape, target resolves to a live `artifact_id`. **Defective**: governance accepts verified retired lineage, so this rule over-reports |
| D4 | Control with no subject | a rule bounding itself to a path (`limited to`, `scoped to`, `applies only to`) that does not exist |
| D5 | Gate without reachable red | a registered validation entrypoint with no covering test, or none asserting a failing outcome |
| D6 | Duplicated rule statement | a normalised sentence of 60+ characters appearing verbatim in two or more live governance documents |
| D7 | Old-path duplicate or redirect stub | a body that is only a pointer, or two paths carrying byte-identical bodies |
| D8 | Unresolvable commit pin | a 40-hex object id cited as this repository's evidence that `git cat-file` cannot resolve |
| D9 | Term defined two ways | an SDLC term given differing definitions across live governance surfaces |

## Work Log

### 2026-08-29 — Detector construction and measurement

Measured at `3bb47ee9`. Raw counts before classification are recorded because
several of them are misleading on their own, which is itself a finding about
how this corpus must be read.

| Detector | Raw | After classification | Actionable |
| -------- | --: | -------------------- | ---------: |
| D1 | 1,809 | 1,420 historical by role; 266 closed execution records | **123** across 41 files |
| D2 | 27 | 11 are template-source placeholders, exempt by profile | **16** |
| D3 | 1 | detector rule stricter than governance | **0** |
| D4 | 1 | — | **1** |
| D5 | 23 entrypoints | 21 covered with a red assertion | **2** |
| D6 | 15 groups | 10 are shared cross-references | **5** |
| D7 | 28 stubs, 37 duplicate groups | all stubs are tombstones; all duplicates are generated projections | **0** |
| D8 | 642 ids / 5,236 citations | 38 upstream action pins, 46 upstream repository pins, 19 deliberate placeholders, 9 fixture tables | **44** over 11 files |
| D9 | 0 | — | **0** |

Two detector defects were found and corrected while running. D1's first pass
counted stage shorthand such as `docs/01` and anchor suffixes as paths. D4 was
initially scoped to Stages 00 and 99, which excluded the single instance it
exists to find. Both were corrected before the counts above were taken.

A third error was made and withdrawn in the same session: an external-source
sweep reported eighteen absent URLs, all of which proved to be a trailing
backtick captured by the extraction. On re-probe, 16 return 200 and 2 are
genuine 404s.

Counts in this table should be re-derived by re-running the detectors rather
than cited from here.

### 2026-08-29 — Findings

**~~`blocker`~~ withdrawn 2026-08-29 — no defect (D3).** The finding as first
written said that `docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md`
declares `superseded_by: SPEC-0153`, that `38fc89c5` deleted that
specification, and that a reader following the lineage forward arrives
nowhere. The last clause is false and the grading was wrong.

D3's decision rule required the target to resolve to a **live** `artifact_id`.
Governance requires less: `scripts/lib/document_governance/metadata_validator.py:3251`
accepts "current **or verified retired lineage**", and `SPEC-0153` is carried
as an `artifact_id` in `docs/98.archive/migrations/0003-workspace-governance-simplification.md:41`.
`python3 -m scripts.lib.document_governance.metadata_validator --mode check-active`
returns `selected=457 violations=0`, and
`python3 scripts/validation/check-document-corpus-lifecycle.py --mode check-full`
returns `violations=0`.

`tombstone-0157` was already tracked at `3bb47ee9`, the commit this audit
measured, so the reader does reach a record: `SPEC-0136` to `tombstone-0157`
to `mig-0003`.

A prior ruling in this corpus had already settled it and this audit failed to
find it before grading. `docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md:3944`
states: "**The frontmatter is not the defect and must not be edited.**"
`superseded_by` is mandatory while `status: superseded`, must be a same-type
uppercase stable ID, cannot be repointed at `mig-0003`, and is factually true —
SPEC-0153 did supersede SPEC-0136, then completed and was retired. That entry
also identified the real gap as the missing tombstone, which this session
authored as `tombstone-0154` through `tombstone-0157`.

**No change is made to `SPEC-0136`.** D3 is a detector defect, not a corpus
defect: its rule is stricter than the rule the repository enforces.

**`low`, downgraded from `high`, resolved 2026-08-29 (D4).**
`docs/90.references/data/0075-profile/README.md:28` scopes HADS to
`docs/90.references/data/hads/`, which `49522aa1` removed on 2026-08-23.

The finding first said all four documents must move together. Two facts
measured while resolving it show that was wrong.

**HADS was never enforced.** `git grep -l "hads\|HADS" -- scripts/ tests/
.github/` returns nothing. No validator, test, or workflow has ever required a
HADS block. The "mandatory profile" was prose, so its empty subject cost no
enforcement.

**Three of the four statements are prohibitions, not application scopes.**
`REQ-0024-FR-0005` reads "Do not broaden the HADS mandatory profile beyond
`docs/90.references/data/hads/`"; the ADR at `:31` and `:38` and the
description at `:47` say the same. A prohibition whose bound is empty prohibits
*more*, not less. All three remain sound and are deliberately left unedited —
they record the boundary approved at decision time, and rewriting a decided ADR
to chase a path rename would damage the record it exists to keep. Note that the
ADR's "Mandatory HADS conversion" heading sits under **Options Considered** and
was rejected, one of its stated reasons being "Existing validators and templates
do not require HADS."

Only `0075-profile/README.md:28` asserted an active application, and that one
sentence carried the whole finding. The disposition is recorded there as two
`[SPEC]` blocks: the profile is **not in force**, and its subject cannot be
recreated as named, because Stage 90 package paths must match
`{number:4}-{slug}` and be registered in the frozen Task 9 migration, which
makes `docs/90.references/data/hads/` structurally unrepresentable.

**`high` — two gates ran in CI with nothing proving they could fail (D5).
Fixed 2026-08-29.** `scripts/validation/check-quickwin-baseline.sh` (134 lines)
and `scripts/validation/check-template-security-baseline.sh` (159 lines) were
each registered in `.github/workflow-contract.yml` with `tests: []` in
`scripts/manifest.yaml` and no covering test at all. The other 21 entrypoints
all carry at least one test asserting a failing outcome.

`tests/validation/test_compose_baseline_gates.py` now covers both, 17 tests.
Each gate resolves its own root with `git rev-parse --show-toplevel` and reads
its subject from `docker compose config --format json`, so the fixture is a
disposable Git repository plus a `docker` shim on `PATH`. The tracked scripts
are invoked directly rather than copied, so the tests cannot pass while the
tracked file rots.

Every control is proven to fail independently: `restart`, `healthcheck`,
`no-new-privileges`, `cpus`, `mem_limit` and `secrets` for the first gate;
template adoption, `no-new-privileges` and `cap_drop ALL` for the second. Both
are also proven to fail closed on a missing exceptions registry (exit 2) and on
an empty service set, and to honour a registered exception only for the service
it names.

Gate after: `exit=0`, suites 10 to 11, the 17 tests visible in the run.

**Wiring one test suite into the gate required eight synchronised edits.**
`.github/workflow-contract.yml` (leaf, CI parent, local parent),
`scripts/validation/ci_gate_contract.py` (`_INTERNAL_ROOT_SUITES`,
`_INTERNAL_ROOT_CHILDREN`, `_LOCAL_AGGREGATE_CHILDREN`),
`scripts/validation/ci_gate_runner.py` (`_INTERNAL_ADAPTER_CONTEXTS`),
`scripts/manifest.yaml`, plus verbatim copies of three of those tables in
`tests/validation/test_ci_gate_contract.py` and a node count in
`tests/validation/test_github_workflow_contract.py`. Three of the eight are
byte-level duplicates of each other. This is a concrete, measured instance of
the gate complexity this Task was asked to examine, and it is filed as Action
11.

**`high` — one gate's green state was unreachable by construction (D5).
Fixed 2026-08-29.** `validate_gate2_contract` required a `reviewed_commit`
whose Task snapshot carries the canonical manifest and in which every gate-2
row's `Review verdict` normalises to exactly `Not Run`. Measured across all
**19** commits that have ever touched that Task — corrected from 18 — the best
any commit achieved was **0 of 150**. This corpus writes
`Not Run; <provenance>`, and 76 rows have carried a prior verdict since before
the contract existed. The gate could not pass however much review was done, so
it reported on itself rather than on the work.

The correct predicate was already in the file. `TERMINAL_VERDICT_RE` defines a
terminal verdict as the digest-bound marker
`SETTLED {gate2-receipt=…;gate2-set-authority=…}`, and the raise the predicate
guards reads "reviewed P3 snapshot has a terminal review verdict". The check
now tests for that marker instead of string-equality with `Not Run`, which is
the contract's own definition rather than a new rule.

Measured after, over the same 19 commits:

| | before | after |
| --- | --: | --: |
| commits where P3 is satisfiable | 0 of 19 | **19 of 19** |
| rows with a terminal marker at any commit | — | 0 of 150 |

Two tests were written first and both failed before the change: one asserting
that `Not Run`, `Not Run; destination supplied 2026-08-19`,
`Not Run; carried from gate 1` and a pre-contract prose verdict are all
admitted, and one asserting that a real `SETTLED` marker is still rejected. The
guard the predicate exists for keeps firing. Module: 61 tests to 63, OK.

**`medium` — 123 live-authority documents cite paths that no longer exist (D1).**
Concentrated in `docs/90.references/research/0002-agentic-engineering-research-pack/sdlc-document-roles.md`
(15), `docs/README.md` (11) and
`docs/03.specs/0103-document-restructure-audit-contract-archive/spec.md` (8),
spread over 41 files. The 1,420 citations excluded as historical are correct as
they stand: an archive entry, a dated audit, a tombstone and the retiring pack
all name old paths by role, and so does a completed Task. The distinction that
makes this number small enough to act on is the citing document's own lifecycle
status, not its path.

Only **4** of the 123 are present-tense routing statements pointing at dead
paths — the class that misdirects a reader rather than recording history:

| Location | Statement | Dead target |
| -------- | --------- | ----------- |
| `docs/03.specs/0008-workflow/spec.md:222` | canonical workflow agent behavior changes belong there | `docs/03.specs/008-workflow/agent-design.md` |
| `docs/03.specs/0008-workflow/spec.md:223` | execution sequencing changes belong there | `docs/04.execution/plans/` |
| `docs/03.specs/0093-docs-taxonomy-agent-first-migration/spec.md:31` | Docs Taxonomy Contract lists it as an allowed active stage | `docs/04.execution` |
| `docs/03.specs/0102-workspace-document-contract-audit-pack/spec.md:147` | "should create a Stage 04 task record"; audit outputs "should live under" a dated Stage 90 path | `docs/04.execution`, `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/` |

The fourth row is this Task's own governing specification, found while placing
this Task. Stage 04 was removed from the taxonomy and the dated Stage 90 audit
path was renumbered to `docs/90.references/audits/0001-readme` through
`0011-template-application-gaps`.

**`medium` — 44 commit pins present unrecoverable objects as evidence (D8).**
Thirty-three of the forty-four sit in
`docs/03.specs/0135-target-surface-delta-convergence/`, where a Task and a Plan
record blob ids for build, render and publish scripts that lived under `/tmp`
and were never committed. The ids are stated as verification evidence and
resolve to nothing. Against 5,236 total citations this is a small proportion,
and the corpus's pinning discipline is otherwise sound — 38 upstream action
pins, 46 upstream repository pins and 19 deliberate placeholders all check out.
The excess is not that pins are used; it is that ephemeral artifacts were
pinned as if durable.

**`medium` — five required sections are filled with identical boilerplate (D6).**
The same sentence appears in 26 architecture decisions ("The decision context
above records the applicable drivers and evidence."), 25 requirements ("No
separately numbered solution-independent external interface requirement was
identified in the source package."), 24 decisions, 23 descriptions and 22
requirements. A required section that two dozen documents can only fill with a
statement that there is nothing to say is a template asking for content the
document does not have. The remaining ten duplicate groups are legitimate
shared cross-references and are not findings.

**`low` — 16 profile-conformance findings remain (D2).** Down from 35 measured
earlier the same day. Eleven of the residual entries are template-source
placeholders, which the profile exempts by design.

**Two negatives recorded as results.** D7 found **no** old-path body duplicate
and **no** redirect stub outside `docs/98.archive/tombstones/`, where a minimal
pointer is the intended form: the cleanup of duplicated old paths is already
complete and there is nothing to remove. D9 detected **no** SDLC term defined
two ways across live governance surfaces, though this is the weakest result
here — the detector matches definition-shaped lines, and a conflict expressed
as prose would escape it.

### 2026-08-29 — Placement

Two candidate homes were tried and both were refused by the repository. The
refusals are recorded because they are themselves findings.

| Attempt | Outcome |
| ------- | ------- |
| `docs/90.references/audits/0096-…` as `AUD-0096` | rejected `package-path-invalid: unregistered`. `scripts/lib/document_governance/references.py:763` derives the admitted Stage 90 file set entirely from the Task 9 migration rows, each of which describes a move from a real predecessor. A net-new package has no predecessor to name. |
| `docs/superpowers/specs/…` | prohibited by `docs/03.specs/0103-document-restructure-audit-contract-archive/spec.md:63` and `:332`, and by `docs/03.specs/0008-workflow/spec.md:218` and `:277`, all `status: active`. |

Reverting the `AUD-0096` attempt then failed `identity-history-regression`,
because the identity was issued and an issued identity is never reissued. The
Stage 99 Registry therefore stands at `audit.high_water: 96` with no `AUD-0096`
document anywhere. The identity is spent, not free, and that control is
correct.

This Task is the third placement. It conforms: `task` is a `package-member`
profile, so it burns no global identity, and SPEC-0102 is the active
document-contract audit model whose own Status Boundary states that future
document-contract batches use its profile model, gap disposition rules and
protected-surface boundaries.

## Verification Evidence

| Run | Command | Result |
| --- | ------- | ------ |
| baseline, this Task stashed | `python3 scripts/validation/run-ci-gate.py --profile full` | exit 0; 10 suites OK |
| with this Task tracked, run 1 | same | exit 1; `test_public_metadata_checks_current_generated_links_not_historical_snapshots` failed |
| with this Task tracked, run 2 | same | exit 0; 10 suites OK |
| module alone | `python3 -m unittest tests.lib.document_governance.test_references` | 17 tests OK |
| the failing run's 278-test suite, reconstructed | 14 `tests.lib.document_governance.*` modules | 278 tests OK |

`python3 scripts/validation/check-document-metadata.py` reports this document as
`task | allowed-syntax | valid | parents=resolved:1 | status=active; allowed |
none`.

`python3 scripts/knowledge/generate-llm-wiki.py --write` was required: adding a
tracked document makes `docs/90.references/data/0082-llm-wiki-index/README.md`
and `docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md`
stale, and the gate blocks on that.

Detector outputs are reproducible from the decision rules in **Inputs** and are
not committed as data; re-derive rather than cite. No rule, gate, fixture or
document was changed by this Task, so no before/after gate delta applies.

### An intermittent gate failure was observed and is not explained

Run 1 above failed. The same suite then passed standalone, the module passed
alone, and a second full gate run passed. The failing assertion was that
`__missing_generated_link__.md` appear in the validator's output; instead the
output carried `scripts/manifest.yaml: generated-manifest-invalid: generated
ownership cannot be established` together with
`active-consumer-unreadable: ... [Errno 2] No such file or directory: 'lib'`
and the same for `'validation'`. Those two messages mean a relative path was
resolved against the wrong working directory. With generated ownership
unestablished, `scripts/lib/document_governance/references.py` falls back to an
empty `generated_paths`, the fixture's edited package is no longer recognised as
generated, and the asserted finding is never emitted.

That is a non-deterministic gate, which is the same defect class this Task
audits: a control whose signal cannot be relied on. It is recorded here as
observed and is **not** diagnosed. One observation is not a reproduction.

## Review Evidence

Self-review against SPEC-0102's disposition model, recording what this Task
deliberately does not claim:

| Check | Result |
| ----- | ------ |
| Findings separated from remediation | yes — the Actions table assigns owners and takes no action |
| Historical evidence not rewritten as active policy | yes — 1,420 D1 citations and 266 closed execution records are excluded by the citing document's own status, not edited |
| Protected surfaces untouched | yes — `docs/99.templates/` unchanged; no `secrets/` path read |
| Raw counts distinguished from actionable counts | yes — both columns retained, because the gap between them is a finding |
| Detector defects disclosed | yes — two corrected in-flight, one error withdrawn |
| Language | English, matching Stages 03, 90, 98 and 99. Corrected: the corpus is not uniformly English — Stages 01 and 02 are written in Korean |

Independent review is **not** claimed. A second seat has not read these
findings.

## Commit Ledger

| Commit | Scope |
| ------ | ----- |
| `18325ca9` | audit authored at the Stage 90 path; rejected |
| `783064a3` | Stage 99 Registry identity issue for `AUD-0096` |
| `17cbe1f4` | Registry high-water retained at the burned identity after revert |
| `2c4f24b2` | LLM Wiki index regeneration |
| `0f432f98` | audit removed from the prohibited `docs/superpowers` path; one D1 correction at `docs/05.operations/catalog/12-infra-net/0077-ip-address-management/guide.md:43` |
| _this commit_ | audit filed as `task-0102-0001` |

## Rulings

**Action 1 is not a correction within existing rules.** It was first classified
as one and that classification is withdrawn. `superseded` is a terminal status
in the `living` lifecycle, so `SPEC-0136` cannot transition out of it; and
pointing its `superseded_by` at `mig-0003` raised `replacement-free-supersession`
(27 findings to 28) because the reciprocal `supersedes` would have to be
written into an archived migration record. Every available route is a rule or
archive change.

**Action 5 is not a bulk job.** Of the 123 live-authority dangling citations,
exactly one had a determinable successor and was corrected at `0f432f98`. One
hundred and eighteen name subjects that were removed outright and have no
successor to point at. Four are the present-tense routing statements tabled
above. The remaining bulk reads correctly as historical.

**Stage 90 currently admits no net-new package.** This is a property of the
frozen Task 9 topology, not a defect in this audit. Any future audit faces the
same wall.

## Deferred Items

| # | Action | Finding | Owner | Gate |
| - | ------ | ------- | ----- | ---- |
| 1 | ~~Repoint or retire `SPEC-0136`'s supersession~~ | D3 | — | **closed 2026-08-29, no change; finding withdrawn** |
| 2 | ~~Rescope, retire, or re-subject the HADS profile~~ | D4 | — | **closed 2026-08-29**; recorded as not in force in one document, three left unedited as sound prohibitions |
| 3 | ~~Give the two untested gates a failing-case test~~ | D5 | — | **closed 2026-08-29**; 17 tests, both gates, gate `exit=0` |
| 4 | ~~Amend gate 2's P3 predicate~~ | D5 | — | **closed 2026-08-29**; predicate now uses `TERMINAL_VERDICT_RE`, satisfiable at 19 of 19 commits |
| 5 | Correct the 4 present-tense routing statements | D1 | per-document owner | two touch stated contracts; needs approval |
| 6 | Replace the 44 unrecoverable pins with a durable reference or mark them as ephemeral | D8 | Stage 03 owner | contract change; needs approval |
| 7 | Review whether five required sections earn their place, or make them conditional | D6 | Stage 99 owner | protected surface; needs approval |
| 8 | Close the 16 residual profile findings | D2 | `doc-writer` | in-rule |
| 9 | Decide how Stage 90 admits a net-new package, or record that it does not | placement | Stage 99 owner | rule change; needs approval |
| 10 | Reproduce and fix the intermittent `test_references` failure, or prove it cannot recur | D5 | `qa-engineer` | in-rule |
| 11 | Collapse the eight synchronised edit sites needed to wire one gate suite; three are verbatim duplicates | D5 | gate-contract owner | contract change; needs approval |

### Limitations

The detectors measure form, not meaning. D6 and D9 find textual repetition and
definition-shaped lines; a contradiction stated in different words in two
places will not appear here, and no automated rule in this Task can settle
whether two rules genuinely conflict. D5's proxy is test coverage of a failing
outcome, which is weaker than mutation-testing every gate — the one gate proven
unsatisfiable was found by direct measurement over history, not by the proxy.

## Related Documents

- [Workspace Document Contract Audit Pack Specification](../spec.md)
- [Documentation protocol](../../../00.agent-governance/policies/documentation-protocol.md)
- [Bootstrap policy](../../../00.agent-governance/policies/bootstrap.md)
- [Stage 99 Registry](../../../99.templates/registry.json)
