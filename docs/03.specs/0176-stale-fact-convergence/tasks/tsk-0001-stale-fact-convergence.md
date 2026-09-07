---
title: "Stale Fact Convergence Execution"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0176-TSK-0001"
parent_ids:
- "SPEC-0176"
- "SPEC-0176-PLAN-0001"
created: "2026-09-07"
---

# Stale Fact Convergence Execution

## Objective

Own every actual command, result, review finding, blocker, and disposition for
SPEC-0176. This Task is the sole execution and handoff authority for the
package; no second progress ledger is created.

## Inputs

- Position, recorded durably rather than by branch name. Work on this package
  happens on a short branch cut from `main` and retired into `main` as soon as it
  is verified, so any branch name written here is dead by the next integration. A
  resuming session reads its position from Git: `git rev-parse --abbrev-ref HEAD`
  for the branch, `git rev-parse HEAD` for the commit, and
  `git log --oneline origin/main..HEAD` for what is not yet on the remote. The
  durable facts are that `main` is the integration target and that the Commit
  Ledger below lists every commit this package produced.
- Audit baseline: local `main` at
  `e37b2dbcd877f6fbbf32205fd4f5e83680630dc9`, clean worktree, six commits ahead
  of `origin/main` at `d890b862e310b519802a1e837089b87a2b27cdf7`.
- Governing owners: REQ-0024, REQ-0025, REQ-0026, AD-0027, AD-0030, ADR-0033,
  SPEC-0176, SPEC-0176-PLAN-0001.
- Authorization: local investigation, local edits, local commits on this branch,
  and local integration into `main`. Push, pull request, remote reference change,
  deployment, live service action, secret values, and global installation remain
  unauthorized. Pushing to `main` is additionally blocked by a registered hook
  and is not attempted by any other route.
- Evidence classes used throughout, kept non-substitutable: `local-executed`,
  `configured`, `repository-enforced`, `official-source`, `local-parser`,
  `unverified-runtime`, `unverified-entitlement`, `unverified-remote`.

## Work Log

### Audit that opened the package (2026-09-07, local-executed)

Eight registered checks were run first, so that the audit could separate what the
gates already prove from what they cannot see. All eight passed:

```text
check-document-metadata.py                 0 findings, 0 parser failures
check-document-links.py --mode all         documents=711 links=6113 failures=0
check-document-corpus-lifecycle.py         violations=0; recovery violations=0
check-agent-governance-contract.py         PASS mode=repository failures=0
check-script-manifest.py                   PASS
check-operations-catalog.py                PASS
check-agentic-audit-semantic-freshness.py  PASS assertions=11 failures=0
report-provider-hook-parity.sh             PASS matrix fresh
```

That result is the reason this package exists. The registered checks prove a
document's existence, profile, and link targets; none of them reads what a
sentence asserts. Every defect below sat inside that blind spot.

A path-claim scan was run over `.agents/`, `.claude/`, `.codex/`, the root shims,
and `llms.txt`, comparing every backticked path against `git ls-files` and the
working tree. It produced seventy-five unresolved candidates and zero defects:
each was a relative filename, a branch-name prefix, or a deliberate negative
statement such as the `graphify-out/wiki/index.md`, `llms-full.txt`, and
`.codex/config.toml` clauses, which correctly say the path does not exist.

### W1: Package opened (2026-09-07, local-executed)

The Spec, Plan, and Task were written at their lifecycle initial statuses,
because the public gate runs `check-document-metadata.py` with
`enforce_initial_status` and proves the walk to `active` from Git history.

The transition budget was measured before any status was chosen, not assumed:

```text
git merge-base origin/main HEAD    d890b862e310b519802a1e837089b87a2b27cdf7
```

At that base the documents this package promotes hold `active` (SPEC-0175 Spec
and Plan), `in-progress` (SPEC-0175 Task), `proposed` (ADR-0033), `accepted`
(ADR-0031), `approved` (REQ-0026), and `active` (AD-0030). Every transition this
package needs is therefore exactly one step from the base and fits the one
transition per document per branch rate. This package's own three documents are
absent from that base and admit no transition at all, which is why they are
created at `draft` and stay there.

The first metadata run rejected the package for a reason worth recording, because
it is the guard working as designed:

```text
identity_spaces.spec: identity-allocation-not-advanced:
  new identity requires atomic allocation advancement
```

Writing `SPEC-0176` into frontmatter does not allocate it. `identity_spaces.spec`
was advanced from `high_water` 175 to 176 and `next_number` 176 to 177 in the
same change, which is what makes the number unavailable to any other allocation.

### The index row implied a status the document did not hold (2026-09-07, local-executed)

The first full changed-profile run passed 356 of 357 tests and failed one:

```text
FAIL: test_current_index_status_matches_each_current_spec
AssertionError: False != True : SPEC-0176
```

The test reads each Stage 03 index row and asserts two things about it: that the
Spec's status word appears in the row, and that the standalone word `active`
appears in the row exactly when the status is `active`. The row satisfied the
first and failed the second, because it described the defect being corrected as
"dead-branch position in the active packages". The word was describing SPEC-0173
and SPEC-0175, not SPEC-0176, but the index is read as a status claim about its
own row and the test is right to refuse the ambiguity. The phrase became "the two
in-flight packages" and the suite returned 33 passed.

Recorded because the failure is worth more than its fix: an index that merely
linked correctly would have passed the link checker, and this test is what makes
the index prose answerable to the frontmatter beside it.

A second point is recorded against this session's own method. The gate was run as
`run-ci-gate.py ... | tail -25` with `echo "GATE EXIT=$?"`, which reports the exit
code of `tail` and printed `GATE EXIT=0` over a failing suite. The failure was
found by reading the output rather than by trusting that number. Exit codes are
read from the gate process directly for the remainder of this Task.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W3 | NOT_RUN: pending | pending |
| 2 | W4 | NOT_RUN: pending | pending |
| 3 | W4 | NOT_RUN: pending | pending |
| 4 | W4 | NOT_RUN: pending | pending |
| 5 | W5 | NOT_RUN: pending | pending |
| 6 | W5 | NOT_RUN: pending | pending |
| 7 | W5 | NOT_RUN: pending | pending |
| 8 | W9 | NOT_RUN: pending | pending |
| 9 | W6 | NOT_RUN: pending | pending |
| 10 | W6 | NOT_RUN: pending | pending |
| 11 | W7 | NOT_RUN: pending | pending |
| 12 | W7 | NOT_RUN: pending | pending |
| 13 | W8 | NOT_RUN: pending | pending |
| 14 | W8 | NOT_RUN: pending | pending |
| 15 | W9 | NOT_RUN: pending | pending |
| 16 | W10 | NOT_RUN: pending | pending |
| 17 | W11 | NOT_RUN: pending | pending |
| 18 | W11 | NOT_RUN: pending | pending |

## Review Evidence

Independent exact-diff review is required by acceptance criterion 18 and has not
been performed. Recorded as NOT_RUN.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| pending | W1 package definition |

## Rulings

- SPEC-0173 is not modified beyond the two stale sentences SPEC-0176 names.
- A guard that fires is treated as correct until proven otherwise; the change is
  adjusted rather than the guard weakened.
- Static configuration and local test results never establish native runtime
  discovery, provider entitlement, Hosted CI, or remote state.
- Unexecuted checks are recorded as NOT_RUN or BLOCKED with their missing input
  and are never promoted to a PASS.

## Deferred Items

| Item | Blocking input or reason |
| --- | --- |
| This package's own lifecycle walk to `active` | The transition check reads the merge base with `origin/main`, and the remote cannot advance without a push that no authorization here grants |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
- [Stage 03 index](../../README.md)
