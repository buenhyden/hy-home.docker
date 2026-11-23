---
title: "Environment Onboarding"
version: "2.2.0"
type: "governance/workspace-guide"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-11-19"
observed_at: "2026-11-20"
reviewed_at: "2026-11-20"
review_cycle: "on-tool-change"
---

# Environment Onboarding

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the guide payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

What a contributor prepares once to work in this workspace, and the first
checks that show the environment is ready. The setup steps themselves stay with
their owners: the [repository README](../../../README.md) for the Docker host,
`.env` and secret layout, the [scripts README](../../../scripts/README.md) for the
validation toolchain, and the [tests README](../../../tests/README.md) for test
runs. This guide connects them and names the boundaries between environments.

#### Prerequisites

Included: a local development checkout on Linux with Git, Docker Engine and
the Docker Compose CLI plugin, Python 3 and Bash. Excluded: the operating host's services,
real secret values, provider accounts and hosted CI, whose results a local run
never stands in for.

This active workspace-environment guide owns the local setup reading route. It
is not a runtime authority for harness mutations. Document adoption, a local
check and a link to a command do not authorize that command or accept a feature;
[approval boundaries](../04.quality/approval-boundaries.md) remain applicable.

#### Procedure

##### Supported environment

| Need | Source of truth |
| --- | --- |
| Git, Docker Engine, the Docker Compose CLI plugin, a local `.env` from `.env.example`, required files under `secrets/` | [Repository README prerequisites](../../../README.md#prerequisites) |
| Python validation dependencies | `scripts/requirements.txt`, installed from the hash lock `scripts/requirements-controller.lock` |
| Opt-in integration tests | `tests/requirements-integration.txt` and a Docker daemon |

##### Python environment

Install the hash lock into its own venv and put that venv's `bin` first on
`PATH` before running scripts or tests. Distribution Python packages can be
older: with `jsonschema` 4.10 there is no `referencing`, and the secret
catalog, SMTP generator, root resource, wiki preparation and metadata sync tests
fail on import or on a nested `python3` call, because some scripts call the
`python3` on `PATH`.

```bash
python3 -m venv .venv
.venv/bin/pip install --require-hashes -r scripts/requirements-controller.lock
export PATH="$PWD/.venv/bin:$PATH"
```

`.venv/` is ignored by Git. Never install into the system interpreter to make a
check pass.

##### First checks

Run these from the repository root after the setup above. None of them changes
a running service.

```bash
bash scripts/validation/validate-docker-compose.sh --preflight
python3 scripts/validation/run-ci-gate.py --profile changed --explain
PYTHONPATH=. python3 -m unittest tests.lib.test_surface_ownership
```

The preflight checks `.env`, required secret and certificate files, key
directories and external networks without creating them. The gate explain
lists what a change would run without running it. A local result is local
evidence only; the pull request's hosted checks own candidate acceptance.

##### Environment boundaries

- A worktree, the HOME operating checkout and a LAB topology are different
  environments; a result in one is not evidence for another.
- The local agent tooling (memory, capture, analysis, forecast, dispatch,
  observe) is maintained through [harness maintenance](../06.maintenance/harness-maintenance.md).
- Secret values are never copied into a checkout, a log or evidence; only
  paths and IDs are recorded.

##### Independent review environment

Use the [review risk standard](../04.quality/quality-standards.md#11-review-risk)
and [review procedure](../../../.agents/governance/workflows.md#review-risk)
for selection and result reuse. The native syntax is in the authored
[Codex adapter](../../../.codex/provider.md) and
[Claude adapter](../../../.claude/provider.md); a generated role name is not
an effective execution boundary.

Prepare only the selected tracked source, actual diff, governing requirements
and relevant checks in an owned disposable source snapshot. Keep dummy
permission targets and writable result scratch separate. Exclude real secret
files, credentials, personal transcripts, Docker sockets and production
endpoints. Snapshot/worktree separation alone supplies no filesystem or
network enforcement. Existing account authentication and model transport are
separate from permissions for review tools to contact arbitrary services.

Check the installed version, effective parent controls, offered tools, MCP
connections and hook sources before the missing observation. Use synthetic
normal-read, refused source-write and outside-read targets; never probe a real
sensitive file. An absent Write tool, an attempted call refused by native
permission rules, and an OS read-only error are different witnesses. Record
which was observed, the unchanged target and the actual fresh-context review.
A fallback route does not repair an earlier failed Desktop route. A fresh
direct CLI context can itself perform independent review; the routine route
need not offer a spawning tool. Keep an instrumented writer-catalog denial
control separate from a routine catalog that offers neither Write nor Agent,
and do not transfer an attempted-call witness between those configurations.

Use the current accounts, selected models and existing limits. A bounded
representative case has at most600s and two actual workers, with providers
observed sequentially. Apply a supported stricter turn/cost limit when it is
verified; a time limit is not a billing guarantee, and unavailable billing or
usage is recorded as null with its reason. Reuse valid same-condition proof;
a failed attempt is followed only by a correction-specific check within the
recorded budget. Do not launch model probes on every CI or Git event.

If an effective environment is missing, record the implemented route, the
missing prerequisite and the exact remaining observation for environment
setup. A known allowed source write remains a failure, not merely an
unobserved result. Retain the bounded verdict and permission events in the
current Task, then remove owned snapshots, dummy targets and temporary
outputs. Preserve persistent tests and other active work; do not retain raw
review-session streams or create another approval ledger.

##### Managed execution and shared resource admission

The registered Compose/LAB and dispatcher entrypoints share the private
host admission implemented by `scripts/lib/ops/environment_admission.py`.
The [maintenance guide](../06.maintenance/harness-maintenance.md#managed-execution-recovery)
owns its operation and recovery. Product profile/companion rules and LAB
resource policy remain in their existing product owners; setup neither
changes the operating configuration nor grants a start permission.

Resolve workspace identity from the real Git common directory and primary
checkout, preserving intentional linked-worktree sharing. Host admission is
separate: a stable private user-owned state location under
`~/.hy-home-execution/` binds to the actual machine. Daemon identity
scopes container/service observations; CPU, memory and disk reservations share
the host namespace across independent clones using these entrypoints. A caller's
plan directory, `--state-dir` or checkout name cannot choose another production
admission store. This user/host boundary is not a system-wide Docker access ACL
and does not claim control of unmanaged actors or another user's allocation.

Before work, record an owned token and pending reservation atomically with
service selection and existing live/external usage. The whole-product service
denominator is the actual current root inventory, never the selected slice.
Use dependency closure for service starts; shared networks, volumes and ports
are footprint/collision constraints, not reasons to start every member.
Pending service sets contribute to the union, and independent reservations
sum conservatively unless shared-instance accounting is actually established.

Use the operator's configured CPU/memory ceilings, existing host reserve and
external workload allowance. Disk admission uses the declared per-run estimate
and observed filesystem capacity with the product policy's ten-percent reserve;
missing data refuses a start. A reservation is not a disk quota. Native scratch
and container storage need their declared bounds and post-run observation;
free-space checks alone do not prove per-process filesystem isolation. Root operating
startup has no per-service lifetime disk estimate, so its bounded intent
conservatively reserves all admissible disk and may serialize starts. Only a
verified complete live snapshot permits the accounting handoff; it supplies no
serving-lifetime disk quota.

For supported plain shell workers, a token-named systemd user control group
supplies CPU/memory/runtime limits and group cancellation, while an allowlisted
Bubblewrap filesystem/network boundary excludes operating home data, Docker
sockets and arbitrary network access. A gated child must record its stable
PID/start-time/boot identity before controller release; a vanished controller
cannot release it into real work. Missing required control support refuses the
bounded execution rather than falling back to an unrestricted child. The
representative profile is at most two actual workers,1CPU/512MiB memory and
256MiB scratch reservation each, at most600s and any stricter plan timeout.
This shell profile is not a provider model call or an authentication transport
profile; P08/P12 consume the separately selected native CLI environment and
perform only their missing feature observations within their finite budgets.

The installed Linux tools and P06 read-only Codex/Claude routes are reusable
at their recorded scopes. Native review tool removal, native permission denial,
OS write denial, a process cgroup and a Docker LAB on the operating daemon prove
different boundaries. A LAB/worktree does not become a whole-process sandbox
by its name; current accounts do not authorize copying operating secrets into
one. Root Compose remains an operating/recreation path. Its successful start
hands accounting to a verified complete live snapshot; uncertain partial state
retains its reservation and requires recovery rather than automatic teardown.

Interrupted, expired and failed records remain charged while their resources
are live or absence is unknown. Cleanup requires matching token and stable
process/container ownership; neither bare PID/PGID, project prefix nor a ledger
mtime authorizes deletion. Keep source, runtime readiness, observed permission
results and actual human acceptance separate. Environment adoption never
converts a prior failed Desktop/writable-parent surface into a successful one.

#### Verification

##### Provenance

Written on 2026-11-19 by SPEC-0212 TSK-0097 from the repository, scripts and
tests READMEs at `main` `eadd81adc`. On that day nine test modules failed under
the system `python3` for lack of `referencing` and passed with the hash-locked
venv first on `PATH`.

The P05 [typed-guide adoption Task](../../03.specs/0212-request-baseline-and-reconciliation/01.tasks/tsk-0103-p05-docs-sdlc.md)
records the 2026-11-20 role and contract review. The original observations above
remain dated to their actual inputs. This adoption executes no maintenance
command and does not complete any outstanding runtime or owner acceptance.

##### Refresh Triggers

- A prerequisite, lock file or first-check command changes in its owner README.
- A new environment class is added.

#### Related Documents

- [Harness maintenance](../06.maintenance/harness-maintenance.md)
- [Repository README](../../../README.md)
- [Scripts README](../../../scripts/README.md)
- [Tests README](../../../tests/README.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
