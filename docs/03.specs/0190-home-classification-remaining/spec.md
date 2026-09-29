---
title: "Remaining HOME Classification Specification"
version: "0.4.0"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190"
parent_ids:
- "REQ-0027"
- "AD-0031"
created: "2026-09-29"
---

# Remaining HOME Classification Specification

## Overview

SPEC-0189 classified Tempo and Pyroscope as `HOME` and deferred three more
services with the same mismatch: `registry`, `dcgm-exporter`, and
`seaweedfs-s3`. [POL-0078](../../05.operations/policies/0078-compose-profile-vocabulary.md)
puts `registry`, `obs-gpu`, and `storage` in HOME, and
`validate-docker-compose.sh` reads the HOME selection from that table. The
resolved HOME selection has 44 services, and all three are among them. The
documents that call them `OPTIONAL`, on-demand, opt-in, or excluded from HOME
are stale.

The owner ruled on 2026-09-29 to resolve the mismatch; the HOME selection
decides it.

## Boundaries and Inputs

In scope:

- `registry`: GDE-0065, POL-0065, `infra/09-tooling/registry/README.md`, and
  its m0021 inventory row.
- `dcgm-exporter`: GDE-0045, the `alert_rules.local.gpu.yml` comment, the
  `06-observability` README service table, and its m0021 inventory row.
- `seaweedfs-s3`: its m0021 inventory row. GDE-0024, POL-0024, and the
  SeaweedFS README already say HOME.

Out of scope:

- m0021's dated ledgers and snapshot tables, which keep what they recorded.
- Changing any profile, service, or the HOME selection itself.
- Registry authentication and TLS; POL-0065's exposure controls stay.

## Behavior Contract

1. Every current document classifies `registry`, `dcgm-exporter`, and
   `seaweedfs-s3` as `HOME`, selected by `registry`, `obs-gpu`, and
   `storage`.

## Technical Approach

1. Change the classification wording in each listed document.
2. Change the m0021 rows' classification, Consumer, and Disposition cells,
   and confirm with the operations catalog renderer that no projected cell
   drifts.

## Interfaces and Data

None. No Compose, profile, or environment change.

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| A document still calls a HOME service optional | A line-wide search for `OPTIONAL`, `opt-in`, on-demand, and HOME exclusion in each owner |
| The renderer drops hand-written lines | Only the edited rows inside the inventory markers change |

## Acceptance Contract

1. No current document outside m0021's dated ledgers and snapshot tables
   calls `registry`, `dcgm-exporter`, or `seaweedfs-s3` `OPTIONAL`, opt-in,
   on-demand, or excluded from HOME.
2. `run-ci-gate.py --profile full`, `tests/lib`, and `tests/validation` pass.

## Traceability

- REQ-0027 and AD-0031: the HOME development host.
- POL-0078: the HOME profile selection.
- SPEC-0189: the Task that deferred these services.

## Open Questions

None.

## Operational Impact

None. The HOME selection already starts all three services.
