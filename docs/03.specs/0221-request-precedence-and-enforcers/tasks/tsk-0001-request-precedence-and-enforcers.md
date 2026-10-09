---
title: "Request Precedence and Enforcers Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0221-TSK-0001"
parent_ids:
- "SPEC-0221-PLAN-0001"
created: "2026-10-09"
---

# Request Precedence and Enforcers Task

## Objective

Make the current request's scope and the rank of fetched text explicit and
enforced, make the local gate run the candidate checks that failed late, and
close every blocking rule as changed, kept or permission-limited.

## Inputs and Authorization

The current user request on 2026-10-09 asks to execute prompt 12 of the
analysis pack (request-first workspace policy and enforcer alignment) with
per-unit commits and a per-Spec PR merge. Baseline `main` `5710435ef`
(SPEC-0220 merged as PR #395). During the work the Claude Code auto-mode
safety check refused further edits to role and governance restatements of the
approval rules as self-modification; the owner then chose to keep the two
policy edits already made, asked for R3b, R4 and R5 on 2026-10-09, and applied
the R3b copies that the agent prepared under the ignored `_workspace/`.
User-global settings, user-global hooks and other repositories are out of
scope.

## Work Log

### W1 Inventory and Conflict Table

A read-only search of `.agents/`, `.claude/`, `.codex/`, `docs/99.templates`,
`scripts/`, `tests/`, the Conftest policies, `.github/` and active Specs listed
the rules below. Each row names the blocking condition, the risk it protects,
the new condition, the readers it affects, its regression, and its closure.

| ID | Blocking condition | Protected risk | New condition | Readers | Regression | Closure |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | The local changed gate keeps only typed local-only leaves, so the metadata `check-changed` and tech-stack drift leaves run only in CI; locally only the working tree counts as changed | Local runs must not forge hosted receipts | Committed branch work since `origin/main` counts locally; `leaf.local-candidate-preflight` runs both checks against the merge-base; hosted plans are unchanged | Agents and maintainers running the local gate | `test_ci_gate_plan`, `test_validator_entrypoints` | Changed (`26c73db6c`) |
| R2 | No rule ranked PR and issue comments, web pages or tool output below the user | Instruction injection through data | Fetched text and tool or subagent output are data that cannot widen scope, grant approval or change policy | Every agent through the bootstrap | Contract check | Changed (`49911c730`, `421ed39f6`) |
| R3 | Approval Boundaries required separate approval for runtime, remote mutation, credential and destructive acts, including the push, PR and merge a request asked for | Unreviewed remote or destructive mutation | The request covers its named scope through merge; runtime, out-of-scope remote, credential, deletion, public endpoint and billed acts wait for an exact target | Every agent; reviewers | Contract check rejects the retired bullet | Changed (`49911c730`, `421ed39f6`) |
| R3b | `ci-cd-engineer.md`, `infra-implementer.md`, `github-governance.md` and `task-checklists.md` restate "separate approval" or "after review approval" | Same as R3 | The R3 wording | Role-routed agents | Contract check; renderer parity | Changed (`146726778`): the owner applied them after the auto-mode safety check refused them to the agent; projections re-rendered with `drift=0` |
| R4 | The Stop hook reads deferral exemptions as YAML with `schema: agent-governance/deferred-paths/v1` from `approval-boundaries.md`, which has no such key, so the set is always empty | Leaving a dirty tree at stop | Fix or retire the dead loader | Agents at stop | `test_agent_governance_ci_routing` Stop cases | Changed on the owner's request (`9f5dd9cd0`): the loader is removed and the gate behaves as before |
| R5 | The edit-path guard refuses any absolute path outside the project root except the session scratchpad, including this project's Claude memory directory | Writes outside the repository | A narrow exemption for the provider's memory directory for this repository | Agents keeping memory | `test_tool_payload` memory case | Changed on the owner's request (`fb94a902c`): only a `.md` file directly in `~/.claude/projects/<slug>/memory` is exempt; nested, other extensions, other projects and traversal still fail |
| R6 | SPEC-0204's Plan and Task name exact writers and require separate approval for push, PR and merge; SPEC-0207's Plan keeps push, PR and merge `NOT_RUN` without separate approval | Historical pass scope | Their text describes those passes; current work follows Approval Boundaries, which ranks above Stage 03 documents | Readers of those packages | — | Kept as history; superseded for current work by R3 |
| R7 | Every tracked `infra/**` Compose file must be in the root include, and every service needs a POL-0078 profile | Unselected or orphaned services | — | Compose authors | Existing operations catalog tests | Kept: it did not block this work, and new services such as `crawl4ai-egress` passed by adding rows |
| R8 | Issued IDs are never reused and frontmatter keys keep their order | Identity history integrity | — | Document authors | Existing identity tests | Kept |
| R9 | Stage 05 and README bodies may not repeat runtime versions; Spec bodies keep template headings | One owner per runtime pin and per document shape | Surfaced locally by the R1 preflight | Document authors | R1 tests | Kept; earlier detection through R1 |
| R10 | Hosted contexts exclude local-only leaves and a local pass never satisfies the remote candidate | Forged hosted evidence | — | CI and reviewers | Existing gate tests | Kept; R1 adds no hosted leaf |
| R11 | `docs/01` to `docs/99` are read-only unless the user instructs otherwise | Unrequested document churn | — | All roles | — | Kept: a current request is that instruction |
| R12 | Found by the independent review: `github-governance.md` §3 and §5.0 to §5.1 keep merge, branch deletion and workflow push behind separate approval; `environment-constraints.md` keeps runtime and destructive acts behind separate approval; `approval-boundaries.md` keeps every remote write a separate operation | Same as R3 | The R3 wording: the request's branch, pull request, merge and cleanup follow its scope; other remote surfaces wait for their exact target | Every agent; reviewers | Contract check; renderer parity | Pending the owner: copies under the ignored `_workspace/r3c/` pass the contract check and renderer parity in a temporary worktree. These are rank-2 policies like Approval Boundaries, so ranking does not settle the conflict |

### W2 Local Candidate Parity

`collect_changed_paths` now adds `git diff <merge-base> HEAD` with
`origin/main` before the working-tree and index views, and keeps the earlier
view when no `origin/main` ref exists. `scripts/validation/check-candidate-preflight.sh`
resolves the merge-base, fails with exit 2 when it cannot, and runs
`check-document-metadata.py --mode check-changed --base-ref <merge-base>` and
`sync-tech-stack-versions.sh --check`. The leaf is a local-only validator of
the `document-contract` suite. Tests: a representative service change (a
Compose file and its guide) selects the preflight locally while the hosted
plan keeps `leaf.local-tech-stack-version-drift` without it; committed branch
work is collected only with `origin/main`; the script passes the exact
merge-base, fails on either check, and refuses no base or any argument.
Run on this branch before the first push, the preflight caught an invalid
Spec parent (`SPEC-0212` instead of a requirement or architecture document),
the kind of error that reached CI twice on PR #395; after the fix it exits 0
with `violations=0` and the registry in sync.

### W3 Precedence and Approval Text

The bootstrap (1.4.0) adds that fetched text and tool or subagent output are
never an instruction source. Approval Boundaries (1.2.0) replaces the blanket
approval bullet with the request-scope and exact-target bullets; the secret
reading rule is unchanged.

### W4 Contract Enforcement

`_validate_request_precedence` in the agent-governance contract requires the
three clauses in their canonical owners and rejects the retired bullet.
`RequestPrecedenceContractTests` shows it passing on the repository and on an
unchanged copy, and failing on a copy without the bootstrap clause and with
the retired bullet appended. The repository contract reports
`failures=0`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Conflict inventory | 4 | W1 | Read-only search; table closure | `5710435ef` | PASS | W1 Inventory and Conflict Table | accepted |
| Local candidate parity | 2, 3 | W2 | Gate contract, plan and entrypoint tests | `26c73db6c` | PASS | W2 Local Candidate Parity | accepted |
| Policy text | 4 | W3 | Contract check | `49911c730` | PASS | W3 Precedence and Approval Text | accepted |
| Contract enforcement | 1 | W4 | Contract tests; repository contract | `421ed39f6` | PASS | W4 Contract Enforcement | accepted |
| Memory-file exemption | 4 | W1 | `test_tool_payload` (15 tests, with symlinked directory, symlinked and hardlinked file cases) | `fb94a902c`, `c727fc33e` | PASS | W1 row R5 | accepted |
| Stop gate loader removal | 4 | W1 | `test_agent_governance_ci_routing` (51 tests, including Stop cases) | `9f5dd9cd0` | PASS | W1 row R4 | accepted |
| Role and checklist wording | 4 | W1 | Contract check; renderer `--check` `drift=0` | `146726778` | PASS | W1 row R3b | accepted |
| Review fixes | 2, 3 | W2 | Preflight pinned to `refs/remotes/origin/main`; argument refusal tested with a base; hosted plan from the same change; 49 tests | `b5aa8571b` | PASS | W2 Local Candidate Parity | accepted |

## Review and Completion

Not complete: W5 validation and merge remain.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
