---
title: "Recovery and Authentication Acceptance"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
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

- 2026-09-25 W12: the retired and entry-closed items were re-checked
  against the live host and `main`; results are under Verification Evidence.

## Verification Evidence

W12, retired and entry-closed items (criterion 12):

| Item | Disposition | Reason and evidence |
| --- | --- | --- |
| Terrakube Keycloak client and API ForwardAuth removal | Retired until `iac` activation | The decision (dedicated public client `home-terrakube`, drop ForwardAuth, verify audience and RBAC) is recorded in `infra/09-tooling/terrakube/docker-compose.yml` beside the router and in GDE-0079; `iac` is outside HOME |
| CI alignment follow-ups (remote branch protection, workflow cleanup, pre-commit update ownership, digest maintenance, caching, non-gating workflow retention) | Retired while CI passes steadily | CodeQL 15 of 15 successful on `main`; CI Quality Gates on `main` succeeded on each completed run from `a599a5fca` through `e229ec9d0`, and the others were cancelled by newer pushes. `b8ac86c64` failed only on the end-of-file fixer for `.claude/settings.json`, an owner-held file |
| SEC-002 | Closed at entry | The OpenBao metrics token that SPEC-0181 rotated (expiry 2026-10-24); `OpenBaoMetricsScrapeFailing` is loaded with health `ok` and state `inactive` |
| Secret value files at mode 664 | Closed at entry, re-verified | After W2 the new AI-009 file was created at `664`; the owner set it to `640`. Now 102 at `0640`, 4 at `0600`, 1 at `0400` and `rootCA.pem` at `0644`; none at `0664` (only `.gitkeep` placeholders are) |
| Renovate host units | Closed at entry, re-verified | `hyhome-renovate.service` and `.timer` in `/etc/systemd/system` are regular `0644` files identical to `infra/09-tooling/renovate/systemd/`; the timer is enabled |
| compose-core-readiness Vault rig | Kept as a generic fixture | Owner decision; its override header states it is a self-contained harness fixture independent of production OpenBao (#264) |
| Open WebUI vector store | Kept local | `VECTOR_DB` is unset, so Open WebUI uses its local store; the unused `VECTOR_DB_URL` and the docs claiming Qdrant were corrected (#264), and the recreated container has no `VECTOR_DB*` variable |

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
| #263 | SPEC-0182 active; Task 0001 in progress | merged |
| this PR | W12 closures; Task 0003 in progress | open |

## Rulings

See the Plan.

## Deferred Items

None yet.
