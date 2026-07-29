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
  first review attempt required this bounded correction, so only the final
  corrected C0/I0 pair can activate implementation. This approval does not
  authorize remote, runtime, secret-payload,
  dependency-installation, controlled-wrapper, or direct pre-commit actions.
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
| T-TSDC-004 | Cut over workflow and QA ownership to typed gates | CI/security | TSDC-010–014 | gate contract, runner, exact projection, workflow, and CI script tests | original agents remain historical; fresh R2 agents only after final corrected Plan reviews | blocked pending corrected Revision R2 Plan reviews |
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
| T-TSDC-001 | Task 1 implementation agent | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M0; APPROVED; COMMIT_READY YES | `72eef68c..43f78ad5` | approved; completed | Fresh independent reviewers found no unresolved issues. Per-row manifest verdicts remain pending for Task 6 blocking promotion. |
| T-TSDC-002 | Task 2 documentation-surface implementation agent | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M0; APPROVED; COMMIT_READY YES | `78af8462..b28764a9` | approved; completed | Fresh independent reviewers found no unresolved issues after canonical-contract remediation. All 136 manifest row verdict pairs remain pending for Task 6. |
| T-TSDC-003 | Task 3 static-version implementation agent / replacement remediation implementers | C0/I0/M0; SPEC_COMPLIANCE YES; COMMIT_READY YES | C0/I0/M0; PASS; COMMIT_READY YES | `b1e62873..60e0313c` | approved; completed | Fresh independent reviewers found no unresolved issues across all four pinned implementation commits. Exact stale-absence protects all 15 mappings, global dequoted service-name uniqueness prevents ambiguity, and all 141 manifest verdict pairs remain pending for Task 6. |
| T-TSDC-004 | Task 4 workflow/QA implementation agent / replacement remediation implementers | C0/I4/M0; SPEC_COMPLIANCE NO; COMMIT_READY NO | C0/I4/M1; CHANGES_REQUIRED; COMMIT_READY NO | `ba93483c..78f9f012` final fix re-review; prior review chain begins at `6fabbf05` | blocked after fix round 5/5 | TSDC-012 remains load-bearing: the validator cannot yet prove one CI owner across all valid shell/Python/helper execution equivalences and bounded provenance paths. No finding is waived; all 148 manifest verdict pairs remain pending. |
| T-TSDC-005 | pending | pending | pending | not available | pending | Task 4 review pending |
| T-TSDC-006 | pending | pending | pending | not available | pending | Tasks 1–5 pending |
| Whole branch | not applicable | pending fresh reviewer | pending different fresh reviewer | not available | pending | Final implementation not started |

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
| T-TSDC-005 | Audit and remote evidence | `docs(audit): reconcile target surface evidence` | not started | Task 4 review pending |
| T-TSDC-006 | Blocking promotion and closure | `docs(task): close target surface delta convergence` | not started | Tasks 1–5 pending |

## Deferred and Blocked Items

| Item | State | Reason | Destination |
| --- | --- | --- | --- |
| T-TSDC-004 semantic ownership proof | blocked pending corrected Revision R2 Plan reviews | Five original remediation rounds and the two-attempt Revision R1 Plan review loop remain exhausted. Revision R2 is approved; its first fresh specification review found five Important defects while quality/security passed. Implementation cannot start until the bounded correction receives a final independent specification and quality/security C0/I0 pair. | final corrected C0/I0 Plan review pair, then T-TSDC-004R activation |
| Remote branch-protection synchronization | deferred | Observation-only scope; mutation needs separate approval, rollback, and read-back | future approved GitHub control-plane task |
| Push, pull request, workflow dispatch, and merge | deferred | No external-write approval | finishing workflow after explicit user choice |
| Remote failed-run root-cause analysis | unverified | Raw authenticated logs were not approved or read | separately approved bounded investigation |
| Live Compose/runtime validation | deferred | This wave changes static support/evidence only | domain runtime task with separate approval |
| CD, release, and deployment implementation | deferred | Outside Spec 135 | Spec 127 successor work |
| Self-hosted runner compatibility claim | unverified | No authenticated runner inventory | future control-plane inventory |
| Broad dependency/container vulnerability scanning | partial gap | Existing scoped checks do not establish broad SCA/image coverage | Spec 126 successor work |
| Controlled Agent all-files pre-commit | blocked by approval | No exact one-attempt approval for this wave | final Task 6 gate if separately approved |

The T-TSDC-004R Revision R2 Plan-review gate blocks Tasks 4 through 6. The
original five-round implementation blocker and exhausted
Revision R1 Plan reviews remain historical evidence and are neither waived nor
counted as extra attempts. The remaining items prevent only their
corresponding external, runtime, or approval-gated claim.

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
