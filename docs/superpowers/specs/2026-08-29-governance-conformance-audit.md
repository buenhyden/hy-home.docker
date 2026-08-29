# Governance Conformance Audit

**Measured 2026-08-29 at `3bb47ee9`.** This is a findings document, not a Stage 90
audit package: Stage 90 could not admit it, which is finding seven below.

## Objective

Establish, by measurement rather than reading, which documents under
`docs/00.agent-governance`, `docs/01.requirements`, `docs/02.architecture`,
`docs/03.specs`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`
and `docs/99.templates` no longer reflect current governance, and which gates,
fixtures and commit pins are excess rather than control.

This package produces findings and owners. It changes no rule, deletes no
document, and removes no gate. Those follow in separate units, against this
evidence.

## Scope

The tracked Markdown corpus of the eight stages named above — 596 files and
roughly 133,000 lines — together with the 84 scripts registered in
`scripts/manifest.yaml`, the 144 leaves in `.github/workflow-contract.yml`, and
the 48 test modules holding about 57,800 lines.

Out of scope: generated projections under `.claude/`, `.agents/` and `.codex/`;
untracked-by-design paths (`secrets/`, personal settings, generated state);
and any remediation.

## Criteria

Nine detectors, each with a decision rule stated so the result is reproducible
and can be re-run as the corpus moves.

| ID | Detector | Decision rule |
| -- | -------- | ------------- |
| D1 | Dangling path citation | a backticked repository path resolving to no tracked file or directory, classified by the citing document's own `profile_id` and `status` |
| D2 | Profile conformance | findings reported by `check-document-metadata.py` |
| D3 | Supersession lineage | `superseded_by` present, canonical scalar shape, target resolves to a live `artifact_id` |
| D4 | Control with no subject | a rule bounding itself to a path (`limited to`, `scoped to`, `applies only to`) that does not exist |
| D5 | Gate without reachable red | a registered validation entrypoint with no covering test, or none asserting a failing outcome |
| D6 | Duplicated rule statement | a normalised sentence of 60+ characters appearing verbatim in two or more live governance documents |
| D7 | Old-path duplicate or redirect stub | a body that is only a pointer, or two paths carrying byte-identical bodies |
| D8 | Unresolvable commit pin | a 40-hex object id cited as this repository's evidence that `git cat-file` cannot resolve |
| D9 | Term defined two ways | an SDLC term given differing definitions across live governance surfaces |

## Evidence

Measured at `3bb47ee9` on 2026-08-29. Raw counts before classification are
given because several of them are misleading on their own, which is itself a
finding about how this corpus must be read.

| Detector | Raw | After classification | Actionable |
| -------- | --: | -------------------- | ---------: |
| D1 | 1,809 | 1,420 historical by role; 266 closed execution records | **123** across 41 files |
| D2 | 27 | 11 are template-source placeholders, exempt by profile | **16** |
| D3 | 1 | — | **1** |
| D4 | 1 | — | **1** |
| D5 | 23 entrypoints | 21 covered with a red assertion | **2** |
| D6 | 15 groups | 10 are shared cross-references | **5** |
| D7 | 28 stubs, 37 duplicate groups | all stubs are tombstones; all duplicates are generated projections | **0** |
| D8 | 642 ids / 5,236 citations | 38 upstream action pins, 46 upstream repository pins, 19 deliberate placeholders, 9 fixture tables | **44** over 11 files |
| D9 | 0 | — | **0** |

## Findings

**`blocker` — a live specification is superseded by a retired one (D3).**
`docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md` declares
`superseded_by: SPEC-0153`. That specification was deleted by `38fc89c5` and
now exists only as `tombstone-0157`. A reader following the lineage forward
arrives nowhere, and the successor cannot be consulted for the authority the
predecessor handed to it.

**`high` — a mandatory profile is bounded to a deleted directory (D4).**
`docs/90.references/data/0075-profile/README.md:28` scopes HADS to
`docs/90.references/data/hads/`, which `49522aa1` removed on 2026-08-23. The
same bound is restated by `REQ-0024-FR-0005`,
`docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md:31`
and `docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md:47`.
The profile therefore applies to no document: it is a mandatory control over an
empty set, and all four documents must move together.

**`high` — two gates run in CI with nothing proving they can fail (D5).**
`scripts/validation/check-quickwin-baseline.sh` (134 lines) and
`scripts/validation/check-template-security-baseline.sh` (159 lines) are each
registered in `.github/workflow-contract.yml` and have no covering test at all.
The other 21 entrypoints all carry at least one test asserting a failing
outcome. A gate whose red state nothing exercises is indistinguishable from a
gate that cannot go red.

**`high` — one gate's green state is unreachable by construction (D5).**
`validate_gate2_contract` requires a `reviewed_commit` whose Task snapshot
carries the canonical manifest and in which every gate-2 row's `Review verdict`
normalises to exactly `Not Run`. Measured across all 18 commits that have ever
touched that Task, the best any commit achieves is **0 of 150**. This corpus
writes `Not Run; <provenance>`, and 76 rows have carried a prior verdict since
before the contract existed. The gate cannot pass however much review is done,
so it reports on itself rather than on the work. This is the clearest instance
of excess in the corpus, and it is excess of the expensive kind: an
unsatisfiable gate costs the full price of a control and returns no signal.

**`high` — Stage 90 admits no new reference package (found by attempting one).**
This audit was first authored as `AUD-0096` under
`docs/90.references/audits/0096-governance-conformance/`. The corpus rejected it:
`package-path-invalid: unregistered or empty package directory`. Stage 90's
package set is frozen to the target paths of the Task 9 migration, and all 116
rows describe a move from a real predecessor. A package with no predecessor
cannot be registered without writing a row that claims a migration which never
happened, so the reference stages are closed to net-new packages by
construction. That is why this document sits outside `docs/90.references`
rather than inside it, and why the audit it reports on has no Stage 90 identity.

This finding cost the gate two red runs and a revert, which is the intended
behaviour of the controls and is recorded rather than hidden: commit `18325ca9`
added the package, the gate failed on it, and `7fdf2adb` reverted it whole. The
revert then failed a second control, `identity-history-regression`: `AUD-0096`
had been issued in repository history and an issued identity can never be
reissued, so rolling the Registry back below it is itself a regression. The
Registry therefore stands at `high_water: 96` with no `AUD-0096` document
anywhere. That is correct — the identity is spent, not free — and it is the
clearest demonstration in this audit that the identity controls are sound even
where the package controls are closed.

**`medium` — 123 live-authority documents cite paths that no longer exist (D1).**
Concentrated in `docs/90.references/research/0002-…/sdlc-document-roles.md` (15),
`docs/README.md` (11) and `docs/03.specs/0103-…/spec.md` (8), spread over 41
files. The 1,420 citations excluded as historical are correct as they stand: an
archive entry, a dated audit, a tombstone and the retiring pack all name old
paths by role. So does a completed Task. The distinction that makes this
number small enough to act on is the citing document's own lifecycle status,
not its path.

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
The same sentence appears in 26 architecture decisions
("The decision context above records the applicable drivers and evidence."), 25
requirements ("No separately numbered solution-independent external interface
requirement was identified in the source package."), 24 decisions, 23
descriptions and 22 requirements. A required section that two dozen documents
can only fill with a statement that there is nothing to say is a template
asking for content the document does not have. The remaining ten duplicate
groups are legitimate shared cross-references and are not findings.

**`low` — 16 profile-conformance findings remain (D2).** Down from 35 measured
earlier the same day. Eleven of the residual entries are template-source
placeholders, which the profile exempts by design.

**Two negatives worth recording as results.** D7 found **no** old-path body
duplicate and **no** redirect stub outside `docs/98.archive/tombstones/`, where
a minimal pointer is the intended form: the cleanup of duplicated old paths is
already complete and there is nothing to remove. D9 detected **no** SDLC term
defined two ways across live governance surfaces, though this is the weakest
result here — the detector matches definition-shaped lines and a conflict
expressed as prose would escape it.

## Conformance

Not conformant. Two findings block: a live specification whose successor has
been retired, and a mandatory profile with no subject. Two gates carry no
evidence that they can fail and one cannot succeed.

The corpus is nevertheless in better condition than the raw counts suggest.
Of 1,809 dangling citations, 93 percent are correct historical records. Of
5,236 commit pins, 99.2 percent resolve or are correctly foreign. The old-path
duplication this audit was asked to find does not exist. The real defects are
few, specific, and concentrated.

## Actions

| # | Action | Finding | Owner |
| - | ------ | ------- | ----- |
| 1 | Repoint or retire `SPEC-0136`'s supersession to a live successor | D3 | Stage 03 owner |
| 2 | Rescope, retire, or re-subject the HADS profile across its four documents | D4 | HADS rollout owner |
| 3 | Give the two untested gates a failing-case test, or retire them | D5 | `qa-engineer` |
| 4 | Amend gate 2's P3 predicate to distinguish "no verdict this round" from "no verdict ever", or withdraw the gate | D5 | Spec 137 owner |
| 5 | Correct the 123 live-authority path citations | D1 | per-document owner |
| 6 | Replace the 44 unrecoverable pins with a durable reference or mark them as ephemeral | D8 | Stage 03 owner |
| 7 | Review whether five required sections earn their place, or make them conditional | D6 | Stage 99 owner |
| 8 | Close the 16 residual profile findings | D2 | `doc-writer` |
| 9 | Decide how Stage 90 admits a net-new package, or accept that it does not | D5 | Stage 99 owner |

Actions 2, 4, 6 and 7 change rules or contracts and require approval before
execution. Actions 1, 5 and 8 are corrections within existing rules.

## Limitations

The detectors measure form, not meaning. D6 and D9 find textual repetition and
definition-shaped lines; a contradiction stated in different words in two
places will not appear here, and no automated rule in this package can settle
whether two rules genuinely conflict. D5's proxy is test coverage of a failing
outcome, which is weaker than mutation testing every gate — the one gate proven
unsatisfiable was found by direct measurement over history, not by the proxy.

Two detector defects were found and corrected while running: D1's first pass
counted stage shorthand such as `docs/01` and anchor suffixes as paths, and D4
was initially scoped to Stages 00 and 99, which excluded the single instance it
exists to find. Both were corrected before the counts above were taken. A third
error was made and withdrawn in the same session: an external-source sweep
reported eighteen absent URLs, all of which were a trailing backtick captured by
the extraction. Counts in this package should be re-derived by re-running the
detectors rather than cited from this table.

## Traceability

- [Audits index](../README.md)
- [Documentation protocol](../../../00.agent-governance/policies/documentation-protocol.md)
- [Stage 99 Registry](../../../99.templates/registry.json)
- [Spec 137 Task](../../../03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md)

## Related Documents

- [References index](../../README.md)
- [Bootstrap policy](../../../00.agent-governance/policies/bootstrap.md)
