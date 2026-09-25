---
title: "Recovery and Authentication Acceptance"
version: "0.5.0"
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
- 2026-09-25 W10: options memos drafted as proposed ADR-0041 (offsite backup
  target) and ADR-0042 (OpenBao unseal method), each with the decision
  pending the owner. Inputs: journal `repository sizes` state 429–777 MiB
  (5 GiB budget), host 1 MiB; OpenBao `2.6.2` built-in seals per the official
  2.6.x seal documentation.
- 2026-09-25 W9 (agent part): the SSO behavioural matrix was added to
  GDE-0079 and its no-cookie probes were run against the live gateway;
  results are under Verification Evidence. The owner rows (user outside
  `/admins`, logout, role removal, native OIDC signed in) remain pending
  owner.
- 2026-09-25 W9 Valkey disconnect (owner approved): `oauth2-proxy` was
  detached from `mng_data_net` 14:07:19–14:07:33Z; requests, including one
  with a forged session cookie, were refused (401), so the session store
  fails closed. It was reconnected with alias `oauth2-proxy` and is healthy.
- 2026-09-25 W9 finding: a no-cookie browser request to an SSO route showed
  oauth2-proxy's "Found." link page instead of redirecting, because browsers
  ignore `Location` on a 401. Fixed by rewriting 401 to 302 in the
  `sso-errors` middleware (#274).

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

W9, SSO no-cookie probes (criterion 9, agent rows), 2026-09-25. Read-only
GETs from the host to the gateway at `192.168.0.13:443`, no credentials or
cookies; routers read from the Traefik labels of the running `hy-home-infra`
containers (the file provider declares no routers). 19 live routers carry
`sso-auth` (the Inputs counted 22 in the earlier investigation).

| Probe | Routers | Result |
| --- | --- | --- |
| GET `/` without a cookie | `alertmanager`, `alloy`, `cadvisor`, `comfyui`, `flower`, `jupyter`, `kafka-connect`, `kafka-rest`, `loki`, `mlflow`, `n8n`, `ollama`, `prometheus`, `pyroscope`, `qdrant`, `redisinsight`, `redisinsight-static` (`/favicon.ico`), `schema-registry`, `tempo` | pass: all `401` with `Location` to the Keycloak authorization endpoint of `hy-home.realm`, `client_id=home-proxy-client`, callback `https://auth.hy.home.arpa/oauth2/callback`, S256; no upstream content |
| API client without credentials | `alloy` with `Accept: application/json`, `prometheus` `/api/v1/status/buildinfo` | pass: `401` |
| Native OIDC without a session | `open-webui`, `grafana`, `airflow`, `gatus`, `kafka-ui`, `dozzle`, `openbao` | pass: each API path refuses (`401`, OpenBao `403`) and each login path reaches Keycloak or the app login page; details in GDE-0079 |

Finding: the SSO chain answers `401` with a `Location` header, not `302`,
so a browser renders the one-link "Found" page instead of redirecting. Access
is refused either way; the owner confirms the browser experience during the
logout row.

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
| #269 | W12 closures; Task 0003 in progress | merged |
| #272 | W10 options memos ADR-0041 and ADR-0042 | merged |
| this PR | W9 SSO matrix and no-cookie probes | open |

## Rulings

See the Plan.

## Deferred Items

None yet.
