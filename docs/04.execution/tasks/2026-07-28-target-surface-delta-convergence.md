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

The goal is to close TSDC-001 through TSDC-017 with six logical commits,
complete successor-delta classification, whole-surface validation, document
and static-version convergence, typed local workflow/QA controls, reconciled
canonical evidence, and two independent reviews per task.

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
- No current approval authorizes
  `scripts/validation/run-agent-precommit-all-files.sh`. Any future approval
  is one exact attempt from one clean committed checkpoint.

Rollback is one logical task commit at a time after exact-range review. It
never uses `git reset --hard`, discards unrelated user changes, or attempts a
remote/runtime rollback for surfaces this wave does not mutate.

## Work Breakdown

| Task ID | Description | Type | Requirements | Validation owner | Implementation owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-TSDC-001 | Establish successor manifest and whole-surface contract | contract/data | TSDC-001–003, 007, 009 | delta contract tests and advisory checker | fresh Task 1 implementation agent | implementation_complete_review_pending |
| T-TSDC-002 | Converge README, typed example, archive, and secret inventory | docs/governance | TSDC-003–009 | metadata, target, links, alignment | fresh implementer after Task 1 review | pending |
| T-TSDC-003 | Reconcile static versions and verified active lifecycle drift | infra-support/docs | TSDC-003, 008–009 | version, hardening, supply-chain checks | fresh implementer after Task 2 review | pending |
| T-TSDC-004 | Type workflow triggers, dependencies, and QA ownership | CI/security | TSDC-010–014 | workflow contract and CI script tests | fresh implementer after Task 3 review | pending |
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

## Verification Evidence

### Planning verification

| Check | Expected | Actual |
| --- | --- | --- |
| Spec 135 metadata | one selected document, zero violations | Passed before Plan drafting |
| Spec 135 Markdown | zero errors | Passed before Plan drafting |
| Document implementation alignment | zero failures | Passed before Plan drafting |
| `git diff --check` | zero whitespace errors | Passed before Plan drafting |
| Plan/Task metadata and Markdown | zero failures | Passed: changed metadata selected 3 with 0 violations; explicit three-file markdownlint reported 0 errors |
| Plan/Task cross-links | zero failures | Passed: traceability and implementation alignment reported 0 failures |

### Task execution evidence

| Task | RED evidence | GREEN evidence | Aggregate evidence | Result |
| --- | --- | --- | --- | --- |
| T-TSDC-001 | Initial run: 1 pass/12 missing-module errors. First remediation emitted 12 focused failures; second remediation covered structural, secret, and no-follow failures; third remediation emitted 2 failed-verdict subcase failures. | Initial 15/15; first remediation successor 25/25; second exact set 4/4; third affected CLI set 3/3. Production advisory passed and blocking retained 105 spec plus 105 quality pending findings. | Predecessor target suite 40/40 and CLI pass; bounded metadata/static/Markdown/diff gates passed. Broad known-failing aggregate was not repeated. | implementation_complete_review_pending |
| T-TSDC-002 | Not run — Task 1 review pending | Not run — Task 1 review pending | Not run — Task 1 review pending | pending |
| T-TSDC-003 | Not run — Task 2 review pending | Not run — Task 2 review pending | Not run — Task 2 review pending | pending |
| T-TSDC-004 | Not run — Task 3 review pending | Not run — Task 3 review pending | Not run — Task 3 review pending | pending |
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
| Command | Plan defines one exact wrapper command; it has not run |
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
| T-TSDC-001 | Task 1 implementation agent | First C0/I4/M2, second combined C0/I3/M0, and third focused C0/I1/M0 reported; third remediation re-review pending | First C0/I1/M2 plus second combined C0/I3/M0 reported; third remediation re-review pending | `25f4c52a..` third remediation commit | implementation remediated; reviews not approved | The first and second finding sets plus the third failed-verdict advisory finding have implementation evidence but await distinct reviewer confirmation. |
| T-TSDC-002 | pending | pending | pending | not available | pending | Task 1 review pending |
| T-TSDC-003 | pending | pending | pending | not available | pending | Task 2 review pending |
| T-TSDC-004 | pending | pending | pending | not available | pending | Task 3 review pending |
| T-TSDC-005 | pending | pending | pending | not available | pending | Task 4 review pending |
| T-TSDC-006 | pending | pending | pending | not available | pending | Tasks 1–5 pending |
| Whole branch | not applicable | pending fresh reviewer | pending different fresh reviewer | not available | pending | Final implementation not started |

Reviewers are read-only. Any reviewer-created edit or commit is a process
finding and must not be silently accepted as independent review evidence.

## Commit Ledger

| Unit | Logical purpose | Expected commit | Actual commit | Validation |
| --- | --- | --- | --- | --- |
| Planning specification | Define successor convergence design | `docs(spec): define target surface delta convergence` | `e828745a` | metadata, Markdown, alignment, diff hygiene passed |
| Planning activation | Activate Spec and define Plan/Task | `docs(plan): define target surface delta execution` | `a2ba9eb4` | metadata 3/0, Markdown 3/0, traceability 46/0, alignment 674/5,658/141/0, diff hygiene passed |
| T-TSDC-001 | Successor delta contract | `feat(governance): establish target surface delta contract` | `1671e9be` | focused 15/15, predecessor 40/40, metadata 0 violations, advisory CLI, Ruff, Bash syntax, and diff hygiene pass; aggregate limitations recorded |
| T-TSDC-001 remediation | Harden successor evidence contract after two reviews | `fix(governance): harden target delta evidence` | `72e452d0` | remediation RED/GREEN, successor/predecessor/metadata, advisory/blocking, summary, static QA, and diff hygiene |
| T-TSDC-001 second remediation | Close fresh fail-closed review gaps | `fix(governance): close target delta fail-closed gaps` | `25f4c52a` | advisory structural RED/GREEN, secret-like field matrix, no-follow bootstrap, successor/static/metadata/diff gates |
| T-TSDC-001 third remediation | Reject explicit failed review verdicts in advisory mode | `fix(governance): reject failed advisory verdicts` | this logical commit | verdict-state RED/GREEN, focused advisory/blocking tests, production advisory/blocking, static and diff gates |
| T-TSDC-002 | Document surface convergence | `docs(governance): converge target documentation surfaces` | not started | Task 1 review pending |
| T-TSDC-003 | Static version/lifecycle reconciliation | `fix(infra): reconcile static version and lifecycle drift` | not started | Task 2 review pending |
| T-TSDC-004 | Workflow and QA ownership | `ci(governance): type workflow and qa ownership` | not started | Task 3 review pending |
| T-TSDC-005 | Audit and remote evidence | `docs(audit): reconcile target surface evidence` | not started | Task 4 review pending |
| T-TSDC-006 | Blocking promotion and closure | `docs(task): close target surface delta convergence` | not started | Tasks 1–5 pending |

## Deferred and Blocked Items

| Item | State | Reason | Destination |
| --- | --- | --- | --- |
| Remote branch-protection synchronization | deferred | Observation-only scope; mutation needs separate approval, rollback, and read-back | future approved GitHub control-plane task |
| Push, pull request, workflow dispatch, and merge | deferred | No external-write approval | finishing workflow after explicit user choice |
| Remote failed-run root-cause analysis | unverified | Raw authenticated logs were not approved or read | separately approved bounded investigation |
| Live Compose/runtime validation | deferred | This wave changes static support/evidence only | domain runtime task with separate approval |
| CD, release, and deployment implementation | deferred | Outside Spec 135 | Spec 127 successor work |
| Self-hosted runner compatibility claim | unverified | No authenticated runner inventory | future control-plane inventory |
| Broad dependency/container vulnerability scanning | partial gap | Existing scoped checks do not establish broad SCA/image coverage | Spec 126 successor work |
| Controlled Agent all-files pre-commit | blocked by approval | No exact one-attempt approval for this wave | final Task 6 gate if separately approved |

None of these items blocks Plan review. They prevent only the corresponding
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
