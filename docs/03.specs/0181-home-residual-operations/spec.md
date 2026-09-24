---
title: "OpenBao and hy-home.k8s Integration Operations Specification"
version: "0.3.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0181"
parent_ids:
- "REQ-0027"
created: "2026-09-24"
---

# OpenBao and hy-home.k8s Integration Operations Specification

## Overview

Close the OpenBao and hy-home.k8s integration operations that SPEC-0180 left
as residual risk. Most of them need one owner-run OpenBao session. The owner
narrowed this package on 2026-09-24; every other SPEC-0180 residual moved to
[SPEC-0182](../0182-home-residual-backlog/spec.md). The directory keeps its
first slug because the archived SPEC-0180 links to it.

## Boundaries and Inputs

Inputs are SPEC-0180 Task 0008's deferred list and live list, the
hy-home.k8s handoff of 2026-09-24, the CodeQL results on #250, the OpenBao
subject (GDE/POL/RUN-0085), the hy-home.k8s integration subject
(GDE/POL/RUN-0096) and POL-0021 for backup custody.

In scope:

1. A fresh OpenBao raft snapshot in offline custody under POL-0021 (none
   exists on the host), and offline custody of the recovery shares.
2. The hy-home.k8s Argo CD notifications entry
   `secret/platform/notifications` (`slack_token`), with an operator policy
   grant so that a later replacement needs no root session.
3. Confirmation that the `k8s-bootstrap` token role caps tokens at `7200`
   seconds (RUN-0096 Session 3).
4. A reissued Kiali Grafana token in `secret/platform/grafana-api` before the
   current one expires on 2026-12-22, with the old token deleted.
5. The Prometheus metrics token: an alert when the OpenBao scrape fails, and a
   rotation before the current token expires on 2026-10-22.
6. A fresh OpenBao Agent SecretID, so the Agent renders again.
7. Three CodeQL `py/clear-text-storage-sensitive-data` alerts on test
   rehearsal passwords, dismissed as used in tests.

Out of scope: everything in SPEC-0182, hy-home.k8s repository changes, and
the manual unseal versus auto-unseal decision.

Live mutation, credential work and remote changes each need their own
approval. The owner runs every command that touches a token, share, OTP or
KV value; the agent never requests, types or prints one.

## Behavior Contract

Each item closes only with evidence of its kind: a merged change with its
checks for repository work, a live result stated as names, statuses, counts
and versions for runtime work, and an owner statement for offline custody.
A failed or unexecuted step is never recorded as done. Snapshot contents,
tokens, shares and KV values never enter output, diffs, the Task or a PR.

## Technical Approach

Repository changes merge first: the operator policy grant, the metrics scrape
alert and the updated procedure. The owner then runs one OpenBao session from
the main checkout in the order the Plan gives: the operator steps, then one
temporary root session for the steps the operator policy does not allow,
ending with root revocation; the notifications entry is written by the
operator after the policy update. The agent checks preconditions and results
read-only and records them in the Task.

## Interfaces and Data

OpenBao KV `secret/platform/notifications` and `secret/platform/grafana-api`,
the `hy-home-operator` and Prometheus metrics policies, the `k8s-bootstrap`
token role, the renderer AppRole, `secrets/security/openbao_token.txt`,
`secrets/backup/openbao/`, the Prometheus `openbao` job and its alert rules,
and the Grafana `k8s-kiali` service account.

## Failure Modes and Guardrails

Do not continue past a failed snapshot. Do not widen an OpenBao policy beyond
the paths an item needs. Revoke the temporary root before the session ends and
verify `Started false`. If a new metrics token fails validation, keep the old
file and revoke the new token by accessor. Keep `/tmp/bao-k8s` owner-only and
remove it when the session ends.

## Acceptance Contract

1. The operator policy grants the notifications path, and the Prometheus
   OpenBao scrape has a failure alert; both merge with their checks recorded.
2. A snapshot taken in the session sits in owner-only `secrets/backup/openbao/`,
   and the owner records a copy of it and of the recovery shares in offline
   custody.
3. `secret/platform/notifications` exists, the hy-home.k8s
   `argocd-notifications-secret` ExternalSecret reports synced and Argo CD
   `platform-argocd-config` reports Healthy.
4. The `k8s-bootstrap` role reads `7200` and the temporary root is revoked.
5. `secret/platform/grafana-api` holds a new token, Kiali reads Grafana with
   it after an ESO refresh, and the old token is deleted.
6. Prometheus scrapes OpenBao with a new metrics token, the old token is
   revoked, and its new expiry is recorded.
7. The OpenBao Agent consumed a fresh SecretID and renders again.
8. The three CodeQL alerts are dismissed with a recorded reason.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0031 Home and Development Host](../../02.architecture/descriptions/0031-home-development-host.md)
- [SPEC-0180](../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md)
- [SPEC-0180 Task 0008](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0008-storage-security-lakehouse-convergence.md)
- [SPEC-0182](../0182-home-residual-backlog/spec.md)
- [Plan](plan.md)
- [Task](tasks/tsk-0001-openbao-k8s-operations.md)
- [OpenBao runbook](../../05.operations/catalog/03-security/0085-openbao/runbook.md)
- [hy-home.k8s integration runbook](../../05.operations/catalog/12-infra-net/0096-k8s-integration/runbook.md)

## Open Questions

None blocking. The offline custody medium is the owner's choice and is
recorded by name only.

## Operational Impact

The session recreates Prometheus (metrics token) and restarts only the
OpenBao Agent (SecretID). The k8s side refreshes two ExternalSecrets.
