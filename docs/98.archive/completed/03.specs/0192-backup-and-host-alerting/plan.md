---
title: "Backup and Host Alerting Plan"
version: "0.4.0"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0192-PLAN-0001"
parent_ids:
- "SPEC-0192"
created: "2026-09-29"
---

# Backup and Host Alerting Plan

## Objective

Alert on stale backups and low system-disk space, and make the `n8n` health
check see a lost database, as [SPEC-0192](spec.md) describes.

## Dependencies

- Owner approval to recreate `node-exporter` and `n8n` and to run the backup
  once (W2).

## Execution Sequence

1. W1: Add the contract assertions and observe them fail; change the script,
   node-exporter, the rules, the `n8n` health check and RUN-0021; run
   `promtool check rules` (criteria 1, 3, 5).
2. W2: Create the metrics directory as the host user, recreate
   `node-exporter` and `n8n`, reload Prometheus, run the backup once, and
   check the metric, both rules and `n8n` readiness (criteria 2, 3, 4).
3. W3: Run the full gate and both unit suites (criterion 6).

## Risk and Rollback

W1 is one commit; reverting it and recreating the two services restores the
current state. The metric file is inert without the mount.

## Verification

- The new contract tests, `bash -n`, `promtool check rules`, and pre-commit.
- Prometheus queries for the metric, the rule health and `ALERTS`.
- `run-ci-gate.py --profile full`, `tests/lib`, and `tests/validation`.

## Rulings

None yet.
