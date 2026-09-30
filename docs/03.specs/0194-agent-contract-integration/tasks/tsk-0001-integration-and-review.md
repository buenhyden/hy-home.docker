---
title: "Agent Contract Integration and Review"
version: "1.0.3"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0194-TSK-0001"
parent_ids:
- "SPEC-0194"
- "SPEC-0194-PLAN-0001"
created: "2026-09-29"
branch_integration_receipts:
- source_commit: "c86f55518b8a9a156e10e38fbd52d1a883063d6a"
  source_package_path: "docs/03.specs/0190-agent-contract-hardening"
  source_artifact_id: "SPEC-0190"
  preserved_package_path: "docs/98.archive/superseded/03.specs/0190-agent-contract-hardening"
  target_package_path: "docs/03.specs/0194-agent-contract-integration"
  target_artifact_id: "SPEC-0194"
  disposition: "historical-superseded"
---

# Agent Contract Integration and Review

## Objective

Execute the [Plan](../plan.md), preserve the source packet's actual limits,
and record the integration result.

## Inputs

- Frozen source packet: `c86f55518b8a9a156e10e38fbd52d1a883063d6a`.
- Implementation branch `codex/agent-contracts` HEAD: `a46539a7b`.
- Target `buenhyden/hy-home.docker`, branch `main`.
- REQ-0024, AD-0027, current `main`, and active SPEC-0182.

## Work Log

- 2026-09-30: Latest main `517397f27` is incorporated. Review PR #319 publishes
  `5502672f5`; its hosted checks remain pending. Local approved successor
  `1389d23ce` passed metadata (4 documents, zero violations), Markdown,
  renderer drift=0 and independent read-only review. It remains unpublished
  until #319 lands. On clean committed implementation candidate `db971359b`,
  the manual changed profile passed (empty-path repository-integrity fallback).
  The controlled all-files wrapper also passed with before/after/changed/
  unexpected counts all zero. Logs are `/tmp/contract-final-changed-db971.log`
  and `/tmp/contract-final-precommit-db971.log`. Full is still running on a
  separate clean copy of that exact commit; no final full PASS is inferred.

- 2026-09-30: Committed activation `cc936b314` passed metadata for all three
  immediate transitions, Markdown and independent read-only review. The source
  `a46539a7b` merge is now prepared locally. The three conflicts retain current
  recovery-skill lifecycle, current Stage 03 inventory, and SPEC high-water
  195/next 196 while adding the source evaluation path registration. All 12
  original package members match `c86f55518` byte-for-byte under the superseded
  archive. The separately completed HOME SPEC-0190 remains unchanged. This is a
  candidate integration result, not a main merge or final acceptance result.

- 2026-09-30: Approved predecessor `522433593` passed immediate-transition
  metadata (4 documents, zero violations), Markdown, renderer drift=0 and
  independent read-only review. Spec/Plan now enter active and this Task enters
  in-progress locally under the existing implementation approval. Original
  source integration and exact-byte handoff follow this committed activation;
  remote publication still waits for each predecessor PR to land.

- 2026-09-30: Review predecessor `91031eb99` records the independently reviewed
  scope, coverage ruling and bootstrap results. The owner already explicitly
  approved design, Spec, Plan and implementation, including separate SPEC-0195
  observations and the 80% changed-Python-line denominator. This local stage
  promotes Spec/Plan to approved, Task to ready and the reviewed recovery skill
  to active. Publication waits for the preceding review stage to land. Source
  integration and any receipt still wait for active Spec/Plan and in-progress
  Task; no native/runtime execution is authorized by this transition.

- 2026-09-30: Bootstrap commit `a887e35e59a4465a2624afd67018cb67d1014af6`
  was pushed to `origin/codex/contract-integration`; draft PR #318 targets
  `main` in `buenhyden/hy-home.docker`. Its prior remote branch and PR were
  absent. The user authorized push, PR, merge and cleanup; recovery is a reviewed
  revert retaining the source commits. Required check `validation-changed`
  failed as workflow run 36669340357 on two baseline whitespace defects.
  Commit `94b1bf373` corrects only those defects. Updating the PR description
  triggered the registered `edited` event and cancelled run 36671793467;
  replacement run 36673358901 failed on a high-severity brace-expansion
  advisory. PR #318 was subsequently observed merged at 2026-09-30T06:00:00Z,
  with head `94b1bf373` and merge `517397f27`; this merge is not CI PASS evidence.
  Commit `3a5c32a12` updates only the three affected lock entries to official
  patched versions 1.1.21 and 5.0.12. Independent read-only security review,
  npm audit (zero vulnerabilities), and npm ci dry-run (531 planned packages)
  passed. The next review PR must pass its own required hosted check.

- 2026-09-29: The owner requested integration, push, merge, main synchronization
  and branch/worktree cleanup, excluding separately ongoing SPEC-0182. The owner
  also explicitly requested automated checks plus independent read-only agent
  semantic review. Repository target is buenhyden/hy-home.docker; no protection
  changes, forced pushes, real service operations, or credentials are included.
- Draft registration and its independent review precede lifecycle promotion.
  At initial drafting, no receipt, push, pull request, merge, or cleanup had occurred.

## Verification Evidence

The owner explicitly answered "변경된 실행 줄 80%로 명시" on 2026-09-30
after reviewing the changed-line and incomplete whole-file denominators.
Criterion 7 uses that aggregate changed executable-line scope; the original
source packet remains immutable. This is an explicit scope ruling, not a claim
that whole-file coverage passed.

Stdlib trace measurement on source `a46539a7b`, relative to `24b3e45c7`,
observed 954/1,020 changed executable lines (93.53%). The separate whole-file
lower bound is 6,974/13,075 (53.34%), not 80% acceptance. The denominator is
stdlib `trace._find_executable_linenos()` intersected with rename-aware Git
added/modified hunk lines; the evaluator move is R073, not a wholly new file.

| Affected Python file | Observed changed executable lines | Total changed executable lines |
| --- | ---: | ---: |
| `.agents/evaluations/agent_output_eval.py` | 393 | 393 |
| `scripts/lib/agent_governance/agent_governance_contract.py` | 278 | 319 |
| `scripts/lib/document_governance/links.py` | 264 | 285 |
| `scripts/lib/document_governance/metadata/lifecycle.py` | 5 | 6 |
| `scripts/lib/document_governance/references.py` | 1 | 1 |
| `scripts/lib/document_governance/registry.py` | 0 | 0 |
| `scripts/lib/document_governance/spec_packages.py` | 8 | 11 |
| `scripts/lib/gate/ci_gate_adapters.py` | 3 | 3 |
| `scripts/validation/check-script-manifest.py` | 1 | 1 |
| `scripts/validation/ci_gate_runner.py` | 1 | 1 |

The initial broad stdlib trace attempt reached its 1,800-second limit without
a saved result; no coverage is inferred from it. A narrower additional
instrumentation sample used exact source filenames, omitted test/stdlib
instrumentation, and saved line sets on each test and timeout:

```sh
rtk proxy env -i PATH=/home/hyunyoun/.local/bin:/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 timeout 600 python3 -B /tmp/agent-contract-coverage-focused.py
```

The temporary helper used only stdlib trace/unittest and existing tests; no
repository tooling, dependency, gate, or test was changed. After 540.02 seconds
it saved counts and returned exit 2 (timeout): 81 selected tests completed
without failures, errors or skips, the 82nd was interrupted, and 11 were not
started. Its sample is not a passing whole-suite result. The large
`test_skill_resource_bounds_are_enforced` case was omitted from this additional
measurement only; registered gate selection remains intact. Parent-process
line observations exclude subprocesses, copied fixtures, threads, and branch
coverage. The observed line sets cover non-test Python sources only. The precise temporary
line-set receipt is
`/tmp/agent-contract-coverage-measured-lines.json`; the table above preserves
its result here. Independent read-only merge_preflight review reproduced the 954/1,020 result
from Git and the exact line sets and cleared this Python metric. Shell
coverage is not claimed; existing shell syntax, ShellCheck and functional
regressions remain separate requirements.

On 2026-09-30, origin/main advanced to 0470e3950. Its completed SPEC-0192
backup package and active SPEC-0193 remain unchanged. The unpublished
integration draft was allocated SPEC-0194 to avoid their identities. Prior
full-run output was unavailable after interruption; no PASS is inferred.

The owner explicitly answered "별도 후속 작업으로 이관" on 2026-09-30.
Actual R04/R15/R18/R19/R22 and model-entitlement observations now belong to
SPEC-0195-TSK-0001 with unchanged conditions and missing status. This authorizes
transfer, not execution. Coverage and delivery gates remain in this Task.

On 2026-09-30, `python3 scripts/validation/run-ci-gate.py --profile full`
completed with exit 0 on the 13-file bootstrap candidate based on 0470e3950.
Observed results include 617 document/history regressions, 239 gate regressions,
72 Compose selections (360 total selected services), Conftest 16/16, 294/294 and
66/66, and baseline tests 124 with 23 explicitly skipped runtime cases.
Those skipped cases do not prove runtime recovery. The existing historical-link
warning remains baseline debt. No real service, native model, or credential
operation ran. Later edits only record this result and the approved transfer.

The separate PR-base metadata check found one newly introduced forbidden Task
heading. Its content was moved into this existing Verification Evidence section;
the correction and new follow-up documents passed PR-base metadata
(selected=10, violations=0, exceptions=0, overrides=0), Markdown (11 files),
and cached diff checks. These checks do not replace final merged-candidate QA.

Before the later bootstrap and coverage observations above, source evidence
was focused/local-static; public profiles, hosted CI, native observations,
coverage and runtime recovery were unobserved. The historical source QA attempt
stopped at identity-history regression:
high-water mark 190 observed 191; no runtime leaf ran. This is NOT PASS.

Bootstrap validation: PR-base metadata selected 7 documents with zero violations,
exceptions or overrides; repository agent contract and renderer PASS, drift=0;
Markdown 8 files PASS. The first bootstrap full run exposed the new skill count
and Git-untracked projection; exact count 23 to 24 plus staging the new sources
fixed those inputs. Provider regressions then passed 49/49 in 35.938 s. The next
full run exposed the missing skill-discovery route. Reusing the original
discovery-only keyword entry fixed it; route regressions passed 5/5 in 0.115 s.
Neither failed full run is reported as successful.

After resumption, origin/main advanced to acce0a6ba, completing and preserving
SPEC-0191. The owner clarified that main remains the target because local and
remote dev branches do not exist. The owned draft was preserved in a named Git
stash, latest main was fast-forwarded, and the draft restored; its obsolete
SPEC-0191 assessment was corrected without touching frozen evidence or SPEC-0182.
The third full attempt failed two OIDC script permission assertions: this
managed checkout had group-writable executable copies. Removing only group/other
write bits in those two copies restored mode 0755 without a Git content change.
Both affected modules passed 19/19 in 0.515 s. That third bootstrap attempt was not PASS; the successful 2026-09-30
bootstrap result above supersedes it. The final integrated merge candidate still
requires its own full result.

The source branch policy change e6ae1ee9b passed independent rules review,
changed metadata (2 documents, zero violations), Markdown and diff checks.
The collision correction has a witnessed RED and 43/43 focused PASS, plus
independent code review. Those source changes await later integration.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1-W5 | Local candidate and exact receipt prepared; remote delivery pending | Current Task after active lifecycle and merge receipt |
| 2 | W1-W3 | Not started | Registered validators and bounded independent reviewer |
| 3 | W4 | Not started | Registered CI gate evidence |
| 4 | W5 | Not started | Forge required-check result |
| 5 | W2/W5/W6 | Not started | Git history and worktree state |
| 6 | W2/W6 | Approved transfer; review and commit pending | SPEC-0195-TSK-0001 for native portions; this Task for retained delivery |
| 7 | W4/W6 | PASS: observed 954/1,020 Python changed lines; independently verified | This Task; owner-approved changed-line denominator |

The temporary measurement receipt SHA-256 is
`c717d7c2ba8ffeb251838359e1908bf1d9e1d9f6ba869a55bcb77bc025214ebf`; the stdlib-only
helper SHA-256 is `1c60c8e4b9f9c17c0592f509dfde677c3dc0dce6bc268bc5f855cbac01caee57`.
They identify the reviewed observation inputs, not a standing branch-tip gate.

### Semantic Review Research

The owner requested fewer repeated human semantic reviews. Existing deterministic
checks and a separate read-only agent reviewer are reused; no review service,
new model call, automatic approval framework, or protection change is added.

- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): required reviews and status checks remain distinct merge conditions.
- [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices): evaluation quality and task-specific cases matter; automated scoring requires validation.
- [Claude Code security](https://code.claude.com/docs/en/security): permission boundaries remain separate from suggested code and tool execution.

The canonical implementation belongs to workflows and quality-standards. It
requires same-revision evidence, an independent reviewer, explicit unknowns,
and escalation for ambiguity, disagreement, high-risk uncertainty, new scope,
or an explicitly required human gate. Rules-engineer reviewed this boundary
before implementation and cleared the resulting two-file policy diff.

The first hosted run 36669340357 completed its regression and security checks
but failed all-files formatting: one blank line after the Pyroscope runbook
code fence and one final newline in the Kafka JMX configuration. Independent
read-only review confirmed commit `94b1bf373` matches those two CI edits exactly,
with no changed values or behavior. PR-base metadata selected 11 documents with
zero violations; Markdown and YAML checks passed (existing YAML warnings remain).

On clean detached `94b1bf373`, the registered
`scripts/validation/run-agent-precommit-all-files.sh` ran with this tracked Task
and the exact bootstrap/fix path prefixes. It returned exit 0:
`hook_result=passed`, before/after/changed/unexpected counts all 0. No formatter
fallout was discarded. The first manual changed run returned exit 0 but an
attempted read-only Markdown check unexpectedly applied the same Pyroscope
blank line during execution; it is not exact-commit evidence. A fresh manual
changed run uses the exact `94b1bf373` tree staged against `0470e3950` (18 paths),
with no concurrent writers, and completed with exit 0. Post-run index tree
identity and an empty unstaged diff confirm the exact `94b1bf373` tree. The log
`/tmp/contract-bootstrap-changed-94b1.log` includes 617 document/history tests
(542.276 seconds), Compose selections, policy/security and final 157 metadata
tests. This bootstrap PASS does not replace the source-integrated candidate QA.

### Source R01-R39 Disposition

Source evidence below is frozen at
`c86f55518b8a9a156e10e38fbd52d1a883063d6a`, from the original final Task's
`Numbered Acceptance Reconciliation` section of W10. `Local PASS` means the recorded
source contract/fixture/review result, not PASS of the final integrated revision.
Original evidence, failed checkpoints, and statuses remain unchanged.

`Delivery pending` requires this Task's final integrated-revision receipts:
registered changed/full profiles, controlled all-files wrapper, required hosted
checks, independent review, and Git delivery. Relevant rows identify these
explicitly; no row makes them PASS before execution.

The owner's explicit 2026-09-30 transfer assigns actual observations for
R04/R15/R18/R19/R22 and the original Plan's entitlement requirement to
SPEC-0195-TSK-0001. Their BLOCKED/NOT_RUN states and strict acceptance remain.
Other native limitations are disclosed limits, not invented extra live-test
requirements. R27 does not require an actual restore.

| Source criterion | Original owner and evidence | Local contract disposition | Remaining owner / delivery condition |
| --- | --- | --- | --- |
| R01 | `W6`, G/P/H role-routing tests and responsibility review | Local PASS: 14 roles, implementation/reviewer/approval boundaries | 0194: retain matrix; no added live role-invocation requirement |
| R02 | `W6`, `W9`, 24-skill/10-resource disposition and consumer review | Local PASS: authored bodies, consumers, focused acceptance recorded | 0194: preserve disposition and consumer mapping |
| R03 | `W2`, `W7`, authority tests and independent policy review | Local PASS: one current authority and failure handling | 0194: integrate the canonical semantic-review delegation change with its own receipt |
| R04 | `W8`, H/N payload, failure, timeout and missing-lint tests | Local PASS: deterministic hook behavior; actual delivery NOT_RUN | 0195 criterion 1: actual native hook delivery |
| R05 | `W6`, P/G mapping, renderer and membership rejection | Local PASS: role/skill/model/tool/permission mapping; invocation is not inferred | 0194: retain validated mappings; actual invocation is separately owned by R15 |
| R06 | `W7`, `W9`, knowledge provenance/invalidation review | Local PASS: fact owner, source, observation, refresh and selected loading | 0194: preserve current-source contract; no live memory store required |
| R07 | `W7`, E/ET envelope and refusal cases plus prompt review | Local PASS: required/partial inputs, outputs and authority boundaries | 0194: retain envelope contract |
| R08 | `W7`, E/ET bounded retry/resume cases and approval review | Local PASS: design/spec/plan approvals and failure/resumption boundaries | 0194: preserve actual authorization and registered lifecycle |
| R09 | `W4`, `W5`, final `W10` H regressions | Local PASS: helper grammar/cwd/exit/discovery/timeout and descendant cleanup | 0194: final public gate and command delivery pending; historical real-helper BLOCKED is not a PASS |
| R10 | `W7`, `W8`, output review and H/N status cases | Local PASS: failures, non-execution and approvals stay visible | 0194: retain contract; no unsupported native rendering claim |
| R11 | `W2` through `W9`, reviewed file/consumer dispositions | Local PASS: accepted findings have owners and transitions; history retained | 0194: finish actual source integration and record approved transfer, not blanket source completion |
| R12 | `W3`, `W6`, G/P/H resource and trigger cases | Local PASS: bounded reachable resources and rejection behavior | 0194: retain regression coverage; percentage evidence is a separate delivery receipt |
| R13 | `W6`, `W10`, model mapping and needs_revalidation review | Local PASS: support/entitlement/runtime remain distinct; no static clearance | 0194 retains mapping; 0195 criterion 4 owns original Plan entitlement observation |
| R14 | `W7`, E/ET and memory/handoff ownership review | Local PASS: durable/short-term ownership, promotion, expiry and invalidation | 0194 retains contract; native cross-provider refusal is owned by R22 |
| R15 | `W6`, `W8`, `W9`, P/N and renderer/consumer checks | Local PASS: canonical/native syntax, source preservation, zero drift and bounded derived modes; native acceptance NOT_RUN | 0195 criterion 2: separate actual Claude/Codex invocation observations |
| R16 | `W7`, `W8`, loading/precedence review | Local PASS: explicit loading, language, safety and global-state boundary | 0194: preserve boundaries; cite real version evidence for any actual native claim |
| R17 | `W5`, `W7`, `W8`, hook/partial-state regressions | Local PASS: Git-hook ownership and configured-versus-executed distinction | 0194: controlled all-files wrapper and actual Git-hook execution evidence pending; no paid call implied |
| R18 | `W10`, preserved bindings and explicit CLI/editor distinction | Contract recorded; editor observation NOT_RUN | 0195 criterion 3: actual version/action/selection/keybinding observation |
| R19 | `W7`, `W9`, E/ET exhaustion/contention/429 cases | Local PASS: deterministic bounds/refusal; actual hard enforcement BLOCKED | 0195 criterion 4: supported real enforcement and separately observed entitlement/account context |
| R20 | `W8`, `W9`, native/trust fixtures and workflow contract | Local PASS: required identities, pins and privilege boundaries preserved | 0194: actual final-revision hosted required checks pending |
| R21 | `W7`, coordination/Task-authority review | Local PASS: Issues linkage, Projects preference/Linear alternative and approval boundary | 0194: record actual PR/branch linkage; no new external coordination platform required |
| R22 | `W7`, E/ET stale/digest/approval/writer recorded-output cases | Local PASS: refusal contract; actual cross-provider behavior NOT_RUN | 0195 criterion 5: native pre-write refusal and valid resumption |
| R23 | `W2`, final `W10` L 96/96 and independent semantic review | Local PASS: normalized authority cases and legitimate exceptions | 0194: retain source-owner separation and review integrated authority changes |
| R24 | `W6`, `W9`, progressive disclosure and E baseline/trigger cases | Local PASS: direct/paraphrased/non-target, functional and baseline coverage | 0194: preserve fixtures; no additional native efficacy experiment required |
| R25 | `W3`, G no-follow/type/race/resource-bound regressions | Local PASS: valid bundles pass and unsafe entries fail | 0194: retain existing contract/tests |
| R26 | `W3`, `W9`, resource/consumer ownership review | Local PASS: skill resources stay skill-owned; shared evaluation ownership follows consumers | 0194: preserve single implementations |
| R27 | `W6`, `W9`, P/G/H routing plus recovery E cases | Local PASS: review skill authored, registered, routed and evaluated | 0194: deliver skill and helpers; real restore is outside this criterion |
| R28 | `W6`, role responsibility and independence review | Local PASS: normal/exception work has distinct responsible roles | 0194: preserve separate operational approval boundary |
| R29 | `W6`, pinned external source/license disposition review | Local PASS: adopted/excluded concepts bounded; no persona/install authority | 0194: preserve existing source and license disposition |
| R30 | `W7`, `W8`, domain/approval and native-grant review | Local PASS: workspace coverage without service/credential grants | 0194: preserve boundary; no service observation required |
| R31 | `W2`, `W6`, `W9`, C/P/registry/renderer checks | Local PASS: proper common/native owners and aligned generated consumers | 0194: retain alignment; actual invocation is separately owned by R15 |
| R32 | `W9`, equivalent pre/post E 10/38 and final E 11/54, consumer tests | Local PASS: four-file migration, obsolete criterion removal and recovery coverage | 0194: deliver .agents/evaluations with consumers and no obsolete root copy |
| R33 | `W2`, `W7`, `W9`, stale-fact/path review | Local PASS: current claims corrected and dated history preserved | 0194: reconcile current main without rewriting frozen results |
| R34 | `W4`, `W5`, final `W10` H/lint evidence | Local PASS: helper implementation/output/fixtures agree; past failures remain explicit | 0194: final profiles and separately defined coverage receipt pending delivery reconciliation |
| R35 | `W6`, four role deltas/ten retentions and P/G/H tests | Local PASS: 14 stable IDs with evidenced responsibilities and permissions | 0194: preserve dispositions; no added live invocation requirement |
| R36 | `W6`, `W9`, 17 retained/6 modified/1 new and resource/consumer tests | Local PASS: two helpers, recovery skill, metadata and evaluator connected | 0194: deliver full consumer set; no additional native efficacy experiment required |
| R37 | `W6`, `W8`, P/N mapping and membership rejection | Local PASS: 28 role projections/24 Claude skill projections; live acceptance not inferred | 0194: preserve mappings and explicit limits |
| R38 | `W7`, `W9`, E/ET lifecycle cases and five-workflow contract | Local PASS: starts/approvals/failure/resume/terminal and check identities retained | 0194: final hosted required-check production and integration pending |
| R39 | `W4`, `W5`, `W9`, final `W10` H/consumer/CLI tests | Local PASS: grammar/cwd/missing-tool/timeout/exit and actual callers | 0194: final public profiles and obsolete-caller integration checks pending |

### Separate Current Coverage Receipt

The owner explicitly selected changed-executable-line coverage with an 80%
threshold. The independently verified Python measurement is 954/1020 changed
executable lines, 93.53%; this is not an 80% full-file coverage claim. Record its
exact measured revision, command and independent review with this Task's current
receipt, rather than attributing it to frozen W10. Shell behavior/lint checks
remain separately evidenced. Coverage is retained in SPEC-0194, not transferred.

### Frozen Evidence Key

The work-unit labels below identify original Task filenames under the source
package named by `branch_integration_receipts`. They are historical provenance
labels, not current references to superseded authority. The existing receipt
provides the exact Git object; current obligations belong to this Spec and
their canonical owners. No preserved body is changed. G/P/H/N/E/ET/L/C are the command groups in
the original Plan's Verification map, not new test commands. W9 records the
355-test final consumer run and W10 records final L96/H50, lint and review
corrections. Earlier failures are retained and superseded only by their actual
recorded reruns.

| Historical work unit | Original Task filename |
| --- | --- |
| `W2` | `tsk-0002-document-authority.md` |
| `W3` | `tsk-0003-skill-resource-boundaries.md` |
| `W4` | `tsk-0004-infra-static-validation.md` |
| `W5` | `tsk-0005-style-classification.md` |
| `W6` | `tsk-0006-recovery-contract-review.md` |
| `W7` | `tsk-0007-workflow-and-handoff.md` |
| `W8` | `tsk-0008-native-hooks.md` |
| `W9` | `tsk-0009-evaluation-consumers.md` |
| `W10` | `tsk-0010-final-acceptance.md` |

On committed candidate `7d60bd5f4`, the controlled all-files wrapper passed
with before/after/changed/unexpected path counts all zero. The first full
profile then failed document links: 73 direct references from the new acceptance
table to superseded payloads and one nested README navigation link. The table
now retains work-unit filenames and the existing receipt provenance without
making the preserved packet current authority; the README states its existing
owner path. The all-document link check then passed with zero failures and the
existing 2,870-link historical warning. No archive body or validator exception
was changed.

The first changed preparation left four old evaluator paths in its index because
rename output omitted the old names. It was interrupted and is not evidence.
A corrected 105-path snapshot matched the candidate bytes but used approved
HEAD `522433593`, so archive source resolution lacked the candidate's committed
receipt and added two history failures. It is not final acceptance evidence.
Independent review confirmed the correct route: run registered changed and full
on the same clean committed candidate, explicitly report changed's empty-path
repository-integrity fallback, and require the real PR-base hosted changed check.
Full retains all implementation suites; no hosted environment is fabricated and
no artificial dirty path is introduced to manipulate selection.

## Review Evidence

Independent read-only merge_preflight review cleared the staged bootstrap and
approved observation transfer after the chronology correction. The final
PR-base metadata recheck selected 10 documents with zero violations, exceptions,
or overrides. This clears bootstrap publication, not final source acceptance.
The initial manual changed attempt was interrupted before publication to run
local and hosted checks on the same committed revision; it is not PASS.

Independent rules review cleared the draft obligation transfer after requiring
strict observed PASS and full R01-R39 inheritance. The same-ID/different-slug
receipt defect is explicitly assigned to W2, rather than hidden by an exception.
Required human approvals remain intact.

## Commit Ledger

- `a887e35e59a4465a2624afd67018cb67d1014af6`: initial integration/native
  follow-up drafts, original recovery skill draft, registration and discovery.
- `91031eb99`: reviewed scope, approved coverage denominator and bootstrap evidence.
- `522433593`: approved Spec/Plan, ready Task and active reviewed recovery skill.
- `cc936b314`: active Spec/Plan and in-progress Task before the source merge.
- The source packet remains immutable evidence; this active Task carries its
  exact historical-superseded receipt for the prepared integration result.

## Rulings

The owner has already authorized design, Spec, Plan, implementation and Git
integration. Independent read-only policy review confirmed local sequential
lifecycle validation/review/commits may precede their remote publication.
Each PR still publishes only the next immediate state after its predecessor
lands; intermediate local commits never bypass merge-base-to-head validation.
Source integration and its receipt begin only with local active Spec/Plan and
in-progress Task. Candidate changes after QA require affected revalidation.

Read-only package inventory at main `0470e3950` found no stale incomplete
package to discard. SPEC-0182 is excluded. SPEC-0193 remains active: its
criterion 9/W7 explicitly waits for SPEC-0182 W8 measurements after 2026-10-03.
Existing completion receipts are preserved, not re-executed or rewritten.

| Package | Evidence-based disposition | Archive commit |
| --- | --- | --- |
| SPEC-0179 | Completed Spec/Plan/Task; criteria 1-14 PASS retained | `39e933314` |
| SPEC-0183 | Completed; criteria 1-8 PASS retained | `559cdd2bc` |
| SPEC-0188 | Completed; criteria 1-6 PASS retained | `7fe6f896b` |
| SPEC-0189 | Completed; criteria 1-3 PASS retained | `7fe6f896b` |
| SPEC-0190 HOME | Completed; criteria 1-2 PASS retained | `159cf8bfb` |
| SPEC-0191 | Completed; criteria 1-4 and failed/retest history retained | `acce0a6ba` |
| SPEC-0192 backup | Completed; criteria 1-6 PASS retained | `f542942fe` |
| SPEC-0190 hardening | Exact historical supersession to SPEC-0194/0195 pending | Frozen source `c86f55518` |

- SPEC-0182 is separate ongoing work and excluded from disposition.
- SPEC-0191 is completed and preserved at acce0a6ba. Its later committed
  receipt supersedes this Task's earlier draft-only assessment; no archive
  body is edited.

## Deferred Items

SPEC-0195 owns the transferred native observations. Coverage, final merged
changed/full results, controlled all-files QA, hosted checks, and Git delivery
remain here. R27 requires read-only recovery review, not an actual restore.
