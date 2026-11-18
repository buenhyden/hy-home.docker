---
title: "W09 Environment Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0087"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-18"
---

# W09 Environment Task

## Scope

### Objective and Parent

Own criterion 143 and work unit W159 under the [Spec](../spec.md) and
[Plan](../plan.md). Bring this workspace to the 4.2.0 W09-ENV design for
its real execution environment, without starting the whole Compose stack.

### Inputs and Authority

The direct 2026-11-18 request runs W09-ENV from the git-ignored 4.2.0
package. On 2026-11-18 the owner directed that work target the Docker
daemon already installed on this server and that this repository needs no
sandbox. An earlier sandbox change, PR 1095, was closed unmerged at the
owner's request, and no rootless daemon was installed.

## Execution Log

### Work Performed

#### Host survey

Read-only observation on 2026-11-18: Docker Engine 29.9.2 as a rootful
daemon with overlayfs, cgroup v2, AppArmor and seccomp; Compose 5.6.1;
12 CPUs, 31 GiB of memory, the root filesystem 72% used with 69 GiB free;
57 containers running. The root project renders 89 services with every
profile and none without a profile, so a start without a profile selects
nothing and only an every-profile selection starts the whole stack.

#### W159 design

The package items that assume a disposable sandbox (a candidate without
the operating socket, run-owned resources and their cleanup, external
write and network denial, reinstall) are not applicable under the owner's
decision. The remaining guarantee is the service selection rule.
ENVIRONMENT-CONSTRAINTS-R149 requires naming the profiles or services to
start, with Compose adding their `depends_on` closure. R150 forbids
selecting every profile for `up`, `start` or `create`, and its Infrastructure
prose states the server-Docker decision. The new hookify rule
`block-whole-stack-compose-start` refuses `--profile '*'` in any quoting,
`--profile=*` and `COMPOSE_PROFILES` holding `*`, including an earlier
`export`, for both `docker compose` and `docker-compose`. Rendering with
`config` and inspection with `ps` stay allowed. The provider registry lists
the rule, and its test joins the hook rule leaf. The rule starts at `draft`, as the
lifecycle requires of a new rule; the loader reads `enabled`, so it is
enforced now, and moving it to `active` follows the owner's acceptance. The rule sees only command
text; a profile list read from an environment file or a command built at
run time is outside it, which the limits list states.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0087 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0087 | ready | in-progress | #w159-design |

### Blockers and Decisions

A read-only check of whether `.env` sets `COMPOSE_PROFILES` was refused by
the session's permission classifier and was not retried; whether the
operating environment file preselects every profile is unobserved.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Host survey | 143 | W159 | `docker version`, `docker info`, `docker compose version`, `nproc`, `free`, `df`, `docker compose config --services` | This server on 2026-11-18 | PASS | Rootful 29.9.2, Compose 5.6.1, 12 CPUs, 31 GiB, 69 GiB free, 57 running; 89 services with every profile, 0 without | required | - |
| Rule RED | 143 | W159 | `test_compose_start_rule` | New tests before the rule | FAIL | 11 failures: every blocked form passed | required | - |
| Rule GREEN | 143 | W159 | `test_compose_start_rule` | Hookify rule | PASS | 11 blocked forms refused; render, inspect and named starts allowed | required | Rule RED |
| Dispatcher probe | 143 | W159 | shared dispatcher with Bash PreToolUse payloads | Every-profile `up` and a named-service `up` | PASS | Deny naming the rule for the first; no decision for the second; no Docker command ran | required | - |
| Native refusal | 143 | W159 | Claude Bash tool and `codex exec` | A command whose text selects every profile for `up` | PASS | Both providers' PreToolUse hooks refused it before it ran; the Codex command was a harmless `echo` | required | - |
| Environment file profiles | 143 | W159 | key presence of `COMPOSE_PROFILES` in `.env` | Operating environment file | NOT_RUN | Read refused by the permission classifier | optional | - |

### Resolution Links

Rule GREEN resolves Rule RED.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 143 | pending | Host survey, Rule GREEN, Dispatcher probe, Native refusal | Awaits the owner's decision | @buenhyden |

### Remaining Conditions

Whether `.env` preselects profiles is unobserved; the owner can confirm it
or allow the key check.

## Handoff

### Promotion Receipt

ENVIRONMENT-CONSTRAINTS-R149 and R150 with their Infrastructure prose, and
the `block-whole-stack-compose-start` rule with its test, hold the W159
behavior.

### Next Owner

The owner decides criterion 143; the rule moves from `draft` to `active`
after that decision.
