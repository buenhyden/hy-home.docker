---
title: "Quality Load Tools and OTel Metric Semantics Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0214-PLAN-0001"
parent_ids:
- "SPEC-0214"
created: "2026-10-07"
---

# Quality Load Tools and OTel Metric Semantics Plan

## Overview

Fix the metric identity defect first, then extend the k6 contract and
executor, then the Locust LAB, then documents. Each unit is one commit.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 3 | Authenticated quality receiver and identity-preserving transform | None | TSK-0001 | Task evidence |
| W2 | 1, 2 | Manifest v2 telemetry and executor OTLP peer | W1 | TSK-0001 | Task evidence |
| W3 | 4 | Locust worker input, max wait and deadline | None | TSK-0001 | Task evidence |
| W4 | 5 | Documents and final validation | W1, W2, W3 | TSK-0001 | Task evidence |
| W5 | 6 | Relay controller, executor relay contract, cancel cleanup | W2 | TSK-0002 | Task evidence |
| W6 | 6 | Dashboard absent-versus-zero rule | W1 | TSK-0002 | Task evidence |
| W7 | 9 | `quality_otlp_net` egress network and Alloy membership | W5 | TSK-0002 | Task evidence |
| W8 | 8 | `lab.py run` supervisor and Locust lifecycle | W3 | TSK-0002 | Task evidence |
| W9 | 7 | Isolated end-to-end relay run | W5, W6 | TSK-0002 | Task evidence |
| W10 | 5, 9 | Documents, HOME Alloy recreation, HOME relay run | W5–W9 | TSK-0002 | Task evidence |

## Verification Plan

Run focused unit tests with RED before GREEN, the existing isolated metrics
harness against the pinned Alloy, Prometheus and Python digests, an isolated
Locust run with a WireMock target, the registered changed-profile local gate
and the pinned staged lint. Remote PR `candidate-quality` owns candidate
acceptance. Isolated projects are owned and cleaned by the harness.

## Risks and Rollback

Reverting W1 restores the previous receiver and transform. HOME Alloy runs the
old configuration until it is recreated, which is a separate operation. The
new token secret is a reference only; its value is issued by the operator.

Version 0.2.0 (W5–W10) adds one HOME change: Alloy is recreated to join
`quality_otlp_net`. Reverting W7 and recreating Alloy again restores its
previous networks. A relay is removed with its run; `quality_run.py cleanup
--run-id` removes a crashed run's leftovers.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-quality-k6-locust-and-otel-semantics.md)
- [Relay and Locust lifecycle Task](tasks/tsk-0002-relay-controller-and-locust-lifecycle.md)
