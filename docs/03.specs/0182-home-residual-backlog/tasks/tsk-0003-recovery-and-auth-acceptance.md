---
title: "Recovery and Authentication Acceptance"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0182-TSK-0003"
parent_ids:
- "SPEC-0182"
- "SPEC-0182-PLAN-0001"
created: "2026-09-25"
---

# Recovery and Authentication Acceptance

## Objective

Carry out W7–W12 of the [Plan](../plan.md) and hold the completion receipt.

## Inputs

Read-only investigation of 2026-09-25:

- **PITR:** RUN-0021 step 5 (`runbook.md:107-148`); only the synthetic
  `BackupRestoreRehearsalTests` ran (2026-09-22).
- **Isolated restores:** MLflow RUN-0088 (`:56-63`) never rehearsed;
  JupyterLab RUN-0089 rehearsed on an empty work directory; CDC RUN-0036 steps
  1–3 rehearsed, 4–6 not (they would use the production slot).
- **Resources:** no procedure or data; cAdvisor, node-exporter and
  dcgm-exporter are scraped.
- **SSO:** the static route matrix is GDE-0079 (`guide.md:419-446`) and
  `RouteAuthContractTests`; 22 live routers carry `sso-errors,sso-auth`; no
  behavioural matrix exists.
- **Offsite and unseal:** POL-0021 control 1 (`policy.md:63-68`) states no
  offsite recovery; OpenBao uses manual Shamir unseal (RUN-0085:37-53);
  auto-unseal was only deferred in the Vault-era ADR-0018.
- **Cold start and reboot:** no runbook; the unseal and the single-use Agent
  SecretID are the known blockers.
- **Entry-closed:** SEC-002 (`secrets/SENSITIVE_ENV_VARS.md.example:196`) is
  the metrics token rotated in SPEC-0181, expiry 2026-10-24, alert
  `OpenBaoMetricsScrapeFailing`; secret value files by mode: 101 at `0640`, 5
  at `0600`, 1 at `0400`, `rootCA.pem` at `0644`, none at `0664`; Renovate
  units in `/etc/systemd/system` are regular `0644` copies identical to
  `infra/09-tooling/renovate/systemd/`, timer enabled.

## Work Log

Pending.

## Verification Evidence

Pending.

## Review Evidence

Two independent read-only reviews ran on 2026-09-25, one on specification,
plan and traceability, one on operational safety and feasibility. Both
returned APPROVE WITH FIXES. The blocking finding was that stopping
`mng-valkey` for the SSO outage check would also stall n8n and Airflow; the
check now disconnects only OAuth2 Proxy. The other findings (run order W6
before W4, `mng-pg` dump permissions, rollback tag and CDC checks, SeaweedFS
recreate order and backup window, disposal preconditions, root-level removal,
the registry backup directory, Restic retention of deleted data, criterion
wording for CDC steps, RPO/RTO, ADRs, owner-declined rows and retirements)
are applied in the same PR. The owner's approval follows.

## Commit Ledger

| PR | Scope | State |
| --- | --- | --- |
| #261 | SPEC-0182 to review; Plan and three Tasks | merged |
| #262 | SPEC-0182 Spec and Plan approved; Tasks ready | merged |
| this PR | SPEC-0182 active; Task 0001 in progress | open |

## Rulings

See the Plan.

## Deferred Items

None yet.
