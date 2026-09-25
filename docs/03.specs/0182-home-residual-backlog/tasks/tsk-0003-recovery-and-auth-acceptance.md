---
title: "Recovery and Authentication Acceptance"
version: "0.6.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-26"
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
- 2026-09-25 W9 after #274: the fix is live (the Traefik file provider reloaded
  on pull, 15:06Z). No-cookie browser requests to `prometheus`, `alertmanager`
  and `n8n` now get `302` to Keycloak. `prometheus` `/api/v1/...` still
  answers `401`; `alloy` with `Accept: application/json` now gets `302` with
  a redirect page and no upstream content, so it is still refused. The `403`
  page for a user outside `/admins` is confirmed in the owner row.
- 2026-09-25 W7 (owner approved): three restore rehearsals ran in isolation
  14:56–15:14Z and passed; results under Verification Evidence. JupyterLab
  has no files in its production work directory, so there is no real content
  to restore; the owner accepted the 2026-09-22 synthetic-notebook rehearsal
  (RUN-0089) as the W7 evidence. All `w7-` containers, networks, volumes and
  scratch were removed and verified; production services stayed healthy.
- 2026-09-25 W10: the owner accepted ADR-0041 (Cloudflare R2) and ADR-0042
  (auto-unseal deferred, manual Shamir kept) in #276. The R2 implementation
  (#277) was put on hold by the owner before setup, but an agent merge loop
  that kept running after it was stopped merged it; #279 reverts it. It is
  re-landed with the owner's R2 setup.
- 2026-09-25 W11: the cold start and reboot runbook is RUN-0098 (#278), in the
  manual-unseal order of ADR-0042. Docker service and socket are enabled and
  the five `k3d-hyhome-*` containers use `unless-stopped`. The supervised
  reboot is pending owner.

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

W7, restore rehearsals (criterion 7), 2026-09-25, each on an `--internal`
network with no route to production and scratch on the data disk:

| Rehearsal | Window (UTC) | Recovery point | Counts vs production | Elapsed vs POL-0021 | Result |
| --- | --- | --- | --- | --- | --- |
| RUN-0021 step 5, PITR from the real pgBackRest repository | 14:56:12–15:04:30 | Set `20260922-073354F_20260924-183526D`, WAL through `000000010000000300000080`, stopped at the target `2026-09-25 14:55:25+00`, new timeline 2 | `mlflow.experiments` 2=2, `mlflow.runs` 2=2, `analytics.hyhome_dbt_connectivity` 1=1, `debezium_heartbeat.heartbeat` 1=1 | about 8m18s against RTO 4h; no loss at the target, inside the 5 min RPO | pass |
| RUN-0088, MLflow | 15:06:40–15:08:05 | Read-only `pg_dump` of `mlflow` at 15:06:56 | `experiments` 2=2, `runs` 2=2, `metrics` 1=1, `params` 1=1, `tags` 8=8; artifacts 2=2 objects, SHA-256 equal | about 1m25s; no POL-0021 row | pass |
| RUN-0089, JupyterLab | not run | production work directory empty | none | none | owner accepted the 2026-09-22 synthetic rehearsal |
| RUN-0036 steps 4–6, CDC | 15:10:45–15:14:02 | Disposable source and slot `w7_hyhome_app_slot`, final `confirmed_flush_lsn` `0/1C47EE0`, `wal_status=reserved` | 3 rows (1 snapshot, 2 streamed); a row written while paused arrived once after resume: no duplicates, no gaps | about 3m17s; no POL-0021 row | pass |

Deviations: MLflow was dumped read-only instead of stopping `mlflow`
(RUN-0088 step 1), with a local artifact root and the two production objects
compared by hash. CDC used JSON converters instead of Avro with Schema
Registry; lifecycle, pause/resume and idempotency do not depend on the
converter. The live `hyhome-app-postgres` connector and `hyhome_app_slot`
were not touched.

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
| #274 | SSO `401` to `302` rewrite | merged |
| #275 | W9 SSO matrix and no-cookie probes | merged |
| #276 | ADR-0041 and ADR-0042 accepted | merged |
| #277 | R2 offsite copy | merged against the owner's hold |
| #278 | W11 RUN-0098 cold start and reboot runbook | merged |
| #279 | Revert #277 until the R2 setup | open |
| this PR | W7, W9, W10 and W11 records | open |

## Rulings

See the Plan.

## Deferred Items

| Item | Owner | Trigger or date |
| --- | --- | --- |
| R2 setup (bucket, lock, token, secrets, `init`) and re-landing #277 | @buenhyden | When the owner is ready; RUN-0021 §8 comes back with it |
| W9 owner rows: user outside `/admins`, logout, role removal, native OIDC signed in | @buenhyden | Before the completion receipt |
| W11 supervised reboot and the RUN-0098 rehearsal record | @buenhyden | After fresh backups and `restic check` |
| W8 queries over 2026-09-26 to 10-02 | agent | 2026-10-03 |
| RUN-0021 steps 5–6 put `scratch` in `mktemp -d` on the system disk; RUN-0088 step 1 has no rehearsal path that leaves `mlflow` running | agent | Next RUN-0021 or RUN-0088 edit |
