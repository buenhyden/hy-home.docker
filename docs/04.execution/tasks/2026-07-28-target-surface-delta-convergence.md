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
| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | gate contract, runner, exact projection, workflow, and CI script tests | fresh Task 4.1 implementation agent; original agents remain historical | active Wave B |
| T-TSDC-005 | Reconcile canonical audit and remote observation evidence | evidence/docs | TSDC-015–016 | audit semantic, generators, links | fresh implementer after Task 4 review | pending |
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
| T-TSDC-004 | Missing wrapper; four missing-module errors; bounded reader 2 failures/1 error; `148 != 141`; missing local wrapper-test route; missing purpose-folder registration; mixed quoted/unquoted `on` failed both orderings; seven required permission co-mutations returned no baseline finding; round 3 produced 15 failures across five methods; round 4 produced 13 failures across four methods; final round 5 produced 29 failures across eight methods. | Successive workflow suites pass 9/9, 11/11, 14/14, 17/17, 20/20, and 27/27. Final round 5 focused methods pass 8/8, eval tests 38/38, and Stage 00 mutations 4/4. Focused CLI 7/23/8, exact manifest 148/89/59/0, and advisory remain green. | Static gates pass, but final independent reviews return specification C0/I4/M0 and quality/security C0/I4/M1. TSDC-012 remains bypassable through valid shell/Python/helper execution forms and bounded-provenance gaps. Every manifest review pair remains pending. | blocked after fix round 5/5 |
| T-TSDC-005 | Not run — Task 4 review pending | Not run — Task 4 review pending | Not run — Task 4 review pending | pending |
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
| T-TSDC-005 | pending | pending | pending | not available | pending | Task 4 review pending |
| T-TSDC-006 | pending | pending | pending | not available | pending | Tasks 1–5 pending |
| Whole branch | not applicable | pending fresh reviewer after Task 4 | pending different fresh reviewer after Task 4 | not available | active | Task 4.3 bounded remediation attempt 1 is implementation-complete and requires fresh Task 4.4 re-review; Wave C, Tasks 5–6, and final branch review remain gated. |

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
| T-TSDC-005 | Audit and remote evidence | `docs(audit): reconcile target surface evidence` | not started | Task 4 review pending |
| T-TSDC-006 | Blocking promotion and closure | `docs(task): close target surface delta convergence` | not started | Tasks 1–5 pending |

## Deferred and Blocked Items

| Item | State | Reason | Destination |
| --- | --- | --- | --- |
| T-TSDC-004R-1 typed gate contract | completed | Commits `fdc01e1c`, `af898045`, and `af22e129` close the accepted implementation and evidence findings; final specification review is C0/I0/M0 and final quality/security review is C0/I0/M1 with approval. | start T-TSDC-004R-2 from this clean committed review-evidence boundary; close the non-blocking full strict-JSON positive-fixture minor during canonical schema-v2 conversion |
| T-TSDC-004R-2 typed gate runner | review-approved | The sole Task 4.2V implementation and its fresh specification plus quality/security reviews are C0/I0. The accepted adapter pair remains frozen and all manifest verdicts remain pending. | execute the canonical Task 4.3 atomic workflow/local-projection cutover from the clean controller evidence checkpoint |
| T-TSDC-004R-3 atomic projection cutover | remediation implementation-complete / re-review pending | Attempt 1 closes the accepted Task 4.4 execution-context, checkout, umbrella, descriptor, and shared-node findings; Ruff, registered child gates, and remote state remain unverified under the active boundary. | run a fresh independent Task 4.4 specification and quality/security re-review before Wave C |
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
implementation C0/I0 pair. Task 4.3 Wave B has completed bounded remediation
attempt 1 and awaits the independent Task 4.4 re-review pair; Wave C,
Tasks 5–6, and final whole-branch review remain blocked by their canonical
prerequisites.
The original five-round
implementation blocker, exhausted Revision R1 Plan reviews, and superseded
`5d089dd4` and `b73d2a99` checkpoints remain historical evidence and grant no
authority. The remaining items prevent only their corresponding external,
runtime, or approval-gated claim.

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
