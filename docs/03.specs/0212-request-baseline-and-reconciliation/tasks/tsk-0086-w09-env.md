---
title: "W09 Docker Sandbox Task"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0086"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# W09 Docker Sandbox Task

## Scope

### Objective and Parent

Own criterion 142 and work units W158 and W159 under the [Spec](../spec.md)
and [Plan](../plan.md). Bring the Docker profile of the 4.2.0 W09-ENV
design into place: an isolated environment for candidate and test Docker
work that never touches the production daemon, its data or its secrets.

### Inputs and Authority

The direct 2026-11-18 request runs W09-ENV from the git-ignored 4.2.0
package, with designs D11 and D17. On 2026-11-18 the owner chose a per-user
rootless Docker daemon, which needs the `uidmap` package that only the owner
can install. Changes to the production stack, its daemon, networks or
volumes are outside this Task.

## Execution Log

### Work Performed

#### Host survey

Read-only on 2026-11-18: Ubuntu 24.04.5, kernel 6.8.0-147, bare metal,
12 CPUs, 31 GiB memory with 20 GiB available, 71% of a 249 GiB root disk
used. The production daemon is Docker 29.9.2 on `/var/run/docker.sock`
with 57 running containers; the user is in the `docker` group, which is
root-equivalent. `/dev/kvm` and QEMU exist but the user is not in the
`kvm` group. `dockerd-rootless-setuptool.sh` and `rootlesskit` exist,
`newuidmap` and `newgidmap` do not, and the user has a subordinate ID
range. `lxc`, `bwrap` and `k3d` exist. No sandbox entry and no guard
against a whole-stack start existed.

The rendered model has 89 services, all behind profiles, with 158 bind
mounts, 4 Docker socket mounts and 61 secret users. Run alone under the
final checks, 4 services are allowed as defined (`conftest`,
`crawl4ai-egress`, `storybook`, `wiremock`); the rest reach the host
through binds, secrets, env files, devices or GPUs, which the sandbox must
not receive.

#### W158 design

`scripts/operations/sandbox_env.py` has `doctor` (read-only host and daemon
facts), `install` (the rootless setup tool, refused without `uidmap`, and
`--uninstall`), `plan`, `up`, `down` and `cleanup`. `plan` renders the
compose model read-only, resolves the `depends_on` closure of named
services, refuses an empty, `all` or wildcard selection and more than 8
services or 4 GiB of memory limits, and blocks per service: the Docker
socket, a bind outside the repository (read-only) or the run directory, a
real secret file, host networking or PID, privilege, and a missing memory
limit. A security review of the first commit found four bypasses, closed
in the same change: read-only binds into the repository's `secrets/`,
`.env*`, `.git` and `.workspace-*` paths; named volumes that are external
or bind a host path through driver options; network modes other than
`none` or a selected service, and external networks; and host or shared
IPC, UTS, user and cgroup namespaces, devices and GPU reservations,
added capabilities, unconfined profiles, custom runtimes, and config or
env files outside the run directory. A second review found that a bind
of a parent directory, such as the repository root, still exposed those
paths, and that `volumes_from` was unchecked; a bind now must neither be
nor contain a private path, and `volumes_from` is refused. `up` runs only on the rootless socket, never a production socket,
overrides every used network to `internal`, records the
`hyhome-sbx-<run>` project in the ignored `.workspace-sandbox/` and removes
only that run if the start fails. `down` and `cleanup` remove only
recorded sandbox projects. `tests/fixtures/sandbox/compose.yaml` is a
synthetic fixture with one allowed closure and three refused services.
ENVIRONMENT-CONSTRAINTS-R149 to R154 and RUN-0004 state the behavior.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0086 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0086 | ready | in-progress | #w158-design |

### Blockers and Decisions

W159 is blocked until the owner installs `uidmap`; without it the rootless
daemon cannot start, and the production socket is never a substitute.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sandbox RED | 142 | W158 | `test_sandbox_env` | New tests on `ebc758a4a` | FAIL | Import error: no sandbox module | required | - |
| Sandbox GREEN | 142 | W158 | `test_sandbox_env` | Sandbox module and fixture | PASS | 10 tests: closure and refusals, host reach, secret stores, volume drivers and namespaces, budgets, socket choice, internal networks, failed start, owned cleanup, fixture render, doctor | required | Sandbox RED |
| Contract checks | 142 | W158 | sandbox, script manifest, routing and surface suites | Sandbox change | PASS | 161 tests | required | - |
| Fixture plan | 142 | W158 | `sandbox_env.py plan` on the fixture | Host Docker CLI, read-only render | PASS | `app` gives `app` and `cache`; socket, `/etc` bind and real secret refused; empty, `all` and `db*` refused | required | - |
| Live sandbox | 142 | W159 | install, `up`, refusal, isolation and `cleanup` on the rootless daemon | Real host | NOT_RUN | Waits for the owner to install `uidmap` | required | - |

### Resolution Links

Sandbox GREEN resolves Sandbox RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 142 | pending | Sandbox GREEN, Contract checks, Fixture plan | Awaits W159 and the owner's decision | @buenhyden |

### Remaining Conditions

W159 needs `uidmap`, then a rootless install, a fixture start, the
refusals, a network isolation check and cleanup on the real host.

## Handoff

### Promotion Receipt

`sandbox_env.py`, the sandbox fixture, ENVIRONMENT-CONSTRAINTS-R149 to R154
and RUN-0004 hold the W158 behavior.

### Next Owner

The owner installs `uidmap`; the implementer then owns W159. The owner
decides criterion 142.
