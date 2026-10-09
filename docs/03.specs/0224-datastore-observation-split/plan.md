---
title: "Datastore Observation Split Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0224-PLAN-0001"
parent_ids:
- "SPEC-0224"
created: "2026-10-09"
---

# Datastore Observation Split Plan

## Overview

Measure what the exporters need, narrow the monitor roles and give MNG its
own, move the exporters onto them, label the scrapes, split the alerts and
dashboards by scope, rehearse in isolation, roll out on HOME, document, and
validate. Commits follow that order.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Monitor roles: MNG PostgreSQL job and SQL, DEV SQL, both Valkey monitor rules, secrets | None | TSK-0001 | Task evidence |
| W2 | 1 | Exporters on the monitor roles; Valkey exporter flags | W1 | TSK-0001 | Task evidence |
| W3 | 1 | Scrape labels and the DEV target start script | W2 | TSK-0001 | Task evidence |
| W4 | 1 | Scoped alerts and dashboards | W3 | TSK-0001 | Task evidence |
| W5 | 2, 3 | Isolated rehearsal, consumer fixes, HOME rollout and failure checks | W4 | TSK-0001 | Task evidence |
| W6 | 3 | READMEs and Runbooks | W5 | TSK-0001 | Task evidence |
| W7 | 4 | Changed gate, staged style check, candidate quality, merge | W6 | TSK-0001 | Task evidence |

## Verification Plan

Unit tests for each contract, promtool on both configurations and the alert
scenarios, the isolated rehearsal against the pinned images, HOME probes and
Prometheus queries without secret output, a client inventory of MNG Valkey,
the changed gate, the staged style check and the remote candidate.

## Risks and Rollback

- Recreating MNG Valkey drops every shared connection for a few seconds; AOF
  keeps the data and consumers reconnect.
- A monitor secret outside the base64 alphabet stops the provision job, and
  the exporter then waits on it; the job's message names the rule.
- MNG Valkey renders its ACL at start, so a missing or malformed
  `mng_valkey_monitor_password` stops the shared server; create and check the
  secret before recreating it.
- Rollback: revert the commits, recreate the four exporters, both Valkey
  servers and Prometheus, and rerun the DEV monitor job. The MNG monitor role
  and its two secrets can stay unused or be dropped by the owner.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-datastore-observation-split.md)
