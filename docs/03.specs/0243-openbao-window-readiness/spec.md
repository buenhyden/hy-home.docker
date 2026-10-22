---
title: "OpenBao Maintenance Window Readiness"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0243"
parent_ids:
- "REQ-0003"
- "AD-0004"
- "ADR-0042"
created: "2026-10-14"
---

# OpenBao Maintenance Window Readiness

## Overview

An independent `iac-reviewer` readiness review of RUN-0085's maintenance
window on 2026-10-14 returned NOT READY. W0 and W3 to W7 depend on tools,
mounts and decisions that do not exist, and four defects would stop the
window part-way: the gateway path to OpenBao breaks after W4 (D1), nothing
creates the renderer token roles W3a and W5 need (D2), the restore tool likely
fails on the pinned image (D3), and W5's Prometheus `restart` cannot apply the
CA mount (D4). W4 also has no reviewed way back. The owner asked to review
and proceed and chose (AskUserQuestion) a readiness Spec that fixes the text
first and leaves tool work to later work units.

The 2026-10-22 v28 scope reuses accepted readiness work and the later HOME
execution record. It fixes the remaining W3/Finish handoff, snapshot identity,
TLS timeout and existing opt-in native regression gaps. The Task reports HOME
2.7.1 and accepted attempt `-06`; this session neither repeats those operations
nor accepts the entire deployment.

## Scope

In scope: RUN-0085's window text; the restore tool's server start; a reviewed
apply step for the renderer policies and token roles; the W3a inputs; a W3b
transfer and receipt; the Traefik, Prometheus and Gatus CA mounts; an hourly
logrotate unit; and a W4 cut-over procedure or an owner decision to fix
forward. Out of scope: running any window step, SEC01's image acceptance,
and P06. Local v28 edits authorize no controller scale/refresh, sudo cleanup,
credential/lock mutation or new risk acceptance. The user chose to retain the
existing 2026-11-15 deadline for the three D1 risks and prepare improvements;
POL-0085 remains their policy owner.

## Contracts

1. RUN-0085 states every window prerequisite and stop that the review found
   missing, and marks each unbuilt step BLOCKED.
2. The restore tool starts the pinned image's server with its configuration,
   proved by a native rehearsal on a synthetic snapshot with both images.
3. W1c applies the renderer policies and token roles with root before W3,
   through a reviewed command that leaves a value-free receipt.
4. W3a's contract, quiescence lease, renderer bundle and security receipt
   each have a reviewed producer.
5. W3b sends the W3 snapshot and receipt to R2 and records a value-free
   receipt through a reviewed tool.
6. Traefik, Prometheus and Gatus get the OpenBao CA mount at their declared
   Compose pins, with image promotion subject to each service's recorded
   SEC01 acceptance. Scoped overrides retain the observed pre-window images
   for rollback only. An hourly logrotate call shares the daily state; W4 has
   a reviewed cut-over procedure or a recorded owner decision to fix forward.

## Acceptance Criteria

1. RUN-0085 states contract 1 and the document checks pass.
2. The restore tool's native rehearsal passes on both images.
3. The W1c command and receipt pass review and a synthetic rehearsal.
4. Each W3a input producer passes review and a synthetic rehearsal.
5. The W3b tool passes review and a read-only R2 rehearsal.
6. The mount overrides, logrotate unit and W4 rollback decision pass review.
7. Independent IaC and security reviews of each unit find nothing blocking.

Residual verification under existing criteria 1/2/7 covers context/UID/original
replicas, stop/recovery and an exact six-resource Store/fresh-refresh/Application
gate, strict snapshot `entity_id == ""`, a 60-second native TLS probe with error
propagation, and default opt-in skips. Missing exact resource names, installed
versions or window-specific operator authority block only their operational
steps. Earlier criterion acceptance does not review this diff or prove execution.

## Failure Conditions

Missing window prerequisites or unbuilt input producers keep their steps
BLOCKED. A source-only server-start fix, unreviewed renderer apply or absent
R2 transfer receipt cannot establish restore or window readiness; rollback
overrides retain pre-window images without replacing SEC01 image acceptance
or executing the window.

## Related Documents

- [REQ-0003](../../01.requirements/0003-security.md)
- [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md)
- [ADR-0042](../../02.architecture/decisions/0042-openbao-unseal-method.md)
- [SPEC-0242](../0242-single-admin-openbao-custody/spec.md)
- [Plan](plan.md)
