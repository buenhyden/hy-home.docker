---
title: "OpenBao Agent Telemetry and Alert Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0239-PLAN-0001"
parent_ids:
- "SPEC-0239"
created: "2026-10-14"
---

# OpenBao Agent Telemetry and Alert Plan

## Overview

Add the listener and telemetry, the network and scrape job, then the alerts
and their cases; observe the pinned image locally; review; deliver.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 3 | Agent listener and telemetry, `obs_net`, scrape job, local image probe | None | TSK-0001 | Task evidence |
| W2 | 2 | Alert rules and promtool cases | W1 | TSK-0001 | Task evidence |
| W3 | 4 | Guide and README rows, checks, independent reviews | W1, W2 | TSK-0001 | Task evidence |
| W4 | 5 | Hosted candidate | W3 | TSK-0001 | Task evidence |

## Verification Plan

Run the new tests against `main` (RED) and the branch (GREEN), the OpenBao
agent contract, compose baseline, runtime compatibility and SEC01 version
suites, both promtool fixtures with the cached promtool image, `promtool check
rules`, changed metadata, links and markdownlint. Start the pinned Agent image
with `--network none` and no credentials, read its metrics path and probe the
other paths.

## Risks and Rollback

- **Unauthenticated endpoint.** Any `obs_net` or `secrets_net` peer can read
  the Agent's counters; they carry no secret or token.
- **Wider network membership.** Joining `obs_net` lets the Agent reach other
  `obs_net` services, and Agent-to-server traffic may use either shared
  network; it stays TLS-verified against the pinned CA.
- **Not deployed.** The change applies on the next Agent recreate, which is a
  separately approved runtime step.
- **Rollback.** Revert the commits; the Agent returns to no listener.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-openbao-agent-alert.md)
