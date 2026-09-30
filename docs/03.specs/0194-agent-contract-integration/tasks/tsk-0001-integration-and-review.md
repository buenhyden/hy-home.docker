---
title: "Agent Contract Integration and Review"
version: "0.1.3"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "specs"
artifact_id: "SPEC-0194-TSK-0001"
parent_ids:
- "SPEC-0194"
- "SPEC-0194-PLAN-0001"
created: "2026-09-29"
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

- 2026-09-30: Bootstrap commit `a887e35e59a4465a2624afd67018cb67d1014af6`
  was pushed to `origin/codex/contract-integration`; draft PR #318 targets
  `main` in `buenhyden/hy-home.docker`. Its prior remote branch and PR were
  absent. The user authorized push, PR, merge and cleanup; recovery is a reviewed
  revert retaining the source commits. Required check `validation-changed`
  failed as workflow run 36669340357 on two baseline whitespace defects.
  Commit `94b1bf373` corrects only those defects. Updating the PR description
  triggered the registered `edited` event and cancelled run 36671793467;
  replacement run 36673358901 is pending on the same commit. This preparation of review status
  remains unpublished until that initial-draft PR passes and merges.

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
| 1 | W1-W5 | Not started | Current Task after active lifecycle and merge receipt |
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
with no concurrent writers, and remains pending until its recorded exit.

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
- The source packet is an evidence input, not this Task's commit. A
  `branch_integration_receipts` entry is written only after active lifecycle
  and an integration result.

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
