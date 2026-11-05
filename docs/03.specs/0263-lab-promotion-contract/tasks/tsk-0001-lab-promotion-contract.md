---
title: "LAB Promotion Contract Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0263-TSK-0001"
parent_ids:
- "SPEC-0263-PLAN-0001"
created: "2026-11-05"
---

# LAB Promotion Contract Task

## Overview

### Objective

Carry out the six work units of the Plan:

- **Layout.** Bring the 15 LABs into the `labs/<name>/` layout, each with a
  promotion manifest.
- **supabase.** Move it onto LAB secret copies.
- **Readiness.** Add the promotion readiness check.
- **Documents.** Write the promotion operations documents.

## Inputs and Authorization

On 2026-11-05 the owner asked that supabase move into the LAB structure and
that LABs get a structure and rules for promotion into `infra/`. The owner
answered the three open questions recorded in the Spec Background (host
budget, supabase secret copies, the read-only `vector` socket) and approved
SPEC-0263 in this session.

**Earlier permission:** the owner allowed reading and editing the secrets
registry file for this work. The agent's permission settings still deny
`secrets/`, so the owner applies the registry edits that W3 prepares.

**This Task does not:**

- start any container;
- promote any LAB;
- read or write any secret value.

## Work Log

### Current contract decision

The owner approved SPEC-0263 on 2026-11-05. The Plan waits for the owner's
review.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0263 | draft | approved | #current-contract-decision |

### Decisions

These are agent calls, made in the Plan for the owner to check:

- **Manifest kinds.** `opensearch-cluster` and `kafka-cluster` are
  `replace-same`. `valkey-cluster` and `postgresql-ha` are `undecided`,
  because HOME runs both an `mng-db` and a `dev-db` node of each. The other
  11 are `undecided`.
- **Reserve.** The first reserve is 2 CPUs, 4096 MiB of memory and 10% of
  each filesystem kept free. The host measured on 2026-11-05 has 12 CPUs and
  32020 MiB.
- **New operations subjects.**
  - OPS-0107 is `lab-promotion`, with a policy and a runbook.
  - OPS-0108 is `kafka-cluster`.
  - OPS-0109 is `opensearch-cluster`.
- **The readiness check.** It is a `lab.py readiness` subcommand, not a new
  script.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 7 | W6 | metadata | `check-document-metadata.py --mode check-changed --base-ref main` on the Plan working tree over `56446f74c` | PASS | selected=4 violations=0 | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |
| 5 | pending | - | - | @buenhyden |
| 6 | pending | - | - | @buenhyden |
| 7 | pending | - | - | @buenhyden |

## Review and Completion

No work unit has started, and no criterion is accepted.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
