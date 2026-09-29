---
title: "Contract Hardening Final Acceptance"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0010"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Contract Hardening Final Acceptance

## Objective

Verify the approved local branch as a whole and reconcile all numbered
acceptance criteria with actual evidence, preserving unresolved observations.

## Inputs

- [Approved Spec](../spec.md), [approved Plan](../plan.md), and unit Tasks.
- Branch codex/agent-contracts, baseline 24b3e45c7fba5f11455c2a9b333463dfccfd3398.
- User-selected finish: preserve the managed worktree and local commits.
- Final execution waits for W8/W9 implementation and independent unit review.
  This draft records preflight only; it does not declare those units complete.

## Work Log

The final verification and branch-finishing skills were read explicitly.
The existing selected branch-preservation option controls integration; no new
menu, publication, merge, deletion or archival is needed.

Read-only public changed/full explain each resolved 13 public validators during
preflight. Compose rendering and Conftest container execution appear among the
selected routes. Inspect exact invocation effects before running either profile;
no runtime action follows merely from the name of a validation command.

## Verification Evidence

BLOCKED / NOT_RUN: final changed/full execution and controlled all-files wrapper.
Independent read-only safety preflight resolved 36 actual leaf invocations for
each current local profile; explain lists only 13 canonical validator routes.
Default Compose validation creates .env/dummy secret paths; PostgreSQL
check-config-only invalidates a canonical handoff and queries Docker resources;
Conftest runs/removes a container and can pull an image. Baseline checks render
real checkout Compose configuration. The runner isolates HOME but strips a
DOCKER_HOST override, so it cannot select a dedicated daemon by that route.
No registered equivalent offline/fixture profile exists. Replacing required
leaves would weaken the gate and is not an acceptance route.

A later separately authorized run needs a clean disposable checkout at the exact
reviewed commit, no copied private inputs, an explicitly scoped Docker daemon
and already-local images (or explicit pull permission). The all-files wrapper
also reaches the same public changed gate and Docker-based hadolint. It cannot
run safely merely because some pre-commit dependency caches already exist.
No public profile or Docker operation was executed in this preflight.

W1's historical PASS selected a narrower docs-state suite set and did not cover
the now-selected operations leaves. It cannot establish current final acceptance.
Whole-branch review and final 39-criterion reconciliation remain in progress.

PATH preflight found pre-commit at the existing user-local executable with its
own venv and Docker CLI at /usr/bin/docker. coverage, shellcheck, yamllint, ruff
and conftest were absent from PATH. This is an availability observation, not
permission to install or proof about cached pre-commit environments.

Final-review correction: a child leader could exit successfully while a
background descendant survived. Paired synthetic Docker/Git regressions
(non-capture/capture) witnessed two failures in 1.920s. Reusing the existing
stop routine now sends SIGKILL to remaining group members after the leader wait
and calls it on normal completion too; original command exits remain intact.
Final H: 49/49 PASS in 19.574s, exit 0. Two ShellCheck SC1007 findings were
corrected with explicit empty CDPATH assignments; five changed shell files then
passed the existing pinned ShellCheck, exit 0. No real Docker was used.

Existing pinned cached linters were located without installation. Four changed
YAML files passed yamllint; 60 admitted changed Markdown files passed
markdownlint-cli2 with a temporary identical configuration except fix=false.
These are scoped checks, not the blocked all-files wrapper. Coverage remains
unavailable. W8's earlier tool absence meant PATH availability at that time.

Further final-review corrections: common private-key/SSH/keystore paths were
accepted as ordinary tracked bind inputs. Five synthetic cases witnessed
pre-read marker failures (2.765s). The shared path classifier now blocks the
known names/components before reading; eight final marker cases pass. This is
a known-path denylist, not secret-content scanning; arbitrarily renamed secrets
must be excluded by the reviewed-input prerequisite. Security reviewer CLEAR.

Classification previously emitted raw newline/control-containing Git filenames.
Three cwd cases witnessed RED (0.381s). Bash printf %q now preserves each path
as one physical record; the skill documents escaping and forbids evaluating the
reported data. Regressions cover newline, forged count and ESC names. Independent
code reviewer CLEAR. Final H after both fixes: 50/50 PASS, 21.614s, exit 0.

An earlier combined L/P/H/native-payload run passed 206/207 cases. Its remaining
non-mutation test observed a concurrent root commit changing Git status, not a
link-check mutation. Rerun that test without commits after the final link fix;
this failed checkpoint is retained and is not a final success receipt.

### Numbered Acceptance Reconciliation

These rows distinguish local contract evidence from unresolved observation.
They do not assert all 39 criteria complete. Unit Tasks contain exact receipts;
the Plan command map supplies the registered command expansions.

| Criterion | Unit | Local evidence | Remaining limit |
| --- | --- | --- | --- |
| R01 | W6 | 14 roles retained; recovery responsibility routed | Native invocation unobserved |
| R02 | W6/W9 | 24-skill file disposition and 10-resource stocktake | Native usage/efficacy unobserved |
| R03 | W2/W7 | Current policy authority and semantic review PASS | None in local contract |
| R04 | W8 | H/N payload, failure and skipped-lint checks PASS | Real hook delivery NOT_RUN |
| R05 | W6 | Role/skill/provider mapping and renderer PASS | Native invocation NOT_RUN |
| R06 | W7/W9 | Owner, provenance, invalidation and current routing reviewed | No live memory store claimed |
| R07 | W7 | Input/output/refusal handoff envelope reviewed | None in local contract |
| R08 | W7 | Separate approvals, bounded retry and resume contract | Native enforcement unobserved |
| R09 | W4/W5/W10 | Helper CLI/cwd/exit and process-group regressions PASS | Public full gate BLOCKED |
| R10 | W7/W8 | Output status and approval visibility reviewed | Native rendering NOT_RUN |
| R11 | W2-W9 | File dispositions and active consumer transition recorded | Final branch closure pending |
| R12 | W3/W6 | Resource bounds and rejection regressions PASS | Coverage percentage unmeasured |
| R13 | W6/W10 | Model identities and needs_revalidation preserved | Entitlement/runtime BLOCKED |
| R14 | W7 | Task/knowledge/handoff ownership and expiry contract | Cross-provider live behavior NOT_RUN |
| R15 | W6/W9 | Canonical/native sets and maintenance disposition PASS | Native provider acceptance NOT_RUN |
| R16 | W7/W8 | Loading/precedence and provider boundaries explicit | Native version behavior unobserved |
| R17 | W5/W8 | Git-hook ownership and partial state regressions | All-files wrapper BLOCKED |
| R18 | W10 | User bindings preserved; CLI is not editor evidence | Editor observation NOT_RUN |
| R19 | W7/W9 | Recorded exhaustion/contention/429 refusal cases PASS | Actual hard budget enforcement BLOCKED |
| R20 | W8/W9 | Five workflow identities and local trust fixtures retained | Hosted CI NOT_RUN |
| R21 | W7 | Task authority; Projects preference/Linear alternative recorded | No external coordination adopted |
| R22 | W7 | Stale HEAD/digest/approval/writer recorded cases PASS | Cross-provider live refusal NOT_RUN |
| R23 | W2/W10 | Normalized authority/link tests and semantic review | Final multiline HTML regression pending |
| R24 | W6/W9 | Progressive disclosure and synthetic baseline/trigger cases | Native effectiveness unobserved |
| R25 | W3 | Unsafe resource/path/type/executable rejection PASS | None in local contract |
| R26 | W3/W9 | Skill-owned resources retained; shared evaluator migrated | None in local contract |
| R27 | W6/W9 | Recovery skill registered, routed and evaluated | No actual restore performed |
| R28 | W6 | Implementation/review/human approval responsibilities distinct | Operational approval remains separate |
| R29 | W6 | Selected external concepts and license disposition preserved | No upstream persona/install adoption |
| R30 | W7/W8 | Domain and action boundaries reviewed | No service/credential observation |
| R31 | W2/W6/W9 | Registry/metadata/native consumers agree | Native behavior NOT_RUN |
| R32 | W9 | Four files moved; same 10/38 pre/post; new 11/54 PASS | Final local closure pending |
| R33 | W2/W7/W9 | Stale active paths corrected; dated facts preserved | Future source changes invalidate observations |
| R34 | W4/W5/W10 | Helper output and fixture checks align | Public full profile/coverage BLOCKED |
| R35 | W6 | Four role edits; ten justified retains; 14 stable IDs | Native invocation unobserved |
| R36 | W6/W9 | 17 unchanged, 6 modified, 1 new skill; 10 resources | Native effectiveness unobserved |
| R37 | W6/W8 | 28 role projections and 24 Claude skills retained/validated | Live acceptance NOT_RUN |
| R38 | W7/W9 | Workflow refusal/resume and five Actions retained | Hosted required checks NOT_RUN |
| R39 | W4/W5/W9/W10 | CLI/consumer/escape/pathspec corrections tested | Final link and branch checks pending |

## Review Evidence

Independent final reviewer approved the descendant correction: CLEAR.
Whole-branch review continues. Unit reviews remain in their owning
Tasks and do not substitute for final acceptance.

## Commit Ledger

Local logical commits are recorded in the unit Tasks and Git history. Root
validates actual lifecycle predecessors before final acceptance execution.

## Rulings

- No hidden SKIP, hook bypass, reduced required selector, fabricated native
  result or unsupported 80 percent coverage claim.
- Run safe checks within approval; preserve FAIL/BLOCKED/NOT_RUN distinctly.
- Final fixes stay within already approved W2-W9 paths and receive affected
  verification plus independent review.
- No new dependency, personal state, global configuration, remote mutation,
  paid model call, service operation or secret access is authorized.

## Deferred Items

Native discovery/invocation/hook delivery, editor actions, hosted CI and actual
budget enforcement require their separately scoped observations. Operational
recovery success remains outside the read-only recovery-contract review.
Applicable unresolved acceptance keeps the Spec Package open.
