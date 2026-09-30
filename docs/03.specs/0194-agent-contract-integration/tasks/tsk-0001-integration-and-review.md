---
title: "Agent Contract Integration and Review"
version: "0.1.1"
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
  is running as workflow run 36669340357. This preparation of review status
  remains unpublished until that initial-draft PR passes and merges.

- 2026-09-29: The owner requested integration, push, merge, main synchronization
  and branch/worktree cleanup, excluding separately ongoing SPEC-0182. The owner
  also explicitly requested automated checks plus independent read-only agent
  semantic review. Repository target is buenhyden/hy-home.docker; no protection
  changes, forced pushes, real service operations, or credentials are included.
- Draft registration and its independent review precede lifecycle promotion.
  At initial drafting, no receipt, push, pull request, merge, or cleanup had occurred.

## Verification Evidence

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

Source evidence is focused/local-static. Public changed/full,
hosted CI, native/provider observations, coverage, and runtime recovery remain
unobserved. The historical source QA attempt stopped at identity-history regression:
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

- SPEC-0182 is separate ongoing work and excluded from disposition.
- SPEC-0191 is completed and preserved at acce0a6ba. Its later committed
  receipt supersedes this Task's earlier draft-only assessment; no archive
  body is edited.

## Deferred Items

SPEC-0195 owns the transferred native observations. Coverage, final merged
changed/full results, controlled all-files QA, hosted checks, and Git delivery
remain here. R27 requires read-only recovery review, not an actual restore.
