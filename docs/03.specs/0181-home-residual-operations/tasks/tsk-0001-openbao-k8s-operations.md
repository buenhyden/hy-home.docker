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

## Verification Evidence

W1 checks: promtool 5 rules SUCCESS; metadata check-changed 0 violations;
links, corpus lifecycle, operations catalog and markdownlint pass; governance
unittest OK; pre-commit passed except two local-only permission tests
(group-write bit from this worktree's umask 002 on two entrypoint scripts,
not tracked by Git), which pass after `chmod g-w`. Two independent reviews
returned APPROVE WITH FIXES; their findings are fixed in this PR. Session
results are added as each work unit runs.

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
| this PR | SPEC-0181 active; Task in progress for the owner session | open |

## Rulings

| Decision | Basis | What could be wrong / cost |
| --- | --- | --- |
| Narrow SPEC-0181 to OpenBao and hy-home.k8s operations | Owner decision 2026-09-24; one session closes most items | The rest waits in SPEC-0182 |
| Reissue the Kiali token now, not in December | Owner decision; same session | The new token expires about 2026-12-23 |
| Grant notifications to the operator | Owner decision; matches the other platform entries | A compromised operator session could replace the Slack token |

## Deferred Items

None yet.
