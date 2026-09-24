---
title: "OpenBao and hy-home.k8s Integration Operations Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0181-PLAN-0001"
parent_ids:
- "SPEC-0181"
created: "2026-09-24"
---

# OpenBao and hy-home.k8s Integration Operations Plan

## Objective

Close the eight [Spec](spec.md) criteria with one repository change and one
owner-run OpenBao session. [Task 0001](tasks/tsk-0001-openbao-k8s-operations.md)
records preconditions, results and the completion receipt.

## Dependencies

- The repository change (W1) merges before the session, because the session's
  client container mounts the policies from the main checkout.
- OpenBao unsealed and healthy; the OIDC operator can log in; two unseal shares
  are available for the temporary root.
- The owner has a Slack bot token (`xoxb-`) and an offline medium.
- The hy-home.k8s side can force two ExternalSecret refreshes.

## Execution Sequence

The owner runs every step that touches a token, share, OTP or KV value, from
the main checkout, following the
[hy-home.k8s integration runbook](../../05.operations/catalog/12-infra-net/0096-k8s-integration/runbook.md)
(RUN-0096) and the [OpenBao runbook](../../05.operations/catalog/03-security/0085-openbao/runbook.md)
(RUN-0085). The agent runs the read-only checks before and after.

1. W1: Repository change: the operator policy grants
   `secret/platform/notifications`; the `OpenBaoMetricsScrapeFailing` alert
   fires when the OpenBao scrape is down for ten minutes; RUN-0085 gains the
   metrics token and SecretID commands and RUN-0096 the Slack token procedure.
2. W2: Snapshot and custody: after the 5.3 operator login, save
   `/s/k8s/pre-spec-0181.snap`; at the end move it to owner-only
   `secrets/backup/openbao/` (RUN-0096 Phase 8) and copy it and the recovery
   shares to the offline medium.
3. W3: Notifications: host `slack.token` (umask 077, editor); in the root
   session only `R policy write hy-home-operator /policies/operator.hcl`;
   after 5.4.3 the operator runs the RUN-0096 Slack token commands (`kv put`
   and the `current_version` read), which exercises the new grant; ESO
   refresh of `argocd-notifications-secret`, then Argo CD
   `platform-argocd-config` Healthy.
4. W4: Token role and root: `R read -field=token_explicit_max_ttl
   auth/token/roles/k8s-bootstrap` reads `7200`; if not, run the 5.4.2
   `R write auth/token/roles/k8s-bootstrap …` line and read again while root
   is open. The root part ends with 5.4.3 (`root revoked`, `Started false`).
5. W5: Kiali: 5.1a issues the new token on the host before the container
   starts; the operator updates `secret/platform/grafana-api`; ESO refresh of
   `kiali-grafana-auth`; the cluster owner confirms Kiali reaches Grafana
   without an authentication error; the old `k8s-kiali` token is deleted in
   Grafana.
6. W6: Metrics token: in the root session, RUN-0085 step 5 commands issue and
   check the new token; the host replaces the file and recreates only
   Prometheus; `up{job="openbao"}` is `1`; the old token is revoked by
   accessor and the custody file replaced.
7. W7: Agent SecretID: the operator issues it (RUN-0085 delivery commands);
   within ten minutes the host stops only the Agent, installs the file and
   starts it; no `no known secret ID` lines follow.
8. W8: CodeQL: alerts #23, #24 and #26 dismissed as used in tests (done
   2026-09-24 before this Plan).

Session order (two host terminals: A holds the `-it` client container, B runs
host commands):

1. B: 5.1 directory only (`umask 077; mkdir -p /tmp/bao-k8s`; the k3d CA is
   not needed), `slack.token` in an editor, then 5.1a (`200`, `401`).
2. A: 5.2 container, 5.3 login and `pre-spec-0181.snap` (W2).
3. A: W7 SecretID; B: its host install within ten minutes of the write.
4. A: W5 `kv put secret/platform/grafana-api`.
5. A: 5.4 root: `R policy write hy-home-operator` (W3), W4 read, W6 token
   and checks; B: W6 file replace, Prometheus recreate and `up` query; A: old
   accessor revoke; then 5.4.3.
6. A: W3 operator `kv put secret/platform/notifications`; exit.
7. B: Phase 8 cleanup, the metrics custody file, offline copies (W2).
8. Cluster side: ESO refreshes, Argo CD and Kiali checks; Grafana: delete the
   old `k8s-kiali` token.

## Risk and Rollback

- A failed snapshot stops the session before any change.
- A new metrics token that fails its checks is revoked by accessor; the old
  file stays and Prometheus is not recreated.
- A SecretID that expires before delivery is simply reissued; the Agent stays
  as it is now, without a working token and rendering nothing new.
- A wrong KV value is replaced with a new version; the previous version stays
  readable for rollback.
- If root revocation fails, stop and revoke by accessor before anything else.

## Verification

Before the session the agent checks OpenBao health, the absence of
`/tmp/bao-k8s`, the client image and the mounted files, all read-only. After
it the agent checks the Phase 8 cleanup, file modes, the Prometheus target,
Agent logs and ExternalSecret status, never reading a value. Repository
checks: promtool on the rule file, metadata, links, operations catalog,
corpus lifecycle and pre-commit.

## Rulings

- One session, with the root part as short as possible: root only for the
  operator policy write, the role read and the metrics token; the
  notifications entry is written by the operator afterwards.
- The notifications grant mirrors the existing `prometheus-api` and
  `grafana-api` grants: create, read and update on data, read on metadata.
- The metrics alert detects a lapsed token after the fact; the 720h TTL and
  the recorded expiry are the before-the-fact control.
