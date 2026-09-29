---
title: "Backup and Host Alerting"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0192-TSK-0001"
parent_ids:
- "SPEC-0192"
- "SPEC-0192-PLAN-0001"
created: "2026-09-29"
---

# Backup and Host Alerting

## Objective

Execute W1 to W3 of the [Plan](../plan.md) and record the evidence for every
acceptance criterion of [SPEC-0192](../spec.md).

## Inputs

- SPEC-0182 Task 0002, entries of 2026-09-29: the preflight stop at 17.5 GiB
  free and the `n8n` 503 period.
- 2026-09-29 measurements: Alertmanager Slack notifications 49 sent, 0
  failed; a throwaway node-exporter v1.12.1 with the systemd collector failed
  with "An AppArmor policy prevents this" on the D-Bus connection;
  `node_filesystem_avail_bytes{mountpoint="/"}` is collected.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted.

## Verification Evidence

Not started.

## Review Evidence

None yet.

## Commit Ledger

None yet.

## Rulings

- 2026-09-29: Owner approved the package, the W2 runtime changes
  (recreate `node-exporter` and `n8n`, one backup run) and the pushes.

## Deferred Items

None yet.
