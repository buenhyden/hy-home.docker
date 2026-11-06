---
title: "Hermes Report Source Capture Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0265-PLAN-0001"
parent_ids:
- "SPEC-0265"
created: "2026-11-06"
---

# Hermes Report Source Capture Plan

## Overview

The Plan sequences the plugin and prompt change first, then observability and
documentation, then the owner-approved Gateway operations. Nothing is
implemented by this draft.

## Scope

The scope and exclusions are those of SPEC-0265.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2, 4, 6 | Versioned report argument, report store, `source_text` from stored bytes, rejection and `BLOCKED` paths | None | TSK-0001 | plugin unit tests |
| W2 | 3 | Receipt-set private record and `source_ref` binding | W1 | TSK-0001 | plugin tests for `private_records.py` |
| W3 | 5 | Email and Telegram derivation from the stored file; same-digest test | W1 | TSK-0001 | derivation test |
| W4 | 7, 8, 9 | Submission prompt, `update-cron-prompts.sh`, per-execution scratch paths, owner H, D and G items as prompt and validator work (criterion 9) | W1 | TSK-0001 | `test_deploy_scripts.py`; prompt text checks |
| W5 | 10 | Low-cardinality metrics, Alertmanager rule, Grafana panel | W1 | TSK-0001 | metric label test; rule and dashboard lint |
| W6 | 11 | Workload README and document checks | W1, W2, W3, W4, W5 | TSK-0001 | metadata, link, lifecycle and contract checks |
| W7 | 12 | Owner-approved: Gateway backup on the schema-4 image, restore test on a copy, cutover to the Blog-data schema 5 image | W1, W2, W3, W4, W5, W6 | TSK-0001 | operation evidence; NOT_RUN until run |
| W8 | 13 | Blog-data per-report exclusion, dry run listing the 16 reports excluded, then owner-approved apply | W7 | TSK-0001 | dry-run output; NOT_RUN until run |
| W9 | 12, 14 | Owner-approved: install plugin, restart Gateway outside `hermes-gateway.service`, update cron prompts, observe one run per job | W1, W2, W3, W4, W5, W6 | TSK-0001 | live run evidence; NOT_RUN until run |

## Verification Plan

Run the plugin and deploy tests named above and the document checks of
`docs/03.specs/AGENTS.md`. W7 to W9 are operations; their rows stay NOT_RUN
until the owner approves and the evidence is recorded in the Task.

## Risks and Recovery

### Risks and Rollback

- A report near the 1 MiB request limit is rejected; the prompt tells the
  agent the size bound and the run goes `BLOCKED` rather than truncating.
- The Blog-data sensitive heuristic may hold a report export; that is a hold,
  not a failure.
- Rollback of W1 to W5 reverts the plugin and prompts to 0.3.0 and the
  previous prompt block. Rollback of the Gateway cutover restores the
  schema-4 backup and reattaches `c05e5b88`, losing records written after the
  backup. The old image is never attached to a schema-5 database, because the
  new image's backup command cannot create a schema-4 recovery point.
- The Blog-data runbook still names an older server A state; correct it there,
  not here.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-report-source-capture.md)
