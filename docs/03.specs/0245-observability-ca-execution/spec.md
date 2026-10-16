---
title: "Observability CA Execution"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0245"
parent_ids:
- "REQ-0003"
- "AD-0003"
- "ADR-0042"
created: "2026-10-16"
---

# Observability CA Execution

## Overview

The owner authorized backup and isolated-restore validation followed by a
bounded CA application and recreation for the current host's Prometheus and
Gatus services. Earlier observation established that neither service had the
declared CA mount applied at runtime. Prometheus remains on its observed 3.14
rollback image; no version upgrade is included. Gatus needs a smallest-delta
image from its exact current immutable identity that copies the tracked
CA-aware entrypoint, because the current entrypoint cannot be trusted to
establish the required CA bundle.

SPEC-0243 remains the broader OpenBao maintenance-window readiness package.
This package does not open an OpenBao window, render secrets, unseal OpenBao,
or change any service outside the two named observability services.

## Scope

In scope:

- preflight identification of the current host, Compose selection, declared
  source, running image, persistent data boundary, and CA mount for
  `prometheus`, then `gatus`;
- one service at a time for service-specific consistent backup and isolated
  restore rehearsal; both services pass those recovery gates before either CA
  application or recreation, which then proceeds Prometheus before Gatus;
- preserving Prometheus on the observed 3.14 rollback image;
- building a Gatus delta from the exact current immutable image identity,
  copying only the reviewed tracked CA-aware entrypoint without a network or
  pull, recording a unique tag and immutable image ID/digest, and retaining
  the old image identity for rollback;
- sanitized durable Task receipts containing identities, checksums, exits,
  health results, and recovery decisions; and
- service-specific post-recreate health and CA-consumer checks.

Out of scope:

- an OpenBao maintenance window, OpenBao unseal, secret reads, renderer-role
  operations, certificate/key rotation, or CA content capture;
- a Prometheus 3.15 upgrade, manual TSDB/WAL manipulation, volume deletion,
  data migration or replacement, or an unreviewed image pull;
- recreating a service before its own backup and isolated restore pass;
- any unlisted service, stack-wide restart, deployment, or restoration of a
  production data volume; and
- accepting or altering SPEC-0243's draft criteria or its Task.

## Contracts

1. The Task identifies the exact current host target and each service's
   Compose files, source commit, running image identity, declared image,
   persistent-data boundary, and CA mount without retaining credentials,
   secrets, raw configuration, or database contents.
2. Prometheus remains on the observed 3.14 image. Before its recreation, a
   reviewed service-specific procedure produces a consistent backup and proves
   that backup in an isolated, egress-disabled restore environment. A source
   render or a volume copy alone is not sufficient.
3. Before Gatus recreation, a reviewed service-specific procedure produces a
   consistent SQLite backup and proves it in an isolated, egress-disabled
   restore environment. The rehearsal does not attach production data,
   credentials, routes, or networks.
4. Gatus is built only as a reviewed minimal delta: `FROM` the exact current
   running immutable image identity and `COPY` the tracked CA-aware entrypoint,
   with no network or pull and no binary change. The Task records its unique
   tag and immutable image identity, preserves the previous image identity for
   rollback, and stops if the image or entrypoint identity differs from the
   reviewed input.
5. A recreation occurs only after both services' backup and isolated restore
   gates pass, one service at a time in Prometheus-then-Gatus order, with the
   exact reviewed Compose selection. The Task records health and CA-consumer
   results separately and stops before the next service on any non-PASS result.
6. A failure leaves the production data volume untouched. The Task records the
   stop state and uses only the reviewed service-specific rollback path; no
   generic restart, deletion, or restore is inferred.
7. Independent operational, security, and data-recovery review plus selected
   source/document checks pass before each execution gate is accepted.

## Acceptance Criteria

1. The Task records the exact two-service target and value-free preflight
   identity for the current host.
2. Prometheus has a reviewed consistent backup and isolated restore rehearsal
   that passes before any Prometheus recreation, while retaining the observed
   3.14 image.
3. Gatus has a reviewed consistent SQLite backup and isolated restore rehearsal
   that passes before any Gatus recreation.
4. The Gatus delta image is traceable to the exact current running immutable
   base, the reviewed tracked entrypoint, a unique tag, immutable image
   identity, and a retained prior-image rollback identity.
5. Prometheus then Gatus are recreated only after criteria 2 and 3 both pass,
   and each has separate health and CA-consumer PASS evidence.
6. Any failed gate preserves production data and records an explicit stop or
   reviewed rollback result.
7. Independent operational, security, and recovery reviews plus selected
   checks pass without secret or data-payload exposure.

## Failure Conditions

Missing preflight identity, unverified backup consistency, an unproved isolated
restore, unknown Gatus image/entrypoint provenance, a non-PASS health result,
or unavailable approved isolation keeps the next service action `NOT_RUN`.
No criterion authorizes manual data manipulation, deletion, migration, or
replacement; a generic restart, source upgrade, secret read, OpenBao operation,
or workaround outside the reviewed procedure is also excluded. Ordinary
application writes during the reviewed service stop/start are not a data
replacement claim.

## Related Documents

- [REQ-0003](../../01.requirements/0003-security.md)
- [AD-0003](../../02.architecture/descriptions/0003-security-architecture.md)
- [ADR-0042](../../02.architecture/decisions/0042-openbao-unseal-method.md)
- [SPEC-0243](../0243-openbao-window-readiness/spec.md)
- [Prometheus Runbook](../../05.operations/runbooks/07-observability/0045-prometheus.md)
- [Gatus Runbook](../../05.operations/runbooks/07-observability/0087-gatus.md)
- [Plan](plan.md)
- [Task](tasks/tsk-0001-observability-ca-execution.md)
