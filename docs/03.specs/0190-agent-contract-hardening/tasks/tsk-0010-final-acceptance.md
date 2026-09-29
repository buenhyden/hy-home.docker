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
