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
| D4 | Control with no subject | a rule bounding itself to a path (`limited to`, `scoped to`, `applies only to`) that does not exist. **Under-scoped**: it read prose only, and missed both the code-side prefix sets and the two scripts that require a removed file |
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
| D4 | 1 | detector read prose only | **3** after re-running over code |
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

**Wiring one test suite into the gate required twelve synchronised edits.
Reduced to eight on 2026-08-29.**

| Site | Before | After |
| ---- | ------ | ----- |
| `.github/workflow-contract.yml` — leaf, CI parent, local parent | 3 | 3 |
| `ci_gate_contract.py` — `_INTERNAL_ROOT_SUITES` | 1 | **0**, derived |
| `ci_gate_contract.py` — `_INTERNAL_ROOT_CHILDREN`, `_LOCAL_AGGREGATE_CHILDREN` | 2 | 2 |
| `ci_gate_runner.py` — `_INTERNAL_ADAPTER_CONTEXTS` | 1 | 1 |
| `scripts/manifest.yaml` — `tests` | 1 | 1 |
| `test_ci_gate_contract.py` — six copied tables | 3 | **0**, aliased |
| `test_github_workflow_contract.py` — node count | 1 | 1 |
| **Total** | **12** | **8** |

`_INTERNAL_ROOT_SUITES` was a second literal listing the same suites as
`_INTERNAL_ROOT_CHILDREN`. Measured across all 16 internal CI roots, the first
is exactly the `leaf.`-prefixed members of the second with the prefix removed,
in order, so it is now derived. `PinDerivationTests` pins that invariant,
including a case proving the derivation tracks a change rather than agreeing
once by coincidence; a root that legitimately needs the two to differ has to
change that test first.

`tests/validation/test_ci_gate_contract.py` restated six of the module's
private pins verbatim. They are used only to synthesise a conformant registry
that the mutation tests then break, never to cross-check the module, so a copy
proved nothing the module did not already state. They are now aliases.
Verification is unchanged: every mutation test still breaks the same fixture,
which still builds 85 nodes and 2 job roots, and the module's test count is 10
before and 13 after — the three added are the new derivation tests.

Net: 250 deleted lines against 73 added.

**One item on that list is not duplication and was kept.** The node count in
`test_github_workflow_contract.py` is a deliberate tripwire on graph size:
deriving it from the YAML it guards would make it vacuous. Naming it as
duplication was wrong.

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

**6** of the 123 are present-tense routing statements pointing at dead paths —
the class that misdirects a reader rather than recording history. All six were
corrected on 2026-08-29. The figure was first reported as 4; a targeted sweep
for routing verbs over all 1,084 `04.execution` citations found two more, in
the taxonomy SSoT itself.

| Location | Statement | Corrected to |
| -------- | --------- | ------------ |
| `0008-workflow/spec.md:222` | canonical workflow agent behavior changes belong in `docs/03.specs/008-workflow/agent-design.md` — unpadded and nonexistent | `docs/00.agent-governance/roles/workflow-supervisor.md` |
| `0008-workflow/spec.md:223` | execution sequencing changes belong in `docs/04.execution/plans/` | the owning package's `plan.md` |
| `0093-docs-taxonomy-agent-first-migration/spec.md:31` | Docs Taxonomy Contract lists `docs/04.execution` as an allowed active stage | stage removed from the set, with the reason stated |
| `0102-…/spec.md:147` | "should create a Stage 04 task record"; audit outputs "should live under" a dated Stage 90 path | co-located Task, plus the note that Stage 90 admits no net-new package |
| `docs/README.md:9` | the document flow includes `04.execution` | flow corrected; Plan and Task placement stated |
| `docs/README.md:112` | leaf language rule scoped to `docs/04.execution/plans/**` and `tasks/**` | scoped to `docs/03.specs/**`, `plan.md` and `tasks/**` included |

The fourth row is this Task's own governing specification, found while placing
this Task. **The taxonomy SSoT contradicted itself.** `docs/README.md:9` put
`04.execution` in the active flow while `:87` and `:88` in the same file already
mapped `docs/05.plans/` to `docs/03.specs/{number:4}-{slug}/plan.md` and
`docs/06.tasks/` to `.../tasks/`. D9 did not catch this because it matches
definition-shaped lines and this is a prose flow sentence against a mapping
table — the limitation this Task states for D9, now with a concrete instance.

`docs/README.md:121` also settles this Task's language choice as policy rather
than preference: "`03.specs/` | English-only technical specifications and
contracts".

**`medium` — commit pins present unrecoverable objects as evidence (D8).
Marked ephemeral 2026-08-29.** Re-measured by citation line rather than by pin,
`git cat-file -e <id>^{}` fails on **121** lines across 17 files. Classifying
each by whether the pin is offered as *this repository's* evidence leaves **55**
actionable:

| Where | Lines | Class |
| ----- | ----: | ----- |
| `0135-…/tasks/tsk-0001-delta-convergence.md` | 26 | commits on the isolated branch and worktree named in its own **Inputs**, both since deleted |
| `0135-…/tasks/tsk-0001-delta-convergence.md` | 14 | blob ids of `/tmp` build, render and publish scripts, never committed |
| `0135-…/plan.md` | 14 | the same `/tmp` script blobs |
| `0137-…/tasks/tsk-0004-canonical-research-refresh.md` | 1 | a draft blob that was never committed |

The other **66** are correct as they stand and were not touched: upstream
GitHub pins in the Stage 90 research packs (`ai-agent-catalogs.md`,
`spec-driven-sdlc.md`, `security-governance.md`), each carrying its own
`https://github.com/...` URL; the `actions/checkout` pin in
`hookify.block-unpinned-gha-action.md`; the Diataxis and agency-agents upstream
pins; and the git null OID used as a command placeholder in `0137/plan.md`.

Against 5,236 commit citations the actionable share is about one percent, and
the corpus's pinning discipline is otherwise sound. The defect is not that pins
are used; it is that ephemeral artifacts were pinned as if durable.

**No durable replacement exists**, so Action 6's first branch was unavailable:
the objects are gone, and inventing a substitute would be fabricating evidence.
Each affected document now carries an in-place statement of which ids do not
resolve and why. The ids themselves are kept — deleting them would erase what
the Task actually did — so the raw unresolvable count is deliberately unchanged
at 64 Stage 03 lines. What changed is that a reader can no longer mistake one
for verification.

**`medium` — two required sections have never once carried content (D6).
Fixed 2026-08-29. The figure of five was wrong.** Counting each section against
its own denominator, rather than counting repeated sentences, separates three
distinct cases:

| Section | Documents | Boilerplate | Real | Verdict |
| ------- | --------: | ----------: | ---: | ------- |
| `Interface Requirements` (REQ) | 25 | **25** | 0 | never used |
| `Decision Drivers` (ADR) | 26 | **26** | 0 | never used |
| `Non-functional Requirements` (REQ) | 25 | 22 | 3 | earns its place |
| `Traceability` (ADR) | 26 | 24 | 2 | earns its place |
| `Traceability` (AD) | 25 | 23 | 2 | earns its place |
| `Stakeholders and Concerns` (AD) | 25 | 5 | **20** | earns its place |
| `Quality Attributes` (AD) | 25 | **0** | 25 | fully used — not a finding |

`Quality Attributes` and `Stakeholders and Concerns` were named as boilerplate
and should not have been: D6 matched a framing sentence that *precedes* real
content, not an empty section. `Quality Attributes` carries content in 25 of 25.

Two sections are genuinely dead. `Interface Requirements` has never once been
filled in the entire corpus, and interfaces are already owned elsewhere — the
`spec` profile requires `Interfaces and Data`, and `architecture-description`
requires `Components` and `Data Flow`. `Decision Drivers` has never once been
filled either, and the boilerplate sentence says why: "The decision context
above records the applicable drivers and evidence" — `Context` owns it.

Both moved from `required_sections` to `optional_sections` in the Stage 99
Registry. `Non-functional Requirements` was **kept required**: its 3 real users
are the newest and most substantial requirement documents, so the 22 are
migration residue rather than proof the section is useless. Nothing was
rewritten in the 51 existing documents — they keep the section and stay valid.



**`low` — 16 profile-conformance findings; 14 closed 2026-08-29, 2 blocked
by a control working correctly (D2).** These appear only in the validator's
descriptive `report` mode. All three enforcing modes returned `violations=0`
before and after.

**The diagnosis offered here first was wrong and is withdrawn.** It claimed all
16 shared one cause — that the Stage 99 registry's path sets do not describe the
tree — and that none was an in-rule correction. Acting on it produced
`configuration-error: profile-path-overlap`, which is what disproved it: the
registry already carries a dedicated `operations-domain-readme` profile whose
`path_pattern` is exactly `docs/05.operations/catalog/{domain}/README.md`. The
13 domain READMEs were never unrouted; they simply carried no frontmatter at
all. That is an in-rule correction, as Action 8 originally said.

| Findings | Subject | Disposition |
| -------: | ------- | ----------- |
| 13 | `docs/05.operations/catalog/<domain>/README.md` | **closed**: added `profile_id: operations-domain-readme`. Every required section was already present; only the frontmatter was missing. No `status`, because that profile's `lifecycle_id` is `null` |
| 1 | `docs/05.operations/incidents/README.md` | **closed**: no profile claimed this path, so it is registered on `readme.additional_paths` and given `profile_id: readme` |
| 2 | `docs/98.archive/migrations/0001-…`, `0002-…` | **closed 2026-08-30 as no-change**; see Action 15 — they are historical evidence under the contract of their time, and the Registry change already cleared their provenance keys |

The registry did need one change, but a narrower one than claimed: the
`migration` profile's `optional_frontmatter` was `supersedes`/`superseded_by`
only, so the seven archive provenance keys those two records carry were each
`type-inappropriate-key`. Those keys are now admitted, which cleared that code.

**The last two cannot be closed through the gate, and the reason is a control
behaving correctly.** `mig-0001` and `mig-0002` carry `status: archived`. The
`migration` profile's `historical` lifecycle admits only `draft`, `completed`
and `superseded`, so `archived` is not a legal status for them and the record
cannot enter the profile without transitioning. Rewriting them to
`status: completed` was attempted and reverted: it raised
`invalid-transition: lifecycle transition requires explicit override:
archived -> completed`, and the override is a `--transition-override-file`
argument that the gate cannot supply, because `suite_registry.validate_execution_argv`
pins `check-document-metadata.py` to exactly `("--mode", "check-changed")`.

Closing these two therefore needs an authorised transition, not an edit. It was
not routed around.

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

### An intermittent gate failure was observed and is still not reproduced

Run 1 above failed. The same suite then passed standalone, the module passed
alone, and every full gate run since has passed. The failing assertion was that
`__missing_generated_link__.md` appear in the validator's output.

**The first diagnosis offered here was wrong and is withdrawn.** It read
`active-consumer-unreadable: ... [Errno 2] No such file or directory: 'lib'`
and the same for `'validation'` as proof that a relative path had been resolved
against the wrong working directory. It is not. `_open_anchored_regular`
(`operations_catalog.py:527`) walks `relative.parts[:-1]` with `os.stat(part,
dir_fd=…)`, and the test fixture copies only `scripts/manifest.yaml`,
`docs/90.references`, `docs/99.templates/registry.json` and one archive file —
so `scripts/lib` and `scripts/validation` genuinely do not exist under that
root. Those two messages are expected fixture output in every run, passing ones
included.

What remains unexplained is the one message that is not expected:
`scripts/manifest.yaml: generated-manifest-invalid`. `validate_current_references`
emits it only when `generated_reference_owners` raises, and it then falls back
to an empty `generated_paths`, so the fixture's edited package stops being
recognised as generated and the asserted finding is never produced. That is a
sufficient mechanism for the observed failure.

It has not been reproduced. `generated_reference_owners` was run 15 times
against a freshly built copy of the same fixture shape and returned 8 owners
every time. One observation is not a reproduction, and the action stays open.

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
| 5 | ~~Correct the present-tense routing statements~~ | D1 | — | **closed 2026-08-29**; 6 corrected, not 4 |
| 6 | ~~Replace the unrecoverable pins or mark them ephemeral~~ | D8 | — | **closed 2026-08-29**; 55 marked ephemeral, 66 confirmed correctly foreign; no durable replacement exists |
| 7 | ~~Review whether five required sections earn their place~~ | D6 | — | **closed 2026-08-29**; 2 of the 5 moved to optional, 3 were not findings |
| 8 | ~~Close the 16 residual profile findings~~ | D2 | — | **14 closed 2026-08-29**; 2 remain, needing an authorised `archived -> completed` transition the gate's pinned argv cannot supply |
| 9 | ~~Decide how Stage 90 admits a net-new package, or record that it does not~~ | placement | — | **closed 2026-08-29**; recorded that it does not, in `docs/90.references/audits/README.md` |
| 10 | Reproduce the intermittent `test_references` failure — specifically, what makes `generated_reference_owners` raise — or prove it cannot recur | D5 | `qa-engineer` | in-rule; 15 direct probes did not reproduce it |
| 11 | ~~Collapse the synchronised edit sites needed to wire one gate suite~~ | D5 | — | **closed 2026-08-29**; 12 sites to 8, no verbatim duplicate left |
| 12 | ~~Decide whether the `docs/04.execution/` entries in live prefix allowlists should be dropped~~ | D4 | — | **closed 2026-08-29**; 5 removed, 8 kept because they exist to reject or to read history |
| 13 | ~~Re-approve, retire, or re-route the two security scripts~~ | D4 | — | **closed 2026-08-29 by re-routing**; granting the egress remains an operator act and nothing was granted |
| 16 | Correct the 22 self-successor `rewrite` rows to `retain`, and give each what `retain` obliges | D3, D4 | manifest owner | **needs 5 operations runbooks that do not exist**; the disposition edit alone turns the gate red |
| 14 | Decide how `test_document_metadata` gets real Git objects — a clone/worktree, or an explicit fixture mode — then clear the residual 30 and gate-register it | D5 | `qa-engineer` | **design decision**; 83 of 113 recovered mechanically, the rest is one collision |
| 17 | Excise the inert `readme_profiles` subsystem, or restore it to the Registry | D4 | `rules-engineer` | 7 call sites, 185 of 185 READMEs match nothing; equivalence check available |
| — | ~~Reduce commit-SHA tracking complexity~~ | — | — | **closed 2026-08-30 as a negative result**; the volume is a digest-verified per-row provenance column, and compressing it would break gate 2 |
| 15 | ~~Decide whether the gate should be able to pass `--transition-override-file`~~ | D5 | — | **closed 2026-08-30: no.** The argv pin is correct; the two records that wanted it stay as historical evidence |

### Two operator scripts are unrunnable, found 2026-08-29 (D4)

`blocker` for the capability, not for the gate. Neither script is
gate-registered — both are `kind: operations` in `scripts/manifest.yaml` — so
CI is unaffected and both fail closed. The capability is simply gone.

| Script | Requires | Enforced at |
| ------ | -------- | ----------- |
| `scripts/security/seed-grype-db-cache.sh` | `docs/04.execution/tasks/2026-07-23-security-supply-chain-runtime-closure.md` to exist and to contain the exact line `Grype DB network approval: confirmed` | `:142` exits `EXIT_POLICY` `seed-contract-surface-missing`; `:143` exits `seed-network-approval-missing` |
| `scripts/security/verify-sample-service-supply-chain.sh` | `docs/04.execution/tasks/2026-07-19-security-supply-chain-remediation.md` and the line `Scorecard network approval: confirmed` | `:122` `policy-task-or-cosign-config-boundary-missing`; `:762` for the Scorecard marker |

`65e994f3` moved those task documents out of Stage 04, and `9ef889b5` removed
the last copy of either approval marker. `git grep` finds neither string
anywhere in the tracked corpus. Both scripts therefore stop at their first
policy check.

Both also declare `authority: docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md`,
which is `status: superseded`.

**Resolved 2026-08-29 by re-routing, without granting anything.** Of the three
options — re-approve, retire, re-route — only the third is mine to take. Each
marker is a written human approval for outbound network egress, so writing one
would manufacture that approval; and retiring two security tools on an
ambiguous instruction is the one move that cannot be undone.

`infra/supply-chain.network-approvals.md` is now the approval surface, and both
scripts read it as `APPROVAL_DOC`. It sits beside the policy files the same
scripts already read, under a path the current taxonomy admits, so a stage
rename cannot carry it away again. It grants nothing: it records that no
approval is on file and documents the exact line an operator must add.

Behaviour is unchanged — both still fail closed — but the failure is now
accurate. `seed-grype-db-cache.sh` reports `seed-network-approval-missing`
rather than `seed-contract-surface-missing`, which named a missing contract
surface when what was missing was the approval.

**Their one covering test never exercised the approval path.**
`test_grype_db_seed.py:93` asserts only that the harness *contains* the string
`Grype DB network approval: confirmed`, which stayed green throughout the
period both scripts were unrunnable. `NetworkApprovalSurfaceTests` now
exercises it: that no marker is granted on the tracked surface, that
`grep -Fqx` would match the documented form if one were added, and that neither
script cites Stage 04 any more. Module: 12 tests to 16.

Their manifest `authority` is still `SPEC-0136`, which is `superseded`. That is
not specific to these two — see Action 16.

### A 263-test suite has been red and ungated, found 2026-08-29 (D5)

`blocker`. `tests/validation/test_document_metadata.py` covers
`check-document-metadata.py`, the most-invoked validator in this corpus. At
`f3a634d0` it ran **263 tests with 105 failures and 8 errors** — 43 percent
failing — while the full gate stayed at `exit=0`. It is registered in neither
`.github/workflow-contract.yml` nor `ci_gate_runner.py`, so no profile has ever
executed it.

This is the same class as the fourteen `tests/lib/document_governance` suites
that `ci_gate_contract.py` records as having "ran under no profile until
2026-08-29", and it is larger.

**One line of harness explains most of it.** The module set
`PROFILES = HistoricalDocument(ROOT, "49406580…", "docs/99.templates/support/document-metadata-profiles.yaml")`
and `run_checker` passed `str(profiles)` on the command line. `HistoricalDocument`
is a recovery handle, not a path: `str()` yields a dataclass repr whose
`.suffix` is `.yaml')`, so `--profiles` named no file and every test reaching
profile loading died on it. The blob itself resolves and is 50,688 bytes.

Materialising it to a real file once per process recovers **62 of the 113**:

| | failures | errors |
| --- | --: | --: |
| before | 105 | 8 |
| after the harness fix | **43** | **6** |

**A second fixture omission accounted for 19 more.**
`copy_registry_contract_fixture` staged its files with `git add` and never
committed, leaving `HEAD` unborn, so the validator's Spec Package snapshot read
failed with `cannot read Spec Package Git snapshot`. Committing the fixture
takes `RepositoryContractIntegrationTests` from 20 failing to green.

| Stage | failures + errors |
| ----- | ----------------: |
| before this session | **113** |
| after materialising the profiles blob | 49 |
| after committing the registry contract fixture | **30** |

**Why the module cannot simply be migrated onto the canonical Registry.** The
first diagnosis said the blocker was `allocation bootstrap lacks approved
lineage`, which is right but understated the reason. That error comes from
`identity_history.py:478`: `load_registry` validates identity-allocation
lineage against **this repository's real history** — `_approved_migration_document`,
`merge-base` against real commits, and the prior Registry blob. A synthetic
fixture repository can never satisfy it, so the module's use of a frozen
profiles snapshot was a deliberate workaround, not simply rot.

Nor can that snapshot be re-frozen: `docs/99.templates/support/` was deleted,
so `docs/99.templates/support/document-metadata-profiles.yaml` exists only at
commit `49406580` and no newer version of that contract exists. The contract
moved to `registry.json` entirely.

**The remaining 30 are one finding, not thirty.** Read individually they look
unrelated; read together every one is the same collision.
`check-document-metadata.py` resolves frozen contracts and recovery blobs from
**this repository's real Git history**, and `test_document_metadata.py`
exercises it against synthetic fixture repositories that by construction have
neither.

| Cluster | Count | The frozen thing it collides with |
| ------- | ----: | --------------------------------- |
| `ReadmeProfileTests` | 6 | the profiles YAML at `49406580` carries a `stage-index` profile the Registry does not, and no profile for the five `tests/**/README.md` added since |
| `ChangedBodyDeficitGitTests` | 5 | the fixture copies `mig-0003` in, and `load_current_operation_mappings` then demands recovery blobs the fixture repo has never held — `historical document recovery must resolve to a regular blob` |
| `ProfileSchemaTests` | 7 | the target-surface manifest's 483 entries still name `docs/03.specs/133-…` unpadded and omit the renumbered wiki data packages; its promotion digest is pinned |
| `MetadataValidationTests` | 6 | Registry-transition limits for `guide`, `policy`, `runbook` |
| `Task2StableTaxonomyFixtures`, `Task5ChangedMetadataRegressionTests` | 3 | `38fc89c5` retired `SPEC-0153`, so `test_spec_0153_canonical_package_satisfies_registry_metadata` measures something else |
| `ChangedModeRolloutTests` | 1 | the transition override, recorded separately below |

The remedy is a design decision, not thirty small edits: either run these tests
against a clone or worktree of the real repository so the objects resolve, or
give the validator an explicit fixture mode that declares which frozen
authorities are absent. Both are Action 14.

**A whole classification subsystem is inert under the live contract.**
`readme_profiles`, `matching_readme_profiles`, `classify_readme_profile`,
`readme_frontmatter_consumer` and `SDLC_TAXONOMY_BOUNDED_README_INPUTS` are
read at seven call sites in `metadata_validator.py` and branch on profile names
such as `template-catalog`. `build_registry_profiles` emits no `readme_profiles`
key at all, so under the canonical Registry every one of those lookups returns
an empty mapping. Measured: **185 tracked READMEs, 185 with zero matches.**

The legacy loader still requires it — `load_profiles` raises
`readme_profiles must be a non-empty mapping` — so the subsystem is live only
on the retired contract that only the tests use. Registry-era README
classification is done instead by the `readme`, `operations-domain-readme` and
`spec-package-readme` profiles, which is what Action 8 used.

**Not removed here, and deliberately.** Deleting the six tests while leaving
seven call sites of unreachable code would be worse than either extreme, and
excising the subsystem means removing live validation branches from a
7,000-line validator. That is its own unit of work, filed as Action 17, with a
ready-made safety check: the subsystem is inert, so `--mode report`,
`check-active` and `check-contracts` output must be byte-identical before and
after.

One more vacuity instance was found and removed rather than repointed:
`test_shell_reads_the_registry_without_duplicate_template_schema_tables`
asserted textual properties of `scripts/validation/check-repo-contracts.sh`,
which `1c620dd0` deleted when validation moved to the public suites. That
deletion had also left two present-tense citations in the active `SPEC-0093` —
its stated Validation Contract and a runnable command block — both corrected.

**The suite is deliberately still not gate-registered.** Registering 49 red
tests would break the gate. The order has to be fix, then register.

### The transition-override mechanism is unsatisfiable, found 2026-08-29 (D5)

`high`. This is the second unsatisfiable control in the corpus, after gate 2's
P3, and it is why Action 8's last two findings cannot be closed.
`load_transition_overrides` fails on two independent grounds:

| Ground | Detail |
| ------ | ------ |
| Evidence path | `metadata_validator.py:6140` requires `evidence_task` to start with `docs/03.specs/spec-` and be named `task.md`. **Zero** files named `task.md` exist in this repository and no `docs/03.specs/spec-*` directory does; the Registry emits `docs/03.specs/{number:4}-{slug}/tasks/tsk-{number:4}-{slug}.md` |
| Status vocabulary | it reads `common.allowed_statuses`, but `build_registry_profiles` emits a `common` of `frontmatter_order` and `typed_keys` only, so under the canonical Registry the set is empty and every row is rejected as an unknown lifecycle status |

Its one covering test passes only because the fixture invents the retired path
shape — a fixture keeping a dead contract alive, which is the fixture excess
this Task was asked to examine.

Both product fixes were written, measured to work, and then **reverted**: they
cannot be landed with a passing test until the module is migrated off the
retired profiles document, and landing a product change on a red test is not
acceptable. Filed as Action 14.

Even fixed, the mechanism stays unreachable from the gate, because
`suite_registry.validate_execution_argv` pins `check-document-metadata.py` to
exactly `("--mode", "check-changed")` and cannot pass
`--transition-override-file`.

**Action 15 answered 2026-08-30: that pin is correct and must stay.** Its
docstring states the rule — "Admit complete validation capabilities, never
arbitrary CLI arguments" — and `--transition-override-file` is precisely an
argument that *weakens* validation, since it authorises a transition that would
otherwise fail. A gate that can be handed its own exemption on the command line
is not a gate. The pin is doing its job.

The consequence is real and is accepted: a reverse transition can be made
locally with an override, but the resulting commit cannot pass CI while
`check-changed` still selects it, because CI cannot be given the override. To
close that, the override would have to become a **tracked artifact discovered
by convention** rather than a CLI argument — no argv change, pin intact.

**That is not built, and the reason is proportion.** The only thing asking for
it is `mig-0001` and `mig-0002`: two archived migration records whose
frontmatter predates the `migration` profile, reported in `report` mode only,
flagged by no gate. Building a CI-honoured override mechanism to clear two
report-mode findings would add exactly the kind of gate machinery this Task was
asked to reduce.

**So the two records stay as they are, and that is the disposition, not a
deferral.** They carry `status: archived` with the pre-`migration` archive
schema — `archived_from`, `archived_commit`, `archived_blob`,
`preservation_class` — which is an accurate description of what they are:
historical evidence written under the contract of their time. The Registry
change made in Action 8 already stopped their provenance keys being reported as
`type-inappropriate-key`. Rewriting the remainder would trade real recovery
evidence for schema tidiness.

### Fourteen manifest rows are governed by a superseded specification (D3)

`medium`, found 2026-08-29 while resolving Action 13. Fourteen of the 84 rows
in `scripts/manifest.yaml` declare
`authority: docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md`, and that
specification is `status: superseded`. Its successor `SPEC-0153` is retired with
`Replacement: none`, so the authority chain for those fourteen scripts
terminates in an archived migration record.

They are not one domain: `scripts/manifest.yaml` and `scripts/README.md`
themselves, the gate contract and runner, the workflow contract, compose
validation and readiness, secrets generation, the QA tool wrapper, and both
supply-chain scripts. `SPEC-0136` was a broad convergence spec, which is why so
many point at it, and no single live specification replaces it.

**The control that would catch this is scoped away from them.**
`_authority_findings` requires the authority to be an active typed Runbook, but
it only inspects rows with `mutation: runtime` **and** `disposition: retain`.
Measured: it reaches **2 of the 84 rows**. All fourteen `SPEC-0136` rows are
excluded, including the six that are `mutation: runtime` — exactly the rows the
check exists for.

**Root cause, found 2026-08-30: a self-successor is being used as an
exemption.** `disposition: retain` obliges a row to carry a domain-first
Operations Runbook authority when it is `mutation: runtime`, a non-empty
`tests` list, a non-empty `consumers` list, and `successor: null`. Any other
disposition obliges only a **tracked successor path** — and a row satisfies
that by naming *itself*.

**22 of 84 rows do exactly that.** Only two of the 24 `rewrite` rows are real
rewrites, both pointing at `check-document-links.py`. The other 22 declare that
they will be rewritten into themselves, which is not a disposition; it is a
no-cost exemption held open by pointing at oneself.

What those 22 currently avoid owing:

| Obligation | Rows that would fail it today |
| ---------- | ----------------------------: |
| a non-empty `tests` list | 5 |
| a non-empty `consumers` list | 8 |
| a domain-first Operations Runbook authority, being `mutation: runtime` | 6 |

**Not corrected here, and the reason is not caution about the edit.** Setting
those rows to `retain` is the accurate value and a one-line change each, but it
turns the gate red until each row is given what it then owes — and five of the
six runtime scripts have **no** Operations Runbook at all. `git grep` finds
`validate-docker-compose.sh` named in eighteen runbooks and `gen-secrets.sh`,
`seed-grype-db-cache.sh`, `verify-sample-service-supply-chain.sh`,
`compose-core-readiness.lib.sh` and `run-compose-core-readiness.sh` in none.
Closing this means authoring five operations runbooks describing procedures —
secrets generation, supply-chain verification, compose readiness — that must be
written by someone who runs them, not inferred from the scripts.

### Commit-SHA tracking: measured, and it is not excess (2026-08-30)

The request named branch SHA tracking as complexity to reduce. Measured across
`docs/`, `scripts/`, `tests/` and `.github/`: **4,421 citations of 595 distinct
40-hex ids across 142 files**, and the concentration looks damning — four ids
account for 2,244 of the citations, 51 percent.

| Id | Citations |
| -- | --------: |
| `889d3868` | 889 |
| `232effd9` | 804 |
| `6f2703d8` | 288 |
| `9917fcda` | 263 |

**The concentration is a per-row provenance column, not repetition for its own
sake.** `mig-0003` has 905 rows and 905 `recovery_commit` fields with 4 distinct
values, 881 of them identical. `0137/tsk-0001-rebuild.md` cites `9917fcda` 262
times, and **253 of those are cells in its old-claim migration ledger** — only
3 are prose.

**Compressing either would break verification, not tidy it.**
`gate2_claim_review_contract.py:270` computes
`subject_digest_v1 = canonical_digest(self.as_subject())`, and `as_subject()`
is `dict(zip(SUBJECT_KEYS, self.values[:10]))` — the first ten columns,
**including both 40-hex commit columns**. Those digests feed `ledger_digest` and
`population_digest`, which gate 2 verifies against pinned values. A ledger-level
default with per-row inheritance would change every subject digest in the
population.

The migration ledgers are worse candidates still: they are archived provenance
under `docs/98.archive/`, and rewriting them for compactness would edit
historical evidence — the same principle that kept `SPEC-0136`'s frontmatter and
`mig-0001`/`mig-0002`'s schema untouched.

**So the finding is a negative, and it is recorded as a result.** There is no
SHA-tracking excess to remove. What was actually wrong with the pins was
different and is already closed: 55 citations named objects that no longer
resolve, and those are marked ephemeral in place under Action 6. Raw citation
volume is a property of a normalised, digest-verified ledger, not a defect.

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
