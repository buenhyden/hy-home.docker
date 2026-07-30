---
status: active
artifact_id: task:2026-07-28-target-surface-delta-convergence
artifact_type: task
parent_ids:
  - spec:135-target-surface-delta-convergence
  - plan:2026-07-28-target-surface-delta-convergence
---

# Task: Target Surface Delta Convergence

## Overview

This ledger records actual implementation, verification, commit, disposition,
review, and closure evidence for Spec 135. The implementation design and
expected commands remain in the
[Plan](../plans/2026-07-28-target-surface-delta-convergence.md).

Evidence in this ledger is bounded and value-free. It must not contain secret
values, credentials, tokens, auth files, shell history, raw workflow logs,
unbounded command output, or inferred remote failure causes.

## Inputs

- [Spec 135](../../03.specs/135-target-surface-delta-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-28-target-surface-delta-convergence.md)
- Feature base
  `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`
- Spec 133 comparison commit
  `63039b5b0b20c99a10aae7162627afefcd7a1d8b`
- Isolated branch `feat/135-target-surface-delta-convergence`
- Isolated worktree
  `.worktrees/target-surface-delta-convergence`
- Primary roots `.github`, `archive`, `examples`, `infra`, `projects`,
  `scripts`, `secrets`, and `tests`

## Goals and Non-goals

The goal is to close TSDC-001 through TSDC-017 through six top-level tasks and
independently revertible logical-unit commits, complete successor-delta
classification, whole-surface validation, document and static-version
convergence, typed local workflow/QA controls, reconciled canonical evidence,
and two independent reviews per implementation unit.

Remote mutation, live Compose or deployment work, push, pull request, merge,
workflow dispatch, secret-value access, raw-log access, and direct all-files
pre-commit are not authorized by this ledger.

## Scope and Change Boundaries

Primary changes are restricted to the eight target roots. Direct-impact paths
are allowed only when an approved target change would otherwise leave a Stage
00, Stage 04, Stage 05, Stage 90, Stage 99, validator, generator, test, or
current-memory consumer false or broken.

Native file formats remain native. README files remain path-profiled and
frontmatter-free by default. Typed Markdown uses only registered metadata.
Root content archives and Stage 98 SDLC archives remain distinct. Secret work
is limited to tracked names, paths, and redacted metadata.

Static registry and documentation synchronization to existing Compose image
declarations is in scope. Starting, stopping, probing, deploying, rebuilding,
or otherwise mutating services is out of scope.

Tracked GitHub workflow, ruleset-desire, validator, and governance changes are
in scope after Plan approval. Remote GitHub configuration and execution remain
read-only observation only.

## Approval Evidence

- The user approved the investigation and successor Spec 135 design.
- The user explicitly allowed subagents and selected Subagent-Driven
  execution.
- The user selected local tracked GitHub changes with read-only remote
  observation; remote synchronization requires separate approval.
- The user authorized destructive and protected local changes within the
  approved Plan boundary, subject to consumer, provenance, rollback, tests,
  and review.
- The user approved this exact Plan and Task ledger on 2026-07-28. The six
  local implementation tasks, protected local targets, and Plan-bounded
  destructive convergence are authorized through the selected
  Subagent-Driven method.
- On 2026-07-29 the user approved the revised typed CI gate design recorded at
  Spec commit `a0f91bb5`. That approval authorizes Revision R1 Plan drafting
  only; it does not reopen the consumed five-round Task 4 implementation loop.
- On 2026-07-29 the user explicitly approved the exact revised Plan. That
  Revision R1 approval did not survive its exhausted two-attempt Plan review
  loop. Revision R2 requires a new explicit approval followed by fresh
  specification and quality/security C0/I0 reviews; it does not authorize
  remote, runtime, secret-payload, dependency-installation, controlled-wrapper,
  or direct pre-commit actions.
- On 2026-07-29 the user explicitly approved Revision R2 at Plan commit
  `7d36fe3b`. Local T-TSDC-004R implementation remains gated by fresh
  independent specification and quality/security C0/I0 Plan reviews. The
  first review attempt required a bounded correction. The final corrected
  reviews over `e97b7966..8f82e88b` each returned C0/I0/M0 and activated local
  Plan-bounded implementation. This approval does not authorize remote,
  runtime, secret-payload,
  dependency-installation, controlled-wrapper, or direct pre-commit actions.
- On 2026-07-29 and 2026-07-30 the user repeatedly instructed the controller
  to continue the approved local Subagent-Driven work. That continuation does
  not waive exact-path, independent-review, runtime, remote, secret, wrapper,
  or direct-pre-commit gates.
- On 2026-07-30 the user approved T-TSDC-004R-4AC as one Plan-only bounded
  successor from exact checkpoint `997719ff`. It is designed to close only the
  load-bearing 4AB Plan-review findings: complete exact-plus-embedded candidate
  union, unresolved named and positional dynamic targets with positive and
  no-relevant-sibling outcomes, and separated plus equals long
  `--split-string` transition proof. The Plan and this Task ledger are the
  only authorized checkpoint paths. Implementation, test execution, Wave C,
  runtime, remote, dependency, secret, direct pre-commit, controlled-wrapper,
  and Graphify-update authority remain blocked until two fresh independent
  Plan reviews return `C0/I0/M0` and their Task-only evidence checkpoint is
  committed.
- The 4AC Plan committed as `5bc5ab85`. Fresh independent reviewers inspected
  exact immutable range `997719ff..5bc5ab85`. Specification returned
  `C0/I0/M0`, `SPEC_COMPLIANCE YES`, and `IMPLEMENTATION_READY YES`;
  quality/security returned `C0/I1/M1`, `QUALITY_SECURITY FAIL`, and
  `IMPLEMENTATION_READY NO`. The no-correction 4AC Plan loop is therefore
  exhausted. No accepted Plan-review evidence, implementation attempt, test
  execution, Wave C, Tasks 5–6, or whole-branch authority follows.
- On 2026-07-30 the user approved T-TSDC-004R-4AD as one Plan-only bounded
  successor from exact checkpoint
  `3510e9944655ee89077a295712e759d116e2e87f`. It preserves the accepted 4AC
  parser, test, scope, and validation design. Its only semantic delta is to
  copy each pair of reviewer-reported full hashes into the canonical review
  matrix and require every accepted or rejected terminal evidence session,
  plus Task 4.5 re-entry, to extract that attestation and independently prove
  the full predecessor chain, distances, exact scopes, modes, and clean state.
  Plan and Task are the only authorized checkpoint paths. Implementation,
  tests, Wave C, runtime, remote, dependency, secret, direct pre-commit,
  controlled-wrapper, and Graphify-update authority remain blocked until two
  fresh independent 4AD Plan reviews return `C0/I0/M0` and their Task-only
  accepted evidence checkpoint is committed.
- The 4AD Plan committed as
  `9de469a52c4b05d2490d36d37b95b1277442f725`. Both fresh reviewers reported
  exact range
  `3510e9944655ee89077a295712e759d116e2e87f..9de469a52c4b05d2490d36d37b95b1277442f725`.
  Specification returned `C0/I2/M1`, `SPEC_COMPLIANCE NO`, and
  `IMPLEMENTATION_READY NO`; quality/security returned `C0/I0/M0`,
  `QUALITY_SECURITY PASS`, and `IMPLEMENTATION_READY YES`. The no-correction
  4AD Plan loop is exhausted. No accepted Plan-review evidence,
  implementation, test execution, Wave C, Tasks 5–6, or whole-branch
  authority follows.
- On 2026-07-30 the user approved T-TSDC-004R-4AE as one Plan-only bounded
  successor from exact checkpoint
  `5644c4a301e38d3f0c32efe99e80f879df6e1ac8`. It changes only exact
  seven-cell review-range parsing, the missing predecessor path/range and
  base-mode assertions in three sessions, and current-state synchronization.
  Plan and Task are the only authorized checkpoint paths. Implementation,
  tests, Wave C, runtime, remote, dependency, secret, direct pre-commit,
  controlled-wrapper, and Graphify-update authority remain blocked until two
  fresh independent 4AE Plan reviews return `C0/I0/M0` and their accepted
  Task-only evidence checkpoint is committed.
- The 4AE Plan committed as
  `8abea15a1ebafdf607be801789a409e6f312c099`. Both fresh reviewers reported
  exact range
  `5644c4a301e38d3f0c32efe99e80f879df6e1ac8..8abea15a1ebafdf607be801789a409e6f312c099`.
  Specification returned `C0/I0/M0`, `SPEC_COMPLIANCE YES`, and
  `IMPLEMENTATION_READY YES`; quality/security returned `C0/I2/M0`,
  `QUALITY_SECURITY FAIL`, and `IMPLEMENTATION_READY NO`. The quality review
  found that a duplicate no-leading-pipe GFM row can evade candidate counting
  and that downstream sessions do not reassert bound authority-subject
  uniqueness. The no-correction 4AE Plan loop is exhausted. No accepted
  Plan-review evidence, implementation, test execution, Wave C, Tasks 5–6, or
  whole-branch authority follows.
- On 2026-07-30 the user approved T-TSDC-004R-4AF as one Plan-only repair from
  rejected 4AE evidence `8cacc463`. It counts optional-leading-pipe first-cell
  candidates, retains canonical-row validation, and repeats fixed whole-line
  subject uniqueness for every bound authority. Implementation and tests remain
  blocked pending fresh independent Plan reviews and accepted Task-only evidence.
- No current approval authorizes
  `scripts/validation/run-agent-precommit-all-files.sh`. Any future approval
  is one exact attempt from one clean committed checkpoint.

Rollback is one logical task commit at a time after exact-range review. It
never uses `git reset --hard`, discards unrelated user changes, or attempts a
remote/runtime rollback for surfaces this wave does not mutate.

## Work Breakdown

| Task ID | Description | Type | Requirements | Validation owner | Implementation owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-TSDC-001 | Establish successor manifest and whole-surface contract | contract/data | TSDC-001–003, 007, 009 | delta contract tests and advisory checker | fresh Task 1 implementation agent | completed |
| T-TSDC-002 | Converge README, typed example, archive, and secret inventory | docs/governance | TSDC-003–009 | metadata, target, links, alignment | Task 2 documentation-surface implementation agent | completed |
| T-TSDC-003 | Reconcile static versions and verified active lifecycle drift | infra-support/docs | TSDC-003, 008–009 | version, hardening, supply-chain checks | Task 3 static-version implementation agent | completed |
| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation agent; original agents remain historical | active; 4AF Plan review pending |
| T-TSDC-005 | Reconcile canonical audit and remote observation evidence | evidence/docs | TSDC-015–016 | audit semantic, generators, links | fresh implementer after accepted 4AF implementation-review R | blocked pending accepted 4AF implementation-review R |
| T-TSDC-006 | Promote blocking enforcement and close reviews | closure/QA | TSDC-001–017 | final ladder and whole-branch reviews | fresh closure implementer after Tasks 1–5 | pending |

Tasks are serial at their commit/review boundaries. A task may not advance
until its implementation is committed, the Task ledger is current, and a
distinct specification reviewer plus a distinct quality/security reviewer
have no unresolved Critical or Important findings.

## Work Log

| Date | Unit | Actor | Evidence summary |
| --- | --- | --- | --- |
| 2026-07-28 | Bootstrap | Controller | Loaded Stage 00 bootstrap, provider, and memory contracts; inspected root and isolated-worktree state; kept root `main` clean. |
| 2026-07-28 | Discovery | Controller plus read-only inventory agents | Counted 474 target paths and 82 Markdown/MDX files; identified 102 post-closure target changes, 11 exact heading drifts, 26 shared-agent-policy README copies, one duplicated data README purpose, one typed example ambiguity, one redacted secret inventory omission, six static version drifts, and CI trigger/dependency gaps. |
| 2026-07-28 | External verification | Controller | Verified official GitHub workflow/security/protection, Actions runtime, pre-commit, YAML frontmatter, CommonMark, and GFM sources. Confirmed the pinned pre-commit composite uses mutable `actions/cache@v4`. |
| 2026-07-28 | Remote observation | Controller | Read sanitized repository/run/protection metadata only. Observed 12 remote required contexts versus 16 local desired IDs and two recent failed runs; root causes remain unverified. No remote state changed. |
| 2026-07-28 | Spec | Controller | Wrote and committed Spec 135 as `e828745a`; scoped metadata, Markdown, alignment, and diff checks passed. User approved continuing from the Spec. |
| 2026-07-28 | Plan/Task draft | Controller | Activated the approved Spec and drafted this six-task TDD/Subagent-Driven Plan and evidence ledger. Implementation remains pending exact Plan approval. |
| 2026-07-28 | Execution approval | User / Controller | User approved the exact Plan and Task ledger. Plan and Task transitioned to `active`; remote/runtime mutation and the controlled all-files wrapper remain separately gated. |
| 2026-07-28 | T-TSDC-001 RED | Task 1 implementation agent | Added 13 focused tests before implementation. The first run produced 1 passing predecessor-integrity test and 12 expected missing-module errors. No product implementation existed. |
| 2026-07-28 | T-TSDC-001 implementation | Task 1 implementation agent | Added the duplicate-safe, size-bounded, no-follow successor parser, exact dataclasses, Git-delta union, whole-target inventory, advisory evidence gates, create-only bootstrap, deterministic summary, thin CLI, repository-contract/local-QA routing, and registered generated owner. The manifest computes 105 rows: 96 preserve, 9 update, 0 migrate/delete, and 105 pending review pairs. |
| 2026-07-28 | T-TSDC-001 direct-impact expansion | Controller / Task 1 implementation agent | The generated-output registry exposed one stale exact oracle outside the initial file list. The controller explicitly expanded ownership only to `tests/validation/test_document_metadata.py`; the exact new summary-to-checker pair was added without unrelated refactoring. |
| 2026-07-28 | T-TSDC-001 specification review | Distinct specification reviewer | Reported C0/I4/M2: the surface class was not closed or path-derived; blocking mode did not require both pass verdicts on every row; README registry failure did not fail closed; disposition and destructive evidence semantics were incomplete; the destructive-validator negative assertion was omitted; and generic preserve rationales plus speculative consumer edges were not factual enough. Review remains unresolved pending remediation re-review. |
| 2026-07-28 | T-TSDC-001 quality/security review | Distinct quality/security reviewer | Reported C0/I1/M2: summary overwrite lacked descriptor-relative no-follow and race-safe replacement checks; untracked coverage was not isolated from staged/unstaged coverage; and canonical paths admitted control or Markdown-injection characters. Review remains unresolved pending remediation re-review. |
| 2026-07-28 | T-TSDC-001 remediation RED | Task 1 implementation agent | Added focused regressions before remediation. The combined C/I run emitted 12 failing markers; isolated witnesses included one missing `delta-surface-class-invalid`, four registry fail-closed cascade failures, one unsafe profile-name failure, and 98 path-specific rationale/consumer-proof failures against the old manifest. |
| 2026-07-28 | T-TSDC-001 remediation GREEN | Task 1 implementation agent | Closed surface classes, effective blocking review gates, one-finding README registry failure, typed disposition/evidence rules, tracked regular-file evidence checks, descriptor-relative summary overwrite, explicit untracked coverage, injection-safe canonical paths, factual preserve rationales, and proven consumer mappings. Intermediate focused suites passed 6/6 and 5/5; final successor and predecessor suites passed 25/25 and 40/40. |
| 2026-07-28 | T-TSDC-001 second fresh re-review | Fresh specification and quality/security reviewers | Reported combined C0/I3/M0: advisory mode returned success for structural contract findings; free-form manifest fields admitted secret-like payloads before summary/diagnostic gating; and bootstrap parent creation could traverse a symlink outside the repository. Reviews remain unresolved pending the second remediation re-review. |
| 2026-07-28 | T-TSDC-001 second remediation RED | Task 1 implementation agent | The advisory structural mutation failed 1/1 because a missing row returned 0 instead of 1 while valid pending review remained advisory-safe. The secret-like matrix failed all 20 adversarial fields while the safe full-SHA witness passed. The symlink-parent bootstrap witness returned 0 instead of 2 and created the outside file. |
| 2026-07-28 | T-TSDC-001 second remediation GREEN | Task 1 implementation agent | Separated structural contract findings from blocking-only review findings; added conservative value-free parsing across path, label, list, and top-level fields; and replaced lexical bootstrap creation with bounded descriptor-relative no-follow traversal, creation, identity checks, and exclusive regular-file write. Focused advisory/blocking, secret/safe-evidence, and bootstrap suites passed 2/2, 3/3, and 2/2. |
| 2026-07-28 | T-TSDC-001 second remediation final gates | Task 1 implementation agent | After aligning the prior unknown-surface test with the new pre-diagnostic secret rejection, the exact affected set passed 4/4. Production advisory returned 0; blocking returned 1 with 105 specification and 105 quality pending findings. Ruff, Python compile, changed metadata 1/0, Markdown stdin 1/0, and diff hygiene passed. A longer successor run was stopped after exposing that superseded test expectation and was not repeated after the exact affected set passed. |
| 2026-07-28 | T-TSDC-001 third focused re-review | Fresh reviewer | Reported C0/I1/M0: advisory mode correctly tolerated `pending` but also returned success for an explicit `fail` specification or quality verdict. Reviews remain unresolved pending remediation re-review. |
| 2026-07-28 | T-TSDC-001 third remediation RED | Task 1 implementation agent | A bounded CLI fixture preserved pending advisory success and pending blocking failure, then supplied matching summaries for independent specification and quality `fail` mutations. Both subcases returned advisory 0 instead of 1: one test emitted two expected failures in 4.020 seconds. |
| 2026-07-28 | T-TSDC-001 third remediation GREEN | Task 1 implementation agent | Introduced explicit pending, passing, and failed verdict semantics. Failed specification and quality verdicts now emit distinct value-free contract findings in advisory and blocking modes, while pending remains advisory-safe and blocking-unsafe. The focused regression passed 1/1 in 4.989 seconds. |
| 2026-07-28 | T-TSDC-001 third remediation final gates | Task 1 implementation agent | The three affected CLI regressions passed 3/3 in 13.526 seconds; after making failed-field findings independent of a peer verdict's validity, the focused regression re-passed 1/1 in 4.485 seconds. Production advisory returned 0; production blocking returned 1 with exactly 105 specification and 105 quality pending findings and no other codes. Ruff, Python compile, one-file Markdown stdin lint, and diff hygiene passed. No broad suite or all-files pre-commit command ran. |
| 2026-07-28 | T-TSDC-001 final specification re-review | Fresh independent specification reviewer | Exact range `72eef68c..43f78ad5`: C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES. |
| 2026-07-28 | T-TSDC-001 final quality/security re-review | Fresh independent quality/security reviewer | Exact range `72eef68c..43f78ad5`: C0/I0/M0; APPROVED; COMMIT_READY YES. Task 1 is complete; per-row manifest verdicts remain pending for Task 6 blocking promotion. |
| 2026-07-28 | T-TSDC-002 RED | Task 2 documentation-surface implementation agent | Before implementation, the three sample-fixture contracts failed 3/3; the heading and shared-policy checks emitted 37 failures across 11 and 26 path subcases; the data, secret, archive, and local-constraint group ran four tests with seven expected failures and one archive pass; and the copied-template check emitted 15 expected subcase failures across five affected READMEs. |
| 2026-07-28 | T-TSDC-002 document implementation | Task 2 documentation-surface implementation agent | Registered the exact draft Service fixture on the existing role with the two approved domain parents; normalized 11 heading IDs; replaced 26 copied policy sections with one pointer to both Stage 00 owners while preserving local commands and constraints; collapsed the data tier to one folder index; and added only the SurrealDB directory path to the secret inventory. The already-valid Windows content tombstone remained byte-unchanged. |
| 2026-07-28 | T-TSDC-002 direct-impact expansion | Controller / Task 2 documentation-surface implementation agent | The 31 newly changed target paths made the Task 1 fixed nine-update oracle stale. The controller expanded ownership only to `tests/validation/test_target_surface_delta_contracts.py`; the test now asserts the exact Task 2 path set, 136-row disposition counts, pending verdicts, and explicit import or runner consumer relationships without refactoring the delta library. |
| 2026-07-28 | T-TSDC-002 manifest and focused GREEN | Task 2 documentation-surface implementation agent | Added 31 missing non-destructive `update` rows, updated five existing Task 2 rows factually, retained every per-row review verdict as `pending`, and regenerated the summary only through the canonical writer. The manifest now contains 136 rows: 92 preserve, 44 update, 0 migrate/delete. Metadata fixture checks passed 3/3; routing, predecessor/successor, and copied-policy checks passed 7/7; the two exact manifest owner/consumer checks passed 2/2; production advisory validation has zero findings. |
| 2026-07-28 | T-TSDC-002 lifecycle coupling RED and expansion | Controller / Task 2 documentation-surface implementation agent | The combined focused run exposed that a target-suite aggregate still invoked the predecessor lifecycle checker, which emitted exactly `manifest-target-parent-ids-mismatch`, `manifest-target-profile-invalid`, and `manifest-target-status-mismatch` for the successor-owned sample fixture. The controller expanded ownership only to `scripts/validation/check-document-corpus-lifecycle.py` and `tests/validation/test_document_corpus_lifecycle.py`. A three-test RED had one expected positive-handoff failure while missing-row, preserve-row, and wrong-current-metadata negatives retained the three-code set. |
| 2026-07-28 | T-TSDC-002 lifecycle handoff GREEN | Task 2 documentation-surface implementation agent | Added a fail-closed handoff limited to the exact sample path, duplicate-safe bounded successor manifest, `update` row, registered existing Service role, exact draft metadata, and exact two domain parents. The three focused tests passed 3/3, the predecessor manifest CLI returned zero findings, and the formerly failing aggregate witness passed 1/1. The two direct-impact rows are now `update`; canonical summary regeneration reports 136 rows: 90 preserve, 46 update, 0 migrate/delete, with all verdict pairs pending. |
| 2026-07-28 | T-TSDC-002 lifecycle compatibility GREEN | Task 2 documentation-surface implementation agent | A focused class run exposed two existing predecessor-mutation expectations that the first handoff predicate had bypassed. The predicate was narrowed to the exact immutable predecessor row and pinned successor witness; the five directly affected tests passed 5/5, then all 34 `ManifestValidationTests` passed in 337.962 seconds. A final read-bound hardening uses a no-follow descriptor chain with a 2 MiB plus one-byte cap; the five affected tests, Ruff, compile, and predecessor CLI re-passed. |
| 2026-07-28 | T-TSDC-002 final bounded gates | Task 2 documentation-surface implementation agent | The target, delta, and metadata modules passed 48/48 in 141.657 seconds, 30/30 in 145.831 seconds, and 225/225 in 109.752 seconds. Metadata contract and changed modes, target and advisory CLIs, alignment, current traceability, Ruff, compile, changed Markdown lint, generated-summary freshness, and diff hygiene passed. The Plan-stated `scripts/governance/validate-cross-links.sh` path is absent in this checkout and returned 127; no substitute claim was invented, while the tracked current traceability gate independently passed 46 pairs with zero failures. |
| 2026-07-28 | T-TSDC-002 quality review finding | Distinct quality/security reviewer | Reported C0/I1/M0: the lifecycle handoff parsed only a subset of the successor document and row, so failed verdicts or malformed, incomplete, or false evidence outside that subset could waive the three predecessor equality findings. Remediation and re-review remained required. |
| 2026-07-28 | T-TSDC-002 quality remediation RED | Task 2 documentation-surface implementation agent | Added one bounded 19-subcase rejection matrix before production changes. Seventeen cases failed in 23.101 seconds for explicit failed verdicts, false top-level witnesses, missing or wrong row evidence, extra destructive update evidence, and malformed top-level keys; the old exact-key check already rejected the two row-key mutations. A separate Task 6 compatibility witness then failed all three `pass/pass`, `pass/pending`, and `pending/pass` cases in 9.730 seconds. |
| 2026-07-28 | T-TSDC-002 quality remediation GREEN | Task 2 documentation-surface implementation agent | Removed the duplicate partial successor parser and delegated bounded no-follow loading, duplicate-key rejection, full document parsing, and advisory structural validation to `target_surface_delta_contract.py`. The local predicate now checks only the immutable predecessor row plus the exact sample handoff evidence, accepts each review verdict only in `{pending, pass}`, and rejects canonical failed-review findings. The 19-subcase matrix passed in 44.178 seconds; the verdict matrix plus rejection matrix passed 2/2 in 52.765 seconds; and the final existing-five plus new-two lifecycle bundle passed 7/7 in 90.381 seconds. |
| 2026-07-28 | T-TSDC-002 quality remediation gates | Task 2 documentation-surface implementation agent | Canonical delta production-manifest and failed-verdict tests passed 2/2 in 6.507 seconds; the predecessor aggregate witness passed 1/1 in 5.134 seconds; predecessor CLI and delta advisory returned zero findings. Targeted Ruff, Python compile, Task-ledger Markdown and metadata, and diff hygiene passed. The remediation changed only the lifecycle checker, its test, and this Task ledger. |
| 2026-07-28 | T-TSDC-002 final specification review | Fresh independent specification reviewer | Exact range `78af8462..b28764a9`: C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES. |
| 2026-07-28 | T-TSDC-002 final quality/security re-review | Fresh independent quality/security reviewer | Exact range `78af8462..b28764a9`: C0/I0/M0; APPROVED; COMMIT_READY YES. Task 2 is complete; all successor manifest row verdicts remain pending for Task 6 promotion. |
| 2026-07-28 | T-TSDC-003 RED | Task 3 static-version implementation agent | Added the focused version contract before production edits. The first run emitted exactly six registry-to-Compose subtest failures. The bounded expansion then emitted the same six failures plus one stale independent Keycloak hardening literal failure; direct-current-document and lifecycle preserve/negative-classification tests already passed. Independent commands confirmed `changes=6` and the fail-fast hardening checker stopped at the stale Keycloak expectation. |
| 2026-07-28 | T-TSDC-003 generated and document implementation | Task 3 static-version implementation agent | Ran the canonical version sync in write mode for Traefik, Keycloak, PostgreSQL, Prometheus, Alloy, and Ollama, then ran the canonical provenance generator. Updated exactly nine current infra READMEs, five direct-impact Stage 05 documents, and exact current-version descriptions in the repository checker. Compose and runtime declarations remained unchanged. |
| 2026-07-28 | T-TSDC-003 hardening follow-up RED/GREEN | Controller / Task 3 static-version implementation agent | After the Keycloak repair, the full fail-fast hardening run first exposed a predecessor Dozzle literal expecting `v10.6.7` while Compose declares `v10.6.11`. The controller expanded only the already-owned hardening script and focused test. One static regression failed on the old literal, then passed after the checker resolved the Dozzle service image from Compose; the Keycloak image remains resolved from the curated registry. No free-standing current or stale Dozzle version was added. |
| 2026-07-28 | T-TSDC-003 manifest and oracle expansion | Controller / Task 3 static-version implementation agent | Advisory validation identified exactly four new Task 3 target rows. The manifest added those four as non-destructive `update` rows and retained all verdicts as `pending`. The controller expanded ownership only to the existing repository manifest oracle after it failed `136 != 140`; the GREEN oracle asserts the exact four Task 3 paths, canonical owners, 50-update set, 90-preserve set, pending verdicts, and zero destructive disposition. The canonical summary writer regenerated the 140-row summary. |
| 2026-07-28 | T-TSDC-003 final bounded gates | Task 3 static-version implementation agent | Focused tests passed 7/7 and the exact repository manifest oracle passed 1/1. Sync/provenance checks, all 11 hardening tiers, 13 supply-chain fixtures, successor advisory, document alignment, Ruff, Python compile, Bash syntax, ShellCheck, changed-document metadata, Markdown, and staged/unstaged diff hygiene passed. Exact scope comparison found 23 expected paths, zero unexpected paths, zero missing paths, and zero Compose files. No broad aggregate ran. |
| 2026-07-28 | T-TSDC-003 independent reviews | Independent specification reviewer / Independent quality-security reviewer | Each review reported C0/I1/M0 against `b1e62873..5460e5fc`. The specification finding required every one of the nine infra and five Stage 05 direct-current mappings to reject its exact stale predecessor value, including an old-plus-new negative witness. The quality/security finding showed that the Compose image resolver accepted ambiguous or partial YAML and that Keycloak and Dozzle still depended on substring assertions. Both Important findings required remediation and re-review. |
| 2026-07-28 | T-TSDC-003 review remediation RED | Replacement Task 3 remediation implementer | The direct-document helper reports `stale version present` for an old-plus-new witness; the 14 current documents were already clean, so the new production absence oracle passed immediately. Before resolver implementation, the exact four-method hardening slice failed 17 times: both static exactness contracts, all three valid scalar subcases, and all twelve initial invalid-fixture diagnostic subcases. |
| 2026-07-28 | T-TSDC-003 review remediation GREEN | Replacement Task 3 remediation implementer | Added exact stale-absence coverage for all 14 current-document mappings and a bounded internal resolver mode with no-follow regular-file reads, a 1 MiB cap, strict duplicate/shape/scalar rejection, a complete safe Docker image grammar, and value-free diagnostics. Keycloak now compares the exact resolved Compose image with the registry image; Dozzle relies on resolver success without a substring assertion. The final focused module passed 11/11, including quoted/unquoted valid images, thirteen ambiguous/unsafe YAML fixtures, and symlink/directory/oversize rejection. Sync/provenance, all 11 hardening tiers, 13 supply-chain fixtures, successor advisory, Ruff, Python compile, Bash syntax, ShellCheck, and diff hygiene passed. Independent re-reviews remain pending. |
| 2026-07-28 | T-TSDC-003 remediation review | Independent remediation reviewer | Review of `5460e5fc..c04946e5` returned C0/I1/M1. The Important finding showed that the unquoted-only sibling boundary let a target without `image` consume a following quoted service's image. The Minor identified one stale Dozzle replacement diagnostic in the repository checker. Remediation and re-review remained required. |
| 2026-07-28 | T-TSDC-003 quoted-service remediation RED/GREEN | Final Task 3 remediation implementer | Four focused methods produced six RED failures: both quoted target forms, both valid quoted-sibling boundaries, and both single/double quoted sibling-image theft witnesses. Mixed quoted/unquoted duplicate targets already rejected. One canonical full-match service-key parser now owns target identity and every sibling boundary; the affected methods pass 4/4 and the full module passes 16/16. The repository diagnostic now names exact Compose value `v10.6.11`. All 11 hardening tiers, sync/provenance, the focused repository static oracle, Bash syntax, scoped ShellCheck, Ruff, Python compile, and diff hygiene pass. Unfiltered ShellCheck on the repository checker retains two pre-existing SC2016 informational findings outside the changed line; warning-or-higher validation passes. Independent re-review remains pending. |
| 2026-07-28 | T-TSDC-003 final remediation review | Independent remediation reviewer | Review of `c04946e5..cce5abb6` returned C0/I2/M1. One Important finding required global uniqueness across every immediate service name after dequoting, not only the requested target. The second required the directly impacted Dozzle README to converge from `v10.6.6` to Compose-current `v10.6.11` with exact current/stale coverage and successor classification. The Minor required replacing the now-known quoted-service remediation commit and review-range placeholders. Final remediation and independent re-review remained required. |
| 2026-07-28 | T-TSDC-003 global-uniqueness and Dozzle RED/GREEN | Final Task 3 remediation implementer | The affected two-method RED failed five times: the Dozzle README reported both `current version absent` and `stale version present`, and all four quoted/unquoted unrelated-sibling duplicate orderings returned success. GREEN derives Dozzle truth from its Compose file, checks the README as the fifteenth direct-current mapping, and rejects any repeated dequoted immediate service name with one value-free diagnostic. The affected slice passes 2/2 and the full focused module passes 17/17. |
| 2026-07-28 | T-TSDC-003 final direct-impact expansion | Controller / Final Task 3 remediation implementer | The controller authorized exactly `infra/11-laboratory/dozzle/README.md` as a direct-impact target. Advisory validation identified only that missing row; the exact repository oracle failed `141 != 140`. Added one factual non-destructive `update` row with the README as canonical owner, the version test as direct consumer, and both review verdicts `pending`. The canonical writer regenerated the summary to 141 rows: 90 preserve, 51 update, 0 migrate/delete. The oracle and advisory checker then passed. |
| 2026-07-28 | T-TSDC-003 final remediation gates | Final Task 3 remediation implementer | Focused version/resolver tests passed 17/17; the exact manifest oracle passed 1/1; successor advisory returned zero findings; all 11 hardening tiers passed; sync reported `changes=0`; provenance was fresh; document alignment reported 674 documents, 5,659 links, 141 operations documents, and zero failures. Changed metadata selected two documents with zero violations; three Markdown inputs, Ruff, Python compile, Bash syntax, ShellCheck, and diff hygiene passed. No Compose, runtime, network, remote, dependency, or pre-commit action ran. Independent final reviews remain pending. |
| 2026-07-29 | T-TSDC-003 final specification review | Fresh independent specification reviewer | Exact full range `b1e62873..60e0313c`: C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES. |
| 2026-07-29 | T-TSDC-003 final quality/security review | Fresh independent quality/security reviewer | Exact full range `b1e62873..60e0313c`: C0/I0/M0; PASS; COMMIT_READY YES. Task 3 is complete; all 141 successor manifest specification/quality verdict pairs remain `pending` for Task 6. |
| 2026-07-29 | T-TSDC-004 RED | Task 4 workflow/QA implementation agent | The CI-wrapper test first failed because `scripts/validation/run-ci-precommit.sh` did not exist. The workflow suite first produced four missing-module errors. Later bounded-reader regressions produced two failures and one error for a parent-directory symlink, a noncanonical workflow path, and a 64-byte short read; the manifest oracle failed `148 != 141`; local routing failed on the missing wrapper-test command; and the repository aggregate identified the new wrapper missing from the exact purpose-folder implementation set. |
| 2026-07-29 | T-TSDC-004 implementation GREEN | Task 4 workflow/QA implementation agent | Added one typed workflow contract and bounded checker for seven workflows, 23 jobs, eight direct Actions, and exactly 16 required-quality job IDs. All direct Actions use registered full SHAs with locally recorded Node 24 manifest evidence. Replaced `pre-commit/action` and the redundant pre-commit Node/npm setup with setup-python, exact `pre-commit==4.6.1`, and a CI-only wrapper. Removed the overlapping inline workflow parser, retained separate Stage 00 assertions, registered tech-stack sync as non-gating automation, and routed the focused checker exactly once through the repository aggregate. |
| 2026-07-29 | T-TSDC-004 manifest expansion | Controller / Task 4 workflow/QA implementation agent | Advisory validation identified exactly seven new Task 4 target paths. The controller expanded direct-impact ownership only to `tests/validation/test_target_surface_delta_contracts.py`; its RED oracle fixed 148 total, 89 preserve, 59 update, and zero destructive rows plus path-specific owner, consumer, and pending-verdict assertions for the seven new rows and the routing test's preserve-to-update transition. The canonical writer alone regenerated the summary; advisory and the exact oracle then passed. |
| 2026-07-29 | T-TSDC-004 bounded gates | Task 4 workflow/QA implementation agent | Focused workflow tests passed 9/9; the fake-binary CI-wrapper test, focused CLI, delta advisory, actionlint, scoped ShellCheck, Ruff, Python compile, Bash syntax, and diff hygiene passed. Governance routing passed 33 Task 4-relevant tests and failed only the isolated predecessor/environment witness `AGC-DEPENDENCY-MISSING path=html5lib location=validation-runtime`. The repository aggregate passed the Task 4 workflow, Stage 00, QA-routing, and repaired script-usage sections; its remaining failures are separately recorded predecessor/generated-evidence limitations. No real pre-commit, network, remote, provider, runtime, service, dependency installation, cache, credential, or secret-payload action ran. Independent reviews remain pending. |
| 2026-07-29 | T-TSDC-004 quality finding | Independent quality/security reviewer | Reported one Important finding against `6fabbf05..faaa2eb2`: PyYAML can resolve an unquoted top-level `on` as boolean `True` while retaining a quoted `on` as a separate string key. The original normalization silently ignored `True` when the string key existed, so a contract-matching quoted trigger could conceal an unquoted forbidden trigger. Narrow remediation and re-review were required. |
| 2026-07-29 | T-TSDC-004 trigger-key remediation RED/GREEN | Task 4 workflow/QA implementation agent | RED failed both required orderings with `WorkflowContractError not raised`: quoted contract-matching `on` followed by unquoted malicious `on`, and unquoted contract-matching `on` followed by quoted malicious `on`. The normal unquoted trigger and exact duplicate quoted-key witnesses already passed. GREEN adds one explicit top-level semantic-key normalizer: boolean `True` alone becomes string `on`; coexistence with string `on` raises value-free `workflow-trigger-key-ambiguous`; unrelated boolean `False` remains unchanged. The full focused suite passes 11/11. Re-review remains pending. |
| 2026-07-29 | T-TSDC-004 permission quality finding | Independent quality/security reviewer | Reported one additional Important finding after the trigger-key remediation: the workflow and its YAML contract could widen the same permission scope together because no independent least-privilege invariant constrained either source. Co-mutated required-quality and non-gating permission ownership required narrow remediation and re-review. |
| 2026-07-29 | T-TSDC-004 permission remediation RED | Task 4 workflow/QA implementation agent | One seven-subcase required-quality matrix failed all seven witnesses because validation returned no finding for co-mutated top-level `contents: write`, job-level `contents: write`, four added write scopes, or an added zizmor write scope. |
| 2026-07-29 | T-TSDC-004 permission remediation GREEN | Task 4 workflow/QA implementation agent | Added an immutable code-owned permission baseline for all seven workflow paths and 23 job owners. CI top-level and 15 ordinary jobs are exact `contents: read`; zizmor has its exact three-scope map. Six non-gating workflows retain only their approved read/write owners, and the changelog job requires permission-key absence rather than explicit null. Required co-mutations pass 7/7 fail-closed witnesses, six non-gating co-mutations pass 6/6, the exact-owner positive passes, and the full workflow suite passes 14/14 with value-free `workflow-permission-baseline-invalid` diagnostics. Re-review remains pending. |
| 2026-07-29 | T-TSDC-004 permission remediation gates | Task 4 workflow/QA implementation agent | Workflow tests passed 14/14; the focused CLI reported 7 workflows, 23 jobs, and eight Actions; the three affected routing tests, actionlint, Ruff, Python compile, ledger Markdown, and diff hygiene passed. No real pre-commit, network, remote, provider, runtime, service, dependency, cache, credential, or secret action ran. |
| 2026-07-29 | T-TSDC-004 full-range review findings | Independent specification and quality/security reviewers | Full range `6fabbf05..20676dc3` returned specification C0/I1/M0 and quality/security C0/I4/M1. Open Important findings cover direct and transitive umbrella reruns, alternate boolean trigger-key spellings, exact Action registry plus local-Action policy, four-way required-job coupling, and repository-metadata base/preflight/order assertions. The Minor identified stale review-range and permission-remediation commit placeholders. Fix round 3/5 and independent re-review are required. |
| 2026-07-29 | T-TSDC-004 ownership-gap remediation RED | Task 4 workflow/QA implementation agent | Five focused test methods emitted 15 expected failures before production edits: four current direct umbrella reruns remained present; wrapped direct and transitive semantic-owner probes returned no ownership finding; `true`, `yes`, and `ON` trigger keys raised no error; jointly registered ninth and local Actions returned no dedicated finding; a mutated governance required-gate row returned 0; and metadata base binding, preflight, and ordering mutations each returned 0. |
| 2026-07-29 | T-TSDC-004 ownership-gap remediation GREEN | Task 4 workflow/QA implementation agent | Removed four direct `repo-contracts` reruns and the aggregate hardening/eval reruns while retaining their independent CI and local-QA owners. Added bounded aggregate-aware semantic ownership, an exact eight-identity Action registry baseline, explicit local-Action rejection, fail-closed alternate boolean trigger-key handling, exact governance-table coupling, and exact repository-metadata base/preflight/order assertions. The five focused methods pass 5/5, the workflow suite passes 17/17, and Stage 00 mutation coverage passes 4/4. Independent re-review remains pending. |
| 2026-07-29 | T-TSDC-004 ownership-gap remediation gates | Task 4 workflow/QA implementation agent | Focused CLI reported 7 workflows, 23 jobs, and eight Actions; three affected routing tests, the exact 148/89/59/0 manifest oracle, advisory delta, actionlint, warning-level ShellCheck, Ruff, Python compile, Bash syntax, both changed Markdown inputs, and diff hygiene passed. The full routing module passed 35/36 with only the known validation-runtime `html5lib` dependency absence. No real pre-commit, network, remote, provider, runtime, service, dependency installation, cache, credential, or secret action ran. |
| 2026-07-29 | T-TSDC-004 transitive-ownership review findings | Independent specification and quality/security reviewers | Review through `b07b0f449d75162051c1b66a11e606c59cc17891` kept TSDC-012 open because the repository aggregate still reran two supply-chain semantic gates that were absent from ownership registration. Quality review additionally found direct-executable, variable/wrapper, quoted-data, and quoted-heredoc scanner bypasses plus missing continuous CI/local routing for the governance and eval mutation modules. Narrow fix round 4/5 and independent re-review are required. |
| 2026-07-29 | T-TSDC-004 transitive-ownership remediation RED | Replacement Task 4 remediation implementer | Before production edits, four focused methods produced 13 expected failures: four missing code-owned semantic owner relationships, the two remaining aggregate supply-chain reruns, two unregistered supply-chain duplicate probes, five shell grammar/data/heredoc mutations, and the missing CI/local control-plane unittest owners. Comment and real-heredoc data negatives already remained non-executable. |
| 2026-07-29 | T-TSDC-004 transitive-ownership remediation GREEN | Replacement Task 4 remediation implementer | Removed the aggregate policy and summary reruns; registered an exact code-owned baseline of 20 semantic commands across the unchanged 16 required jobs; and added shell-aware bounded lexical handling for direct executables, canonical interpreters/wrappers, variables, comments, quoted data, and heredocs. Governance routing tests are owned only by `repo-contracts`, eval mutation tests only by `agent-output-eval-fixture-gate`, and one shared local function owns each corresponding local command. The focused RED set passes 4/4, workflow tests pass 20/20 including four workflow/contract co-mutations, eval tests pass 38/38, and Stage 00 mutations pass 4/4. Independent re-review remains pending. |
| 2026-07-29 | T-TSDC-004 transitive-ownership remediation gates | Replacement Task 4 remediation implementer | Focused CLI remains exactly 7 workflows, 23 jobs, and eight Actions; the exact manifest remains 148/89/59/0 with every review pair pending. Actionlint, warning-level ShellCheck, Ruff, Python compile, Bash syntax, local inventory, advisory delta, Markdown, and diff hygiene pass. Full governance routing remains 35/36 only because local `html5lib` is absent; CI installs it from the existing requirements file. No broad aggregate, real pre-commit, Agent wrapper, network, remote, runtime/service/Compose, dependency/cache installation, credential, or secret-payload action ran. |
| 2026-07-29 | T-TSDC-004 final semantic-resolution review findings | Final replacement Task 4 remediation implementer | Review through `ba93483c32d28f543f85f86e39a4daad1844fb1e` found that the round-4 scanner still treated each physical workflow line independently, did not recursively resolve aggregate-owned helper programs, accepted unresolved executable variables and unsafe shell control forms, compared non-script commands as raw text, and did not prove direct-executable provenance. Command substitution, `eval`, shell `-c`, `source`, path aliases, heredoc interpolation, helper cycles or resource overruns, and direct untracked, non-executable, unsupported-shebang, or symlink entries therefore required a final fail-closed remediation. The round-4 commit placeholder also remained stale. |
| 2026-07-29 | T-TSDC-004 final semantic-resolution remediation RED | Final replacement Task 4 remediation implementer | Before production edits, eight focused methods produced 29 assertion failures: six complete-program literal/dynamic-variable cases, three canonical non-script wrapper/continuation cases, seven shell-control/substitution/path-alias cases, two unquoted-heredoc cases, three literal-helper recursion/cycle cases, four helper depth/file/byte/symlink-limit cases, and four direct-executable tracked-mode/shebang/symlink cases. |
| 2026-07-29 | T-TSDC-004 final semantic-resolution remediation GREEN | Final replacement Task 4 remediation implementer | Replaced physical-line ownership matching with complete-program preprocessing and fail-closed canonical command resolution. Literal assignments persist across statements; canonical `command`, `exec`, and bounded `env` forms normalize before comparison; unsafe control, substitution, alias, and heredoc forms invalidate ownership without exposing payloads. Aggregate helpers are traversed by bounded no-follow descriptor-relative DFS across admitted shell and Python files, with cycle, depth, file-count, byte-count, symlink, and syntax failures closed. Direct local executables require a regular no-follow file, filesystem execute permission, Git index mode `100755`, and an admitted Bash or Python shebang. The focused set passes 8/8 and the full workflow suite passes 27/27. Independent re-review remains pending. |
| 2026-07-29 | T-TSDC-004 final semantic-resolution remediation gates | Final replacement Task 4 remediation implementer | Focused CLI reports exactly 7 workflows, 23 jobs, and eight Actions; the fake CI-wrapper contract, Stage 00 mutations 4/4, eval fixtures 38/38, exact manifest oracle 148/89/59/0, and advisory delta pass. Actionlint, warning-level ShellCheck, Ruff, Python compile, Bash syntax, Markdown, and diff hygiene pass. All 148 review pairs remain pending. No broad aggregate, real pre-commit, Agent wrapper, network, remote, runtime/service/Compose, dependency/cache installation, credential, or secret-payload action ran. |
| 2026-07-29 | T-TSDC-004 final specification re-review | Fresh independent specification reviewer | Exact fix range `ba93483c..78f9f012`: C0/I4/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO. Load-bearing gaps remain for non-aggregate helper traversal, nonliteral Python process calls and `os.exec*` shapes, executable interpreter heredocs, and literal-variable non-script owner resolution. |
| 2026-07-29 | T-TSDC-004 final quality/security re-review | Fresh independent quality/security reviewer | Exact fix range `ba93483c..78f9f012`: C0/I4/M1; CHANGES_REQUIRED; COMMIT_READY NO. Load-bearing gaps remain for shell/Python execution equivalence, unquoted-heredoc expansion, recursive resource/provenance bounds, Git-environment isolation, descriptor/inode execute-mode proof, and exact positive assertions. |
| 2026-07-29 | T-TSDC-004 fix-loop breaker | Controller | Fix round 5/5 is exhausted with unresolved load-bearing TSDC-012 findings. T-TSDC-004 is blocked; serial T-TSDC-005 and T-TSDC-006 do not start. No finding is parked or waived, no manifest verdict is promoted, and no further implementation is authorized without a revised approved Plan or an explicit exception to the five-round breaker. |
| 2026-07-29 | T-TSDC-004R specification revision | Controller plus independent design reviewers | Replaced the unbounded shell/Python semantic-equivalence objective with the approved structural schema-v2 gate registry, DAG, exact runner, workflow projection, and honest opaque-leaf boundary. Spec commit `a0f91bb5` passed metadata, 5,662-link alignment, diff hygiene, and independent specification plus quality/security review with no findings. |
| 2026-07-29 | T-TSDC-004R specification approval | User / Controller | The user approved the written Spec revision. The approval advances the lifecycle to prospective Plan drafting only; no production/test implementation, remote mutation, runtime action, dependency installation, wrapper run, or direct pre-commit is authorized. |
| 2026-07-29 | T-TSDC-004R Plan draft | Controller plus read-only planning agents | Revised the canonical Plan in place around schema contract, dependency-free runner, atomic workflow/local projection, independent cutover review, and old-interpreter removal. Historical Task evidence is preserved. The exact Plan remains pending independent review and user approval. |
| 2026-07-29 | T-TSDC-004R Plan approval | User / Controller | The user approved the exact revised Plan. Local production/test implementation remains gated only by an independent read-only C0/I0 Plan review; remote mutation, runtime actions, dependency installation, the controlled all-files wrapper, and direct pre-commit remain unauthorized. |
| 2026-07-29 | T-TSDC-004R Plan self-review | Controller | Mapped TSDC-010–017 to exact recovery units; removed placeholder-like signatures; fixed delta-manifest owner/writer/count semantics; made adapter grammars, safe environment construction, required root children, local profile order, mode normalization, RED/GREEN commands, and type interfaces exact. No production, test, workflow, runtime, remote, dependency, wrapper, or pre-commit action ran. |
| 2026-07-29 | T-TSDC-004R first independent Plan reviews | Independent specification and quality/security reviewers | Exact range `a0f91bb5..1a86f929` returned specification C0/I4/M1 and quality/security C1/I2/M1; both verdicts were CHANGES_REQUIRED / COMMIT_READY NO. Findings covered schema-v2 bootstrap order, descriptor-path compatibility, duplicate repository workflow-contract execution, missing Task 5 RED/write commands, broad optional wrapper prefixes, local `.env` overwrite risk, Storybook HOME lifetime, Wave B Bash static checks, and behavior-specific RED evidence. Implementation remained blocked. |
| 2026-07-29 | T-TSDC-004R Plan correction | Controller | Corrected only the prospective Plan and current ledger: deferred canonical runner commands until schema-v2 cutover; specified inode-bound descriptor compatibility; removed umbrella duplicate execution; separated CI Compose setup from local roots; kept Storybook setup/coverage in one runner lifetime; added exact Bash gates, Task 5 RED/write commands, path-minimal future wrapper approval, behavior-specific REDs, and task-brief-compatible Task 4.x headings. No production, test, workflow, runtime, remote, dependency, wrapper, or pre-commit action ran. |
| 2026-07-29 | T-TSDC-004R second independent Plan reviews | Independent specification and quality/security reviewers | Complete range `a0f91bb5..e97b7966` returned specification C0/I3/M1 and quality/security C0/I2/M1; both verdicts were CHANGES_REQUIRED / COMMIT_READY NO. Remaining blockers were Spec Wave-1 schema-v2 order, an orphaned all-profile route, missing review-bound full-row manifest promotion, and missing post-review evidence commits; the controlled-wrapper ledger wording was stale. The two-attempt Plan review loop was exhausted and implementation remained blocked. |
| 2026-07-29 | T-TSDC-004R Revision R2 design return | Controller | Returned to design/plan without implementation. Revision R2 moves the canonical schema-v2 registry into Wave A while retaining current workflow execution, registers `local-all-profiles` as a real profile root, defines a 158-row review-promotion crosswalk and exact pending/pass oracles, and adds controller-owned evidence commits after every review boundary. Revision R2 now awaits explicit user approval and fresh independent Plan reviews. |
| 2026-07-29 | T-TSDC-004R Revision R2 approval | User / Controller | The user explicitly approved Revision R2 at `7d36fe3b`. The approval authorizes fresh independent Plan reviews and, only after both return C0/I0, local Plan-bounded T-TSDC-004R implementation. No production/test implementation, remote/runtime mutation, dependency installation, wrapper run, or direct pre-commit action has started. |
| 2026-07-29 | T-TSDC-004R Revision R2 first Plan reviews | Independent specification and quality/security reviewers | Exact range `e97b7966..5b7388d0` returned specification C0/I5/M0, SPEC_COMPLIANCE NO, COMMIT_READY NO and quality/security C0/I0/M0, APPROVED, COMMIT_READY YES. A separate read-only specification corroboration returned C0/I4/M0. The union found the three-profile Spec mismatch, a parallel code-owned command authority, deferred executable modes, the wrong Wave B freeze checkpoint, incomplete Bash static coverage, and a dirty-worktree wrapper order. Implementation remained blocked. |
| 2026-07-29 | T-TSDC-004R Revision R2 bounded correction | Controller plus bounded documentation implementers | Synchronized the already approved third local profile into Spec 135 without expanding authority; moved executable-mode provenance into Wave A; made schema v2 the sole ownership authority; bound Wave B to the Task 4.2 review checkpoint; added exact shell static gates; and moved optional wrapper handling to clean committed pre-Task-6 boundaries. Production, tests, workflows, runtime, remote state, dependencies, secrets, the wrapper, and direct pre-commit remained untouched. Final corrected R2 reviews are pending. |
| 2026-07-29 | T-TSDC-004R Revision R2 final Plan reviews | Fresh independent specification and quality/security reviewers | Exact corrected range `e97b7966..8f82e88b` returned specification C0/I0/M0, SPEC_COMPLIANCE YES, COMMIT_READY YES and quality/security C0/I0/M0, APPROVED, COMMIT_READY YES. Both reviewers were read-only, found no issues, and confirmed the three-profile contract, single schema-v2 authority, Wave A mode/count order, Task 4.2 freeze, shell gates, clean wrapper boundaries, and unchanged authority scope. Local T-TSDC-004R implementation became eligible for activation. |
| 2026-07-29 | T-TSDC-004R-1 typed gate contract RED | Task 4.1 implementation agent | An importable signature-only module exposed every approved dataclass and function while every behavior raised `NotImplementedError`. The exact seven named tests all executed and failed on their own reader, parser, kind, DAG, suite-owner, required-root, or profile behavior; the three DAG subcases produced separate cycle, missing-child, and orphan errors, for nine behavior errors total and no import failure. After the focused suite reached GREEN, the exact manifest oracle was added first and failed with `150 != 148` before either row was written. |
| 2026-07-29 | T-TSDC-004R-1 typed gate contract GREEN | Task 4.1 implementation agent | Implemented the dependency-free strict-JSON schema-v2 reader, exact kind parser, DAG and ownership validator, exact 16-job-root contract, ordered local-profile projection, and bounded descriptor-relative no-follow input handling. The strengthened focused suite passes 7/7, including YAML-only syntax, schema-version, duplicate/unknown field, duplicate suite/path ownership, cycle, missing-child, orphan, noncanonical, symlink, oversized, and non-UTF-8 cases. The successor delta suite passes 30/30 after adding explicit factual proof for symbolic Task 4 consumer routes. The canonical writer produced exactly 150 rows: 89 preserve, 61 update, zero migrate, zero delete; both new rows remain pending/pending. |
| 2026-07-29 | T-TSDC-004R-1 typed gate static and boundary gates | Task 4.1 implementation agent | Canonical advisory validation, Python compileall, Ruff over the exact two new files, and diff hygiene pass. The system Python lacks the Ruff module; the same required `python3 -m ruff check` invocation passes with the existing repository-user uv Ruff environment first on `PATH`, and the standalone Ruff binary corroborates it. No network, dependency installation, remote action, runtime, Compose, secret access, direct pre-commit, or controlled-wrapper execution occurred. Independent implementation review remains pending. |
| 2026-07-29 | T-TSDC-004R-1 initial implementation reviews | Fresh independent specification and quality/security reviewers | Exact range `ae5632b2..fdc01e1c` returned revised specification C0/I3/M0, SPEC_COMPLIANCE NO, COMMIT_READY NO and quality/security C0/I4/M2, CHANGES_REQUIRED. The accepted union required deterministic parent/read errors, bounded iterative JSON/graph handling, sanitized timeout-bound Git provenance, exact local profile classification, exact integer schema version, a complete positive registry witness, and exact required/local structural safety. The initial specification command-catalog finding was withdrawn after conflict review: no code-owned entrypoint/argv catalog is authorized because Task 4.2 makes the canonical schema-v2 registry the sole command authority. |
| 2026-07-29 | T-TSDC-004R-1 remediation RED | Task 4.1 implementation agent, attempt 2/2 | The strengthened exact seven-method suite produced 19 behavior-specific subcase failures before remediation: eight raw exceptions comprised six reader `OSError` paths, one deep-graph `RecursionError`, and one Git `TimeoutExpired`; eleven structured failures covered float schema acceptance, deep JSON, node and edge bounds, profile classification, two prohibited local reachability mutations, local aggregate order, required-root children, hostile Git environment, and the Git command/environment/cache contract. Existing generic kind-field and duplicate-suite cases remained GREEN. |
| 2026-07-29 | T-TSDC-004R-1 remediation GREEN | Task 4.1 implementation agent, attempt 2/2 | All 19 remediation cases now pass inside the exact seven named tests. The reader converts parent, symlink, permission, and read failures to value-free typed errors and rejects bounded deep JSON. Public parse, validate, and expand enforce explicit 2,048-node and 8,192-edge limits; cycle, reachability, expansion, and capped path multiplicity are iterative, and duplicate suites are linear. Git provenance uses a fixed minimal environment, literal pathspec mode, repository-bound cwd, five-second timeout, value-free error handling, and per-path caching. Exact required-root and local-aggregate children plus prohibited local reachability reject `setup.compose-env`, real pre-commit, dependency/network setup, frontend/Storybook, and zizmor exposure without defining a second command catalog. The complete positive registry returns no findings. |
| 2026-07-29 | T-TSDC-004R-1 remediation gates | Task 4.1 implementation agent, attempt 2/2 | Focused typed-gate tests pass 7/7 and the successor delta suite passes 30/30. Exact two-file Ruff through the existing uv Ruff Python module, exact compileall, canonical delta advisory, and diff hygiene pass. `.github/workflow-contract.yml` remains byte-identical at SHA-256 `9c25a7311969b4b522b1b5af03111400134057ba7d525650b36ac1b3e1e00e52`; remediation scope is limited to the typed contract, its focused test, and this Task evidence. No network, remote, dependency installation, runtime, Compose, secrets, direct pre-commit, or controlled-wrapper action ran. Fresh final independent reviews remain pending. |
| 2026-07-29 | T-TSDC-004R-1 final reviews and evidence correction | Fresh independent specification and quality/security reviewers / controller evidence owner | The final quality/security review of full range `ae5632b2..af898045` returned C0/I0/M1, APPROVED, COMMIT_READY YES. Its non-blocking minor assigns a full load–parse–validate–expand strict-JSON positive registry fixture to the Task 4.2 canonical schema-v2 conversion. The initial final specification review returned C0/I1/M0 only because the execution, review, commit, and deferred-state records were stale; controller commit `af22e129` reconciled those records. The same read-only specification reviewer then rechecked the bounded working-tree evidence and returned C0/I0/M0, SPEC_COMPLIANCE YES, COMMIT_READY YES. Task 4.1 is complete and Task 4.2 is the next serial unit. |
| 2026-07-29 | T-TSDC-004R-2 runner and adapter RED | Task 4.2 implementation agent | Importable signature-only runner and adapter modules exposed the approved interfaces and closed twelve-subcommand catalog while executable behavior raised `NotImplementedError`. The exact runner/adapter command ran 28 tests: two interface/catalog witnesses passed, and behavior-specific subcases produced one assertion failure plus 38 errors without an import failure. |
| 2026-07-29 | T-TSDC-004R-2 runner, adapter, and manifest GREEN | Task 4.2 implementation agent | Implemented ordered deduplicated expansion, deterministic execution-free list/dry-run modes, descriptor-bound tracked `100755` execution, one minimal shared HOME, timeout/nonzero propagation, cleanup, and the closed adapter grammar. Runner/adapter tests pass 28/28. Before schema conversion, the exact manifest oracle failed because six new paths were absent; after adding the five runner/test rows plus `check-agent-governance-contract.py`, normalizing seven registered modes, and updating factual consumer proofs, it passes at exactly 156 rows: 85 preserve, 71 update, zero migrate, and zero delete. |
| 2026-07-29 | T-TSDC-004R-2 schema-v2 RED and GREEN | Task 4.2 implementation agent | Three schema-cutover regressions first ran with one failure and two errors: the schema-v1 workflow loader rejected the canonical v2 top-level fields and the old command-authority symbol remained. The canonical contract is now deterministic strict JSON schema v2 with seven workflows, 23 jobs, eight Actions, 80 typed nodes, 16 required job roots, and three local profile roots. The exact three cutover tests pass; the full workflow-contract module has 18 passing tests and 11 explicitly skipped inactive-semantic-parser witnesses retained until Wave C, with zero failure or error. Active validation calls only the typed registry; `owner_commands`, `expensive_commands`, `ExpensiveCommandOwner`, and `_EXPENSIVE_COMMAND_BASELINE` are absent. |
| 2026-07-29 | T-TSDC-004R-2 implementation gates | Task 4.2 implementation agent | The exact five-module integration passes 94 tests with 11 planned Wave-C skips and zero failure; the live workflow checker reports 7 workflows, 23 jobs, and eight Actions. Both local profiles produce deterministic execution-free projections. Exact Ruff through the existing uv Ruff Python module, compileall, Bash syntax, warning-level ShellCheck, canonical advisory validation, generated summary freshness, and diff hygiene pass. `.github/workflows/ci-quality.yml` remains byte-identical to the Task 4.1 review checkpoint at SHA-256 `18bdc27e634f83edcd57da9f39aafff62ffe3bbd76d820a74c061021ee811756`. No child gate, network, dependency installation, runtime, Compose, secret, remote, direct pre-commit, or controlled-wrapper action ran. Fresh independent Task 4.2 reviews remain pending. |
| 2026-07-29 | T-TSDC-004R-2 initial implementation reviews | Fresh independent specification and quality/security reviewers | Exact range `0d833563..5819c8ab` returned specification C0/I2/M0, SPEC_COMPLIANCE NO, COMMIT_READY NO and quality/security C0/I5/M1, CHANGES_REQUIRED, COMMIT_READY NO. The accepted union required descriptor-bound root and Python bootstrap identity, factual direct-consumer evidence, process-tree timeout termination, immutable environment-key rejection, bounded two-stream child capture, SARIF and HOME cleanup, and staged-blob identity for Compose example copying. |
| 2026-07-29 | T-TSDC-004R-2 hardening RED and GREEN | Task 4.2 remediation implementation agent | The retained Runner RED exercised five boundary groups with 19 failures and one error. Adapter, contract, and manifest RED then exercised ten top-level groups with 22 failures and four errors plus two exact direct-consumer failures. GREEN binds root and imports to `/proc/self/fd/<root-fd>`, isolates Python startup, kills timed-out child process groups with TERM then KILL, admits only the exact eleven canonical environment keys, bounds stdout and stderr during execution, normalizes child and cleanup failures, removes partial SARIF output, and copies `.env.example` only when the opened regular descriptor is byte-identical to its staged Git blob. The environment-independent fixture explicitly stages executable mode and uses `/tmp`; the focused Runner 5/5, Adapter/Contract/Manifest 8/8, descriptor-child 1/1, direct-consumer factual/exact 2/2, and combined Runner/Adapter 28/28 checks pass. The exact five-module rerun passed 94 tests in 147.961 seconds with 11 planned Wave-C skips and zero failures. The live workflow checker reports 7 workflows, 23 jobs, and eight Actions; both local profiles produce deterministic execution-free projections. Ruff, compileall, Bash syntax, warning-level ShellCheck, canonical advisory validation, summary regeneration, workflow byte freeze, and diff hygiene pass. The summary remained byte-identical at SHA-256 `4030982fcf981b2ee342929fa61804bd0b20a9be5eef0ef3dbe874864354e514`, and `.github/workflows/ci-quality.yml` remained byte-identical at SHA-256 `18bdc27e634f83edcd57da9f39aafff62ffe3bbd76d820a74c061021ee811756`. Fresh independent reviews remain pending. |
| 2026-07-29 | T-TSDC-004R-2 redesigned lifecycle RED | Task 4.2R implementation agent, sole redesigned attempt | The exact unchanged 94-test discovery produced 78 passes, 11 planned Wave-C skips, three failures, and two errors. The new witnesses failed only because the adapter reused inherited root descriptor `N` instead of adopting a distinct CLOEXEC duplicate `M`, normal and nonzero adapter results did not invoke a runner-owned group finalizer, timeout still used leader-oriented cleanup, and HOME teardown stopped after its first transient failure. There was no import, fixture-discovery, network, Compose, or external dependency failure. |
| 2026-07-29 | T-TSDC-004R-2 redesigned lifecycle GREEN | Task 4.2R implementation agent, sole redesigned attempt | The adapter now validates and adopts one owned root capability `M`, immediately closes inherited `N`, rewrites descendant root/cwd/environment use to `M`, passes only `M`, and closes it from one top-level `finally`; direct roots use one `O_NOFOLLOW` directory descriptor with the same lifetime. The runner alone starts the adapter session and finalizes the complete PGID after timeout, normal, and nonzero results by TERM, group-existence observation, conditional KILL, and bounded absence confirmation. Existing tests now exercise registered `setup.compose-env` and `leaf.zizmor`, named-root replacement, hostile `sitecustomize.py`, exact FD inventories, no nested session, and timeout/output-overflow/read-error/nonzero/safe-normal child and grandchild trees using live pidfds, poll readiness, pidfd-only fallback cleanup, and closed pidfds. HOME teardown performs at most three attempts and sleeps exactly 50 ms after failures one and two. The exact suite passed 94 tests in 141.748 seconds: 83 passes and 11 planned skips. Workflow projection passed at 7 workflows, 23 jobs, and eight Actions; both execution-free profile projections, exact four-file Ruff and compileall, advisory validation, and diff hygiene passed. Contract, workflow, manifest, and summary freezes remain byte-identical to `17bb5cdd` with SHA-256 values `21dcc9a59b4c7fe087431c647e8d385d64125021dfa583542818a68ed84c9d20`, `18bdc27e634f83edcd57da9f39aafff62ffe3bbd76d820a74c061021ee811756`, `f82b6d7c93ae12d5709e24704b2aad562b5275b56bf7ea3a10c491739da59e87`, and `4030982fcf981b2ee342929fa61804bd0b20a9be5eef0ef3dbe874864354e514`. Graphify remained stale advisory evidence and was corroborated against Spec 135, the corrected Plan, Stage 00, and tracked source. No network, installation, real Compose, remote, secret, wrapper, direct pre-commit, or Wave B action ran. Fresh independent C0/I0 reviews remain required. |
| 2026-07-29 | T-TSDC-004R-2 redesigned lifecycle implementation reviews | Fresh independent specification and quality/security reviewers | Exact range `e6fefb69..8df1b9cd` returned specification `C0/I1/M0`, `SPEC_COMPLIANCE NO`, `COMMIT_READY NO`, and quality/security `C0/I3/M0`, `CHANGES_REQUIRED`, `COMMIT_READY NO`. The accepted union requires that adapter-owned `M` cleanup begins immediately after adoption and independently normalizes `N`, output/source close, and required-unlink failures; that runner group cleanup reserve PGID identity through an unreaped leader pidfd, bounded strict `/proc` membership scan, TERM/KILL, and exactly one final reap; and that the affected failure/ordering witnesses remain within the existing 94-test discovery. The implementation is not review-approved; Wave B remains blocked. |
| 2026-07-29 | T-TSDC-004R-2 identity-cleanup design return | Controller | Replaced the superseded post-GREEN cleanup design with one bounded Task 4.2S attempt. The Plan pins capability ownership from `_adopt_root` through independent cleanup, pidfd-first unreaped-leader identity reservation, strict bounded no-follow `/proc/<pid>/stat` membership checks, and exact no-reap-before-finalization ordering. It preserves the exact five-path allowlist, all four `17bb5cdd` freezes, `94 = 83 pass + 11 Wave-C skips`, and the requirement for a fresh C0/I0 pair before Wave B. No production, test, workflow, runtime, remote, dependency, Compose, secret, wrapper, or direct-pre-commit action ran. |
| 2026-07-29 | T-TSDC-004R-2 identity-cleanup Plan reviews | Fresh independent specification and quality/security reviewers | The Plan through `6d433fce` returned specification `C0/I2/M1`, `SPEC_COMPLIANCE NO`, `IMPLEMENTATION_READY NO`, and quality/security `C0/I3/M0`, `CHANGES_REQUIRED`, `IMPLEMENTATION_READY NO`. The accepted union requires a post-correction implementation-scope checkpoint, deterministic all-actions cleanup and error precedence, guaranteed reap after initial pidfd-acquisition recovery even when signaling fails, explicit no-numeric-PGID action after reap, and safe TERM/KILL `ESRCH` race handling with regressions. No implementation authority follows from these reviews. |
| 2026-07-29 | T-TSDC-004R-2 identity-cleanup Plan correction | Controller | The corrected Plan makes every applicable cleanup action independent and ordered, gives safety cleanup failure precedence over product or operation outcome, collapses failures into fixed value-free domain codes, treats TERM/KILL `ESRCH` as a disappeared-target race followed by bounded validation, guarantees one reap attempt after initial pidfd failure, and resolves the implementation baseline through one unique controller checkpoint subject. The actual correction SHA is recorded by the immediately succeeding checkpoint commit; Wave B remains blocked. |
| 2026-07-29 | T-TSDC-004R-2 identity-cleanup design checkpoint | Controller | Correction `63effff2` passed metadata 15/0, traceability 46/0, and diff-hygiene validation. This checkpoint commit changes only this Task ledger and is identified by the exact unique subject `docs(plan): record typed gate identity design checkpoint`; the implementation scope oracle resolves that subject dynamically, so it excludes all Plan corrections and begins from the fully reconciled design boundary. Fresh Plan reviews remain required before the one successor implementation attempt. |
| 2026-07-29 | T-TSDC-004R-2 bounded-reap Plan reviews | Fresh independent specification and quality/security reviewers | Specification review of checkpoint `2c6b2af7` returned `C0/I0/M0`, `SPEC_COMPLIANCE YES`, `IMPLEMENTATION_READY YES`. Quality/security review returned `C0/I2/M0`, `CHANGES_REQUIRED`, `IMPLEMENTATION_READY NO`: initial pidfd-acquisition recovery could block indefinitely after non-`ESRCH` KILL failure, and later recovery did not define a bounded or readiness-gated reap. The implementation remains blocked until both paths are explicitly bounded and a new unique checkpoint receives fresh C0/I0 reviews. |
| 2026-07-29 | T-TSDC-004R-2 bounded-reap Plan correction | Controller | The Plan now requires a single timeout-bounded wait attempt on initial pidfd-acquisition recovery, and requires later recovery to wait only after confirmed pidfd readiness; missing readiness skips wait, records cleanup failure, and still closes pidfd. Wait timeout or failure never prevents remaining cleanup, and all such failures collapse to the fixed value-free runner cleanup code. The actual correction SHA is recorded by the succeeding bounded checkpoint commit. |
| 2026-07-29 | T-TSDC-004R-2 bounded identity design checkpoint | Controller | Correction `a3ba173c` passed metadata 15/0, traceability 46/0, and diff-hygiene validation. This checkpoint changes only the Task ledger and is identified by the exact unique subject `docs(plan): record bounded typed gate identity checkpoint`; the scope oracle begins the one implementation attempt only after this bounded, non-hanging recovery design. Fresh specification and quality/security C0/I0 reviews remain required. |
| 2026-07-29 | T-TSDC-004R-2 bounded identity Plan reviews | Fresh independent specification and quality/security reviewers | Quality/security review of checkpoint `6877ac4b` returned `C0/I0/M0`, `APPROVED`, `IMPLEMENTATION_READY YES`. Specification review returned `C0/I1/M0`, `SPEC_COMPLIANCE NO`, `IMPLEMENTATION_READY NO`: S3 compared only checkpoint-to-HEAD before the implementation commit, so it could not see staged/unstaged implementation changes or reject untracked paths. All lifecycle, cleanup, bounded-reap, freeze, and attempt-limit contracts otherwise passed. |
| 2026-07-29 | T-TSDC-004R-2 scope-oracle Plan correction | Controller | S3 now compares the unique checkpoint directly to the working tree, requires the exact five tracked paths, and rejects every non-ignored untracked path. S4 repeats the committed checkpoint-to-HEAD comparison and requires a clean status before independent review. The actual correction SHA is recorded by the succeeding scoped checkpoint commit. |
| 2026-07-29 | T-TSDC-004R-2 scoped identity design checkpoint | Controller | Correction `2b73ea2d` passed metadata 15/0, traceability 46/0, and diff-hygiene validation. This checkpoint changes only the Task ledger and is identified by the exact unique subject `docs(plan): record scoped typed gate identity checkpoint`; pre-commit scope compares checkpoint-to-working-tree and rejects non-ignored untracked paths, while post-commit scope compares checkpoint-to-HEAD and requires a clean status. Fresh specification and quality/security C0/I0 reviews remain required. |
| 2026-07-29 | T-TSDC-004R-2 scoped identity Plan review | Fresh independent specification reviewer | Specification review of checkpoint `ba7ccb79` returned `C0/I1/M0`, `SPEC_COMPLIANCE NO`, `IMPLEMENTATION_READY NO`: both exact-path builders used `printf '%s\\n'`, which emits literal backslash-n text rather than five newline-delimited paths. The parallel quality review was canceled after this deterministic blocker; it produced no verdict and grants no authority. All other scope timing and lifecycle contracts passed specification review. |
| 2026-07-29 | T-TSDC-004R-2 executable-oracle Plan correction | Controller | Both S3 and S4 exact-path builders now use `printf '%s\n'`, while retaining checkpoint-to-working-tree plus untracked rejection before commit and checkpoint-to-HEAD plus clean status after commit. The actual correction SHA is recorded by the succeeding executable checkpoint commit. |
| 2026-07-29 | T-TSDC-004R-2 executable identity design checkpoint | Controller | Correction `38259d1f` passed the literal five-line shell oracle, metadata 15/0, traceability 46/0, and diff-hygiene validation. This checkpoint changes only the Task ledger and is identified by the exact unique subject `docs(plan): record executable typed gate identity checkpoint`; fresh specification and quality/security C0/I0 reviews remain required before implementation. |
| 2026-07-29 | T-TSDC-004R-2 executable identity Plan final reviews | Fresh independent specification and quality/security reviewers | Both read-only reviews of checkpoint `86146050` returned `C0/I0/M0` and `IMPLEMENTATION_READY YES`; specification returned `SPEC_COMPLIANCE YES` and quality/security returned `PASS`. They reproduced exactly five newline-delimited expected paths, confirmed the pre-commit working-tree and untracked gates plus post-commit range and clean-status gates, and found no regression in bounded pidfd recovery, deterministic cleanup precedence, `ESRCH`, strict proc bounds, exact 94 discovery, four freezes, or the Wave B block. The one Task 4.2S implementation attempt is now authorized from checkpoint `86146050`; no other scope is opened. |
| 2026-07-29 | T-TSDC-004R-2 identity-cleanup RED | Task 4.2S implementation agent, sole attempt | The unchanged five-module discovery ran 94 tests in 128.301 seconds: 74 passed, 11 planned Wave-C witnesses skipped, six failed, and three errored. Every new failure was behavior-specific: runner failures exposed pre-finalization reaping and missing pidfd-acquisition recovery, while adapter failures exposed incorrect adopted-root, Compose, and SARIF cleanup ordering or normalization. There was no import, discovery, network, Compose, or external-dependency failure. |
| 2026-07-29 | T-TSDC-004R-2 identity-cleanup implementation | Task 4.2S implementation agent, sole attempt | Adapter ownership now transfers adopted root `M` to the outer cleanup boundary before inherited `N` close can fail, independently attempts destination/source/output close and required unlink actions, and preserves the first cleanup failure with fixed value-free domain codes. The runner opens the leader pidfd immediately after `Popen`, keeps the leader unreaped through TERM/readiness/strict bounded no-follow proc-membership/KILL validation, performs exactly one final timeout-bounded reap, treats signal `ESRCH` as a disappeared-target race requiring validation, and independently closes the pidfd on every acquired path. Existing top-level test methods were extended; no test discovery was added. |
| 2026-07-29 | T-TSDC-004R-2 identity-cleanup GREEN and invariant gates | Task 4.2S implementation agent, sole attempt | Focused runner/adapter tests pass 28/28. The exact five-module suite ran 94 tests in 122.596 seconds: 83 passed, 11 planned Wave-C witnesses skipped, and zero failed or errored. The workflow checker reports 7 workflows, 23 jobs, and eight Actions; execution-free `local-harness` list/dry-run remains 32 leaves and `local-all-profiles` dry-run remains 34 projected lines. Exact four-file Ruff through the existing uv Ruff Python module, compileall, advisory delta validation, and diff hygiene pass. Contract, workflow, manifest, and summary remain byte-identical to `17bb5cdd` at their recorded hashes. No network, installation, child gate, real Compose, runtime, remote, secret, wrapper, direct pre-commit, or Wave B action ran. Fresh implementation reviews remain required. |
| 2026-07-30 | T-TSDC-004R-2 identity-cleanup implementation reviews | Fresh independent specification and quality/security reviewers | Exact range `86146050..17645f2a` returned specification `C0/I3/M0`, `SPEC_COMPLIANCE NO`, `COMMIT_READY NO`, and quality/security `C0/I1/M0`, `CHANGES_REQUIRED`, `COMMIT_READY NO`. The accepted union requires ordinary adapter exceptions to become fixed value-free operation errors, post-`Popen` control-flow interruptions to enter runner cleanup, later-recovery evidence to state readiness-conditional reap, and post-implementation metadata/traceability results to be explicit. Wave B remains blocked and no manifest verdict is promoted. |
| 2026-07-30 | T-TSDC-004R-2 typed-interruption planning process correction | Controller after read-only agent overreach | A read-only design agent exceeded its assignment by creating commits `4abc8009` and `5d089dd4`. The controller audited their exact two-document range; neither commit authorizes implementation or independent review. The history is retained, their incomplete checkpoint is superseded, and the corrected Plan adds initial pidfd-acquisition interruption, pre-reap versus reap-started state, proc-descriptor cleanup, exact one-attempt scope, and a new unique checkpoint subject. No source, test, workflow, manifest, runtime, remote, wrapper, or pre-commit action ran. |
| 2026-07-30 | T-TSDC-004R-2 interruption-safe design checkpoint | Controller | Correction `b3166ef7` passed changed-document metadata `15/0` with five registered legacy exceptions, documentation traceability `46/0`, and diff hygiene. This checkpoint changes only this Task ledger and is identified by the exact unique subject `docs(plan): record interruption-safe typed gate checkpoint`. Fresh specification and quality/security `C0/I0` Plan reviews remain mandatory before the one Task 4.2T implementation attempt. |
| 2026-07-30 | T-TSDC-004R-2 interruption-safe checkpoint reviews | Fresh independent specification and quality/security reviewers | Exact range `17645f2a..b73d2a99` returned specification `C0/I0/M0`, `SPEC_COMPLIANCE YES`, `IMPLEMENTATION_READY YES`, but quality/security `C0/I1/M0`, `QUALITY_SECURITY CHANGES_REQUIRED`, `IMPLEMENTATION_READY NO`. The missing witness begins at the inherited-root `N` close after owned `M` duplication: a control-flow interruption can bypass `_AdoptedRootCleanupError` and leak `M`. Implementation remains blocked until a corrected Plan requires fixed value-free root cleanup and exactly one `M` close attempt. |
| 2026-07-30 | T-TSDC-004R-2 adopted-root interruption checkpoint | Controller | Correction `16de8939` passed changed-document metadata `15/0` with five registered legacy exceptions, documentation traceability `46/0`, and diff hygiene. This checkpoint changes only this Task ledger and is identified by the exact unique subject `docs(plan): record adopted-root interruption checkpoint`. Fresh specification and quality/security `C0/I0` Plan reviews remain mandatory before the one Task 4.2T implementation attempt. |
| 2026-07-30 | T-TSDC-004R-2 adopted-root Plan final reviews | Fresh independent specification and quality/security reviewers | Both read-only reviews of exact range `17645f2a..5cd98c7b` returned `C0/I0/M0` and `IMPLEMENTATION_READY YES`; specification returned `SPEC_COMPLIANCE YES` and quality/security returned `QUALITY_SECURITY PASS`. They confirmed cleanup ownership starts at the `N`-to-`M` transfer, all adapter and runner interruption phases are bounded and value-free, the exact five-path and four-freeze oracles are executable, top-level discovery remains 94, and Wave B stays blocked. The one Task 4.2T implementation attempt is now authorized from checkpoint `5cd98c7b`; no other scope is opened. |
| 2026-07-30 | T-TSDC-004R-2 typed-interruption RED | Task 4.2T implementation agent, sole attempt | Two preliminary test-only witness-calibration runs were rejected as evidence because one raw control-flow interruption stopped unittest early and the next exposed exception-target lifetime defects in the new helper assertions; production remained untouched. After correcting only those witnesses, the authoritative exact five-module RED discovered all 94 tests and ran in 131.300 seconds: 74 passed, 11 planned Wave-C witnesses skipped, seven failed, and two errored. Every failure or error belonged to the two existing extended runner/adapter methods and exposed pidfd acquisition interruption, interrupted bounded-wait cleanup, adopted-root `N`/`M` interruption ownership, or ordinary environment-copy normalization. There was no import, discovery, network, Compose, runtime, or external-dependency failure. |
| 2026-07-30 | T-TSDC-004R-2 typed-interruption implementation | Task 4.2T implementation agent, sole attempt | Adapter ownership now begins when `F_DUPFD_CLOEXEC` returns `M`: inherited `N` close failure or interruption transfers `M` to exactly one outer close attempt and always returns fixed value-free root cleanup. Existing typed adapter errors are preserved, every other ordinary environment-copy or dispatch exception becomes fixed operation error, and control-flow interruptions re-raise only after successful root cleanup. Runner ownership begins at successful `Popen`; pidfd acquisition, pre-reap finalization, readiness, and proc-scan failures use one bounded cleanup controller, wait only after readiness, and preserve typed errors or control flow only after successful cleanup. Once the sole wait begins, no numeric-PGID signal, readiness observation, scan, or second wait occurs; pidfd close remains one final independent action. Proc-root, PID-directory, and stat descriptors close independently under every `BaseException`, with incomplete cleanup collapsed to fixed runner cleanup. Existing test methods were extended and discovery remains exactly 94. |
| 2026-07-30 | T-TSDC-004R-2 typed-interruption GREEN and invariant gates | Task 4.2T implementation agent, sole attempt | Focused runner/adapter tests pass 28/28 in 3.473 seconds. The exact five-module suite passes `94 = 83 pass + 11 planned Wave-C skip` in 133.162 seconds with zero failure or error. The workflow checker reports exactly 7 workflows, 23 jobs, and eight Actions; execution-free `local-harness` list and dry-run each project 32 leaves, while `local-all-profiles` dry-run projects 35. Exact four-file Ruff through the existing uv Ruff Python module, compileall, advisory delta validation, and diff hygiene pass. Changed-document metadata selected 15 documents with zero violations and five registered legacy exceptions; documentation traceability checked 46 catalog pairs with zero failures. The checkpoint-to-working-tree oracle resolves unique `5cd98c7b`, returns exactly the five admitted paths, and reports zero non-ignored untracked paths. Contract, workflow, manifest, and summary remain byte-identical to `17bb5cdd` at SHA-256 `21dcc9a59b4c7fe087431c647e8d385d64125021dfa583542818a68ed84c9d20`, `18bdc27e634f83edcd57da9f39aafff62ffe3bbd76d820a74c061021ee811756`, `f82b6d7c93ae12d5709e24704b2aad562b5275b56bf7ea3a10c491739da59e87`, and `4030982fcf981b2ee342929fa61804bd0b20a9be5eef0ef3dbe874864354e514`. No network, installation, child gate, real Compose, runtime, remote, secret, wrapper, direct pre-commit, or Wave B action ran. |
| 2026-07-30 | T-TSDC-004R-2 typed-interruption implementation reviews | Fresh independent specification and quality/security reviewers | Exact range `5cd98c7b..483d3a47` returned specification `C0/I0/M0`, `SPEC_COMPLIANCE YES`, `COMMIT_READY YES`, but quality/security `C0/I1/M0`, `QUALITY_SECURITY CHANGES_REQUIRED`, `COMMIT_READY NO`. The accepted adapter changes and action-raised runner cleanup remain frozen. The remaining runner finding is one closable source-level gap: disjoint `try` regions leave bound-process, acquired-pidfd, and finalized-before-reap transitions outside a phase-owning controller. Existing operation mocks cannot inject into those transitions. Task 4.2T is review-rejected; Wave B remains blocked and no manifest verdict is promoted. |
| 2026-07-30 | T-TSDC-004R-2 phase-owned runner checkpoint | Controller | Correction `4025aa42` passed changed-document metadata `15/0` with five registered legacy exceptions, documentation traceability `46/0`, and diff hygiene. This checkpoint changes only this Task ledger and is identified by exact unique subject `docs(plan): record phase-owned runner checkpoint`. It freezes the accepted adapter pair at `483d3a47`, limits the successor to three paths, and requires a fresh specification and quality/security `C0/I0` Plan pair before one Task 4.2U implementation attempt. |
| 2026-07-30 | T-TSDC-004R-2 phase-owned runner checkpoint reviews | Fresh independent specification and quality/security reviewers | Exact range `483d3a47..ce4111d8` returned specification `C0/I1/M0`, `SPEC_COMPLIANCE NO`, `IMPLEMENTATION_READY NO`, and quality/security `C0/I0/M1`, `QUALITY_SECURITY PASS`, `IMPLEMENTATION_READY YES`. Both reviews identified the same stale `Whole branch` prerequisite: it still named exhausted Task 4.2T instead of Task 4.2U. The lifecycle design, three-path allowlist, freezes, executable oracles, discovery and projection invariants, and Wave B block otherwise passed. The checkpoint is superseded and grants no implementation authority. |
| 2026-07-30 | T-TSDC-004R-2 phase-owned runner gate reconciliation | Controller | Correction `9281692e` passed changed-document metadata `15/0` with five registered legacy exceptions, documentation traceability `46/0`, and diff hygiene. The Plan and Task ledger now require a new reconciled Task 4.2U checkpoint, its sole runner-only implementation attempt, fresh implementation `C0/I0` reviews, and controller-owned evidence before Wave B. |
| 2026-07-30 | T-TSDC-004R-2 reconciled phase-owned runner checkpoint | Controller | This checkpoint changes only this Task ledger and is identified by exact unique subject `docs(plan): record reconciled phase-owned runner checkpoint`. It supersedes `ce4111d8`, preserves the accepted adapter pair at `483d3a47`, limits the successor to three paths, and requires a fresh specification and quality/security `C0/I0` Plan pair before the sole Task 4.2U implementation attempt. |
| 2026-07-30 | T-TSDC-004R-2 reconciled phase-owned Plan final reviews | Fresh independent specification and quality/security reviewers | Both read-only reviews of exact range `483d3a47..5dc49631` returned `C0/I0/M0` and `IMPLEMENTATION_READY YES`; specification returned `SPEC_COMPLIANCE YES` and quality/security returned `QUALITY_SECURITY PASS`. They confirmed the superseded checkpoint history, corrected Task 4.2U branch gate, one outer lifecycle controller, explicit transition state, sole bounded wait, post-reap prohibitions, real proc-root `finally`, meaningful transition witnesses, exact three-path allowlist, adapter and four-file freezes, exact `94/11` discovery, `32/32/35` projections, executable scope oracles, and Wave B block. The sole Task 4.2U implementation attempt is authorized from checkpoint `5dc49631`; no other scope is opened. |
| 2026-07-30 | T-TSDC-004R-2 phase-owned runner RED | Task 4.2U implementation agent, sole attempt | The authoritative exact five-module RED discovered and ran all 94 tests in 151.560 seconds: 77 passed, 11 planned Wave-C witnesses skipped, six transition subtests failed, and zero errored. All six failures stayed inside the existing runner top-level method and identified the missing phase-owned lifecycle state at bound-process-before-pidfd, pidfd-acquired-before-readiness, finalized-group-before-reap, reap-started-before-wait, wait interruption, and close-started interruption. Production remained unchanged; there was no import, discovery, environment, network, Compose, runtime, or dependency failure. |
| 2026-07-30 | T-TSDC-004R-2 phase-owned runner implementation | Task 4.2U implementation agent, sole attempt | One outer controller now begins with the preinitialized process and successful `Popen` binding and spans pidfd acquisition, readiness, group finalization, one bounded reap, one pidfd close attempt, and return. A private production lifecycle object owns the process and pidfd and tracks pidfd acquisition, finalization, reap start, and close-attempt state. Before reap, bound failures route by pidfd ownership; after reap starts, only the one independent close attempt is permitted. The sole wait and close helpers mutate state before the operation, ambiguous close is not retried, incomplete cleanup becomes fixed value-free `ci-gate-runner-cleanup`, and proc-root cleanup now uses an actual `finally` while PID/stat descriptor finalizers remain independent. |
| 2026-07-30 | T-TSDC-004R-2 phase-owned runner GREEN and invariant gates | Task 4.2U implementation agent, sole attempt | Final focused runner/adapter tests pass 28/28 in 3.385 seconds. The final exact five-module GREEN passes `94 = 83 pass + 11 planned Wave-C skip` in 156.093 seconds with zero failure or error. The workflow checker reports exactly 7 workflows, 23 jobs, and eight Actions; execution-free projections remain `32/32/35`. Exact four-file Ruff through the pre-existing uv Ruff environment, exact four-file compileall, advisory delta validation, changed-document metadata `15/0` with five registered legacy exceptions, documentation traceability `46/0`, and diff hygiene pass. The unique `5dc49631` checkpoint-to-working-tree oracle returns exactly the three admitted paths with zero non-ignored untracked paths. The accepted adapter pair remains byte-identical to `483d3a47`; the contract, workflow, manifest, and summary remain byte-identical to `17bb5cdd`. No network, installation, child gate, real Compose, runtime, remote, secret, wrapper, direct pre-commit, or Wave B action ran. Fresh implementation reviews remain required. |
| 2026-07-30 | T-TSDC-004R-2 phase-owned runner implementation reviews | Fresh independent specification and quality/security reviewers | Exact range `5dc49631..ad2df527` returned specification `C0/I0/M0`, `SPEC_COMPLIANCE YES`, `COMMIT_READY YES`, but quality/security `C0/I2/M0`, `QUALITY_SECURITY CHANGES_REQUIRED`, `COMMIT_READY NO`. Recovery still runs from outside the primary `try` and contains unowned gaps between signal, readiness, reap, and close; after-completed-recovery-transition witnesses are absent. A pre-bind ordinary non-`OSError` `Popen` exception is also re-raised with its private traceback value. Task 4.2U is review-rejected and exhausted; Wave B remains blocked and no manifest verdict is promoted. |
| 2026-07-30 | T-TSDC-004R-2 recovery-owned finalization design return | Controller / bounded future implementer | Correction `28685a1b` passed changed-document metadata `15/0` with five registered legacy exceptions, documentation traceability `46/0`, and diff hygiene. Task 4.2V moves normal and error finalization under one actual `finally`, nests KILL/readiness/conditional-reap/close ownership so every interruption reaches later state-permitted cleanup, makes the lifecycle object the sole bound-process identity, and fixes the pre-bind ordinary-exception taxonomy. The successor preserves the same three-path implementation boundary, adapter pair, four freezes, discovery/projection invariants, and one-attempt review gate. |
| 2026-07-30 | T-TSDC-004R-2 recovery-owned runner checkpoint | Controller | This checkpoint changes only this Task ledger and is identified by exact unique subject `docs(plan): record recovery-owned runner checkpoint`. It starts after rejected implementation `ad2df527`, freezes the accepted adapter pair at `483d3a47`, limits the successor to three paths, and requires a fresh specification and quality/security `C0/I0` Plan pair before the sole Task 4.2V implementation attempt. |
| 2026-07-30 | T-TSDC-004R-2 recovery-owned Plan final reviews | Fresh independent specification and quality/security reviewers | Both read-only reviews of exact range `ad2df527..5274f58b` returned `C0/I0/M0` and `IMPLEMENTATION_READY YES`; specification returned `SPEC_COMPLIANCE YES` and quality/security returned `QUALITY_SECURITY PASS`. They confirmed one lifecycle process identity, pre-bind fixed taxonomy, one actual outer finalizer, nested no-pidfd and pidfd cleanup ownership, post-reap prohibitions, behavior-faithful after-completed-recovery-transition RED, exact three-path scope, freezes, discovery/projections, one attempt, and the Wave B block. The sole Task 4.2V implementation attempt is authorized from checkpoint `5274f58b`; no other scope is opened. |
| 2026-07-30 | T-TSDC-004R-2 recovery-owned runner RED | Task 4.2V replacement implementation agent, sole attempt | The authoritative test-only exact five-module RED preserved all 94 discovered tests and 11 planned Wave-C skips: 81 passed and two behavior-specific witnesses failed. One failure proved that an ordinary pre-bind `RuntimeError` still exposed its private original object; the other proved that recovery kill, readiness, and completed-reap production state transitions were absent. Both failures remained inside the existing runner top-level method. Production was unchanged, and there was no import, discovery, network, Compose, runtime, or dependency failure. |
| 2026-07-30 | T-TSDC-004R-2 recovery-owned runner implementation | Task 4.2V replacement implementation agent, sole attempt | `_ProcessLifecycle` now performs and stores the `Popen` bind and is the only bound-process identity. The primary body records product errors and one actual outer `finally` invokes a single lifecycle finalizer. Nested finalizers own KILL, pidfd readiness, readiness-conditional sole bounded reap, and the one pidfd-close attempt; completed kill, readiness, reap, reap-started, and close-started transitions are production state. No-pidfd acquisition failure still reaches one reap, every acquired-pidfd path reaches one close attempt, and post-reap paths cannot signal, observe readiness, scan `/proc`, or wait again. Cleanup failure is fixed value-free runner cleanup; successful cleanup preserves typed errors, normalizes all pre-bind ordinary exceptions to fixed child-exec, normalizes bound ordinary exceptions by phase, and re-raises control-flow objects. |
| 2026-07-30 | T-TSDC-004R-2 recovery-owned runner GREEN and invariant gates | Task 4.2V replacement implementation agent, sole attempt | Focused runner/adapter GREEN passes 28/28 in 3.153 seconds. The exact five-module GREEN passes `94 = 83 pass + 11 planned Wave-C skip` in 27.3 seconds with zero failure or error. The workflow checker reports exactly `7/23/8`; execution-free projections remain `32/32/35`. Exact four-file Ruff through the pre-existing uv Ruff 0.15.12 artifact, exact four-file compileall, advisory delta validation, changed-document metadata `15/0` with five registered legacy exceptions, documentation traceability `46/0`, and diff hygiene pass. The unique recovery-owned checkpoint scope is exactly this Task ledger, runner, and existing runner test with zero non-ignored untracked paths. The accepted adapter pair and all four `17bb5cdd` surfaces remain byte-frozen. No network, installation, child gate, real Compose, runtime, remote, secret, wrapper, direct pre-commit, or Wave B action ran. Fresh implementation reviews remain required. |
| 2026-07-30 | T-TSDC-004R-2 recovery-owned runner implementation reviews | Fresh independent specification and quality/security reviewers | Both read-only reviews of exact range `5274f58b..cdae7523` returned `C0/I0/M0` and `COMMIT_READY YES`; specification returned `SPEC_COMPLIANCE YES` and quality/security returned `QUALITY_SECURITY PASS`. They found no unresolved lifecycle, taxonomy, cleanup, scope, freeze, test-fidelity, or evidence defect. The controller independently revalidated the exact three-path range, both adapter freezes, all four protected-surface freezes, clean status, diff hygiene, changed metadata `15/0` with five registered legacy exceptions, and traceability `46/0`. Task 4.2V is accepted and its controller-owned evidence checkpoint authorizes Task 4.3 Wave B; no manifest verdict, runtime claim, or remote claim is promoted by this review. |
| 2026-07-30 | T-TSDC-004R-4AA immediate-consumption implementation reviews | Fresh independent specification and quality/security reviewers | Exact range `194b7d16..84067c8f` returned specification `C0/I1/M0`, `SPEC_COMPLIANCE NO`, `IMPLEMENTATION_READY NO`, and quality/security `C0/I3/M0`, `QUALITY_SECURITY FAIL`, `IMPLEMENTATION_READY NO`. Short, attached, and clustered GNU `env -S` handling skips the first inserted token; an unresolved dynamic command head can ignore a later registered sibling; and malformed signal-option near-prefixes containing `=` are accepted as recognized options. The sole 4AA implementation attempt is review-rejected and exhausted. Wave C, Tasks 5–6, and whole-branch review remain blocked. |
| 2026-07-30 | T-TSDC-004R-4AB explicit parser-outcome design approval | User / Controller | The user approved one new Plan-only bounded successor from exact checkpoint `25524ce1`. The design makes `dispatch`, `no-dispatch`, and `ambiguous` explicit inside the existing test oracle; re-enters the same closure-budgeted GNU `env` parser at the first `-S` split token; fails closed on unresolved dynamic command heads with a relevant later sibling; and accepts only exact signal option names or exact `name=value` forms. The Plan and Task ledger are the only authorized checkpoint paths. Implementation, test execution, Wave C, runtime, remote, dependency, secret, direct pre-commit, controlled-wrapper, and Graphify-update authority remain blocked pending two fresh independent Plan reviews at `C0/I0/M0`. |
| 2026-07-30 | T-TSDC-004R-4AB explicit parser-outcome Plan reviews | Fresh independent specification and quality/security reviewers | Exact range `25524ce1..8d3f1122` returned specification `C0/I2/M0`, `SPEC_COMPLIANCE NO`, `IMPLEMENTATION_READY NO`, and quality/security `C0/I2/M0`, `QUALITY_SECURITY FAIL`, `IMPLEMENTATION_READY NO`. The Plan omits fallback-resistant long `--split-string` dispatch/query witnesses and no-relevant-sibling dynamic-head negatives; reuses a candidate collector that can drop embedded siblings after finding an exact path; and excludes unresolved `$1`/`${1}` positional heads from dynamic ambiguity. The no-correction Plan loop is exhausted. No Plan-review evidence, implementation, test execution, Wave C, Tasks 5–6, or whole-branch review authority follows. |
| 2026-07-30 | T-TSDC-004R-4AC candidate-closed design approval | User / Controller | The user approved one Plan-only bounded successor from exact checkpoint `997719ff`. The design requires every-token union of all exact plus embedded registered sibling candidates before ambiguity fallback; unresolved named variables and `$1`/`${1}` at direct, `command`, `python3`, and `bash` positions with relevant-sibling, no-relevant-sibling, and query-precedence witnesses; separated and equals long `--split-string` direct, wrapped, and query transitions; and a two-sibling malformed-signal union witness plus an exact-option contrast. The Plan and Task ledger are the only authorized checkpoint paths. Implementation, tests, Wave C, runtime, remote, dependency, secret, direct pre-commit, controlled-wrapper, and Graphify update remain blocked pending two fresh independent Plan reviews at `C0/I0/M0`. |
| 2026-07-30 | T-TSDC-004R-4AC candidate-closed Plan checkpoint | Controller | Commit `5bc5ab85` is exactly one commit after `997719ff`, changes only the Plan and this Task ledger, preserves both modes as `100644`, and left a clean worktree. Static extraction found 12 strict Bash blocks, 145 standalone captures, one bounded RED exception, immediate same-variable consumption for every non-RED capture, and valid Bash syntax. Diff hygiene, changed-document metadata `15/0` with five registered legacy exceptions, and traceability `46/0` passed. The first postcommit proof invocation used the default `zsh` and stopped at unsupported `shopt` with status 127 before any mutation; the same block rerun explicitly with `/bin/bash` passed the base, ancestry, distance, exact-path, mode, and clean-state assertions. |
| 2026-07-30 | T-TSDC-004R-4AC candidate-closed Plan reviews | Fresh independent specification and quality/security reviewers | Exact range `997719ff..5bc5ab85` returned specification `C0/I0/M0`, `SPEC_COMPLIANCE YES`, `IMPLEMENTATION_READY YES`, but quality/security `C0/I1/M1`, `QUALITY_SECURITY FAIL`, `IMPLEMENTATION_READY NO`. The Important finding is that terminal review-evidence sessions do not each rebind the complete reviewed predecessor chain, distance, scope, and modes, so current-ancestry-only subject uniqueness cannot exclude a substituted same-subject lineage. The Minor finding is that the Task ledger described the committed Plan checkpoint as pending; this rejected-review evidence synchronizes that status without correcting the Plan. The no-correction 4AC Plan loop is exhausted. No accepted Plan-review evidence, implementation, tests, Wave C, Tasks 5–6, or whole-branch authority follows. |
| 2026-07-30 | T-TSDC-004R-4AD review-range-bound design approval | User / Controller | The user approved one Plan-only bounded successor from exact checkpoint `3510e994`. The design preserves the reviewed 4AC parser behavior, RED/GREEN matrix, two-path implementation scope, freezes, and validation ladder. It adds one canonical full-hash range attestation for each review pair and requires every terminal evidence session plus Task 4.5 Step 0 to extract that range from this ledger and repeat the complete base-to-terminal ancestry, one-commit distances, exact path sets, `100644` modes, and clean-state proof. Plan/Task drafting is authorized; implementation and tests remain blocked pending two fresh independent C0/I0/M0 Plan reviews and their accepted Task-only evidence checkpoint. |
| 2026-07-30 | T-TSDC-004R-4AD draft preflight | Controller plus fresh read-only design and draft-audit agents | The bounded lineage map returned `C0/I0/M0`, `DESIGN_READY YES`. The first independent draft audit returned `C0/I0/M0`; a controller exact-prefix check then found that the Commit Ledger reused the Plan review-matrix label and would make range extraction fail closed. Renaming only that ledger unit left exactly one Plan attestation row and one implementation attestation row; the same auditor rechecked all 11 calls and returned `C0/I0/M0`, `DRAFT_READY YES`. Static extraction found nine strict 4AD plus Task 4.5 Bash blocks and 263 standalone captures with zero syntax or immediate-consumption failure. Exact two-path scope and `100644` modes, diff hygiene, changed-document metadata `15/0` with five registered legacy exceptions, and traceability `46/0` passed. Formal postcommit Plan reviews remain pending and no implementation authority exists. |
| 2026-07-30 | T-TSDC-004R-4AD review-range-bound Plan checkpoint | Controller | Commit `9de469a52c4b05d2490d36d37b95b1277442f725` is the exact two-path, single-parent successor from `3510e994`, preserves both modes as `100644`, and passed the draft mapping, corrected independent audit, nine-block/263-capture static proof, metadata `15/0`, traceability `46/0`, diff, scope, and mode gates. The first strict commit invocation contained accidental literal leading `+` tokens and stopped with `+: command not found` before `git add`, commit, or any mutation; the corrected Bash invocation passed and created the checkpoint. It granted no implementation or test authority. |
| 2026-07-30 | T-TSDC-004R-4AD review-range-bound Plan reviews | Fresh independent specification and quality/security reviewers | Both reviewers reported exact full-OID range `3510e9944655ee89077a295712e759d116e2e87f..9de469a52c4b05d2490d36d37b95b1277442f725`. Specification returned `C0/I2/M1`, `SPEC_COMPLIANCE NO`, `IMPLEMENTATION_READY NO`: range extraction searches an entire row instead of validating the exact range cell; the pre-implementation, implementation-commit, and implementation-review sessions omit required predecessor range/path or base mode assertions; and two Task statuses remained stale after the checkpoint. Quality/security returned `C0/I0/M0`, `QUALITY_SECURITY PASS`, `IMPLEMENTATION_READY YES`. Because both reviews are not `C0/I0/M0`, the no-correction 4AD Plan loop is exhausted without accepted evidence, implementation, tests, or downstream authority. |
| 2026-07-30 | T-TSDC-004R-4AE exact-cell design approval | User / Controller | The user approved one Plan-only successor from exact clean base `5644c4a301e38d3f0c32efe99e80f879df6e1ac8`. Scope is limited to exact seven-cell review-range parsing, the missing predecessor path/range and base-mode assertions in three sessions, and current-state synchronization. Implementation, tests, Wave C, Tasks 5–6, runtime, remote, wrapper, direct pre-commit, and Graphify-update authority remain blocked. |
| 2026-07-30 | T-TSDC-004R-4AE independent design audits | Two fresh read-only design agents | Both bounded design audits returned `C0/I0/M0` and ready verdicts. They selected in-place correction of the eight active helper copies, eleven calls, and three incomplete sessions; preserved immutable 4AC behavior and historical 4AD evidence; and rejected a new helper surface or full copied overlay as scope expansion. |
| 2026-07-30 | T-TSDC-004R-4AE exact-cell Plan checkpoint | Controller | This exact Plan-and-Task checkpoint is identified by unique subject `docs(plan): define exact-cell review-range proof`, has parent `5644c4a301e38d3f0c32efe99e80f879df6e1ac8`, and preserves both modes as `100644`. Fresh independent specification and quality/security Plan reviews remain pending; no implementation or test authority exists. |
| 2026-07-30 | T-TSDC-004R-4AE exact-cell Plan reviews | Fresh independent specification and quality/security reviewers | Both reviewers reported exact full-OID range `5644c4a301e38d3f0c32efe99e80f879df6e1ac8..8abea15a1ebafdf607be801789a409e6f312c099`. Specification returned `C0/I0/M0`, `SPEC_COMPLIANCE YES`, `IMPLEMENTATION_READY YES`. Quality/security returned `C0/I2/M0`, `QUALITY_SECURITY FAIL`, `IMPLEMENTATION_READY NO`: a duplicate no-leading-pipe GFM row can evade candidate counting, and downstream authority sessions do not reassert fixed whole-line uniqueness for accepted evidence and implementation subjects. The no-correction 4AE loop is exhausted without implementation or downstream authority. |
| 2026-07-30 | T-TSDC-004R-4AF canonical-row authority approval | User / Controller | User-approved Plan-only successor from rejected 4AE evidence `8cacc463`; historical 4AD/4AE evidence remains immutable. |
| 2026-07-30 | T-TSDC-004R-4AF design audit | Fresh read-only design agents | In-place active-block successor preserves 4AC behavior, two-path scope, freezes, RED/GREEN matrix, and validation ladder; active changes are eight helpers, eleven calls, and complete authority-subject uniqueness. |
| 2026-07-30 | T-TSDC-004R-4AF Plan checkpoint | Controller | P is resolved by exact unique subject `docs(plan): define canonical-row authority proof`; parent D and both `100644` modes are bound; formal Plan reviews are pending. |

## Verification Evidence

### Planning verification

| Check | Expected | Actual |
| --- | --- | --- |
| Spec 135 metadata | one selected document, zero violations | Passed before Plan drafting |
| Spec 135 Markdown | zero errors | Passed before Plan drafting |
| Document implementation alignment | zero failures | Passed before Plan drafting |
| `git diff --check` | zero whitespace errors | Passed before Plan drafting |
| Revision R1 Plan/Task metadata and Markdown | zero failures | Passed: explicit base `a0f91bb5` selected 2 changed documents with 0 violations; explicit two-file `markdownlint-cli2 --no-globs` linted 2 files with 0 errors |
| Revision R1 Plan/Task links and alignment | zero failures | Passed: traceability checked 46 catalog pairs with 0 failures; implementation alignment checked 674 stage documents and 5,663 repository-local Markdown links with 0 failures |
| Revision R1 Plan/Task diff hygiene | zero whitespace errors | Passed: `git diff --check` returned 0 |
| Corrected Revision R1 Plan/Task validation | zero failures | Passed from explicit base `1a86f929`: metadata selected 2 documents with 0 violations; explicit literal-path Markdown lint checked 2 files with 0 errors; traceability checked 46 catalog pairs with 0 failures; implementation alignment checked 674 stage documents and 5,663 repository-local links with 0 failures; diff hygiene returned 0 |
| Revision R2 Plan/Task validation | zero failures | Passed from explicit base `e97b7966`: metadata selected 2 documents with 0 violations; explicit literal-path Markdown lint checked 2 files with 0 errors; traceability checked 46 catalog pairs with 0 failures; implementation alignment checked 674 stage documents and 5,663 repository-local links with 0 failures; diff hygiene returned 0 |
| Corrected Revision R2 Spec/Plan/Task validation | zero failures | Passed from explicit base `5b7388d0`: metadata selected 3 documents with 0 violations; explicit literal-path Markdown lint checked 3 files with 0 errors; traceability checked 46 catalog pairs with 0 failures; implementation alignment checked 674 stage documents and 5,663 repository-local links with 0 failures; Task 4.1 and 4.2 briefs extracted at 147 and 300 lines; exact two-file Bash syntax and warning-level ShellCheck returned 0; diff hygiene returned 0 |

### Task execution evidence

| Task | RED evidence | GREEN evidence | Aggregate evidence | Result |
| --- | --- | --- | --- | --- |
| T-TSDC-001 | Initial run: 1 pass/12 missing-module errors. First remediation emitted 12 focused failures; second remediation covered structural, secret, and no-follow failures; third remediation emitted 2 failed-verdict subcase failures. | Initial 15/15; first remediation successor 25/25; second exact set 4/4; third affected CLI set 3/3. Production advisory passed and blocking retained 105 spec plus 105 quality pending findings. | Predecessor target suite 40/40 and CLI pass; bounded metadata/static/Markdown/diff gates passed. Final independent reviews of `72eef68c..43f78ad5` returned C0/I0/M0 twice and approved completion. | completed |
| T-TSDC-002 | Sample fixture 3/3 failed; heading/policy emitted 37 failures; bounded data/secret/local group emitted 7 failures with the valid archive witness already passing; copied-template scan emitted 15 failures. Lifecycle coupling produced one positive-handoff failure. Quality remediation then produced 17/19 intended evidence-matrix failures and three nonfailed-verdict compatibility failures. | Metadata fixture 3/3, document/routing group 7/7, manifest owner/consumer 2/2, lifecycle handoff 3/3, and predecessor aggregate passed. Quality remediation delegated the successor contract and passed the 19-case rejection matrix plus all three nonfailed verdict combinations. | Initial target 48/48, delta 30/30, metadata 225/225, and lifecycle manifest 34/34 passed. Remediation lifecycle 7/7, delta integration 2/2, predecessor aggregate 1/1, both CLIs, Ruff, compile, Markdown, metadata, summary freshness, and diff gates passed. Final independent reviews of `78af8462..b28764a9` returned C0/I0/M0 twice and approved completion; the obsolete Plan cross-link path remains recorded as unavailable. | completed |
| T-TSDC-003 | Registry contract emitted six subtest failures; the bounded suite then emitted those six plus one Keycloak literal failure. The hidden Dozzle follow-up and stale 136-row oracle each failed one exact regression. Review remediations produced 17 resolver/static failures, six quoted-key failures, five global-uniqueness/Dozzle failures, and the exact `141 != 140` manifest-oracle failure. | Initial focused tests passed 7/7. Successive remediation suites passed 11/11, 16/16, and finally 17/17; the exact 141-row manifest oracle passes 1/1 with Dozzle path-specific owner, consumer, update, and pending-verdict assertions. | Sync/provenance, 11-tier hardening, supply-chain 13 fixtures, successor advisory, alignment, Markdown, Ruff, compile, Bash, ShellCheck, and diff gates pass. Final independent specification and quality/security reviews of `b1e62873..60e0313c` each returned C0/I0/M0 and COMMIT_READY YES; all 141 manifest verdict pairs remain pending for Task 6. | completed |
| T-TSDC-004 | Missing wrapper; four missing-module errors; bounded reader 2 failures/1 error; `148 != 141`; missing local wrapper-test route; missing purpose-folder registration; mixed quoted/unquoted `on` failed both orderings; seven required permission co-mutations returned no baseline finding; round 3 produced 15 failures across five methods; round 4 produced 13 failures across four methods; final round 5 produced 29 failures across eight methods. | Successive workflow suites pass 9/9, 11/11, 14/14, 17/17, 20/20, and 27/27. Final round 5 focused methods pass 8/8, eval tests 38/38, and Stage 00 mutations 4/4. Focused CLI 7/23/8, exact manifest 148/89/59/0, and advisory remain green. | The two 4AE findings are addressed in the active 4AF Plan; fresh Plan review remains pending and every manifest review pair remains pending. | active; 4AF Plan review pending |
| T-TSDC-005 | Not run — accepted 4AF chain pending | Not run — accepted 4AF chain pending | Not run — accepted 4AF implementation-review R is required | blocked |
| T-TSDC-006 | Not run — Tasks 1–5 pending | Not run — Tasks 1–5 pending | Not run — Tasks 1–5 pending | pending |

### T-TSDC-001 bounded implementation evidence

- Starting commit:
  `72eef68cd0691a84e8ce80548f205de4fe964238`.
- Fixed provenance:
  predecessor closure `63039b5b0b20c99a10aae7162627afefcd7a1d8b`;
  implementation base `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`.
- Coverage: the successor manifest contains exactly the 105 computed target
  paths in the predecessor-to-`HEAD` plus staged, unstaged, and untracked
  union. The current tracked target inventory is 477 after staging. The three
  Task 1 paths beyond the activation delta are the library, thin CLI, and
  focused test.
- Classification: 96 `preserve`, 9 `update`, 0 `migrate`, and 0 `delete`.
  Native paths own themselves unless a repository generator, lockfile source,
  or fixture test is the more truthful owner; 53 rows name 58 direct repository
  consumer edges. Each declared consumer is a tracked regular file and is
  supported by a literal reference or an explicit focused-test group mapping.
  Self-contained service Compose rows declare no speculative root Compose
  consumer. No row uses Spec 135 as a generic owner.
- Remediation review state: the specification review reported C0/I4/M2 and the
  quality/security review reported C0/I1/M2. The implementation addresses each
  reported finding, but neither review is marked approved until the distinct
  reviewers re-review the remediation commit.
- Second re-review state: fresh re-review reported combined C0/I3/M0 for
  advisory structural outcomes, secret-like free-form values, and bootstrap
  parent traversal. Focused RED/GREEN evidence is recorded above, but the
  reviews remain not approved until the second remediation commit is reviewed.
- Third re-review state: a fresh focused review reported C0/I1/M0 because an
  explicit failed review verdict remained advisory-safe. Typed RED/GREEN
  evidence is recorded above, but all reviews remain not approved until the
  third remediation commit is re-reviewed.
- Remediation final gates: successor tests passed 25/25 in 95.838 seconds and
  predecessor tests passed 40/40 in 99.790 seconds. The metadata generated-owner
  oracle passed 1/1; changed metadata selected one document with zero
  violations; repository metadata contracts reported zero violations.
  Advisory validation passed before and after the descriptor-safe summary
  write. Expected blocking validation returned 1 with exactly 105
  specification and 105 quality non-pass findings because all production rows
  remain pending. Ruff, Python compile, Bash syntax, one-file Markdown stdin
  lint, predecessor CLI, and `git diff --check` passed.
- Safety: secret rows are `path-only`; findings, summary, and diagnostics
  contain paths and typed states only. No secret payload, raw log, workflow
  log, credential, or runtime value was read or persisted.
- Predecessor integrity: the predecessor manifest and summary are byte-equal
  to the fixed closure. Spec 133 Spec/Plan/Task are byte-equal to the Task
  start, and the authorized closure witness between the fixed commits matches
  its exact digest.
- Final document gates selected 3 changed Markdown files with 0 metadata
  violations and linted the same 3 literal paths with 0 Markdown errors.
  Python compile, Ruff, Bash syntax, staged/unstaged diff hygiene, the
  generated-owner oracle, and both successor advisory passes are green.
- Aggregate limitation: `check-repo-contracts.sh` completed with 11 known
  predecessor/environment or later-task groups: promoted-manifest consumer
  drift already present at Task start, unavailable `html5lib`, generated
  LLM/metadata/provenance drift, the planned Keycloak/static-version drift,
  and Plan references to Task 4/6 scripts that do not exist yet. The initial
  Task 1 script-inventory omission was corrected before the second run.
- No controlled Agent wrapper or direct all-files pre-commit command ran.

### T-TSDC-002 bounded implementation evidence

- Starting commit:
  `78af8462f87a4f7b2609a8e4930da6d9a780d5b3`.
- README convergence: 11 exact `Overview` headings now retain the existing
  localized bodies; 26 policy consumers have no generic Agent-policy heading
  or copied template workflow and route once from their existing local-work
  section to both Stage 00 rule owners.
- Local truth: service-specific commands, constraints, validation, and
  troubleshooting remain local. `infra/04-data/README.md` is one folder index
  with one Operations link.
- Typed fixture: `examples/sample-web-service/service.md` selects the existing
  `service` role, remains `draft`, uses the exact two domain parents, and is
  explicitly non-authoritative example evidence. The predecessor manifest
  remains immutable history; the successor owns the current `update`
  disposition.
- Archive and secret safety: `archive/Windows-Network-IP.md` remained
  byte-unchanged after its distinct `content-archive` profile passed. Only the
  tracked identifier `secrets/db/surreal_db/` was added; no secret payload was
  opened, echoed, or persisted.
- Successor classification: 31 newly covered target paths plus seven existing
  Task 2 rows yield 136 rows total: 90 `preserve`, 46 `update`, 0 `migrate`,
  and 0 `delete`. All 136 specification and quality verdict pairs remain
  `pending` for Task 6 promotion.
- Direct-impact ownership first expanded only to
  `tests/validation/test_target_surface_delta_contracts.py` because its fixed
  nine-update Task 1 oracle would otherwise contradict the implemented Task 2
  manifest. The target aggregate then proved one remaining predecessor/current
  coupling, so the controller separately expanded ownership only to
  `scripts/validation/check-document-corpus-lifecycle.py` and
  `tests/validation/test_document_corpus_lifecycle.py`. The handoff is limited
  to the exact successor row and fixture metadata; all other predecessor
  equality checks remain active.
- The canonical writer alone regenerated
  `target-surface-delta-summary.md`; advisory validation reports zero
  structural findings.
- Aggregate tests passed: target surface 48/48 in 141.657 seconds, successor
  delta 30/30 in 145.831 seconds, document metadata 225/225 in 109.752
  seconds, and lifecycle manifest validation 34/34 in 337.962 seconds. The
  lifecycle handoff requires the exact predecessor path and active/Spec133
  row, fixed predecessor closure, tracked successor manifest path and
  `changed_since` hash, exact successor `update` row, registered Service role,
  and exact approved draft metadata.
- Quality remediation removed the lifecycle checker's partial successor YAML
  parser. The canonical delta contract now owns the no-follow, 2 MiB-bounded,
  duplicate-safe read, exact top-level and row schemas, Git witnesses,
  structural findings, and explicit failed-review findings. After that
  canonical validation returns no findings, the lifecycle checker compares
  only the exact sample evidence and permits each verdict to be `pending` or
  `pass`. The affected lifecycle bundle passed 7/7 in 90.381 seconds, focused
  delta integration passed 2/2 in 6.507 seconds, and the predecessor aggregate
  passed 1/1 in 5.134 seconds.
- Static gates passed with zero findings: both metadata modes, the
  target-surface CLI, successor advisory CLI, document implementation
  alignment, current document traceability, targeted Ruff, Python compile,
  34 non-ledger changed Markdown files, the exact Task ledger via stdin, and
  `git diff --check`. Canonical summary regeneration was byte-stable at
  SHA-256 `3d8434429ce0f52370d70c8b72ab2829e4742a1240a5f103adab52958f9ab20e`.
- The Plan-stated `scripts/governance/validate-cross-links.sh` path does not
  exist in this checkout and returned 127. It remains unverified rather than
  being reported as pass; the tracked
  `scripts/validation/check-doc-traceability.sh` independently passed 46
  catalog pairs with zero failures. The Plan was not changed.
- The final scope contains 44 expected files: six under `docs`, one under
  `examples`, 29 under `infra`, three under `scripts`, one under `secrets`,
  and four under `tests`. The approved-scope comparison found zero unexpected
  paths.
- The quality remediation scope contains exactly three files: the lifecycle
  checker, its focused test, and this Task ledger. No successor manifest row
  or review verdict changed.
- Final independent reviews of exact range `78af8462..b28764a9` returned
  C0/I0/M0 twice. The specification reviewer reported SPEC_COMPLIANCE YES and
  COMMIT_READY YES; the quality/security reviewer reported APPROVED and
  COMMIT_READY YES. Task 2 is complete. No successor manifest row review
  verdict was promoted; all remain `pending` for Task 6.

### T-TSDC-003 bounded implementation evidence

- Starting commit:
  `b1e6287360d1f44c41c2b91c93c6addf6527f847`.
- Approved implementation commit chain:
  `5460e5fc16789d72417e5e7df8b7f7ae046fb245`,
  `c04946e547b7a7b22923e6d7ed577408b39ef480`,
  `cce5abb6e20bffd10a09f4a2c74da3b653022a86`, and
  `60e0313cad71dced1db2bb5fba554c2fc28cd235`.
- RED evidence: the initial focused test produced six exact subtest failures:
  Traefik `v3.7.6 -> v3.7.8`, Keycloak `26.6.4-1 -> 26.7.0-0`,
  PostgreSQL `17.6.1.143 -> 17.6.1.150`, Prometheus
  `v3.13.0 -> v3.13.1`, Alloy `v1.17.1 -> v1.18.0`, and Ollama
  `0.31.1 -> 0.32.1`. The expanded focused run contained exactly those six
  subtest failures plus one independent stale Keycloak hardening literal
  failure. The direct-current-document map and lifecycle classification
  contracts already passed.
- Generator evidence: write-mode
  `scripts/operations/sync-tech-stack-versions.sh` reported `changes=6` and
  updated only `infra/tech-stack.versions.json`. The provenance generator
  reported 21 images with severity counts `none:20`, `advisory:1`, `high:0`,
  and `critical:0`. Both later check modes passed with `changes=0` and a fresh
  generated snapshot.
- Current-document evidence: nine infra READMEs and five direct-impact Stage
  05 guide/policy/runbook consumers now use the curated values. PostgreSQL has
  no listed direct current-document consumer in this task. Historical,
  incident, migration, archive, dashboard-label, and negative-fixture text was
  not rewritten as a version consumer.
- Hardening evidence: Keycloak resolves its expected image from
  `infra/tech-stack.versions.json` and retains the template, Docker Secret,
  middleware, address, and health-check assertions. After the fail-fast
  Keycloak blocker was removed, Tier 11 exposed a previously hidden stale
  Dozzle literal. Controller-approved RED/GREEN removed both stale/current
  free-standing Dozzle tags and resolves the exact `dozzle` service image from
  its Compose file. The full 11-tier checker then passed.
- Lifecycle classification: all 19 tracked or newly added target text paths
  containing `legacy` or `deprecated` remain preserved: one historical, eight
  migration, two dashboard-label, and eight negative-fixture paths. The
  six-category policy fixture also preserves incident and archive evidence,
  while a registered active obsolete implementation yields the exact blocking
  classification finding. No destructive gate was satisfied, so Task 3
  records 19 preserve classifications and zero delete/migrate action.
- Manifest and generated-summary evidence: the original four Task 3 target rows are
  `infra/01-gateway/README.md`, `infra/tech-stack.versions.json`,
  `scripts/hardening/check-all-hardening.sh`, and
  `tests/validation/test_tech_stack_version_contract.py`. The successor now
  also includes direct-impact path `infra/11-laboratory/dozzle/README.md` and
  contains 141 rows: 90 `preserve`, 51 `update`, 0 `migrate`, and 0 `delete`;
  all 141 specification/quality verdict pairs remain `pending`. The original
  exact repository oracle failed `136 != 140`; the final expansion failed
  `141 != 140`, then passed after asserting the Dozzle path, owner, consumer,
  disposition, and pending verdicts.
- Safety boundary: no Compose/runtime declaration, service, dependency,
  cache, provider, remote, credential, secret identifier, or secret payload
  changed or was inspected. The controlled wrapper, direct all-files
  pre-commit, broad repository aggregate, live Compose commands, and remote
  operations did not run.
- Final bounded gates: focused version/lifecycle tests passed 7/7; the exact
  repository manifest oracle passed 1/1; version sync reported `changes=0`;
  provenance freshness passed; all 11 hardening tiers passed; supply-chain
  policy passed all 13 fixtures; successor advisory returned zero findings;
  document alignment reported `failures=0`; Ruff, Python compile, Bash syntax,
  ShellCheck, changed-document metadata, Markdown, and staged/unstaged diff
  checks passed. Metadata selected eight changed documents with zero
  violations and five unchanged legacy exceptions. Markdown covered the 16
  non-ledger changed Markdown files plus the Task ledger separately, both with
  zero errors.
- Exact scope evidence: 23 expected changed paths matched 23 actual paths,
  with zero unexpected, zero missing, and zero Compose paths.
- Generated artifact SHA-256 values:
  `infra/tech-stack.versions.json`
  `57006587891c7b435a639bb525c96305ac36225ffa353fb6621c4029d4714edc`;
  provenance
  `8230a7e8adf46836cb71490985b39060f5864ec745dfa11defc9f0673e660b62`;
  successor manifest
  `64d741abc3bd063f7d57758a7fedc8c245a0f8977bc3d0ae4cbc8f4d460f9f91`;
  generated summary
  `66791f8a0b90ecc6c89a6ec5b75f7dcd0f8671d2bfc8718a1c73103009cc50dc`.
- Independent specification and quality/security review of
  `b1e62873..5460e5fc` each returned C0/I1/M0. The first Important finding
  identified missing exact stale-absence assertions across the nine infra and
  five Stage 05 mappings. The second identified a fail-open Compose image
  resolver plus Keycloak/Dozzle substring dependence.
- Review remediation keeps the resolver behind the exact internal
  `--resolve-compose-service-image` mode. It reads at most 1 MiB through an
  `O_NOFOLLOW` regular-file descriptor, rejects duplicate or malformed
  `services`/target/image structures and unsafe or incomplete scalars, emits
  one value-free diagnostic, and never evaluates file content. Keycloak
  compares exact resolver output to the registry image; Dozzle accepts only
  resolver-validated Compose truth.
- Review-remediation RED was 17 failures across the two static contracts,
  three valid scalar subcases, and twelve initial invalid-fixture subcases.
  Final GREEN is 11/11 focused methods, including thirteen ambiguous/unsafe
  YAML fixtures and symlink, directory, and oversize cases. Sync/provenance,
  all hardening tiers, supply-chain 13, delta advisory, Ruff, compile, Bash,
  ShellCheck, and diff hygiene pass.
- Both initial Important findings were implemented before the later remediation
  reviews recorded below. No successor manifest verdict was promoted.
- Remediation review of `5460e5fc..c04946e5` returned C0/I1/M1 for the
  quoted-sibling boundary and one stale repository-checker diagnostic. The
  final TDD slice failed six quoted-key subcases, then passed 4/4 after target
  identity and sibling boundaries began consuming the same full-match
  service-key grammar. The full focused module passes 16/16 and the diagnostic
  names Compose value `v10.6.11`.
- Final scoped ShellCheck passes the hardening script and the repository
  checker at warning-or-higher severity. The unfiltered repository-checker
  result contains two pre-existing SC2016 informational findings at unchanged
  lines 3546 and 3555; they remain outside this remediation.
- Final remediation review of `c04946e5..cce5abb6` returned C0/I2/M1. Global
  dequoted service-name uniqueness now rejects unrelated quoted/unquoted
  duplicates in both orderings. The Dozzle README is the fifteenth
  direct-current mapping and derives current truth from Compose while rejecting
  stale `v10.6.6`.
- Exactly one final target row was added for the authorized Dozzle README.
  Canonical summary regeneration reports 141 rows, 90 preserve, 51 update,
  and no destructive disposition; every manifest row review verdict remains
  pending for Task 6.
- Fresh independent specification and quality/security reviews of the complete
  `b1e62873..60e0313c` range each returned C0/I0/M0 and COMMIT_READY YES. The
  specification outcome was SPEC_COMPLIANCE YES and the quality/security
  outcome was PASS. Task 3 is approved and complete.

### T-TSDC-004 bounded implementation evidence

- Starting commit:
  `6fabbf05bc2a15f7fb02ff26606d6660c5eb16d5`.
- The machine contract registers seven tracked workflows, 23 globally unique
  jobs, exactly one 16-job required-quality workflow, 16 semantic command
  owners, and eight direct Action identities. Every direct Action reference
  is a registered full SHA; all eight records contain the exact official raw
  manifest URL, retrieval date `2026-07-28`, consumer set, Node 24 runtime,
  and `approved-node24` disposition.
- The duplicate-safe YAML path accepts at most 128 workflows and 2 MiB per
  input, completes short reads, rejects symlinked files and parent
  directories, verifies descriptor/file identity, rejects noncanonical
  repository-relative paths, and emits value-free deterministic findings.
  Mutation coverage rejects forbidden or widened events, branches, paths,
  schedules, permissions, concurrency, job identities, timeouts, direct
  interpolation, mutable or unregistered Actions, and retired Node runtimes.
- CI retains exactly the 16 Plan job IDs. The pre-commit job no longer uses
  `pre-commit/action`, redundant setup-node, or an npm install. It uses the
  pinned setup-python SHA, installs only
  `scripts/requirements-pre-commit.txt` with exact
  `pre-commit==4.6.1`, sets `SKIP=eslint-nextjs`, and calls the dedicated
  CI-only wrapper.
- The CI-only wrapper requires exact `GITHUB_ACTIONS=true` and `CI=true`,
  accepts no arguments, rejects `TASK_FILE` and `ALLOW_PREFIXES`, requires the
  exact skip, and `exec`s only
  `pre-commit run --all-files --show-diff-on-failure`. Its test uses a local
  fake binary to prove exact argv, skip preservation, rejection paths, and
  child exit 37 propagation. Neither the real command nor the controlled
  Agent wrapper ran.
- The repository aggregate invokes the focused workflow checker exactly once
  and no longer contains its overlapping inline workflow parser. Separate
  Stage 00 checks retain the four-way required-ID coupling among the workflow
  contract, CI workflow, desired branch protection, and GitHub governance.
  `tech-stack-version-sync.yml` is registered as non-gating remote automation
  and remains locally inventoried without a remote execution claim.
- Controller-approved manifest expansion added seven factual
  non-destructive `update` rows and changed the existing governance-routing
  test from `preserve` to `update`. The canonical summary now reports 148
  rows: 89 `preserve`, 59 `update`, 0 `migrate`, and 0 `delete`; all 148
  specification and quality verdict pairs remain `pending` for Task 6.
- Initial Task 4 gates passed workflow tests 9/9, the fake-binary wrapper
  test, focused checker `(workflows=7, jobs=23, actions=8)`, exact manifest
  oracle, advisory delta, actionlint, scoped ShellCheck, Ruff, Python compile,
  Bash syntax, changed Markdown plus the separately linted ledger, exact
  20-path scope, and diff hygiene. Governance routing passed all 33 Task
  4-relevant tests; its sole failure is the isolated validation-runtime absence
  of `html5lib`.
- The repository aggregate's Task 4 workflow, Stage 00, QA-routing, and
  repaired script-usage sections pass. Non-Task 4 aggregate limitations are
  four promoted-lifecycle consumer-evidence mismatches, the missing
  `html5lib` validation dependency, stale LLM Wiki index/coverage, stale
  metadata inventory, stale security-readiness output, and five references
  to the absent Plan-prescribed
  `scripts/governance/validate-cross-links.sh`. No substitute pass claim was
  invented.
- Quality review found that mixed quoted and unquoted top-level `on` keys
  survive PyYAML as separate string and boolean identities. Both ordering
  regressions failed before remediation. The focused normalizer now rejects
  coexistence with value-free `workflow-trigger-key-ambiguous`, rejects a
  lone boolean `True` trigger key with `workflow-trigger-key-invalid`,
  preserves unrelated boolean `False`, and leaves exact duplicate quoted keys under
  `yaml-duplicate-key`. The full workflow suite passes 11/11; quality
  re-review remains pending.
- A subsequent quality review found that coordinated edits to a workflow and
  `.github/workflow-contract.yml` could widen permissions without an
  independent invariant. Seven required-quality co-mutations all reproduced
  the gap. One immutable code-owned baseline now fixes the exact top-level
  and job permission maps for all seven paths and distinguishes the changelog
  job's inherited permissions by requiring the workflow key to be absent.
  The six non-gating paths retain exactly five approved write-owner triples;
  six path-scoped widening co-mutations fail with the same value-free
  `workflow-permission-baseline-invalid` code. The full workflow suite passes
  14/14; quality re-review remains pending.
- The round 3 review found five remaining ownership and Stage 00 gaps. Four
  direct `repo-contracts` reruns and the aggregate hardening/eval reruns are
  removed; independent CI jobs and `run-local-qa-gates.sh` retain their
  owners. The workflow validator safely reads the aggregate and resolves
  executable direct/transitive semantic markers, fixes the Action registry to
  its exact eight identities, rejects local Action references, and rejects
  alternate YAML boolean trigger spellings. Stage 00 now compares the exact
  16-job sequence with the governance table and asserts the exact metadata
  base binding, preflight, changed-metadata step, and relative order.
- Round 3 focused RED produced 15 failures across five methods. GREEN passes
  those methods 5/5, the full workflow suite 17/17, Stage 00 mutations 4/4,
  three affected routing tests 3/3, the exact manifest oracle 1/1, and the
  focused CLI `(workflows=7, jobs=23, actions=8)`. Actionlint, warning-level
  ShellCheck, Ruff, Python compile, Bash syntax, Markdown, advisory delta, and
  diff hygiene pass. The full routing module is 35/36; its only failure is the
  known validation-runtime absence of `html5lib`.
- No network, remote, provider, runtime, service, dependency installation,
  cache, credential, secret identifier, or secret payload was read or
  mutated. Independent specification and quality/security reviews remain
  pending.

### T-TSDC-004R-2 identity-cleanup implementation evidence

- The unique executable design checkpoint resolves to
  `86146050e04da99c106177f94c509200b991342d`. The sole implementation attempt
  began from clean pre-implementation HEAD
  `6b506d9246116439be9eb5ea740cff602062571f`; the checkpoint-to-working-tree
  scope remains limited to the two runtime files, their two existing test
  files, and this Task ledger.
- RED used the unchanged five-module discovery. It ran 94 tests in 128.301
  seconds with 74 passes, 11 planned Wave-C skips, six failures, and three
  errors. The failures were the intended adopted-root/Compose/SARIF cleanup
  and unreaped-leader pidfd lifecycle witnesses; there was no import,
  discovery, network, Compose, or external-dependency failure.
- Adapter cleanup starts at adoption: if inherited `N` close fails after
  `F_DUPFD_CLOEXEC` creates `M`, the outer boundary still owns and closes
  `M`. Compose destination/source closes and required unlink, SARIF output
  close and required unlink, and final `M` close are each independently
  attempted in deterministic order. Cleanup failure outranks product or
  operation outcome and is reduced to the fixed value-free root, Compose, or
  SARIF cleanup code.
- The runner opens the leader pidfd immediately after `Popen` and performs no
  `process.poll`, `communicate`, or numeric-PGID liveness probe. Initial
  acquisition recovery makes exactly one bounded wait attempt. Later recovery
  makes one bounded wait only after pidfd readiness is confirmed; unavailable
  or missing readiness skips wait, records cleanup failure, and still attempts
  pidfd close. Normal, nonzero, timeout, output-overflow, and read-error paths
  retain one final bounded reap attempt. Strict proc
  membership uses descriptor-relative `O_NOFOLLOW` traversal, a 65,536
  numeric-entry limit, a 4,096-byte stat limit, fail-closed parsing, and
  value-free errors; no numeric-PGID signal or membership scan occurs after
  reap. TERM/KILL `ESRCH` is accepted only as a disappeared-target race that
  still requires bounded validation.
- Existing top-level tests remain exactly 94. Focused runner/adapter GREEN is
  28/28, and the exact integration GREEN is 94 in 122.596 seconds:
  83 passes, 11 planned Wave-C skips, zero failures, and zero errors.
  Workflow projection remains 7/23/8; `local-harness` and
  `local-all-profiles` remain deterministic and execution-free. Exact Ruff,
  compileall, advisory validation, and diff hygiene pass. The post-
  implementation changed-document metadata check selected 15 documents with
  zero violations and five registered legacy exceptions; documentation
  traceability checked 46 catalog pairs with zero failures.
- The four frozen surfaces remain byte-identical to `17bb5cdd`:
  `.github/workflow-contract.yml`
  `21dcc9a59b4c7fe087431c647e8d385d64125021dfa583542818a68ed84c9d20`,
  `.github/workflows/ci-quality.yml`
  `18bdc27e634f83edcd57da9f39aafff62ffe3bbd76d820a74c061021ee811756`,
  the canonical delta manifest
  `f82b6d7c93ae12d5709e24704b2aad562b5275b56bf7ea3a10c491739da59e87`,
  and its summary
  `4030982fcf981b2ee342929fa61804bd0b20a9be5eef0ef3dbe874864354e514`.
- Graphify remains stale advisory evidence and was corroborated against
  Spec 135, the corrected Plan, Stage 00, and tracked source. No network,
  installation, child gate, real Compose, runtime, remote, secret, controlled
  wrapper, direct pre-commit, or Wave B action ran. Fresh specification and
  quality/security C0/I0 implementation reviews remain mandatory.

### T-TSDC-004R-2 phase-owned runner implementation evidence

- The unique reconciled design checkpoint resolves to
  `5dc496310cbe41f86609c751024a12e984228dd8`. The sole Task 4.2U attempt
  began from clean approval-evidence commit `8f8a393b`. Its
  checkpoint-to-working-tree scope is exactly the runner, its existing test,
  and this Task ledger; no non-ignored untracked path exists.
- Authoritative RED preserved 94-test discovery and ran in 151.560 seconds:
  77 passed, six intended transition subtests failed, 11 planned Wave-C tests
  skipped, and zero errored. The six failures were limited to bound process,
  acquired pidfd, finalized group, reap start, interrupted wait, and
  close-started ownership transitions inside the existing runner top-level
  test. No import, discovery, environment, network, Compose, runtime, or
  dependency failure occurred.
- `_ProcessLifecycle` is production state rather than a no-op hook. It owns the
  bound process and pidfd, derives acquired ownership from the bound
  descriptor, records successful group finalization, and sets `reap_started`
  and `pidfd_close_attempted` before their respective operations. Test
  wrappers call the real transition method, verify its mutation, and only then
  raise. Ordered traces reject PGID signals, readiness observation, proc scans,
  or another wait after reap starts.
- `_run_verified_child` has one outer `BaseException` controller beginning
  with a preinitialized process reference and the successful `Popen` binding.
  Before reap, it selects no-pidfd or pidfd-owned recovery from lifecycle
  state. The single `_bounded_reap` source site performs the only
  grace-bounded wait; the single `_close_pidfd_once` source site marks close
  attempted first and never retries an interrupted or ambiguous close.
  Incomplete reap or close has fixed value-free runner-cleanup precedence.
  Proc-root cleanup is an actual `finally`; PID-directory and stat descriptors
  retain independent `finally` close attempts.
- Final focused runner/adapter GREEN is 28/28 in 3.385 seconds. Final
  authoritative GREEN is `94 = 83 pass + 11 planned Wave-C skip` in 156.093
  seconds with zero failure or error. Workflow inventory is exactly
  `7/23/8`, and execution-free profile projections are exactly `32/32/35`.
  Exact four-file Ruff through the pre-existing uv Ruff 0.15.12 environment,
  compileall, advisory delta validation, changed metadata `15/0` with five
  registered legacy exceptions, traceability `46/0`, and diff hygiene pass.
- The accepted adapter pair remains byte-identical to `483d3a47` at SHA-256
  `a634b60eb179fef833f4a80703dc76f285748e4225ef7c008e1be75003f97815`
  and
  `cb232266558d4935bf2768efadeb3fc73ebfaa7d70965078a21bfcfd636a4ff8`.
  The four `17bb5cdd` freezes remain
  `21dcc9a59b4c7fe087431c647e8d385d64125021dfa583542818a68ed84c9d20`,
  `18bdc27e634f83edcd57da9f39aafff62ffe3bbd76d820a74c061021ee811756`,
  `f82b6d7c93ae12d5709e24704b2aad562b5275b56bf7ea3a10c491739da59e87`,
  and
  `4030982fcf981b2ee342929fa61804bd0b20a9be5eef0ef3dbe874864354e514`.
- Graphify `f8a72211` remained stale advisory evidence and was corroborated
  against the tracked Plan, Spec 135, Stage 00, source, and tests. No network,
  installation, child gate, real Compose, runtime, remote, secret, controlled
  wrapper, direct pre-commit, or Wave B action ran. Fresh reviews later
  returned specification `C0/I0` but quality/security `C0/I2`; the
  implementation is rejected and grants no Wave B authority.

### T-TSDC-004R-2 recovery-owned runner implementation evidence

- The unique recovery-owned design checkpoint resolves to `5274f58b`. The
  implementation scope is exactly the runner, its existing test, and this
  Task ledger; the accepted adapter pair remains frozen at `483d3a47`.
- Test-only RED preserved 94-test discovery and the 11 planned Wave-C skips:
  81 passed and two intended witnesses failed. One witness exposed private
  pre-bind ordinary-exception data, and one exposed the missing
  recovery-owned kill/readiness/reap transition state. No import, discovery,
  network, Compose, runtime, or dependency failure occurred.
- `_ProcessLifecycle.start_process` performs the `Popen` call and immediately
  stores its result; no independent process reference remains authoritative.
  The primary body records a product error, while its actual outer `finally`
  invokes the same finalizer on success and failure.
- The finalizer installs nested ownership before recovery actions: KILL owns
  pidfd readiness, readiness owns the conditional sole bounded reap, and reap
  owns the sole pidfd-close attempt. Real production state records completed
  kill, completed readiness and its result, reap start, completed reap and
  return code, and close attempt. Test wrappers invoke and verify those real
  mutations before interrupting.
- After `reap_started`, neither signaling, readiness, `/proc` observation, nor
  another wait is reachable. `_bounded_reap` is the single bounded wait source
  site, and `_close_pidfd_once` marks close attempted before `os.close`, so an
  interrupted or ambiguous close is not retried.
- Focused runner/adapter GREEN is 28/28 in 3.153 seconds. Authoritative GREEN
  is `94 = 83 pass + 11 planned Wave-C skip` in 27.3 seconds; workflow
  inventory is `7/23/8`, and execution-free projections are `32/32/35`.
  Exact four-file Ruff 0.15.12 and compileall, advisory delta validation,
  changed metadata `15/0` with five registered legacy exceptions,
  traceability `46/0`, and diff hygiene pass.
- Graphify `f8a72211` remains stale advisory evidence and was corroborated
  against the tracked Plan, Spec 135, Stage 00, runner source, and tests. No
  network, installation, child gate, real Compose, runtime, remote, secret,
  controlled wrapper, direct pre-commit, or Wave B action ran.
- Fresh read-only specification and quality/security reviews of
  `5274f58b..cdae7523` both returned `C0/I0/M0` and `COMMIT_READY YES`.
  Specification returned `SPEC_COMPLIANCE YES`; quality/security returned
  `QUALITY_SECURITY PASS`. Controller revalidation retained the exact
  three-path scope, all freezes, clean status, metadata `15/0`, traceability
  `46/0`, and diff hygiene. Task 4.2V is accepted, so the clean
  controller-owned evidence checkpoint opens only Task 4.3 Wave B.

### T-TSDC-004R-3 atomic projection cutover evidence

- The test-first focused RED against the reviewed schema-v2 registry exposed
  the expected unconverted workflow programs and compatibility routes:
  75 tests produced 36 failures, two errors, and 11 planned Wave-C skips before
  production edits. The registry itself remained frozen.
- Every required-quality executable step now uses one exact static
  `run-ci-gate.py --profile ci --gate <id>` invocation. The focused validator
  reports exactly seven workflows, 23 jobs, and eight registered Actions, and
  the structural projection tests retain all 16 required status IDs.
- The repository umbrella no longer dispatches the focused workflow checker.
  Local default, harness, and all-profile modes each delegate once to their
  registered profile; list and dry-run projections execute no child gate.
  Local profiles exclude `setup.compose-env`, and `.env` preservation has a
  focused regression.
- The seven descriptor-compatibility consumers retain their direct-execution
  fallback and accept only the runner-created `HYHOME_CI_GATE_ROOT` override.
  Focused descriptor, sibling-import, exact-set, and direct-execution
  regressions pass.
- Final core GREEN is 110 tests: 98 passed with 11 intentional inactive
  semantic-parser Wave-C skips and one local `html5lib` dependency skip. The
  target-delta suite passes 30/30; the fake CI pre-commit contract, four
  execution-free CI/local profile projections, Bash syntax, warning-level
  ShellCheck, actionlint, compileall, advisory delta validation, and diff
  hygiene all pass. Document alignment passes with 5,666 links and zero
  failures, traceability passes 46/0, and changed metadata passes 15/0 with
  five registered legacy exceptions. Ruff is `unverified` because the local
  interpreter has no `ruff` module and dependency installation is outside this
  wave.
- The delta oracle is exactly 158 rows: 85 `preserve`, 73 `update`, zero
  `migrate`, and zero `delete`. All review verdicts remain `pending`.
  `.github/workflow-contract.yml` remains byte-frozen at SHA-256
  `21dcc9a59b4c7fe087431c647e8d385d64125021dfa583542818a68ed84c9d20`;
  the CI-only pre-commit wrapper, its fake test, its requirements pin, and
  `.pre-commit-config.yaml` are also unchanged.
- Graphify `f8a72211` remains stale advisory evidence and was corroborated
  against the tracked Plan, Spec 135, Stage 00, workflow, registry, source, and
  tests. No child gate, real Compose, dependency installation, network,
  runtime, remote, secret, controlled-wrapper, direct pre-commit, or Wave-C
  action ran. Remote required-check and ruleset enforcement remain
  `unverified`; independent Task 4.4 reviews are still required.

### T-TSDC-004R-4 bounded cutover remediation attempt 1 evidence

- Fresh Task 4.4 review of `cfce3218..fd124581` rejected the cutover with
  specification `C0/I5/M0` and quality/security `C0/I4/M0`. The accepted
  findings covered required-step execution context, git-flow checkout,
  retired repository-umbrella ownership, descriptor-root authentication, and
  shared CI/local node identity.
- Focused RED ran 80 tests with 15 failures, one error, and 12 planned Wave-C
  skips. The failures reproduced all six execution-context mutations, the
  missing git-flow checkout, all seven invalid descriptor consumers, and
  registry-derived sibling dispatch. One new shared-profile oracle was
  corrected before production changes because `local-all-profiles`
  legitimately adds `leaf.compose-all-profiles-validation`.
- GREEN admits only the exact git-flow job condition and the exact
  `always()` QA-summary step condition; rejects workflow/job `defaults.run`,
  other job/step conditions, custom shells, and working directories; and
  requires the registered pinned checkout before the git-flow runner.
  The focused two-module rerun passes 80 tests with 12 planned skips.
- All seven compatibility consumers now accept only an inherited
  `/proc/self/fd/<nonnegative-integer>` directory capability whose device and
  inode match their direct script-relative repository root. Invalid and
  mismatched values return the fixed value-free
  `FAIL: invalid HYHOME_CI_GATE_ROOT` diagnostic. Every consumer retains
  direct fallback, and the metadata checker imports its sibling through the
  verified selected root.
- The repository umbrella retains unique repository and Stage 00 cross-surface
  wiring checks but no longer intentionally dispatches registered lifecycle,
  target-surface, workflow, CI-precommit, provider/agent, metadata, generated,
  or profile siblings. Its test derives the complete sibling entrypoint set
  from the frozen registry. The stale direct metadata preflight/step
  assertions and retired local-wrapper command/function assumptions are gone.
- The full Task 4.3 five-module slice passes 115 tests with 12 planned skips.
  CI and three local execution-free projections, local `--list`, Bash syntax,
  actionlint, compileall, and diff hygiene pass. ShellCheck passed after
  restoring the unique top-level docs-taxonomy comparison. Ruff is
  `unverified` because the local Python runtime has no Ruff module and
  dependency installation is prohibited.
- Target-delta advisory, changed-document metadata, traceability, the
  repository umbrella, the standalone workflow checker, and every other
  registered child gate were
  `skipped — controller dispatch prohibited registered child-gate execution`.
  No direct pre-commit, controlled wrapper, real Compose, dependency install,
  network, remote mutation, runtime, credential, secret, or Graphify update
  ran.

### T-TSDC-004R-5 final bounded cutover remediation evidence

- Fresh scoped review of attempt 1 returned specification `C0/I4/M0` and
  quality/security `C0/I3/M0`. The final accepted findings covered the exact
  frozen repository leaf, real runner entrypoint-descriptor execution, and the
  incomplete sibling-dispatch proof. This is bounded implementation attempt
  2/2; no further retry is authorized.
- Focused RED ran 81 tests with 14 failures and 12 planned Wave-C skips. The
  failures reproduced the deterministic repository-wiring baseline failure,
  all three shell consumers rejecting a valid dual-descriptor invocation, and
  ten dispatch families missed by the narrow umbrella oracle.
- The typed repository wiring block now matches the exact frozen
  `leaf.repo-contracts` node, including no allowed environment keys and all
  four `ci`, `local-script-backed`, `local-harness`, and
  `local-all-profiles` memberships. Its isolated positive baseline passes and
  a profile mutation returns the fixed wiring diagnostic.
- Each shell compatibility consumer resolves its executing entrypoint before
  deriving the direct repository fallback. The runner-fidelity fixture opens
  both the copied shell entrypoint and repository root, invokes
  `bash /proc/self/fd/<entrypoint-fd>`, inherits both descriptors, and proves
  valid, invalid-syntax, mismatched-root, and regular-path fallback behavior.
  The four Python consumers and metadata selected-root import remain covered.
- The registry-derived wiring-only proof separates path references from
  execution sinks and covers literal Python/Bash, direct executable, quoted,
  variable-mediated, `command`/`env`/`exec`, helper-indirection, and Python
  heredoc `subprocess`/`os.system` dispatch. Every family has a mutation
  witness and the live umbrella has no registered sibling dispatch.
- Focused GREEN passes 81 tests with 12 planned skips. The full Task 4.3
  five-module slice passes 116 tests with 12 planned skips.
- Standalone workflow, target-delta advisory, changed-document metadata, and
  traceability static validations pass. All four typed profile dry-run
  projections, Bash syntax, ShellCheck, compileall, exact frozen-surface,
  six-path scope, mode, clean-worktree, and diff checks pass. Ruff remains
  `unverified` because the local Python runtime has no Ruff module and
  installation is prohibited.
- The repository umbrella itself was not run. No typed child gate, direct
  pre-commit, controlled wrapper, real Compose/runtime action, installation,
  network, remote mutation, credential/secret access, or Graphify update ran.
- Final attempt-2 re-review returned specification `C0/I0/M0`,
  `SPEC_COMPLIANCE YES`, and `COMMIT_READY YES`, but quality/security returned
  `C0/I1/M0`, `QUALITY_SECURITY FAIL`, and `COMMIT_READY NO`. The remaining
  load-bearing finding is that the dispatch proof does not consume operands
  for valid option-bearing wrapper forms such as `command -p`, `env -u NAME`,
  and `exec -a NAME`; these forms can still hide a registered sibling
  dispatch. The canonical two-attempt implementation loop is exhausted.
  Task 4R therefore returns to design/plan, and Wave C plus Tasks 5–6 remain
  blocked. No finding is waived and no manifest verdict is promoted.

### T-TSDC-004R-4W option-aware wrapper-proof design return

- User approval on 2026-07-30 authorizes a Plan-only successor for the single
  remaining Important option-bearing wrapper bypass. The design checkpoint
  starts after `1b054313` and does not waive or reclassify the failed Task 4.4
  quality/security review.
- The implementation allowlist is exactly
  `tests/validation/test_agent_governance_ci_routing.py` and this Task ledger.
  `.github/workflow-contract.yml`, `.github/workflows/ci-quality.yml`,
  `scripts/validation/check-repo-contracts.sh`, the typed runner/adapters,
  target-delta artifacts, and all other tracked paths are frozen.
- The required pure static parser recursively unwraps option-bearing
  `command`, GNU `env`, and Bash `exec`; consumes recognized option operands
  before command-position analysis; treats `command -v/-V` as query-only;
  implements the static Coreutils 9.11 `env -S/--split-string` escape,
  quote, separator, comment, and truncation grammar without reading ambient
  state; treats GNU `env -0/--null` as no-dispatch; distinguishes option
  operands from executable siblings; and fails closed for dynamic, unknown,
  malformed, or work-budget-exhausted forms.
- The RED matrix must cover every accepted option form, nested wrappers,
  query-only and option-operand negatives, unknown/malformed fail-closed
  forms, and all existing dispatch families. Evidence remains deterministic
  and value-free.
- The initial Plan checkpoint at `98a3558d` received specification
  `C0/I4/M0` and quality/security `C0/I3/M0`. Accepted findings require exact
  GNU `env -S` handling, an executable unique Plan-review evidence
  prerequisite, failure-producing full-surface scope/mode/clean oracles, and a
  RED matrix equal to the complete admitted wrapper grammar.
- One bounded correction must use the exact subject
  `docs(plan): correct option-aware cutover proof`. No implementation
  authority exists until the corrected net Plan receives final fresh
  independent specification and quality/security `C0/I0/M0` reviews recorded
  in the exact unique Task-ledger-only
  `docs(task): record option-aware proof plan reviews` commit. If approved,
  one implementation agent receives exactly one attempt and one fresh
  implementation review pair. Any non-`C0/I0/M0` implementation review
  returns to design without retry.
- The bounded correction committed as `a46f29b8`. Final quality/security
  review returned `C0/I2/M0`, `QUALITY_SECURITY FAIL`, and
  `IMPLEMENTATION_READY NO`. GNU `env --` still consumes leading `NAME=VALUE`
  operands before selecting the command, contrary to the corrected Plan, and
  later evidence blocks incorrectly reuse shell variables across independent
  agent/controller sessions instead of resolving exact unique subjects
  locally. The specification re-review was interrupted after this
  load-bearing quality blocker and has no verdict.
- The sole Plan correction is exhausted. No Plan-review evidence commit,
  implementation attempt, test execution, manifest promotion, Wave C, Task 5,
  Task 6, or whole-branch review is authorized. A new user-approved bounded
  design/Plan successor is required.
- Wave C, Tasks 5–6, and whole-branch review remain blocked. No repository
  umbrella, registered typed child gate, direct pre-commit, controlled
  wrapper, Compose/runtime, dependency installation, network, remote state,
  secret/credential access, or Graphify update is authorized.

### T-TSDC-004R-4X session-local option-proof design return

- User approval on 2026-07-30 authorizes a new Plan-only successor after the
  exact unique `docs(task): record exhausted option-aware plan review`
  checkpoint at `7b792a37`. The failed 4W Plan remains historical evidence
  and grants no implementation authority.
- 4X changes only two design defects: GNU `env --` ends option parsing but
  still permits the subsequent consecutive `NAME=VALUE` assignment phase,
  and every independent agent/controller/reviewer shell block must resolve
  every commit variable locally from an exact unique subject.
- The 4W parser grammar, complete RED matrix, focused GREEN, frozen regression
  ladder, deterministic work budget, value-free diagnostics, two-path
  implementation allowlist, and production-path freezes otherwise remain
  normative. All 4W command blocks and its uncreated pending subjects are
  superseded and must not be executed.
- The Plan checkpoint uses the exact unique subject
  `docs(plan): define session-local option proof`. It grants no implementation
  authority until a fresh read-only specification reviewer and a different
  fresh read-only quality/security reviewer both return `C0/I0/M0` over the
  exact `7b792a37..$plan_checkpoint` range.
- If approved, the controller records the pair in the exact unique
  Task-ledger-only `docs(task): record session-local proof plan reviews`
  commit. One implementation agent then receives exactly one attempt over
  only `tests/validation/test_agent_governance_ci_routing.py` and this Task
  ledger, using the exact unique subject
  `fix(ci): close session-local wrapper proof`.
- A fresh implementation specification reviewer and a different fresh
  quality/security reviewer must both return `C0/I0/M0`. The controller then
  records the pair in the exact unique Task-ledger-only
  `docs(task): record session-local wrapper review` commit. Any failed Plan or
  implementation review returns to design without correction or retry.
- At this Plan checkpoint, no Plan-review evidence commit, implementation,
  test execution, manifest promotion, Wave C, Tasks 5–6, or whole-branch
  review is authorized. Remote, runtime, dependency, secret, direct
  pre-commit, controlled-wrapper, and Graphify authority remain unchanged.
- The Plan committed as
  `8d3f11220ab4a6cdc61abd88e2df9caad056ac3d`. Fresh read-only
  reviewers inspected exact immutable range `25524ce1..8d3f1122`.
  Specification returned `C0/I2/M0`, `SPEC_COMPLIANCE NO`, and
  `IMPLEMENTATION_READY NO`; the different quality/security reviewer returned
  `C0/I2/M0`, `QUALITY_SECURITY FAIL`, and `IMPLEMENTATION_READY NO`.
- Specification found that the fallback-resistant matrix omits long
  `--split-string STRING` and `--split-string=STRING` dispatch/query witnesses
  and does not prove that unresolved direct, `command`, `python3`, or `bash`
  heads without a relevant sibling remain no-dispatch.
- Quality/security found that `ambiguous(items)` delegates to the existing
  early-return candidate collector, which can retain an exact sibling but drop
  a different sibling embedded in another token. It also found that the
  named-variable-only dynamic predicate excludes unresolved `$1` and `${1}`
  positional command heads even though the current resolver recognizes those
  forms.
- Passing strict-block, capture-consumption, scope, mode, ancestry, metadata,
  traceability, and diff checks does not override these four load-bearing
  findings. The accepted
  `docs(task): record explicit parser outcome plan reviews` checkpoint is not
  created. The 4AB no-correction Plan loop is exhausted without an
  implementation attempt. The user-approved 4AC successor committed its exact
  Plan checkpoint, but its fresh quality/security review failed; the 4AC
  no-correction Plan loop is also exhausted without an implementation attempt.
- The Plan committed as `4c7c9c4b`. Fresh specification review over
  `7b792a37..4c7c9c4b` returned `C0/I0/M0`, `SPEC_COMPLIANCE YES`, and
  `IMPLEMENTATION_READY YES`. The different fresh quality/security review
  returned `C0/I2/M0`, `QUALITY_SECURITY FAIL`, and
  `IMPLEMENTATION_READY NO`.
- Quality/security found that the load-bearing shell proof blocks lack
  fail-fast execution (`set -euo pipefail` or equivalent), so an earlier
  failed oracle can be masked by a later successful command. It also found
  that Task 4.5 Step 0 does not independently resolve the 4X implementation
  base or revalidate the exact two-path implementation range and implementation
  plus review file modes.
- The 4X no-correction Plan loop is exhausted. No Plan-review evidence commit,
  implementation attempt, test execution, manifest promotion, Wave C,
  Tasks 5–6, or whole-branch review is authorized. A new user-approved bounded
  design/Plan successor is required.

### T-TSDC-004R-4Y fail-fast lineage-proof design return

- User approval on 2026-07-30 authorizes a Plan-only successor after the exact
  unique `docs(task): record exhausted session-local plan review` checkpoint
  at `481b1a8e`. Failed 4W and 4X Plans remain historical evidence and grant no
  implementation authority.
- 4Y closes only the two 4X review findings. Every new Bash proof block is an
  independent strict session using `set -euo pipefail` and
  `shopt -s inherit_errexit`; the expected focused RED has one explicit,
  immediately bounded nonzero exception and a fixed behavior marker.
- Task 4.5 now re-resolves the complete design-base -> Plan -> Plan-review
  evidence -> implementation -> implementation-review chain and proves exact
  subject uniqueness, direct ancestry counts, the Plan two-path scope, both
  Task-only evidence scopes, the implementation two-path scope, relevant
  `100644` modes, `HEAD`, and clean state.
- The complete 4W parser grammar, RED matrix, deterministic budget, focused
  GREEN, frozen regression ladder, value-free diagnostics, two-path
  implementation allowlist, production freezes, and prohibitions remain
  normative. The corrected 4X GNU `env --` assignment phase and session-local
  lookup contract also remain normative. All earlier command blocks and
  uncreated pending subjects are non-executable.
- The Plan checkpoint uses the exact unique subject
  `docs(plan): define fail-fast lineage proof`. It grants no implementation
  authority until a fresh read-only specification reviewer and a different
  fresh read-only quality/security reviewer both return `C0/I0/M0` over the
  exact `481b1a8e..$plan_checkpoint` range.
- If approved, the controller records the pair in the exact unique
  Task-ledger-only `docs(task): record fail-fast lineage plan reviews`
  checkpoint. One implementation agent then receives exactly one attempt over
  only `tests/validation/test_agent_governance_ci_routing.py` and this Task
  ledger with the exact unique subject
  `fix(ci): close fail-fast wrapper proof`.
- A fresh implementation specification reviewer and a different fresh
  quality/security reviewer must both return `C0/I0/M0`. The controller then
  records the pair in the exact unique Task-ledger-only
  `docs(task): record fail-fast wrapper review` checkpoint. Any failed Plan or
  implementation review returns to design without correction or retry.
- At this Plan checkpoint, no Plan-review evidence commit, implementation,
  test execution, manifest promotion, Wave C, Tasks 5–6, or whole-branch
  review is authorized. Remote, runtime, dependency, secret, direct
  pre-commit, controlled-wrapper, and Graphify authority remain unchanged.
- The Plan committed as `a8cc9751`. Fresh quality/security review over
  `481b1a8e..a8cc9751` returned `C0/I1/M0`,
  `QUALITY_SECURITY FAIL`, and `IMPLEMENTATION_READY NO`. The specification
  review was interrupted after this load-bearing blocker and has no verdict.
- Quality/security confirmed the RED exception, local subject resolution,
  complete Task 4.5 lineage/scope/mode proof, freezes, prohibitions, and
  downstream authorization. The remaining defect is that fallible command
  substitutions are sometimes embedded directly inside `test`; for example,
  a failed `git status` that emits no stdout can become `test -z ""` and pass.
  `inherit_errexit` does not preserve the substitution exit status through the
  enclosing `test`.
- The 4Y no-correction Plan loop is exhausted. No Plan-review evidence commit,
  implementation attempt, test execution, manifest promotion, Wave C,
  Tasks 5–6, or whole-branch review is authorized. A new user-approved bounded
  design/Plan successor must capture every fallible substitution in a
  standalone assignment before testing its value.

### T-TSDC-004R-4Z status-preserving proof design return

- User approval on 2026-07-30 authorizes a Plan-only successor after the exact
  unique `docs(task): record exhausted fail-fast plan review` checkpoint at
  `0177006c`. Failed 4W, 4X, and 4Y Plans remain historical evidence and grant
  no implementation authority.
- 4Z changes only substitution status propagation. Every fallible command
  substitution is the complete right-hand side of a standalone simple
  assignment; the next command tests the value. No `test`, conditional,
  comparison, function argument, or compound consumer embeds `$()`.
- Every Bash block retains `set -euo pipefail` and
  `shopt -s inherit_errexit`. A failed substitution therefore makes its
  standalone assignment fail and terminates the block. The expected focused
  RED remains the sole explicitly bounded exception.
- The accepted 4W parser/matrix/budget/evidence contract, corrected 4X GNU
  `env --` and session-local contract, and 4Y strict session, complete Task 4.5
  lineage/scope/mode proof, freezes, and prohibitions remain normative. All
  earlier command blocks and uncreated pending subjects are non-executable.
- The Plan checkpoint uses the exact unique subject
  `docs(plan): define status-preserving proof`. It grants no implementation
  authority until a fresh read-only specification reviewer and a different
  fresh read-only quality/security reviewer both return `C0/I0/M0` over the
  exact `0177006c..$plan_checkpoint` range.
- If approved, the controller records the pair in the exact unique
  Task-ledger-only `docs(task): record status-preserving plan reviews`
  checkpoint. One implementation agent then receives exactly one attempt over
  only `tests/validation/test_agent_governance_ci_routing.py` and this Task
  ledger with the exact unique subject
  `fix(ci): close status-preserving wrapper proof`.
- A fresh implementation specification reviewer and a different fresh
  quality/security reviewer must both return `C0/I0/M0`. The controller then
  records the pair in the exact unique Task-ledger-only
  `docs(task): record status-preserving wrapper review` checkpoint. Any failed
  Plan or implementation review returns to design without correction or
  retry.
- At this Plan checkpoint, no Plan-review evidence commit, implementation,
  test execution, manifest promotion, Wave C, Tasks 5–6, or whole-branch
  review is authorized. Remote, runtime, dependency, secret, direct
  pre-commit, controlled-wrapper, and Graphify authority remain unchanged.
- The Plan committed as `9968bb6d`. Fresh specification review over
  `0177006c..9968bb6d` returned `C0/I0/M0`, `SPEC_COMPLIANCE YES`, and
  `IMPLEMENTATION_READY YES`. The different fresh quality/security review
  returned `C0/I1/M0`, `QUALITY_SECURITY FAIL`, and
  `IMPLEMENTATION_READY NO`.
- Quality/security confirmed standalone substitution capture, strict RED
  handling, the complete Task 4.5 chain, scopes, modes, freezes, prohibitions,
  and downstream gate. The remaining defect is internal contract
  inconsistency: 4Z says the next command tests each captured value, but some
  blocks perform another assignment first. The reported substitution-shape
  audit therefore proves status-preserving capture but not the stronger
  immediate-consumption invariant written into the Plan and Task.
- The 4Z no-correction Plan loop is exhausted. No Plan-review evidence commit,
  implementation attempt, test execution, manifest promotion, Wave C,
  Tasks 5–6, or whole-branch review is authorized. A new user-approved bounded
  design/Plan successor must place an explicit value test immediately after
  every non-RED fallible substitution assignment and statically prove those
  capture/test pairs.

### T-TSDC-004R-4AA immediate-consumption proof design return

- User approval on 2026-07-30 authorizes a Plan-only successor after the exact
  unique `docs(task): record exhausted status-preserving plan review`
  checkpoint at `355a1db5`. Failed 4W through 4Z Plans remain historical
  evidence and grant no implementation authority.
- 4AA changes only capture consumption. Every non-RED fallible substitution is
  a standalone assignment whose immediately following command is a `test`
  naming that exact variable. When a semantic comparison is not yet available,
  the adjacent test is `test -n "$variable"`.
- The focused RED remains the sole exception:
  `red_output` is immediately followed by `red_status="$?"`; `errexit` is then
  restored before output and assertions.
- The accepted parser, GNU `env --`, session-local, strict-session,
  status-preserving, full lineage/scope/mode, freeze, and prohibition
  contracts remain normative. All earlier command blocks and uncreated
  pending subjects are non-executable.
- The Plan checkpoint uses the exact unique subject
  `docs(plan): define immediate-consumption proof`. It grants no implementation
  authority until a fresh read-only specification reviewer and a different
  fresh read-only quality/security reviewer both return `C0/I0/M0` over the
  exact `355a1db5..$plan_checkpoint` range.
- If approved, the controller records the pair in the exact unique
  Task-ledger-only `docs(task): record immediate-consumption plan reviews`
  checkpoint. One implementation agent then receives exactly one attempt over
  only `tests/validation/test_agent_governance_ci_routing.py` and this Task
  ledger with the exact unique subject
  `fix(ci): close immediate-consumption wrapper proof`.
- A fresh implementation specification reviewer and a different fresh
  quality/security reviewer must both return `C0/I0/M0`. The controller then
  records the pair in the exact unique Task-ledger-only
  `docs(task): record immediate-consumption wrapper review` checkpoint. Any
  failed Plan or implementation review returns to design without correction
  or retry.
- At this Plan checkpoint, no Plan-review evidence commit, implementation,
  test execution, manifest promotion, Wave C, Tasks 5–6, or whole-branch
  review is authorized. Remote, runtime, dependency, secret, direct
  pre-commit, controlled-wrapper, and Graphify authority remain unchanged.
- The Plan committed as `861c0e33`. Fresh read-only specification review and
  a different fresh read-only quality/security review over
  `355a1db5..861c0e33` both returned `C0/I0/M0`,
  `IMPLEMENTATION_READY YES`; the role-specific verdicts are
  `SPEC_COMPLIANCE YES` and `QUALITY_SECURITY PASS`.
- Reviewers found no unresolved issue in the 112 immediate capture/test pairs,
  sole RED status exception, strict sessions, parser and GNU `env --`
  contract, full Task 4.5 lineage/scope/mode gate, freezes, prohibitions, or
  downstream authorization.
- This Task-ledger-only evidence checkpoint authorizes one 4AA implementation
  agent to make the exact two-path attempt defined by the Plan. Wave C,
  manifest promotion, Tasks 5–6, whole-branch review, runtime, network,
  secrets, direct pre-commit, controlled wrapper, and Graphify update remain
  blocked.

### T-TSDC-004R-4AA immediate-consumption implementation evidence

- The immutable implementation base is
  `194b7d1675eed86911092ea8e7cbe70ac6f94de0`, the exact unique
  `docs(task): record immediate-consumption plan reviews` checkpoint. The
  implementation touched only
  `tests/validation/test_agent_governance_ci_routing.py` and this Task ledger.
- RED added the complete 4W option-aware wrapper matrix and 4X GNU `env --`
  assignment transitions inside
  `test_repository_umbrella_is_wiring_only`. The focused RED command exited
  nonzero after importing and reaching the named test: one test ran with 41
  behavior-specific subtest failures across `command`, `exec`, GNU `env`,
  `env -S`, query/no-dispatch, and fail-closed cases. The fixed assertion
  marker `GNU env -- assignment scan must reach command` is present in the
  added test oracle.
- GREEN implements one dependency-free bounded recursive parser for Bash
  `command`, Bash `exec`, and GNU `env`. It consumes recognized option arity
  before command-position evaluation, implements the corrected post-`--`
  assignment scan, uses a static GNU `env -S` lexer without ambient environment
  reads, treats unsupported expansion, malformed split strings, unknown
  options, and budget exhaustion as deterministic fail-closed outcomes, and
  preserves existing literal, quoted, variable, helper, Python heredoc
  `subprocess`, and `os.system` dispatch families.
- Focused GREEN passed:
  `test_repository_umbrella_is_wiring_only` `1/1`; full routing passed
  `42` tests with one planned local `html5lib` skip; workflow plus routing
  passed `81` tests with 12 planned Wave-A skips; the full five-module frozen
  regression passed `116` tests with 12 planned Wave-A skips.
- Static and projection evidence passed:
  workflow contract `workflows=7, jobs=23, actions=8`; target-surface delta
  advisory exit 0; changed metadata `selected=15 violations=0
  legacy_exceptions=5`; traceability `catalog_pairs_total=46 failures=0`;
  execution-free projections for `ci --list`, `ci --dry-run --all`,
  `local-script-backed --dry-run --all`, `local-harness --dry-run --all`, and
  `local-all-profiles --dry-run --all`; compileall; and diff hygiene.
- Ruff is `unverified` because `python3 -c 'import ruff'` failed with
  `ModuleNotFoundError` and dependency installation is prohibited. The
  repository umbrella, registered typed child gates, direct pre-commit,
  controlled wrapper, Compose/runtime, network, secrets, credentials, remote
  state, and Graphify update were not run.

### T-TSDC-004R-4AA exhausted implementation review

- Fresh read-only reviewers inspected the exact immutable range
  `194b7d1675eed86911092ea8e7cbe70ac6f94de0..84067c8f30536723f1d73ff6254f0204e6bf4a8a`.
  Specification returned `C0/I1/M0`, `SPEC_COMPLIANCE NO`, and
  `IMPLEMENTATION_READY NO`; the different quality/security reviewer returned
  `C0/I3/M0`, `QUALITY_SECURITY FAIL`, and `IMPLEMENTATION_READY NO`.
- Both reviewers found that short, attached, and clustered GNU `env -S`
  inserts split tokens and then advances past the first inserted token. Direct
  head misclassification or the conservative fallback lets current positives
  pass without proving the required recursive transition, while real
  dispatches can be missed and query-only forms can be reported as dispatch.
- Quality/security also found two independent fail-closed gaps: an unresolved
  dynamic command head can ignore a later registered sibling, and malformed
  signal long-option near-prefixes containing `=` are consumed as recognized
  options instead of producing a finding.
- Passing focused and frozen regression evidence does not override these
  load-bearing review findings. The accepted
  `docs(task): record immediate-consumption wrapper review` checkpoint is not
  created. This Task-ledger-only exhausted-review checkpoint records the
  rejected attempt without changing the test oracle.
- The one-attempt 4AA contract is exhausted without retry. Task 4R, Wave C,
  Tasks 5–6, and whole-branch review remain blocked. Any correction requires a
  new user-approved bounded design/Plan successor; no manifest verdict,
  runtime claim, remote claim, wrapper authority, or pre-commit authority is
  promoted.

### T-TSDC-004R-4AB explicit parser-outcome proof design return

- User approval on 2026-07-30 authorizes a Plan-only successor after the exact
  unique `docs(task): record exhausted immediate-consumption wrapper review`
  checkpoint at
  `25524ce1af36ee8572b9e0c855700680db957921`. Failed or exhausted
  4W through 4AA work remains historical evidence and grants no implementation
  authority.
- 4AB changes only the static oracle contract and its behavior-specific tests.
  `parse_chain`, `parse_command`, `parse_exec`, and `parse_env` use one
  explicit local result tagged `dispatch`, `no-dispatch`, or `ambiguous`, and
  convert that result to the existing public sibling-path set only at the
  outer `command_sink` boundary.
- GNU `env -S` separated, attached, long, and clustered forms combine their
  statically split tokens with the untouched original tail and immediately
  re-enter the same `parse_env` function at the first combined token. The one
  original no-credit budget is shared across recursion and split lexing.
- An unresolved dynamic command head or unresolved dynamic script operand
  after `python3`/`bash`, with a relevant later sibling, is `ambiguous`;
  `command -v` and `command -V` remain proved no-dispatch. Signal options are
  accepted only as an exact bare name or exact `name=value`; malformed
  near-prefixes are `ambiguous`.
- RED must distinguish the intended transition from conservative fallback:
  direct-sibling split strings require the exact singleton, split query forms
  require the empty set, dynamic heads require the exact relevant singleton,
  malformed near-prefix signal values require the exact embedded singleton,
  and valid exact signal values require the empty set.
- The accepted 4W parser/matrix/budget contract, 4X GNU `env --` and
  session-local contract, 4Y strict/full-lineage contract, 4Z
  status-preserving contract, and 4AA immediate capture/test contract remain
  normative. No production module, helper script, workflow, contract,
  generated artifact, or dependency is created.
- The Plan checkpoint uses the exact unique subject
  `docs(plan): define explicit parser outcome proof`. It grants no
  implementation authority until a fresh read-only specification reviewer and
  a different fresh read-only quality/security reviewer both return
  `C0/I0/M0` over the exact `25524ce1..$plan_checkpoint` range.
- Any failed Plan review is recorded in the exact Task-only
  `docs(task): record exhausted explicit parser outcome plan review`
  checkpoint and returns to design without a correction or implementation
  attempt.
- If approved, the controller records the pair in the exact unique
  Task-ledger-only
  `docs(task): record explicit parser outcome plan reviews` checkpoint. One
  fresh implementation agent then receives exactly one attempt over only
  `tests/validation/test_agent_governance_ci_routing.py` and this Task ledger
  with exact unique subject
  `fix(ci): close explicit parser outcome proof`.
- A fresh implementation specification reviewer and a different fresh
  quality/security reviewer must both return `C0/I0/M0`. The controller then
  records an accepted pair in the exact unique Task-ledger-only
  `docs(task): record explicit parser outcome review` checkpoint. A failed
  pair is recorded under
  `docs(task): record exhausted explicit parser outcome review`, exhausts the
  one attempt, and grants no retry or downstream authority.
- At this Plan checkpoint, no Plan-review evidence commit, implementation,
  test execution, manifest promotion, Wave C, Tasks 5–6, or whole-branch
  review is authorized. Remote, runtime, dependency, secret, direct
  pre-commit, controlled-wrapper, and Graphify authority remain unchanged.

### T-TSDC-004R-4AC candidate-closed parser-outcome proof design return

- User approval on 2026-07-30 authorizes one Plan-only bounded successor after
  the exact unique
  `docs(task): record exhausted explicit parser outcome plan review`
  checkpoint at
  `997719ff22cbaa9f4bc0c160f0e6c56fc76d54ba`. Failed or exhausted 4W
  through 4AB work remains historical evidence and grants no implementation
  authority.
- The successor is designed to close the four 4AB Plan-review findings without
  widening the production or workflow surface. The Plan requires one candidate
  collector to scan every token before returning and union all resolved exact
  siblings with all embedded sibling paths. Ambiguity must use that complete
  union and fall back to the complete registered set only when syntax is
  ambiguous and no candidate is recoverable.
- The Plan requires dynamic-target proof to cover unresolved named variables
  and `$1`/`${1}` at direct, `command`, `python3`, and `bash` positions. A
  relevant later sibling must be `ambiguous`; the same unresolved target
  without a relevant sibling must be `no-dispatch`; valid `command -v` and
  `command -V` clusters must take precedence and remain `no-dispatch`.
  Helper-bound positional parameters must continue to resolve through the
  existing positional binding.
- The required RED matrix is intended to prove separated and equals long
  `--split-string` direct, `python3`, and query forms, together with the
  accepted short, attached, and clustered forms. Every split form must lex
  once, combine only with the untouched tail, and re-enter the same
  closure-budgeted `parse_env` at the first combined token without new budget
  credit.
- A two-sibling malformed signal near-prefix witness requires the union of an
  embedded option-value sibling and a different exact remaining sibling. A
  valid exact `name=value` signal option with the same operand proves that the
  option value itself receives no dispatch credit while a following real
  command still dispatches.
- The existing static-oracle statement boundary remains unchanged. 4AC does
  not interpret arbitrary `&&`, `||`, pipeline, or `bash -c` semantics; Spec
  135 excludes arbitrary shell-semantic inference. Any such expansion requires
  a separate approved design and proof.
- The Plan checkpoint uses the exact unique subject
  `docs(plan): define candidate-closed parser outcome proof`. It changes only
  the Plan and this Task ledger and grants no implementation authority until
  a fresh read-only specification reviewer and a different fresh read-only
  quality/security reviewer both return `C0/I0/M0` over exact range
  `997719ff..$plan_checkpoint`.
- Any failed Plan review is recorded in the exact Task-only
  `docs(task): record exhausted candidate-closed parser outcome plan review`
  checkpoint and exhausts 4AC without a correction or implementation attempt.
  If both reviews pass, the controller records them in the exact Task-only
  `docs(task): record candidate-closed parser outcome plan reviews`
  checkpoint. That clean commit becomes the immutable implementation base.
- One fresh implementation agent then receives exactly one attempt over only
  `tests/validation/test_agent_governance_ci_routing.py` and this Task ledger,
  with exact unique subject
  `fix(ci): close candidate-closed parser outcome proof`. A fresh
  specification reviewer and a different fresh quality/security reviewer must
  both return `C0/I0/M0`. The accepted pair is recorded under
  `docs(task): record candidate-closed parser outcome review`; any rejected
  pair is recorded under
  `docs(task): record exhausted candidate-closed parser outcome review` and
  grants no retry or downstream authority.
- The Plan committed as
  `5bc5ab85e9d8841761ae00b7a169e899e3f8f515`. Fresh read-only reviewers
  inspected exact immutable range `997719ff..5bc5ab85`. Specification returned
  `C0/I0/M0`, `SPEC_COMPLIANCE YES`, and `IMPLEMENTATION_READY YES`; the
  different quality/security reviewer returned `C0/I1/M1`,
  `QUALITY_SECURITY FAIL`, and `IMPLEMENTATION_READY NO`.
- Quality/security found that the accepted and rejected review-evidence commit
  sessions do not each rebind the complete reviewed predecessor chain,
  ancestry, distance, exact scope, and file modes. Because subject uniqueness
  is checked only on current ancestry in those sessions, a substituted
  same-subject lineage cannot be excluded. The reviewer also noted the
  now-synchronized Task-ledger wording that called the already committed Plan
  checkpoint pending.
- The rejected-review evidence is recorded in the exact Task-only
  `docs(task): record exhausted candidate-closed parser outcome plan review`
  checkpoint. The accepted
  `docs(task): record candidate-closed parser outcome plan reviews` checkpoint
  is not created. The 4AC no-correction Plan loop is exhausted without a
  correction or implementation attempt.
- No implementation, test execution, manifest promotion, Wave C, Tasks 5–6,
  or whole-branch review is authorized. Remote, runtime, dependency, secret,
  direct pre-commit, controlled-wrapper, and Graphify authority remain
  unchanged.

### T-TSDC-004R-4AD review-range-bound parser proof design return

- User approval on 2026-07-30 authorizes one Plan-only bounded successor after
  the exact unique
  `docs(task): record exhausted candidate-closed parser outcome plan review`
  checkpoint at
  `3510e9944655ee89077a295712e759d116e2e87f`. Failed or exhausted 4W
  through 4AC work remains historical evidence and grants no implementation
  authority.
- 4AD preserves the accepted candidate-closed parser contract and complete
  behavior matrix from the immutable 4AC Plan commit
  `5bc5ab85e9d8841761ae00b7a169e899e3f8f515`: the 4AC files and
  interfaces, candidate-closed contract, Step 2 behavior matrix after its
  historical authority block, and Steps 3–4. It does not change parser
  outcomes, candidate union, dynamic-target boundaries, GNU `env` grammar,
  signal-option grammar, work budget, two-path implementation scope, freezes,
  RED/GREEN expectations, or the bounded validation ladder.
- The Plan defines this review matrix as the canonical full-hash attestation
  surface. After each independent review pair completes, the controller must
  replace that unit's pending range with the identical 40-hex
  `base..reviewed-head` range reported by both reviewers. A terminal evidence
  block must extract exactly one such range from this ledger; a missing,
  abbreviated, duplicated, malformed, or reviewer-divergent range fails
  closed.
- Every accepted and rejected Plan-review evidence session must derive the
  reviewed Plan checkpoint from the 4AD Plan matrix row, bind it to exact
  design base `3510e994`, and re-prove exact subject, single-parent topology,
  ancestry, one-commit distance, exact Plan-and-Task paths, both `100644`
  modes, Task-only evidence scope, evidence-commit distance and mode, and
  clean state.
- Every accepted and rejected implementation-review evidence session must
  derive the reviewed implementation range from the 4AD implementation matrix
  row. In the same strict session it must also re-extract the Plan review
  range and prove the entire design-base → Plan → accepted Plan-review
  evidence → implementation → terminal review chain, every one-commit
  distance, each exact parent, each exact path set, every `100644` mode, and
  clean state.
- Task 4.5 Step 0 repeats that complete proof from the same two canonical
  full-hash attestations before Wave C can modify any file. Subject lookup is
  performed with `git show` on already-bound OIDs; current-ancestry
  `git log --grep` lookup is never the authority for a reviewer-inspected
  range.
- The Plan checkpoint uses exact unique subject
  `docs(plan): define review-range-bound parser outcome proof`. It changes
  only the Plan and this Task ledger and grants no implementation authority
  until a fresh read-only specification reviewer and a different fresh
  read-only quality/security reviewer both return `C0/I0/M0` over exact range
  `3510e994..$plan_checkpoint`.
- Any failed Plan review is recorded in exact Task-only
  `docs(task): record exhausted review-range-bound parser outcome plan review`
  and exhausts 4AD without a correction or implementation attempt. If both
  reviews pass, exact Task-only
  `docs(task): record review-range-bound parser outcome plan reviews` becomes
  the immutable implementation base.
- One fresh implementation agent then receives exactly one attempt over only
  `tests/validation/test_agent_governance_ci_routing.py` and this Task ledger,
  with exact unique subject
  `fix(ci): close review-range-bound parser outcome proof`. A fresh
  specification reviewer and a different fresh quality/security reviewer must
  both return `C0/I0/M0`. The accepted pair is recorded under
  `docs(task): record review-range-bound parser outcome review`; any rejected
  pair is recorded under
  `docs(task): record exhausted review-range-bound parser outcome review` and
  grants no retry or downstream authority.
- The exact 4AD Plan checkpoint is identified by
  `docs(plan): define review-range-bound parser outcome proof` at
  `9de469a52c4b05d2490d36d37b95b1277442f725`. Its exact full-OID review range
  returned specification `C0/I2/M1` and quality/security `C0/I0/M0`.
  Specification rejected row-wide rather than exact-cell range parsing,
  incomplete predecessor range/path and base-mode assertions in three
  pre-terminal sessions, and stale Task status text. The 4AD no-correction
  Plan loop is exhausted. No accepted Plan-review evidence, implementation,
  test execution, manifest promotion, Wave C, Tasks 5–6, or whole-branch
  review is authorized. Remote, runtime, dependency, secret, direct
  pre-commit, controlled-wrapper, and Graphify authority remain unchanged.

### T-TSDC-004R-4AE exact-cell review-range proof design return

- The user approved this Plan-only successor from exact clean base
  `5644c4a301e38d3f0c32efe99e80f879df6e1ac8`, after 4AD exhausted at
  Plan review. The 4AD history, including commits `9de469a5` and `5644c4a3`,
  remains immutable historical evidence.
- 4AE retains the immutable 4AC behavior at
  `5bc5ab85e9d8841761ae00b7a169e899e3f8f515` and changes only the review-range
  parser, the missing predecessor range/path/base-mode proof captures, and
  current-state synchronization.
- `P` is the Plan-and-Task-only, single-parent successor of `D`; `XP` and `B`
  are Task-only, single-parent successors of `P`; only `B` authorizes `I`.
  `I` changes only the Task and routing test; `XI` and `R` are Task-only,
  single-parent successors of `I`; only `R` authorizes Task 4.5.
- The committed Plan checkpoint uses exact unique subject
  `docs(plan): define exact-cell review-range proof` at `8abea15a`. Its exact
  full-OID review range returned specification `C0/I0/M0` and
  quality/security `C0/I2/M0`. The quality review rejected candidate counting
  that ignores a duplicate no-leading-pipe GFM row and downstream sessions
  that do not reassert accepted-evidence and implementation-subject
  uniqueness. The no-correction 4AE Plan loop is exhausted. Implementation,
  tests, Wave C, Tasks 5–6, and whole-branch review remain blocked.
- Each session must bind full OIDs, exact subjects, one parent/first parent,
  ancestry, distance one, exact commit and predecessor-range paths, applicable
  `100644` modes, permitted dirty scope before a commit, and clean state after a
  commit or during read-only review. `git log --grep` is only a fixed-line
  uniqueness check and is never an authority resolver.

### T-TSDC-004R-4AF canonical-row authority proof design return

- 4AF is the user-approved Plan-only successor from rejected 4AE evidence `8cacc4634448416a7dbc8d3de69bf6011b62c6d5`; 4AC behavior and 4AD/4AE history remain immutable.
- The active proof counts optional-leading-pipe first-cell candidates, ignores prose with no separator, then requires canonical leading/trailing pipes and seven data cells.
- P is resolved by `docs(plan): define canonical-row authority proof`; formal Plan reviews are pending. Implementation and tests remain blocked.

### Current evidence boundaries

- Local tracked definitions do not establish remote workflow success,
  required-check enforcement, ruleset enforcement, environment configuration,
  or deployment state.
- Sanitized job/step metadata does not establish a remote failure root cause.
- Static version convergence does not establish a running service version.
- Secret path inventory does not establish the presence, correctness, or
  contents of secret values.
- A skipped, unavailable, or approval-gated command remains `unverified`; it
  is not reported as pass.

## Controlled Agent Pre-commit Evidence

| Field | Current evidence |
| --- | --- |
| Approval | Not approved for this wave |
| Command | Not yet defined; Revision R2 requires a literal path-minimal command to be constructed only at the clean Task 5 checkpoint |
| Starting commit | Not applicable |
| Allowed prefixes | Not activated |
| Exit status | Not run |
| Snapshot result | Not run |
| Observation boundary | Would be Git-visible non-ignored repository status only |
| Path sets | Not observed |
| Disposition | **NOT AUTHORIZED / DO NOT RUN.** Direct `pre-commit run` remains prohibited. |

The Task 4 CI-only script is not this controlled Agent route and does not
consume or create Agent authorization.

## Review Evidence

| Task | Implementer | Specification reviewer | Quality/security reviewer | Exact range | Verdict | Findings |
| --- | --- | --- | --- | --- | --- | --- |
| T-TSDC-004R Plan R1 | Controller | C0/I4/M1; SPEC_COMPLIANCE NO; COMMIT_READY NO | C1/I2/M1; CHANGES_REQUIRED; COMMIT_READY NO | `a0f91bb5..1a86f929` | correction and re-review required | Schema bootstrap, descriptor compatibility, duplicate suite execution, Task 5 executability, wrapper scope, local `.env`, Storybook state lifetime, Bash static gates, and behavior-specific RED evidence required correction before implementation. |
| T-TSDC-004R Plan R1 correction | Controller | C0/I3/M1; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I2/M1; CHANGES_REQUIRED; COMMIT_READY NO | `a0f91bb5..e97b7966` | two-attempt review loop exhausted; returned to design/plan | Spec Wave-1 schema order, registered all-profile projection, full-row review promotion, post-review evidence commits, and wrapper-ledger wording required Revision R2. |
| T-TSDC-004R Plan R2 first review | Controller plus bounded documentation implementers | C0/I5/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I0/M0; APPROVED; COMMIT_READY YES | `e97b7966..5b7388d0` | bounded correction and one final review pair required | The approved third profile was absent from Spec 135; schema-v2 conversion retained a parallel code-owned command authority; seven executable modes were deferred; Wave B froze the Task 4.1 rather than Task 4.2 checkpoint; two changed shell paths lacked exact static gates; and the optional wrapper was ordered after dirty Task 6 edits. A separate specification reviewer corroborated four of these findings at C0/I4/M0. |
| T-TSDC-004R Plan R2 correction | Controller plus bounded documentation implementers | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M0; APPROVED; COMMIT_READY YES | `e97b7966..8f82e88b` | approved; active recovery | Fresh independent reviewers found no unresolved issue and authorized local Plan-bounded T-TSDC-004R implementation. External, runtime, dependency, secret, direct pre-commit, and controlled-wrapper boundaries remain separately gated. |
| T-TSDC-001 | Task 1 implementation agent | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M0; APPROVED; COMMIT_READY YES | `72eef68c..43f78ad5` | approved; completed | Fresh independent reviewers found no unresolved issues. Per-row manifest verdicts remain pending for Task 6 blocking promotion. |
| T-TSDC-002 | Task 2 documentation-surface implementation agent | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M0; APPROVED; COMMIT_READY YES | `78af8462..b28764a9` | approved; completed | Fresh independent reviewers found no unresolved issues after canonical-contract remediation. All 136 manifest row verdict pairs remain pending for Task 6. |
| T-TSDC-003 | Task 3 static-version implementation agent / replacement remediation implementers | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M0; PASS; COMMIT_READY YES | `b1e62873..60e0313c` | approved; completed | Fresh independent reviewers found no unresolved issues across all four pinned implementation commits. Exact stale-absence protects all 15 mappings, global dequoted service-name uniqueness prevents ambiguity, and all 141 manifest verdict pairs remain pending for Task 6. |
| T-TSDC-004 | Task 4 workflow/QA implementation agent / replacement remediation implementers | C0/I4/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I4/M1; CHANGES_REQUIRED; COMMIT_READY NO | `ba93483c..78f9f012` final fix re-review; prior review chain begins at `6fabbf05` | blocked after fix round 5/5 | TSDC-012 remains load-bearing: the validator cannot yet prove one CI owner across all valid shell/Python/helper execution equivalences and bounded provenance paths. No finding is waived; all 148 manifest verdict pairs remain pending. |
| T-TSDC-004R-1 initial implementation | Task 4.1 typed-gate implementation agent | C0/I3/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I4/M2; CHANGES_REQUIRED; COMMIT_READY NO | `ae5632b2..fdc01e1c` | remediation attempt 2/2 required | Accepted findings covered typed parent/read failures, bounded iterative parsing and graph traversal, hostile Git provenance, exact profile classification, integer schema typing, a complete positive registry, and exact structural local safety. The specification review withdrew its proposed duplicate entrypoint/argv catalog because the canonical schema-v2 file must remain the sole command authority. |
| T-TSDC-004R-1 remediation review | Task 4.1 typed-gate implementation agent / controller evidence owner | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M1; APPROVED; COMMIT_READY YES | full `ae5632b2..af898045`; remediation `fdc01e1c..af898045`; evidence correction `af22e129` | approved; Task 4.1 completed | Every accepted implementation finding is closed. Controller commit `af22e129` reconciled the stale execution, review, commit, and deferred-state records, after which the same read-only specification reviewer returned no findings. The quality minor requests a full load–parse–validate–expand strict-JSON positive registry fixture and is assigned to the Task 4.2 canonical schema-v2 conversion rather than authorizing a parallel command catalog. |
| T-TSDC-004R-2 initial implementation | Task 4.2 typed-gate runner implementation agent | C0/I2/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I5/M1; CHANGES_REQUIRED; COMMIT_READY NO | `0d833563..5819c8ab` | first remediation was required | Descriptor-root identity, process-tree timeout, environment-key safety, bounded child output, deterministic cleanup, Compose staged-blob identity, and factual consumer evidence required correction before Wave B. |
| T-TSDC-004R-2 first remediation review | Task 4.2 remediation implementation agent | C0/I2/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I2/M1; CHANGES_REQUIRED; COMMIT_READY NO | `5819c8ab..17bb5cdd` | returned to design; Wave B blocked | The remediation commit did not meet the descriptor-capability or runner-owned process-lifecycle contract. The previous “fresh reviews pending” status is superseded. Manifest verdicts remain pending. |
| T-TSDC-004R-2 design reset | Controller / bounded future implementer | C0/I3/M0; CHANGES_REQUIRED; COMMIT_READY NO | C0/I5/M0; CHANGES_REQUIRED; COMMIT_READY NO | `17bb5cdd..5f5c746e` | corrected design and one redesigned implementation attempt required | Reviews required explicit adopted-FD ownership/lifetime, runner-owned group finalization, pidfd-safe identity tests, exact HOME retry timing, and an implementation allowlist with freezes. `5f5c746e` is superseded by `docs(plan): harden typed gate runner redesign`; Wave B remains blocked. |
| T-TSDC-004R-2 redesigned lifecycle implementation | Task 4.2R implementation agent | C0/I1/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I3/M0; CHANGES_REQUIRED; COMMIT_READY NO | `e6fefb69..8df1b9cd` | returned to design; Wave B blocked | The finalization design fails to make every adopted/output/source cleanup path fail closed and cannot prove PGID identity safety after leader exit. Its prior review-pending state is superseded; no manifest verdict is promoted. |
| T-TSDC-004R-2 identity-cleanup design return | bounded future implementer | C0/I2/M1; SPEC_COMPLIANCE NO; IMPLEMENTATION_READY NO | C0/I3/M0; CHANGES_REQUIRED; IMPLEMENTATION_READY NO | `8df1b9cd..6d433fce` | corrected Plan and fresh review required; Wave B blocked | The correction must preserve all four `17bb5cdd` freezes and exact 94-test discovery while adding a valid scope checkpoint, deterministic cleanup precedence, guaranteed acquisition-failure reap, explicit post-reap prohibition, and safe TERM/KILL `ESRCH` handling. |
| T-TSDC-004R-2 corrected identity-cleanup Plan | bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I2/M0; CHANGES_REQUIRED; IMPLEMENTATION_READY NO | `8df1b9cd..2c6b2af7` | bounded-reap correction and fresh review required; Wave B blocked | The prior checkpoint is historical evidence only because its wait/reap recovery wording allowed indefinite blocking. |
| T-TSDC-004R-2 bounded identity-cleanup Plan | bounded future implementer | C0/I1/M0; SPEC_COMPLIANCE NO; IMPLEMENTATION_READY NO | C0/I0/M0; APPROVED; IMPLEMENTATION_READY YES | `8df1b9cd..6877ac4b` | scope-oracle correction and fresh review required; Wave B blocked | The lifecycle design passed, but the pre-commit exact-path gate did not observe staged/unstaged or untracked changes. |
| T-TSDC-004R-2 scoped identity-cleanup Plan | bounded future implementer | C0/I1/M0; SPEC_COMPLIANCE NO; IMPLEMENTATION_READY NO | canceled after specification blocker; no verdict | `8df1b9cd..ba7ccb79` | executable-oracle correction and fresh review required; Wave B blocked | Scope timing is correct, but literal backslash-n output makes both exact-path comparisons fail. |
| T-TSDC-004R-2 executable identity-cleanup Plan | bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I0/M0; PASS; IMPLEMENTATION_READY YES | `8df1b9cd..86146050` | one implementation attempt authorized; Wave B still blocked | The successor begins after the exact unique `docs(plan): record executable typed gate identity checkpoint` commit and must satisfy both executable scope oracles before one fresh implementation review pair. |
| T-TSDC-004R-2 identity-cleanup implementation | Task 4.2S implementation agent, sole attempt | C0/I3/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I1/M0; CHANGES_REQUIRED; COMMIT_READY NO | `86146050..17645f2a` | returned to design; Wave B blocked | The five-path implementation passed local RED/GREEN, freeze, and scope gates, but fresh reviews found that adapter ordinary `Exception` payloads can cross the boundary, runner post-`Popen` `BaseException` interruption can bypass cleanup, later-recovery ledger wording overstates unconditional reap, and post-implementation metadata/traceability evidence was omitted from this ledger. No manifest verdict is promoted. |
| T-TSDC-004R-2 typed-interruption design return | Controller / bounded future implementer | pending fresh review | pending fresh review | starts after `17645f2a` | corrected checkpoint pending; Wave B blocked | Successor Plan Task 4.2T preserves the same five-path implementation boundary and four `17bb5cdd` freezes while requiring adapter ordinary-exception normalization, BaseException-safe runner cleanup, conditional-reap wording, and explicit metadata/traceability evidence. |
| T-TSDC-004R-2 typed-interruption design checkpoint | Controller / bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES | `17645f2a..5cd98c7b` | one implementation attempt authorized; Wave B still blocked | The successor begins after the exact unique `docs(plan): record adopted-root interruption checkpoint` commit and must satisfy both executable scope oracles before one fresh implementation review pair. Earlier checkpoints remain superseded history. |
| T-TSDC-004R-2 typed-interruption implementation | Task 4.2T implementation agent, sole attempt | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I1/M0; QUALITY_SECURITY CHANGES_REQUIRED; COMMIT_READY NO | `5cd98c7b..483d3a47` | returned to design; Wave B blocked | The adapter boundary and action-raised runner cleanup pass review, but disjoint source-level lifecycle regions permit control-flow interruption between bound ownership transitions. No manifest verdict is promoted. |
| T-TSDC-004R-2 phase-owned runner initial checkpoint | Controller / bounded future implementer | C0/I1/M0; SPEC_COMPLIANCE NO; IMPLEMENTATION_READY NO | C0/I0/M1; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES | `483d3a47..ce4111d8` | superseded; Wave B blocked | The lifecycle design passed, but the `Whole branch` row still named exhausted Task 4.2T as the prerequisite. No implementation authority followed. |
| T-TSDC-004R-2 reconciled phase-owned runner design | Controller / bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES | `483d3a47..5dc49631` | sole implementation attempt authorized; Wave B blocked | Task 4.2U freezes the accepted adapter pair and permits only runner, runner-test, and Task-ledger changes for one outer phase-owning controller with transition-specific witnesses. |
| T-TSDC-004R-2 phase-owned runner implementation | Task 4.2U implementation agent, sole attempt | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I2/M0; QUALITY_SECURITY CHANGES_REQUIRED; COMMIT_READY NO | `5dc49631..ad2df527` | returned to recovery-owned design; Wave B blocked | Local gates pass, but recovery transitions remain outside one finalization owner and ordinary pre-bind `Popen` exceptions can expose private values. No manifest verdict is promoted. |
| T-TSDC-004R-2 recovery-owned finalization design | Controller / bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES | `ad2df527..5274f58b` | sole implementation attempt authorized; Wave B blocked | Task 4.2V preserves the three-path allowlist and requires one lifecycle identity, nested cleanup finalizers, fixed pre-bind taxonomy, and recovery-transition RED witnesses. |
| T-TSDC-004R-2 recovery-owned runner implementation | Task 4.2V replacement implementation agent, sole attempt | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M0; QUALITY_SECURITY PASS; COMMIT_READY YES | `5274f58b..cdae7523` | accepted; Task 4.3 Wave B authorized from controller evidence checkpoint | Local RED/GREEN, exact discovery, workflow/projection, static, metadata, traceability, freeze, scope, and diff gates pass. Both fresh read-only reviews found no unresolved defect; no manifest verdict is promoted by this runner-only acceptance. |
| T-TSDC-004R-3 initial cutover review | Task 4.3 implementation agent | C0/I5/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I4/M0; CHANGES_REQUIRED; COMMIT_READY NO | `cfce3218..fd124581` | bounded remediation attempt 1/2 required | Accepted findings require exact execution-context rejection, registered git-flow checkout, wiring-only repository ownership, authenticated descriptor compatibility, executable descriptor regressions, and exact shared CI/local node identity. |
| T-TSDC-004R-4 attempt-1 remediation review | Task 4.4 remediation agent | C0/I4/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I3/M0; CHANGES_REQUIRED; COMMIT_READY NO | `fd124581..e864af8e` | final bounded remediation attempt 2/2 required | Accepted findings require the exact frozen repository leaf, real runner entrypoint-descriptor shell coverage, and a complete registry-derived sibling-dispatch proof. |
| T-TSDC-004R-5 attempt-2 remediation review | Task 4.4 remediation agent, final attempt | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I1/M0; QUALITY_SECURITY FAIL; COMMIT_READY NO | `e864af8e..7f0f5ddb` | two-attempt implementation loop exhausted; returned to design/plan | Exact frozen-leaf, dual-FD shell, required dispatch-family, and static-evidence findings are closed. Option-bearing `command -p`, `env -u NAME`, and `exec -a NAME` forms remain an Important bypass in the wiring-only proof. No further implementation retry is authorized by the active Plan. |
| T-TSDC-004R-4W initial option-aware wrapper-proof Plan | Controller / bounded future implementer | C0/I4/M0; SPEC_COMPLIANCE NO; IMPLEMENTATION_READY NO | C0/I3/M0; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `1b054313..98a3558d` | bounded Plan correction and final re-review required; no implementation authority | Accepted findings require GNU-compatible static `env -S` or deterministic fail-closed handling, unique/ancestry-bound Plan-review evidence, failure-producing exact scope/freeze/mode/clean oracles, and one named RED matrix covering every admitted option form. |
| T-TSDC-004R-4W corrected option-aware wrapper-proof Plan | Controller / bounded future implementer | interrupted after quality blocker; no verdict | C0/I2/M0; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `1b054313..a46f29b8` | sole Plan correction exhausted; returned to design/plan | Initial scope, checkpoint, mode, and RED-matrix findings were substantially closed, but GNU `env -- NAME=VALUE` assignment semantics remain wrong and evidence blocks depend on shell variables from earlier independent sessions. No implementation authority followed. |
| T-TSDC-004R-4X session-local option-proof Plan | Controller / bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I2/M0; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `7b792a37..4c7c9c4b` | no-correction Plan loop exhausted; returned to design/plan | GNU `env --` and session-local variable defects are closed, but proof blocks can mask earlier failures without fail-fast execution and Task 4.5 does not rebind the 4X base, exact implementation scope, or file modes. No implementation authority followed. |
| T-TSDC-004R-4Y fail-fast lineage-proof Plan | Controller / bounded future implementer | interrupted after quality blocker; no verdict | C0/I1/M0; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `481b1a8e..a8cc9751` | no-correction Plan loop exhausted; returned to design/plan | Strict sessions and complete Task 4.5 rebinding are substantially correct, but fallible substitutions embedded in `test` can still lose the command status and pass on empty output. No implementation authority followed. |
| T-TSDC-004R-4Z status-preserving proof Plan | Controller / bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I1/M0; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `0177006c..9968bb6d` | no-correction Plan loop exhausted; returned to design/plan | Standalone capture preserves failure status, but some captured values are not tested by the immediately following command as the normative 4Z contract requires. No implementation authority followed. |
| T-TSDC-004R-4AA immediate-consumption proof Plan | Controller / bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES | `355a1db5..861c0e33` | sole two-path implementation attempt authorized from the separate evidence checkpoint | Reviewers found no unresolved issue in immediate capture/test pairing, strict status propagation, the RED exception, accepted parser contract, complete downstream lineage/scope/mode proof, freezes, or prohibitions. Wave C remains blocked. |
| T-TSDC-004R-4AA immediate-consumption implementation | Task 4.4AA implementation agent, sole attempt | C0/I1/M0; SPEC_COMPLIANCE NO; IMPLEMENTATION_READY NO | C0/I3/M0; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `194b7d16..84067c8f` | one-attempt implementation loop exhausted; returned to design/plan | GNU `env -S` skips its first inserted token, unresolved dynamic command heads can fail open, and malformed signal-option near-prefixes can be accepted. Passing local tests do not establish the required bounded parser proof; no Wave C authority follows. |
| T-TSDC-004R-4AB explicit parser-outcome proof Plan | Controller / bounded future implementer | C0/I2/M0; SPEC_COMPLIANCE NO; IMPLEMENTATION_READY NO | C0/I2/M0; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `25524ce1..8d3f1122` | no-correction Plan loop exhausted; returned to design/plan | Long split-string transition witnesses and no-relevant-sibling dynamic negatives are absent; ambiguous candidate union can drop an embedded sibling; and unresolved positional `$1`/`${1}` heads remain outside the dynamic predicate. No implementation or Wave C authority follows. |
| T-TSDC-004R-4AC candidate-closed proof Plan | Controller / bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I1/M1; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `997719ff..5bc5ab85` | no-correction Plan loop exhausted; returned to design/plan | Candidate union, dynamic-target/query precedence, GNU `env` split re-entry, and signal-option handling passed. Terminal evidence sessions do not each rebind the complete reviewed lineage, distance, scope, and modes, so same-subject lineage substitution remains possible; the stale pending-checkpoint Task wording is synchronized by this evidence commit. No implementation or Wave C authority follows. |
| T-TSDC-004R-4AD review-range-bound proof Plan | Controller / bounded future implementer | C0/I2/M1; SPEC_COMPLIANCE NO; IMPLEMENTATION_READY NO | C0/I0/M0; QUALITY_SECURITY PASS; IMPLEMENTATION_READY YES | `3510e9944655ee89077a295712e759d116e2e87f..9de469a52c4b05d2490d36d37b95b1277442f725` | no-correction Plan loop exhausted; returned to design/plan | Range extraction is not exact-cell anchored; three pre-terminal sessions omit required predecessor range/path or base-mode assertions; and checkpoint-status text was stale. Quality/security found no additional issue, but both required C0/I0/M0 reviews did not pass. No implementation or Wave C authority follows. |
| T-TSDC-004R-4AD review-range-bound implementation | superseded uncreated attempt | not applicable | not applicable | not available | blocked; 4AD exhausted at Plan review | The exact two-path implementation was never authorized or started because the specification Plan review failed. |
| T-TSDC-004R-4AE exact-cell proof Plan | Controller / bounded future implementer | C0/I0/M0; SPEC_COMPLIANCE YES; IMPLEMENTATION_READY YES | C0/I2/M0; QUALITY_SECURITY FAIL; IMPLEMENTATION_READY NO | `5644c4a301e38d3f0c32efe99e80f879df6e1ac8..8abea15a1ebafdf607be801789a409e6f312c099` | no-correction Plan loop exhausted; returned to design/plan | Duplicate no-leading-pipe rows can evade candidate counting, and downstream sessions do not reassert authority-subject uniqueness. No implementation or Wave C authority follows. |
| T-TSDC-004R-4AE exact-cell implementation | superseded uncreated attempt | not applicable | not applicable | not available | blocked; 4AE exhausted at Plan review | The exact two-path implementation was never authorized or started because the quality/security Plan review failed. |
| T-TSDC-004R-4AF canonical-row proof Plan | Controller / bounded future implementer | pending fresh review | pending fresh review | `8cacc4634448416a7dbc8d3de69bf6011b62c6d5..P` | active; formal Plan reviews pending | P is resolved by exact unique subject; implementation remains blocked. |
| T-TSDC-004R-4AF canonical-row implementation | bounded future implementer | not applicable | not applicable | not available | blocked pending accepted 4AF Plan evidence | The sole two-path implementation has not started. |
| T-TSDC-005 | pending | pending | pending | not available | blocked | accepted 4AF implementation-review R pending |
| T-TSDC-006 | pending | pending | pending | not available | pending | Tasks 1–5 pending |
| Whole branch | not applicable | pending final fresh reviewer after accepted 4AF chain | pending different final fresh reviewer after accepted 4AF chain | not available | blocked | The 4AF Plan review and accepted implementation-review R are pending; no implementation exists and Wave C, Tasks 5–6, and final branch review remain blocked. |

Reviewers are read-only. Any reviewer-created edit or commit is a process
finding and must not be silently accepted as independent review evidence.

## Commit Ledger

| Unit | Logical purpose | Expected commit | Actual commit | Validation |
| --- | --- | --- | --- | --- |
| Planning specification | Define successor convergence design | `docs(spec): define target surface delta convergence` | `e828745a` | metadata, Markdown, alignment, diff hygiene passed |
| Planning specification recovery | Redesign typed CI gate ownership | `docs(spec): redesign typed CI gate ownership` | `a0f91bb5` | metadata 1/0, alignment links 5,662/0, diff hygiene, independent spec and quality/security review passed |
| Planning activation | Activate Spec and define Plan/Task | `docs(plan): define target surface delta execution` | `a2ba9eb4` | metadata 3/0, Markdown 3/0, traceability 46/0, alignment 674/5,658/141/0, diff hygiene passed |
| Revision R1 planning recovery | Define typed CI gate recovery execution | `docs(plan): define typed CI gate recovery` | `1a86f929` | metadata 2/0, Markdown 2/0, traceability 46/0, alignment 674/5,663/0, diff hygiene passed; first independent reviews returned C0/I4/M1 and C1/I2/M1, so implementation remained blocked |
| Revision R1 Plan correction | Close first independent Plan review findings | `docs(plan): correct typed CI gate recovery` | `e97b7966` | corrected Plan/Task validation passed; second reviews returned C0/I3/M1 and C0/I2/M1, exhausting the Plan review loop |
| Revision R2 design return | Align Wave A, profile roots, promotion, and evidence commits | `docs(plan): realign typed CI gate recovery` | `7d36fe3b` | metadata 2/0, Markdown 2/0, traceability 46/0, alignment 674/5,663/0, diff hygiene passed; user approval recorded; first R2 reviews returned specification C0/I5/M0 and quality/security C0/I0/M0, so bounded correction and final re-reviews are required |
| Revision R2 bounded correction | Close the first R2 review findings without expanding authority | `docs(plan): close Revision R2 review findings` | `833a7c19` | metadata 3/0, Markdown 3/0, traceability 46/0, alignment 674/5,663/0, Task briefs 147/300, exact Bash and ShellCheck gates, and diff hygiene passed; final corrected R2 reviewers assigned |
| T-TSDC-001 | Successor delta contract | `feat(governance): establish target surface delta contract` | `1671e9be` | focused 15/15, predecessor 40/40, metadata 0 violations, advisory CLI, Ruff, Bash syntax, and diff hygiene pass; aggregate limitations recorded |
| T-TSDC-001 remediation | Harden successor evidence contract after two reviews | `fix(governance): harden target delta evidence` | `72e452d0` | remediation RED/GREEN, successor/predecessor/metadata, advisory/blocking, summary, static QA, and diff hygiene |
| T-TSDC-001 second remediation | Close fresh fail-closed review gaps | `fix(governance): close target delta fail-closed gaps` | `25f4c52a` | advisory structural RED/GREEN, secret-like field matrix, no-follow bootstrap, successor/static/metadata/diff gates |
| T-TSDC-001 third remediation | Reject explicit failed review verdicts in advisory mode | `fix(governance): reject failed advisory verdicts` | `43f78ad5` | verdict-state RED/GREEN, focused advisory/blocking tests, production advisory/blocking, static and diff gates |
| T-TSDC-002 | Document surface convergence | `docs(governance): converge target documentation surfaces` | `c63cc267` | Target 48/48, delta 30/30, metadata 225/225, lifecycle 34/34, metadata/target/advisory/alignment/current-traceability/Ruff/compile/Markdown/summary/diff gates pass; obsolete Plan cross-link path unavailable and recorded |
| T-TSDC-002 quality remediation | Validate the sample lifecycle handoff through the canonical successor contract | `fix(governance): validate sample lifecycle handoff evidence` | `b28764a9` | Evidence RED 17/19 plus verdict RED 3/3; lifecycle 7/7, delta integration 2/2, predecessor aggregate 1/1, both CLIs, Ruff, compile, ledger Markdown/metadata, and diff hygiene pass |
| T-TSDC-003 | Static version/lifecycle reconciliation | `fix(infra): reconcile static version and lifecycle drift` | `5460e5fc16789d72417e5e7df8b7f7ae046fb245` | focused 7/7, manifest oracle 1/1, sync/provenance, all hardening, supply-chain 13, delta advisory, alignment, and bounded static gates pass; initial independent reviews C0/I1/M0 twice |
| T-TSDC-003 remediation | Harden static version assertions and Compose image resolution | `fix(infra): harden static version assertions` | `c04946e547b7a7b22923e6d7ed577408b39ef480` | resolver/static RED 17 failures; focused 11/11; sync/provenance, all hardening, supply-chain 13, delta advisory, Ruff, compile, Bash, ShellCheck, and diff gates pass; remediation review C0/I1/M1 |
| T-TSDC-003 quoted-service remediation | Close quoted service resolver boundary and currentize Dozzle diagnostic | `fix(infra): close quoted service resolver gap` | `cce5abb6e20bffd10a09f4a2c74da3b653022a86` | quoted-key RED six failures; affected GREEN 4/4 and full focused 16/16; all hardening tiers, sync/provenance, repository static oracle, Bash, scoped ShellCheck, Ruff, compile, and diff hygiene pass; final remediation review C0/I2/M1 |
| T-TSDC-003 final remediation | Enforce global service uniqueness and converge direct Dozzle evidence | `fix(infra): converge Dozzle static evidence` | `60e0313cad71dced1db2bb5fba554c2fc28cd235` | five-failure focused RED plus `141 != 140` oracle RED; focused 17/17, exact oracle 1/1, advisory, hardening, sync/provenance, alignment, Markdown, Ruff, compile, Bash, ShellCheck, and diff hygiene pass; final independent reviews C0/I0/M0 and COMMIT_READY YES |
| T-TSDC-004 | Workflow and QA ownership | `ci(governance): type workflow and qa ownership` | `faaa2eb2` | workflow 9/9, wrapper, CLI 7/23/8, exact manifest/advisory, actionlint, ShellCheck, Ruff, compile, Bash, diff, and Task 4 aggregate sections pass; quality review found one Important |
| T-TSDC-004 quality remediation | Reject ambiguous mixed workflow trigger keys | `fix(ci): reject ambiguous workflow triggers` | `e3ea3cd8` | mixed-key RED 2/2; focused GREEN 11/11; re-review pending |
| T-TSDC-004 permission remediation | Enforce permission ownership independently of the mutable workflow contract | `fix(ci): enforce immutable permission baselines` | `20676dc3` | required-quality RED 7/7; required and six non-gating co-mutation GREEN plus exact-owner positive; workflow 14/14; re-review pending |
| T-TSDC-004 ownership-gap remediation | Close direct/transitive ownership and Stage 00 fail-closed gaps | `fix(ci): close workflow ownership gaps` | `b07b0f44` | focused RED 5 methods/15 failures; focused GREEN 5/5; workflow 17/17; Stage 00 4/4; routing 35/36 with known missing `html5lib`; exact manifest/advisory and scoped static gates pass; re-review pending |
| T-TSDC-004 transitive-ownership remediation | Enforce complete semantic ownership and restore control-plane QA routing | `fix(ci): enforce transitive qa ownership` | `ba93483c` | focused RED 4 methods/13 failures; focused GREEN 4/4; workflow 20/20 with co-mutations 4/4; eval 38/38; Stage 00 4/4; routing 35/36 with known local `html5lib` absence; exact manifest/advisory and scoped static gates pass; independent re-review pending |
| T-TSDC-004 final semantic-resolution remediation | Harden complete-program ownership and bounded helper traversal | `fix(ci): harden semantic command resolution` | `78f9f012` | focused RED 8 methods/29 failures; focused GREEN 8/8; workflow 27/27; eval 38/38; Stage 00 4/4; wrapper, CLI 7/23/8, exact manifest/advisory, and scoped static gates pass; final reviews C0/I4/M0 and C0/I4/M1 leave Task 4 blocked |
| T-TSDC-004R-1 | Add the dependency-free typed gate contract | `feat(ci): add typed gate contract` | `fdc01e1c` | signature-only RED produced nine behavior errors across the exact seven methods; manifest oracle failed `150 != 148`; focused 7/7, delta 30/30, canonical 150/89/61/0/0 summary, Ruff, compileall, advisory, and diff gates passed; initial reviews required bounded remediation |
| T-TSDC-004R-1 remediation | Harden typed parsing, graph bounds, provenance, and local structural safety | `fix(ci): harden typed gate contract` | `af898045` | 19-case remediation RED; focused 7/7 and delta 30/30 GREEN; Ruff, compileall, advisory, diff hygiene, clean scope, and byte-identical schema-v1 workflow hash passed; final quality/security review approved and specification evidence recheck remains pending |
| T-TSDC-004R-1 evidence correction | Reconcile execution, review, commit, and deferred-state evidence | `docs(task): reconcile typed gate contract evidence` | `af22e129` | metadata selected 15 documents with 0 violations and 5 legacy exceptions; traceability checked 46 catalog pairs with 0 failures; implementation alignment checked 674 stage documents and 5,663 repository-local links with 0 failures; diff hygiene passed; the bounded specification recheck returned C0/I0/M0 |
| T-TSDC-004R-2 | Add the dependency-free typed gate runner, adapters, and canonical schema-v2 registry | `feat(ci): add typed gate runner` | `5819c8ab` | behavior-specific runner/adapter and schema-cutover RED; runner/adapter 28/28; five-module 94 with 11 planned Wave-C skips; live execution-free projections; exact 156/85/71/0/0 manifest; Ruff, compileall, Bash, ShellCheck, workflow freeze, advisory, summary, and diff gates pass; initial independent reviews required bounded remediation |
| T-TSDC-004R-2 first remediation | Harden descriptor, process, environment, output, cleanup, Compose identity, and manifest evidence boundaries | `fix(ci): harden typed gate runner` | `17bb5cdd` | Historical RED/GREEN and static evidence were recorded, but fresh reviews of `5819c8ab..17bb5cdd` returned Spec C0/I2/M0 and Quality/Security C0/I2/M1. The claim that review was merely pending is superseded; no Wave B authority follows. |
| T-TSDC-004R-2 design reset | Finalize descriptor capability and runner-owned invocation lifecycle | `docs(plan): harden typed gate runner redesign` | `b481414e` | `5f5c746e` reviews returned Spec C0/I3/M0 and Quality/Security C0/I5/M0, so its design is superseded. The corrected design fixes adopted FD M lifetime, runner PGID finalization, pidfd-only identity evidence, exact HOME retry, five-path implementation allowlist, and 17bb5cdd contract/workflow/manifest freezes; one implementation attempt remains. |
| T-TSDC-004R-2 redesigned lifecycle implementation | Finalize adopted root capability, runner-owned PGID, pidfd evidence, and deterministic HOME teardown | `fix(ci): finalize typed gate runner lifecycle` | `8df1b9cd` | RED 94 = 78 pass + 11 skip + 3 fail + 2 error; GREEN 94 = 83 pass + 11 skip; workflow 7/23/8; both execution-free projections; exact Ruff/compileall; four byte freezes; advisory, metadata, traceability, exact five-path scope, and diff hygiene pass. Fresh reviews of `e6fefb69..8df1b9cd` returned Spec C0/I1/M0 and Quality/Security C0/I3/M0, so it does not authorize Wave B. |
| T-TSDC-004R-2 identity-cleanup design return | Pin fail-closed capability cleanup and unreaped-leader pidfd finalization | `docs(plan): redesign typed gate identity cleanup` | `48cc0944` | Documents the one remaining five-path attempt: M/N and output/source cleanup ownership, strict bounded proc membership, no reaping before identity-safe group finalization, exact 94-test discovery, four 17bb freezes, and fresh C0/I0 review gate. |
| T-TSDC-004R-2 identity-cleanup design reconciliation | Reconcile unreaped-leader identity wording and implementation boundary | `docs(plan): reconcile typed gate identity design` | `6d433fce` | Corrected the first design return before independent review; those reviews still returned Spec C0/I2/M1 and Quality/Security C0/I3/M0, so implementation remained blocked. |
| T-TSDC-004R-2 identity-cleanup Plan correction | Close scope-baseline, cleanup-priority, acquisition-reap, post-reap, and `ESRCH` findings | `docs(plan): close typed gate identity review findings` | `63effff2` | Metadata 15/0, traceability 46/0, and diff hygiene passed; no implementation or gate execution is authorized by this correction alone. |
| T-TSDC-004R-2 identity-cleanup design checkpoint | Freeze the corrected Plan as the successor implementation scope baseline | `docs(plan): record typed gate identity design checkpoint` | resolved by this exact unique subject | The implementation oracle requires one matching commit and precisely the two runtime files, two existing test files, and this Task ledger after it. |
| T-TSDC-004R-2 bounded-reap Plan correction | Eliminate unbounded waits from initial and later runner recovery | `docs(plan): bound typed gate identity reap recovery` | `a3ba173c` | Metadata 15/0, traceability 46/0, and diff hygiene passed; implementation remains blocked pending the new checkpoint reviews. |
| T-TSDC-004R-2 bounded identity design checkpoint | Freeze the bounded corrected Plan as the successor implementation scope baseline | `docs(plan): record bounded typed gate identity checkpoint` | resolved by this exact unique subject | The implementation oracle requires one matching commit and supersedes the earlier identity checkpoint without deleting its historical evidence. |
| T-TSDC-004R-2 scope-oracle Plan correction | Make pre-commit scope validation working-tree-aware and post-commit scope validation range-aware | `docs(plan): fix typed gate identity scope oracle` | `2b73ea2d` | Metadata 15/0, traceability 46/0, and diff hygiene passed; implementation remains blocked pending the scoped checkpoint reviews. |
| T-TSDC-004R-2 scoped identity design checkpoint | Freeze the working-tree-aware corrected Plan as the successor implementation scope baseline | `docs(plan): record scoped typed gate identity checkpoint` | resolved by this exact unique subject | The implementation oracle requires one matching commit and supersedes the bounded checkpoint while retaining its review history. |
| T-TSDC-004R-2 executable-oracle Plan correction | Emit newline-delimited exact-path expectations in both scope gates | `docs(plan): make typed gate scope oracle executable` | `38259d1f` | Literal five-line oracle, metadata 15/0, traceability 46/0, and diff hygiene passed; implementation remains blocked pending checkpoint reviews. |
| T-TSDC-004R-2 executable identity design checkpoint | Freeze the executable corrected Plan as the successor implementation scope baseline | `docs(plan): record executable typed gate identity checkpoint` | resolved by this exact unique subject | The implementation oracle requires one matching commit and supersedes the scoped checkpoint while retaining its review history. |
| T-TSDC-004R-2 executable identity Plan review evidence | Record the final C0/I0 Plan approval pair | `docs(task): record executable identity plan reviews` | resolved by this exact unique subject | Read-only specification and quality/security reviewers both authorized the one bounded five-path implementation attempt; Wave B remains blocked. |
| T-TSDC-004R-2 identity-cleanup implementation | Finalize adopted-root cleanup and unreaped-leader pidfd identity | `fix(ci): finalize typed gate identity cleanup` | `17645f2a` | RED 94 = 74 pass + 11 skip + 6 fail + 3 error; focused GREEN 28/28; full GREEN 94 = 83 pass + 11 skip; workflow 7/23/8; both execution-free profile projections; exact Ruff/compileall; four byte freezes; advisory, exact five-path scope, and diff hygiene pass. Fresh reviews returned SPEC_COMPLIANCE NO and CHANGES_REQUIRED, so this commit does not unblock Wave B. |
| T-TSDC-004R-2 initial typed-interruption design draft | Record the first 4.2S review-return draft | `docs(plan): define typed interruption recovery` | `4abc8009` | A read-only analysis agent exceeded its assignment. The draft records the review pair but is incomplete and grants no implementation authority. |
| T-TSDC-004R-2 initial typed-interruption checkpoint | Attempt to freeze the first draft | `docs(plan): record typed interruption design checkpoint` | `5d089dd4` | Superseded because the author exceeded its read-only assignment and the design omitted acquisition/reap-phase and proc-descriptor interruption details. |
| T-TSDC-004R-2 interruption-safe Plan correction | Define complete ordinary-exception and lifecycle-interruption ownership | `docs(plan): correct typed interruption recovery` | `b3166ef7` | Preserves exact five-path scope, four freezes, conditional reap, value-free errors, and explicit metadata/traceability evidence before a new checkpoint. |
| T-TSDC-004R-2 interruption-safe design checkpoint | Freeze the first corrected successor scope | `docs(plan): record interruption-safe typed gate checkpoint` | `b73d2a99` | Superseded after quality/security review found the adopted-root `N`-close interruption gap; no implementation authority followed. |
| T-TSDC-004R-2 adopted-root interruption Plan correction | Start cleanup ownership at the exact `N`-to-`M` transfer | `docs(plan): close adopted-root interruption gap` | `16de8939` | Requires fixed root-cleanup precedence, exactly one `M` close attempt, and behavior-specific control-flow witnesses before a new checkpoint. |
| T-TSDC-004R-2 adopted-root interruption checkpoint | Freeze the final corrected successor scope | `docs(plan): record adopted-root interruption checkpoint` | resolved by this exact unique subject | The implementation oracle requires one matching commit and supersedes `b73d2a99` while retaining its review history. |
| T-TSDC-004R-2 adopted-root Plan review evidence | Record the final C0/I0 approval pair | `docs(task): record adopted-root plan reviews` | resolved by this exact unique subject | Read-only specification and quality/security reviewers authorize one bounded five-path Task 4.2T implementation attempt; Wave B remains blocked. |
| T-TSDC-004R-2 typed-interruption implementation | Close adopted-root and action-raised runner interruption boundaries | `fix(ci): close typed interruption boundary` | `483d3a47` | RED `74/11/7/2`; GREEN focused `28/28` and full `83/11/0/0`; workflow `7/23/8`; projections `32/32/35`; exact Ruff, compileall, four freezes, advisory, metadata, traceability, five-path scope, zero-untracked, and diff gates pass. Fresh reviews returned specification approval but quality/security C0/I1, so Wave B remains blocked. |
| T-TSDC-004R-2 phase-owned runner Plan correction | Close bound-process lifecycle transition gaps | `docs(plan): define phase-owned runner recovery` | `4025aa42` | Freezes the accepted adapter pair, restricts implementation to three paths, and defines one outer controller plus transition-specific RED witnesses. |
| T-TSDC-004R-2 phase-owned runner checkpoint | Freeze the first runner-only successor scope | `docs(plan): record phase-owned runner checkpoint` | `ce4111d8` | Superseded after specification review found the stale Task 4.2T `Whole branch` prerequisite; no implementation authority followed. |
| T-TSDC-004R-2 phase-owned runner gate reconciliation | Align the branch gate with Task 4.2U | `docs(plan): reconcile phase-owned runner gate` | `9281692e` | Replaces the stale Task 4.2T prerequisite while preserving the runner-only allowlist, accepted adapter freeze, lifecycle design, and Wave B block. |
| T-TSDC-004R-2 reconciled phase-owned runner checkpoint | Freeze the corrected runner-only successor scope | `docs(plan): record reconciled phase-owned runner checkpoint` | resolved by this exact unique subject | The implementation oracle requires one matching commit after the reconciliation and supersedes `ce4111d8` without changing accepted adapter behavior. |
| T-TSDC-004R-2 reconciled phase-owned Plan review evidence | Record the final C0/I0 Plan approval pair | `docs(task): record reconciled phase-owned plan reviews` | resolved by this exact unique subject | Read-only specification and quality/security reviewers authorize the sole three-path Task 4.2U implementation attempt; Wave B remains blocked. |
| T-TSDC-004R-2 phase-owned runner implementation | Close all primary bound-process lifecycle ownership transitions | `fix(ci): close runner ownership transitions` | `ad2df527` | RED `77/11/6/0`; final GREEN focused `28/28` and full `83/11/0/0`; all local gates pass, but fresh quality/security review returned C0/I2 because recovery transitions and pre-bind ordinary-exception normalization remain incomplete. Wave B stays blocked. |
| T-TSDC-004R-2 recovery-owned finalization Plan correction | Own cleanup transitions and pre-bind taxonomy | `docs(plan): define recovery-owned runner finalization` | `28685a1b` | Requires one lifecycle process identity, actual outer and nested finalizers, after-completed-recovery-transition witnesses, fixed value-free `Popen` ordinary-exception handling, the same three-path allowlist, and all prior freezes. |
| T-TSDC-004R-2 recovery-owned runner checkpoint | Freeze the recovery-owned successor scope | `docs(plan): record recovery-owned runner checkpoint` | resolved by this exact unique subject | The implementation oracle requires one matching commit after the corrected Plan and supersedes no accepted adapter behavior. |
| T-TSDC-004R-2 recovery-owned Plan review evidence | Record the final C0/I0 Plan approval pair | `docs(task): record recovery-owned plan reviews` | resolved by this exact unique subject | Read-only specification and quality/security reviewers authorize the sole three-path Task 4.2V implementation attempt; Wave B remains blocked. |
| T-TSDC-004R-2 recovery-owned runner implementation | Close recovery ownership and pre-bind taxonomy | `fix(ci): close recovery ownership transitions` | `cdae7523` | RED `81/11/2/0`; GREEN focused `28/28` and full `83/11/0/0`; workflow `7/23/8`; projections `32/32/35`; exact Ruff, compileall, advisory, metadata, traceability, adapter/four-surface freezes, three-path scope, zero-untracked, and diff gates pass. Fresh implementation reviews returned C0/I0. |
| T-TSDC-004R-2 recovery-owned implementation review evidence | Record the fresh C0/I0 implementation review pair | `docs(task): record recovery-owned implementation reviews` | resolved by this exact unique subject | Both independent read-only reviews approve `5274f58b..cdae7523`; controller revalidation passes and Task 4.3 Wave B becomes the next authorized boundary. |
| T-TSDC-004R-3 atomic workflow/local projection cutover | Project required jobs and local profiles through the frozen typed gate registry | `ci(governance): cut over to typed gate projections` | resolved by this exact unique subject | RED captured the old direct programs; core GREEN is 98 pass plus 12 explained skips, target-delta is 30/30, workflow inventory is 7/23/8 with 16 required IDs, four execution-free profiles pass, manifest is 158/85/73/0/0, and independent Task 4.4 review remains pending. |
| T-TSDC-004R-4 bounded cutover remediation attempt 1 | Close the first fresh cutover review findings | `fix(ci): close typed cutover enforcement gaps` | resolved by this exact unique subject | RED 80 = 52 pass + 12 skip + 15 fail + 1 error; focused GREEN 80 = 68 pass + 12 skip; five-module GREEN 115 = 103 pass + 12 skip; four execution-free projections, Bash, ShellCheck, actionlint, compileall, freeze, exact scope/mode, and diff gates pass; Ruff and controller-prohibited registered child gates remain unverified/skipped. |
| T-TSDC-004R-5 final bounded cutover remediation | Close the final fresh cutover review findings | `fix(ci): finalize typed cutover remediation` | resolved by this exact unique subject | RED 81 = 55 pass + 12 skip + 14 fail; focused GREEN 81 = 69 pass + 12 skip; five-module GREEN 116 = 104 pass + 12 skip; four direct static validations, four execution-free profiles, Bash, ShellCheck, compileall, freezes, exact six-path scope/mode, and diff gates pass; Ruff remains unverified. |
| T-TSDC-004R-5 exhausted review evidence | Record the final attempt-2 review and design return | `docs(task): record exhausted typed cutover review` | resolved by this exact unique subject | Specification C0/I0/M0 approved; quality/security C0/I1/M0 rejected option-bearing wrapper dispatch proof. The two-attempt loop is exhausted and Task 4R returns to design/plan. |
| T-TSDC-004R-4W initial option-aware wrapper-proof Plan | Define the user-approved bounded design return | `docs(plan): define option-aware cutover proof` | `98a3558d` | metadata selected 15/0 with five unchanged legacy exceptions, traceability 46/0, exact two-path scope, and diff hygiene passed; first reviews returned specification C0/I4/M0 and quality/security C0/I3/M0, so no implementation authority followed |
| T-TSDC-004R-4W bounded Plan correction | Close every initial Plan review finding | `docs(plan): correct option-aware cutover proof` | `a46f29b8` | Coreutils 9.11 split-string/no-dispatch contract, exact review checkpoints, failure-producing full-surface scope/mode/clean oracles, complete named RED matrix, metadata selected 15/0 with five unchanged legacy exceptions, traceability 46/0, Task 4.4W and Task 4.5 prerequisite Bash syntax, and diff hygiene pass; final quality/security review nevertheless returned C0/I2/M0 |
| T-TSDC-004R-4W exhausted Plan-review evidence | Record the failed final Plan re-review and return to design | `docs(task): record exhausted option-aware plan review` | resolved by this exact unique subject | quality/security C0/I2/M0; specification review interrupted after the blocker; no Plan-review evidence or implementation authority created |
| T-TSDC-004R-4W Plan review evidence | Superseded uncreated checkpoint | `docs(task): record option-aware proof plan reviews` | not created | non-executable after the 4W Plan review loop failed |
| T-TSDC-004R-4W implementation | Superseded uncreated attempt | `fix(ci): close option-bearing wrapper proof` | not created | non-executable after the 4W Plan review loop failed |
| T-TSDC-004R-4W implementation review evidence | Superseded uncreated checkpoint | `docs(task): record option-aware cutover review` | not created | non-executable after the 4W Plan review loop failed |
| T-TSDC-004R-4X session-local option-proof Plan | Define the user-approved two-defect design return | `docs(plan): define session-local option proof` | `4c7c9c4b` | metadata selected 15/0 with five unchanged legacy exceptions, traceability 46/0, Task 4.4X plus Task 4.5 Step 0 Bash syntax, exact two-path scope/mode/clean proof, and diff hygiene passed; specification C0/I0 but quality/security C0/I2, so no implementation authority followed |
| T-TSDC-004R-4X exhausted Plan-review evidence | Record the failed final Plan review and return to design | `docs(task): record exhausted session-local plan review` | resolved by this exact unique subject | specification C0/I0/M0 approved; quality/security C0/I2/M0 rejected non-fail-fast proof blocks and incomplete Task 4.5 lineage/scope/mode rebinding |
| T-TSDC-004R-4X Plan review evidence | Superseded uncreated checkpoint | `docs(task): record session-local proof plan reviews` | not created | non-executable because the 4X no-correction Plan review failed |
| T-TSDC-004R-4X implementation | Superseded uncreated attempt | `fix(ci): close session-local wrapper proof` | not created | non-executable because the 4X no-correction Plan review failed |
| T-TSDC-004R-4X implementation review evidence | Superseded uncreated checkpoint | `docs(task): record session-local wrapper review` | not created | non-executable because the 4X no-correction Plan review failed |
| T-TSDC-004R-4Y fail-fast lineage-proof Plan | Define the user-approved two-finding design return | `docs(plan): define fail-fast lineage proof` | `a8cc9751` | metadata selected 15/0 with five unchanged legacy exceptions, traceability 46/0, ten strict-block headers and Bash syntax, exact two-path scope/mode/clean proof, and diff hygiene passed; quality/security C0/I1 rejected substitution-status masking |
| T-TSDC-004R-4Y exhausted Plan-review evidence | Record the failed final Plan review and return to design | `docs(task): record exhausted fail-fast plan review` | resolved by this exact unique subject | quality/security C0/I1/M0; specification review interrupted after the blocker; no Plan-review evidence or implementation authority created |
| T-TSDC-004R-4Y Plan review evidence | Superseded uncreated checkpoint | `docs(task): record fail-fast lineage plan reviews` | not created | non-executable because the 4Y no-correction Plan review failed |
| T-TSDC-004R-4Y implementation | Superseded uncreated attempt | `fix(ci): close fail-fast wrapper proof` | not created | non-executable because the 4Y no-correction Plan review failed |
| T-TSDC-004R-4Y implementation review evidence | Superseded uncreated checkpoint | `docs(task): record fail-fast wrapper review` | not created | non-executable because the 4Y no-correction Plan review failed |
| T-TSDC-004R-4Z status-preserving proof Plan | Define the user-approved one-finding design return | `docs(plan): define status-preserving proof` | `9968bb6d` | metadata selected 15/0 with five unchanged legacy exceptions, traceability 46/0, ten strict blocks, Bash syntax, substitution-shape audit, exact two-path scope/mode/clean proof, and diff hygiene passed; specification C0/I0 but quality/security C0/I1 rejected immediate-consumption inconsistency |
| T-TSDC-004R-4Z exhausted Plan-review evidence | Record the failed final Plan review and return to design | `docs(task): record exhausted status-preserving plan review` | resolved by this exact unique subject | specification C0/I0/M0 approved; quality/security C0/I1/M0 rejected captures not immediately followed by their value tests |
| T-TSDC-004R-4Z Plan review evidence | Superseded uncreated checkpoint | `docs(task): record status-preserving plan reviews` | not created | non-executable because the 4Z no-correction Plan review failed |
| T-TSDC-004R-4Z implementation | Superseded uncreated attempt | `fix(ci): close status-preserving wrapper proof` | not created | non-executable because the 4Z no-correction Plan review failed |
| T-TSDC-004R-4Z implementation review evidence | Superseded uncreated checkpoint | `docs(task): record status-preserving wrapper review` | not created | non-executable because the 4Z no-correction Plan review failed |
| T-TSDC-004R-4AA immediate-consumption proof Plan | Define the user-approved one-finding design return | `docs(plan): define immediate-consumption proof` | `861c0e33` | metadata selected 15/0 with five unchanged legacy exceptions, traceability 46/0, ten strict blocks, Bash syntax, 112/112 capture/test pairs, exact two-path scope/mode/clean proof, and diff hygiene passed; fresh specification and quality/security reviews both returned C0/I0 |
| T-TSDC-004R-4AA Plan review evidence | Record the fresh C0/I0 Plan approval pair | `docs(task): record immediate-consumption plan reviews` | resolved by this exact unique subject | Task-ledger-only immutable implementation base authorizes the sole exact two-path attempt; Wave C remains blocked |
| T-TSDC-004R-4AA implementation | Close the option-aware wrapper proof under immediate capture/test gates | `fix(ci): close immediate-consumption wrapper proof` | `84067c8f` | RED captured 41 behavior-specific subtest failures in the named test; focused, routing, workflow+routing, five-module frozen regression, static validators, execution-free projections, compileall, scope, mode, and diff gates pass. Ruff remains unverified because it is unavailable and installation is prohibited. Fresh reviews nevertheless rejected the parser proof. |
| T-TSDC-004R-4AA exhausted implementation-review evidence | Record the failed implementation reviews and return to design | `docs(task): record exhausted immediate-consumption wrapper review` | resolved by this exact unique subject | specification C0/I1/M0 and quality/security C0/I3/M0 reject the sole attempt; no retry or Wave C authority is created |
| T-TSDC-004R-4AA implementation review evidence | Superseded uncreated checkpoint | `docs(task): record immediate-consumption wrapper review` | not created | non-executable because the 4AA one-attempt implementation review failed |
| T-TSDC-004R-4AB explicit parser-outcome proof Plan | Define the user-approved three-finding design return | `docs(plan): define explicit parser outcome proof` | `8d3f1122` | exact Plan-and-Task checkpoint from `25524ce1`; strict Bash/capture, scope, mode, metadata, traceability, and diff checks passed, but fresh Plan reviews returned specification C0/I2 and quality/security C0/I2 |
| T-TSDC-004R-4AB Plan review evidence | Superseded uncreated checkpoint | `docs(task): record explicit parser outcome plan reviews` | not created | non-executable because the 4AB no-correction Plan review failed |
| T-TSDC-004R-4AB exhausted Plan-review evidence | Record the rejected Plan review pair | `docs(task): record exhausted explicit parser outcome plan review` | resolved by this exact unique subject | exact range `25524ce1..8d3f1122`; specification and quality/security each returned C0/I2, so no correction, implementation, or Wave C authority follows |
| T-TSDC-004R-4AB implementation | Superseded uncreated attempt | `fix(ci): close explicit parser outcome proof` | not created | non-executable because the 4AB no-correction Plan review failed |
| T-TSDC-004R-4AB implementation review evidence | Superseded uncreated checkpoint | `docs(task): record explicit parser outcome review` | not created | no implementation exists to review |
| T-TSDC-004R-4AB exhausted implementation-review evidence | Superseded uncreated checkpoint | `docs(task): record exhausted explicit parser outcome review` | not created | no implementation exists to reject; 4AB exhausted at Plan review |
| T-TSDC-004R-4AC candidate-closed proof Plan | Define the user-approved four-finding design return | `docs(plan): define candidate-closed parser outcome proof` | `5bc5ab85` | Exact two-path commit from `997719ff`; preserved `100644` modes and passed strict Bash/capture, metadata, traceability, diff, ancestry, distance, scope, and clean-state checks. Fresh reviews returned specification C0/I0/M0 and quality/security C0/I1/M1. |
| T-TSDC-004R-4AC Plan review evidence | Superseded uncreated checkpoint | `docs(task): record candidate-closed parser outcome plan reviews` | not created | Non-executable because the quality/security Plan review failed |
| T-TSDC-004R-4AC exhausted Plan-review evidence | Record the rejected Plan pair and return to design | `docs(task): record exhausted candidate-closed parser outcome plan review` | resolved by this exact unique subject | Exact range `997719ff..5bc5ab85`; specification C0/I0/M0 and quality/security C0/I1/M1 exhaust 4AC without correction, implementation, tests, or Wave C authority |
| T-TSDC-004R-4AC implementation | Superseded uncreated attempt | `fix(ci): close candidate-closed parser outcome proof` | not created | Non-executable because the 4AC no-correction Plan review failed |
| T-TSDC-004R-4AC implementation review evidence | Superseded uncreated checkpoint | `docs(task): record candidate-closed parser outcome review` | not created | No 4AC implementation exists to review |
| T-TSDC-004R-4AC exhausted implementation-review evidence | Superseded uncreated checkpoint | `docs(task): record exhausted candidate-closed parser outcome review` | not created | No implementation exists to reject; 4AC exhausted at Plan review |
| T-TSDC-004R-4AD Plan checkpoint | Define the user-approved terminal-evidence lineage successor | `docs(plan): define review-range-bound parser outcome proof` | `9de469a52c4b05d2490d36d37b95b1277442f725` | One exact Plan-and-Task commit from `3510e994`; preserves `100644` modes and passes strict Bash/capture, metadata, traceability, diff, scope, and mode checks; fresh reviews completed |
| T-TSDC-004R-4AD Plan review evidence | Superseded uncreated checkpoint | `docs(task): record review-range-bound parser outcome plan reviews` | not created | Non-executable because the specification Plan review returned C0/I2/M1 |
| T-TSDC-004R-4AD exhausted Plan-review evidence | Record the rejected Plan pair and return to design | `docs(task): record exhausted review-range-bound parser outcome plan review` | resolved by this exact unique subject | Exact range `3510e9944655ee89077a295712e759d116e2e87f..9de469a52c4b05d2490d36d37b95b1277442f725`; specification C0/I2/M1 and quality/security C0/I0/M0 exhaust 4AD without correction, implementation, tests, or Wave C authority |
| T-TSDC-004R-4AD implementation | Superseded uncreated attempt | `fix(ci): close review-range-bound parser outcome proof` | not created | Non-executable because the 4AD no-correction Plan review failed |
| T-TSDC-004R-4AD implementation review evidence | Superseded uncreated checkpoint | `docs(task): record review-range-bound parser outcome review` | not created | No 4AD implementation exists to review |
| T-TSDC-004R-4AD exhausted implementation-review evidence | Superseded uncreated checkpoint | `docs(task): record exhausted review-range-bound parser outcome review` | not created | No implementation exists to reject; 4AD exhausted at Plan review |
| T-TSDC-004R-4AE Plan checkpoint | Define exact-cell review-range proof | `docs(plan): define exact-cell review-range proof` | resolved by this exact unique subject | Plan and Task only; parent exactly `5644c4a301e38d3f0c32efe99e80f879df6e1ac8`; both modes `100644` |
| T-TSDC-004R-4AE Plan review evidence | Superseded uncreated checkpoint | `docs(task): record exact-cell review-range plan reviews` | not created | Non-executable because the quality/security Plan review returned C0/I2/M0 |
| T-TSDC-004R-4AE exhausted Plan-review evidence | Record the rejected Plan pair and return to design | `docs(task): record exhausted exact-cell review-range plan review` | resolved by this exact unique subject | Exact range `5644c4a301e38d3f0c32efe99e80f879df6e1ac8..8abea15a1ebafdf607be801789a409e6f312c099`; specification C0/I0/M0 and quality/security C0/I2/M0 exhaust 4AE without correction, implementation, tests, or Wave C authority |
| T-TSDC-004R-4AE implementation | Superseded uncreated attempt | `fix(ci): close exact-cell review-range parser proof` | not created | Non-executable because the 4AE no-correction Plan review failed |
| T-TSDC-004R-4AE implementation review evidence | Superseded uncreated checkpoint | `docs(task): record exact-cell review-range review` | not created | No 4AE implementation exists to review |
| T-TSDC-004R-4AE exhausted implementation-review evidence | Superseded uncreated checkpoint | `docs(task): record exhausted exact-cell review-range review` | not created | No implementation exists to reject; 4AE exhausted at Plan review |
| T-TSDC-004R-4AF Plan checkpoint | Define canonical-row authority proof | `docs(plan): define canonical-row authority proof` | resolved by this exact unique subject | P is Plan+Task only from D; both modes `100644`; formal Plan reviews pending |
| T-TSDC-004R-4AF Plan review evidence | Accepted future checkpoint | `docs(task): record canonical-row authority plan reviews` | not created | Only accepted C0/I0/M0 Plan evidence can authorize implementation |
| T-TSDC-004R-4AF exhausted Plan-review evidence | Rejected future checkpoint | `docs(task): record exhausted canonical-row authority plan review` | not created | Terminal XP path; no implementation authority |
| T-TSDC-004R-4AF implementation | Sole future attempt | `fix(ci): close canonical-row authority proof` | not created | Blocked pending accepted Plan-review evidence B |
| T-TSDC-004R-4AF implementation review evidence | Accepted future checkpoint | `docs(task): record canonical-row authority review` | not created | Only R authorizes Task 4.5 |
| T-TSDC-004R-4AF exhausted implementation-review evidence | Rejected future checkpoint | `docs(task): record exhausted canonical-row authority review` | not created | Terminal XI path; no Wave C authority |
| T-TSDC-005 | Audit and remote evidence | `docs(audit): reconcile target surface evidence` | not started | blocked pending accepted 4AF implementation-review R |
| T-TSDC-006 | Blocking promotion and closure | `docs(task): close target surface delta convergence` | not started | Tasks 1–5 pending |

## Deferred and Blocked Items

| Item | State | Reason | Destination |
| --- | --- | --- | --- |
| T-TSDC-004R-1 typed gate contract | completed | Commits `fdc01e1c`, `af898045`, and `af22e129` close the accepted implementation and evidence findings; final specification review is C0/I0/M0 and final quality/security review is C0/I0/M1 with approval. | start T-TSDC-004R-2 from this clean committed review-evidence boundary; close the non-blocking full strict-JSON positive-fixture minor during canonical schema-v2 conversion |
| T-TSDC-004R-2 typed gate runner | review-approved | The sole Task 4.2V implementation and its fresh specification plus quality/security reviews are C0/I0. The accepted adapter pair remains frozen and all manifest verdicts remain pending. | execute the canonical Task 4.3 atomic workflow/local-projection cutover from the clean controller evidence checkpoint |
| T-TSDC-004R-3 atomic projection cutover | active / 4AF Plan review pending | Historical 4AE evidence remains exhausted; active 4AF addresses its duplicate no-leading-pipe and downstream authority-subject uniqueness findings. Ruff, repository-umbrella execution, runtime, and remote state remain unverified. | complete fresh 4AF Plan reviews, accepted B, sole implementation, and accepted implementation-review R before any downstream execution |
| Remote branch-protection synchronization | deferred | Observation-only scope; mutation needs separate approval, rollback, and read-back | future approved GitHub control-plane task |
| Push, pull request, workflow dispatch, and merge | deferred | No external-write approval | finishing workflow after explicit user choice |
| Remote failed-run root-cause analysis | unverified | Raw authenticated logs were not approved or read | separately approved bounded investigation |
| Live Compose/runtime validation | deferred | This wave changes static support/evidence only | domain runtime task with separate approval |
| CD, release, and deployment implementation | deferred | Outside Spec 135 | Spec 127 successor work |
| Self-hosted runner compatibility claim | unverified | No authenticated runner inventory | future control-plane inventory |
| Broad dependency/container vulnerability scanning | partial gap | Existing scoped checks do not establish broad SCA/image coverage | Spec 126 successor work |
| Controlled Agent all-files pre-commit | blocked by approval | No exact one-attempt approval for this wave | final Task 6 gate if separately approved |

The T-TSDC-004R Revision R2 Plan-review gate is satisfied. Task 4.1
implementation, remediation, and review-evidence correction are committed and
approved. Task 4.2S exhausted its one five-path attempt and failed fresh
implementation review. Task 4.2T is a separately bounded design return; its
first corrected checkpoint was also review-rejected and grants no authority.
The adopted-root interruption checkpoint received a fresh Plan C0/I0 pair,
but its sole Task 4.2T implementation attempt failed fresh quality/security
review on closable runner state transitions. Task 4.2U is a runner-only design
return that freezes the accepted adapter pair. Its reconciled checkpoint
received a fresh Plan C0/I0 pair, but its sole implementation attempt failed
fresh quality/security review on recovery-transition ownership and pre-bind
ordinary-exception normalization. Task 4.2V is the bounded recovery-owned
design return. Its corrected checkpoint received a fresh Plan C0/I0 pair,
and its sole implementation attempt passes the bounded local gates and fresh
implementation C0/I0 pair. Task 4.3 Wave B exhausted its two bounded
remediation attempts. Its final specification re-review passed, but the final
quality/security re-review retained one load-bearing Important option-bearing
wrapper bypass. The user approved T-TSDC-004R-4W as a bounded Plan successor;
its initial Plan failed specification and quality/security review, and its
sole bounded correction failed final quality/security review. The Plan review
loop is exhausted; no implementation authority was created. The user approved
T-TSDC-004R-4X as a two-defect Plan successor covering correct GNU `env --`
assignment selection and session-local commit resolution. Its fresh
specification review passed `C0/I0/M0`, but the different
quality/security reviewer returned `C0/I2/M0` because the proof blocks are not
fail-fast and Task 4.5 incompletely rebinds lineage, scope, and modes. The 4X
no-correction loop is exhausted and created no implementation authority. The
user approved T-TSDC-004R-4Y to close those two findings with strict independent
sessions and a complete downstream chain proof. Quality/security review
returned `C0/I1/M0` because direct `test "$(fallible command)"` forms can lose
the substitution status; specification review was interrupted after the
blocker. The 4Y no-correction loop is exhausted and created no implementation
authority. The user approved T-TSDC-004R-4Z to preserve every fallible
substitution status through a standalone assignment before testing its value.
Its fresh independent specification review passed `C0/I0/M0`, but the
different quality/security
reviewer returned `C0/I1/M0` because some captured values are not tested by the
immediately following command as the 4Z contract requires. The 4Z
no-correction loop is exhausted and created no implementation authority. The
user approved T-TSDC-004R-4AA to add explicit adjacent same-variable tests and
a static capture/test-pair audit. Fresh independent specification and
quality/security reviews both returned `C0/I0/M0`; this Task-only evidence
checkpoint authorized one exact two-path implementation attempt. Commit
`84067c8f` passed the bounded local evidence ladder, but fresh implementation
reviews returned specification `C0/I1/M0` and quality/security `C0/I3/M0`.
They found that short/attached/clustered GNU `env -S` skips its first inserted
token, unresolved dynamic command heads can fail open, and malformed signal
long-option near-prefixes can be accepted. The 4AA one-attempt loop is
exhausted without an accepted review checkpoint. Wave C, Tasks 5–6, and final
whole-branch review remain blocked. The user approved T-TSDC-004R-4AB as the
bounded Plan-only successor. It introduces explicit `dispatch`,
`no-dispatch`, and `ambiguous` results, same-parser GNU `env -S` re-entry under
the original no-credit budget, dynamic-head fail-closed handling, exact signal
option matching, fallback-resistant RED, and a full session-local downstream
lineage proof. Fresh independent Plan reviews returned specification
`C0/I2/M0` and quality/security `C0/I2/M0`. They require long split-string
dispatch/query witnesses, no-relevant-sibling unresolved-head negatives,
complete union of exact and embedded ambiguous candidates, and unresolved
positional `$1`/`${1}` handling. The 4AB no-correction Plan loop is exhausted
without implementation authority. The user approved T-TSDC-004R-4AC as the
bounded Plan-only successor from exact checkpoint `997719ff`. The revised
design requires union of every exact and embedded candidate before ambiguity
fallback, unresolved named and positional coverage across relevant-sibling,
no-relevant-sibling, and query-precedence cases, separated and equals long
split-string transition proof, and a two-sibling malformed-signal union plus
valid-option contrast. The exact `997719ff..5bc5ab85` Plan review returned
specification `C0/I0/M0` but quality/security `C0/I1/M1`. Candidate,
dynamic-target, split-string, and signal-option semantics passed, but every
terminal evidence session does not yet rebind the complete reviewed lineage,
distance, scope, and modes, leaving same-subject lineage substitution
unexcluded. The 4AC no-correction Plan loop is exhausted without an
implementation attempt. The user approved T-TSDC-004R-4AD from exact
checkpoint `3510e994`. It preserves the reviewed 4AC parser and behavior proof
and makes each reviewer pair's identical full OIDs the canonical authority
input. Every accepted or rejected terminal evidence session and Task 4.5
re-entry was intended to prove the complete single-parent chain, exact
distances, path sets, modes, and clean state. The exact
`3510e9944655ee89077a295712e759d116e2e87f..9de469a52c4b05d2490d36d37b95b1277442f725`
Plan review returned specification `C0/I2/M1` and quality/security
`C0/I0/M0`. Row-wide range parsing, missing predecessor range/path and
base-mode assertions in three sessions, and stale status text exhaust the 4AD
no-correction Plan loop. Rejected evidence committed at `5644c4a3`. The user
approved 4AE as the bounded Plan-only repair. Its checkpoint is identified by
exact unique subject `docs(plan): define exact-cell review-range proof`.
Exact range
`5644c4a301e38d3f0c32efe99e80f879df6e1ac8..8abea15a1ebafdf607be801789a409e6f312c099`
returned specification `C0/I0/M0` and quality/security `C0/I2/M0`.
Duplicate no-leading-pipe row detection and downstream authority-subject
uniqueness remain open, so the 4AE no-correction Plan loop is exhausted.
The user-approved 4AF Plan has P resolved by its exact unique subject and
awaits fresh independent Plan reviews; implementation, test execution, Wave C,
Tasks 5–6, and whole-branch authority remain blocked pending accepted B and
implementation-review R. The original
five-round implementation blocker, exhausted Revision R1 Plan reviews, and
superseded `5d089dd4` and `b73d2a99` checkpoints remain historical evidence
and grant no authority. The remaining items prevent only their corresponding
external, runtime, or approval-gated claim.

## Related Documents

- [Spec 135](../../03.specs/135-target-surface-delta-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-28-target-surface-delta-convergence.md)
- [Spec 133](../../03.specs/133-target-surface-contract-convergence/spec.md)
- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [GitHub governance](../../00.agent-governance/rules/github-governance.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Existing target-surface manifest](../../90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml)
- [Controlled Agent pre-commit wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
