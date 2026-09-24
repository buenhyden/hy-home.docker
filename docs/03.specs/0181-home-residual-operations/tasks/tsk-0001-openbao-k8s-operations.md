---
title: "OpenBao and hy-home.k8s Integration Operations"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0181-TSK-0001"
parent_ids:
- "SPEC-0181"
- "SPEC-0181-PLAN-0001"
created: "2026-09-24"
---

# OpenBao and hy-home.k8s Integration Operations

## Objective

Carry out the [Plan](../plan.md) for the [Spec](../spec.md): one repository
change and one owner-run OpenBao session, recorded without any token, share,
OTP or KV value.

## Inputs

- SPEC-0180 Task 0008 deferred list and live list (archived).
- hy-home.k8s handoff of 2026-09-24: Argo CD `platform-argocd-config` stays
  Degraded while `argocd-notifications-secret` cannot sync; the Kiali Grafana
  token expires 2026-12-22.
- Read-only state on 2026-09-24: OpenBao 2.6.2 initialized, unsealed, active;
  `/tmp/bao-k8s` absent at the first check, then present (`drwx------`, from
  16:31, owner preparation; contents not listed); client image `openbao/openbao:2.6.2` present;
  `secrets/backup/openbao/` absent; `argocd-notifications-secret`
  `SecretSyncedError`; the OpenBao Agent holds a RoleID but no SecretID and
  logs `no known secret ID`; Prometheus `up{job="openbao"}` is `1` with the
  metrics token that expires 2026-10-22.

## Work Log

### W8 CodeQL (2026-09-24)

Alerts #23, #24 and #26 (`py/clear-text-storage-sensitive-data` in
`tests/validation/test_compose_baseline_gates.py`) dismissed through the API
as `used in tests`, with the reason that each is a random password an isolated
rehearsal writes to a temporary directory. All three report `dismissed`.

### W1 repository change

- `infra/03-security/openbao/config/policies/operator.hcl`: create, read and
  update on `secret/data/platform/notifications`, read on its metadata.
- POL-0096 names the new operator path.
- `alert_rules.vault.yml`: `OpenBaoMetricsScrapeFailing`
  (`up{job="openbao"} == 0` for 10m, warning). promtool: 5 rules, SUCCESS.
- RUN-0085: metrics token rotation and Agent SecretID delivery commands.
- RUN-0096: Slack notifications token procedure and its When to Use row.

### Owner session (2026-09-24, about 18:45–19:12 KST)

The owner ran the client container and every command that touched a share,
OTP, token or KV value; the agent ran the host-side steps that needed no
secret input and the read-only checks, at the owner's instruction ("if you
can do it, do it"). No value was printed.

| Step | Who | Result |
| --- | --- | --- |
| 5.1a Kiali token | owner | Grafana `200` with the new token, `401` without; token `k8s-kiali-20260924`, expires 2026-12-23T09:48Z |
| 5.3 snapshot (W2) | owner | `pre-change.snap` (the Plan's name was `pre-spec-0181.snap`) |
| W7 SecretID | owner issued (18:50:35), agent delivered (18:57:26) | Agent stopped, file installed `600 100:1000`, started; `authentication successful` 1, errors 0, `sink.file: token written` |
| W5 KV | owner | `secret/platform/grafana-api` version `5` |
| 5.4 root | owner | first `R policy write` returned `403`: `/tmp/c/root` was not yet written, so `bao` used the operator login; after the ceremony, root lookup `2` |
| W3 policy | owner | `hy-home-operator` uploaded from `/s/k8s/operator.hcl`, the reviewed #256 file staged by the agent because #256 was not merged yet |
| W4 | owner | `token_explicit_max_ttl` `7200` |
| W6 token | owner | `prometheus` policy written; new token: custody lines `2`, `metrics: allowed`, `policy list: denied` |
| W6 host | agent | file replaced (`640`, group `SECRETS_GID`), Prometheus recreated, `up{job="openbao"}` `1`, `lastError` empty |
| W6 revoke | owner | old accessor revoked, lookup `old: revoked` |
| W6 custody | agent | custody file rewritten in its `key=value` form, 4 lines; new expiry 2026-10-24T10:04Z |
| 5.4.3 | owner | `root revoked`, `Started false` |
| W3 KV | owner, as operator | `secret/platform/notifications` version `1`, `current_version` `1` |
| Phase 8 | agent | tokens, SecretID, custody copies and the staged policy removed; `/tmp/bao-k8s` removed; snapshot moved to `secrets/backup/openbao/` (`700`/`600`, 53788 bytes) |
| W3 k8s | agent | `argocd-notifications-secret` force-synced: `SecretSynced True`; `platform-argocd-config` `Synced Healthy` |
| W5 k8s | agent | `kiali-grafana-auth` force-synced; Kiali still used the old token (Grafana `lastUsedAt` 10:10:06Z) because it reads the token at start; Kiali pod deleted and recreated; `/kiali/api/grafana` `200`; new token `lastUsedAt` 10:11:37Z; old token `k8s-kiali-20260923` deleted (`200`) |
| W1 runtime | agent | after #256 merged, Prometheus reloaded with SIGHUP; `OpenBaoMetricsScrapeFailing` loaded, `inactive`, health `ok` |

Deviations and lessons, now in the runbooks: the session started while #256
(the policy change) was unmerged, so the reviewed policy file was staged in
the session directory; RUN-0096 now says to start only after the policy
change is merged and pulled, and gives the root lookup check that explains a
`403`. Kiali needs a pod recreate after its token refresh. The metrics custody
file uses `key=value` lines; RUN-0085 now writes it in that form. `.snap` files
under `secrets/` were not ignored by Git; `.gitignore` now covers them.

Open after the session: the offline copy of the snapshot and the recovery
shares (owner). The owner's untracked `secrets/platform/notifications` file
(mode 664, created 16:28) was deleted by the owner after the session; the
agent confirmed only that the directory is gone.

Offline custody (owner, 2026-09-24): the owner confirmed copying
`pre-change.snap` and the recovery-share file to offline custody; the medium
was not named.

## Verification Evidence

W1 checks: promtool 5 rules SUCCESS; metadata check-changed 0 violations;
links, corpus lifecycle, operations catalog and markdownlint pass; governance
unittest OK; pre-commit passed except two local-only permission tests
(group-write bit from this worktree's umask 002 on two entrypoint scripts,
not tracked by Git), which pass after `chmod g-w`. Two independent reviews
returned APPROVE WITH FIXES; their findings are fixed in this PR. Session
results are added as each work unit runs.

Completion receipt for SPEC-0181 (criteria 1–8, Plan work units W1–W8):

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: operator grant and `OpenBaoMetricsScrapeFailing` merged in #256 with promtool, metadata, link, catalog and lifecycle checks; the grant is live (uploaded in the session) and the rule loaded `inactive`, health `ok` | [operator.hcl](../../../../infra/03-security/openbao/config/policies/operator.hcl) |
| 2 | W2 | PASS: snapshot `pre-change.snap` in `secrets/backup/openbao/` (`700`/`600`); the owner confirmed an offline copy of it and of the recovery shares (medium not named) | [POL-0021](../../../../docs/05.operations/catalog/04-data/0021-backup-and-restore/policy.md) |
| 3 | W3 | PASS: `secret/platform/notifications` `current_version` `1`, written by the operator; `argocd-notifications-secret` `SecretSynced True`; `platform-argocd-config` `Synced Healthy` | [RUN-0096](../../../../docs/05.operations/catalog/12-infra-net/0096-k8s-integration/runbook.md) |
| 4 | W4 | PASS: `token_explicit_max_ttl` `7200`; `root revoked`, `Started false` | [RUN-0096](../../../../docs/05.operations/catalog/12-infra-net/0096-k8s-integration/runbook.md) |
| 5 | W5 | PASS: `grafana-api` version `5`; after the Kiali pod recreate `/kiali/api/grafana` `200` and the new token has the latest `lastUsedAt`; old token deleted (`200`); new expiry 2026-12-23 | [RUN-0096](../../../../docs/05.operations/catalog/12-infra-net/0096-k8s-integration/runbook.md) |
| 6 | W6 | PASS: new token checks (`metrics: allowed`, `policy list: denied`), `up{job="openbao"}` `1`, old accessor revoked, custody rewritten; new expiry 2026-10-24T10:04Z | [RUN-0085](../../../../docs/05.operations/catalog/03-security/0085-openbao/runbook.md) |
| 7 | W7 | PASS: SecretID delivered within its ten minutes; `authentication successful` 1, errors 0, `sink.file: token written` | [RUN-0085](../../../../docs/05.operations/catalog/03-security/0085-openbao/runbook.md) |
| 8 | W8 | PASS: CodeQL alerts #23, #24 and #26 `dismissed`, reason `used in tests` | N/A: repository code-scanning state on GitHub |

## Review Evidence

Two independent read-only reviews ran on 2026-09-24, one on the Spec, Plan and
traceability, one on command correctness, security and honesty. Both found the
same blocking defect (the metrics token cannot look itself up, so its custody
record would be empty) and returned APPROVE WITH FIXES; all findings are fixed
here. The owner approved the Spec and Plan on 2026-09-24.

## Commit Ledger

| PR | Scope | State |
| --- | --- | --- |
| #256 | SPEC-0181 narrowed and put to review; Plan and Task; W1; SPEC-0182 draft | merged |
| #257 | SPEC-0181 Spec and Plan approved; Task ready | merged |
| #258 | SPEC-0181 active; Task in progress; session record and runbook lessons | merged |
| #259 | Completion receipt (the last change to these bodies) | merged |

The next PR completes SPEC-0181 and moves this package to
`docs/98.archive/completed/03.specs/`; it changes only lifecycle fields here.

## Rulings

| Decision | Basis | What could be wrong / cost |
| --- | --- | --- |
| Narrow SPEC-0181 to OpenBao and hy-home.k8s operations | Owner decision 2026-09-24; one session closes most items | The rest waits in SPEC-0182 |
| Reissue the Kiali token now, not in December | Owner decision; same session | The new token expires about 2026-12-23 |
| Grant notifications to the operator | Owner decision; matches the other platform entries | A compromised operator session could replace the Slack token |

## Deferred Items

None. Every other SPEC-0180 residual is in SPEC-0182. The next metrics token
rotation is due before 2026-10-24 and the next Kiali token before 2026-12-23;
`OpenBaoMetricsScrapeFailing` fires if the metrics token lapses.
