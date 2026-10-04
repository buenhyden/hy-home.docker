---
title: "Recovery and Authentication Acceptance"
version: "0.7.14"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-04"
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
- 2026-09-29 lifecycle review: criteria 8, 9, 10 and 11 stay open. W8's
  window ends 2026-10-02; the W9 owner rows have no result; ADR-0041 chose R2,
  but its implementation was reverted in #279 and not re-landed
  (`infra/09-tooling/restic/README.md` states no R2 path exists); the
  RUN-0098 Verification Record has no rehearsal row. The RUN-0021 and
  RUN-0088 deferred item was resolved in #281.
- 2026-09-29 W9: the owner completed the browser checks the agent could not
  make: Dozzle sign-in, and Grafana, Open WebUI and OpenBao signed in as an
  `/admins` user. Every W9 row now has a result.
- 2026-09-30 W8 handoff for 2026-10-03. Window: 2026-09-26T00:00+09:00
  (`1790348400`) to 2026-10-03T00:00+09:00 (`1790953200`), 168 h. Prometheus
  has no samples 2026-09-26 11:05–18:10 and 2026-09-27 11:55–13:25 KST; state
  the gaps with the figures. Run each query with
  `docker exec infra-prometheus wget -qO- 'http://localhost:9090/api/v1/query?time=1790953200&query=<urlencoded>'`,
  where `C` is `max by (name)(rate(container_cpu_usage_seconds_total{name!=""}[5m]))`
  and `M` is `max by (name)(container_memory_working_set_bytes{name!=""})`
  (2026-10-04 correction: deduplicate overlapping container/target identities before aggregating):
  - containers: `quantile_over_time(0.95, (C)[168h:5m])`,
    `max_over_time((C)[168h:5m])`, and the same two for `M`;
  - host: `1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))` and
    `1 - node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes`, each
    as p95 and max over `[168h:5m]`;
  - GPU: `avg(DCGM_FI_DEV_GPU_UTIL)` p95 and max, `sum(DCGM_FI_DEV_FB_USED)`
    max;
  - disk growth: used bytes (`node_filesystem_size_bytes - node_filesystem_avail_bytes`,
    `fstype!~"tmpfs|overlay|squashfs"`) minus the same `offset 168h`.
  SPEC-0193 W7 sets its limits and alert thresholds from these figures.
- 2026-09-30 W11 stage 0 (owner started the supervised reboot; R2 held):
  `hyhome-backup.sh` run as its unit (`User=hyunyoun`, repo root, no env
  file) 09:37:52–09:39:07 KST, rc 0: pgBackRest differential
  `20260926-185114F_20260930-003754D`, Restic state snapshot `9753742f` and
  host snapshot `6236fc73`, `restic check` no errors in both, state 1783 MiB
  of 5 GiB; backup-age metric 47 s. Before the reboot: `docker.service` and
  `docker.socket` enabled, the five `k3d-hyhome-*` containers
  `unless-stopped` and running, 54 containers running with none unhealthy
  (names saved outside the repo for the comparison), OpenBao unsealed
  (Shamir 2 of 3), `openbao-agent` healthy, 44 GiB free.
- 2026-09-30 W11 supervised reboot (owner): boot 09:44:30 KST; stages 1-5
  pass as the RUN-0098 Verification Record shows (all 54 containers back,
  healthy by 10:03:53; owner unseal and `home-admin` login done before
  10:10). Open: stage 6 SecretID delivery (the agent logs no SecretID to
  read), and ESO `vault-backend` revalidation after the unseal.
- 2026-09-30 SecretID runbook review (owner request): RUN-0098 stage 6
  pointed at RUN-0085 "delivery commands" that did not exist; no Spec,
  Task or runbook ever recorded them. The agent log shows it authenticated
  once (2026-09-24 09:57Z), renewed until 2026-09-25, lost its token at
  2026-09-26 16:51Z (`lifetime watcher done`) and failed 463 times since,
  while its `test -s token` healthcheck stayed healthy. RUN-0085 now has a
  Renderer SecretID Delivery procedure built from checked facts (no host
  `bao`, the RUN-0096 client pattern, agent uid 100 can write its volume,
  `-field` prints without a newline, token helper `$HOME/.vault-token`,
  backoff about 4 minutes), a detection command, and the known limit that
  every token expiry needs a new delivery. RUN-0098 stages 3 and 6 and its
  recovery point to it. Automatic re-login is a security design change
  left to a Spec; ADR-0042 assumed delivery only at restarts.
- 2026-09-30 W11 stage 6: the owner ran the new RUN-0085 delivery; the
  Agent authenticated at 10:30:29 KST. ESO had revalidated at 10:11:17. The
  rehearsal is complete (criterion 11).
- 2026-09-30 W10 R2 re-landing (owner: "R2 setup and re-landing.
  cloudflare"): #279's revert is reverted onto the current tree. Code applied
  as #277 wrote it; the orchestrator runs the offsite step before the
  SPEC-0192 success metric, so only a run that also copied offsite records
  success. GDE, POL and RUN-0021 moved since #277, so its text was carried
  into the current Korean documents (RUN-0021 step 8). The inventory row,
  the Grafana coverage row and the secret-contract counts follow the new
  job and its three secrets; `.env` gained the two empty keys. The state set
  now also holds the pgBackRest repository (524 MiB of the 1769 MiB state
  directory today), which grows the state budget faster; the 2026-10-03 W8
  disk figures cover it. Owner steps (RUN-0021 8.1): the bucket, five lock
  rules, the bucket-scoped token, BKP-004/005, the two `.env` values.
- 2026-09-30 W10 R2 free tier (owner: keep Cloudflare from billing). The
  official pricing and billing pages (checked 2026-09-30): no hard spending
  cap; budget alerts only email (Pay-as-you-go accounts); the free tier is
  per account, Standard storage only, storage billed as the monthly average
  of daily peaks; `DeleteObject` is free. Operations stay in the thousands a
  month, so storage is the only exposure. `copy` now reports the stored
  size, the orchestrator records `hyhome_backup_offsite_repo_bytes`, and
  `HyhomeOffsiteRepoNearFreeTier` fires above 8 GB; a confirmed owner-run
  `forget-prune` keeps 30 days plus 12 monthly snapshots (RUN-0021 8.5, 8.6).
  `index/` left the lock list, because a locked stale index could make a
  later copy skip data that prune had removed. Checked with a stub `restic`
  (size line, refusal without confirmation, the forget arguments) and
  `promtool`; the rule is loaded with health `ok`.
- 2026-09-30 W10 R2 setup (owner: bucket, lock rules, Account API token,
  BKP-004/005, the two `.env` values). BKP-004/005 were 32 and 64 bytes at
  mode 600; BKP-003 existed empty at mode 664, so `gen-secrets.sh` filled it
  (16 characters, mode 640; the value was not printed). `restic-offsite
  init` 12:04:27-12:04:37 KST created the R2 repository with the state
  chunker parameters; the first `copy` 12:04:43-12:06:10 copied every local
  snapshot of both sets (18 in R2) and reported 1303841307 stored bytes;
  `check` 12:06:27-12:06:39 read 10% of the packs with no errors.

## Verification Evidence

W11, supervised reboot rehearsal (criterion 11), 2026-09-30, RUN-0098:

| Stage | Result |
| --- | --- |
| 0. Preconditions | pass: 09:37:52-09:39:07 KST, pgBackRest differential, Restic snapshots `9753742f` and `6236fc73`, `restic check` no errors |
| 1. Docker and containers | pass: boot 09:44:30; `docker.service` active 10:01:23 (about 16.5 min restoring containers, API silent meanwhile); 54 of 54 containers back, all healthy by 10:03:53 |
| 2. Data and auth | pass: `mng-pg` accepting connections; `mng-valkey`, Traefik, Keycloak healthy |
| 3. OpenBao | pass: sealed start, `openbao` and `openbao-agent` healthy |
| 4-5. Unseal and OIDC (owner) | pass: `Sealed false`, active leader, `home-admin` login |
| 6. SecretID (owner) | pass: Agent authenticated 10:30:29, SecretID consumed; the procedure itself was written during the rehearsal (RUN-0085) |
| 7. k3d | pass: five nodes Up, 38 pods Running, `vault-backend` `Ready=True` 10:11:17, six ExternalSecrets synced |

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
| Native OIDC without a session | `open-webui`, `grafana`, `airflow`, `gatus`, `kafka-ui`, `dozzle`, `openbao` | pass: each API path refuses (`401`, OpenBao `403`) and each login path reaches Keycloak or the app login page. Open WebUI `/` 200 (app shell), `/api/models` 401, `/oauth/oidc/login` 302 to Keycloak; Grafana `/` 302 `/login`, 307 `/login/generic_oauth`, 302 to Keycloak, `/api/search` 401; Airflow `/` 200 (app shell), `/api/v2/dags` 401, `/auth/login` 307 to Keycloak; Gatus `/` 200 (app shell), `/api/v1/endpoints/statuses` 401, `/oidc/login` 302 to Keycloak; Kafbat `/` and `/api/clusters` 302 to `/oauth2/authorization/keycloak`, then 302 to Keycloak; Dozzle `/` 307 `/login` (200), `/api/events/stream` 401; OpenBao `/` 307 `/ui/`, `/v1/sys/mounts` 403. `superset` is not running |

Finding: the SSO chain answers `401` with a `Location` header, not `302`,
so a browser renders the one-link "Found" page instead of redirecting. Access
is refused either way; the owner confirms the browser experience during the
logout row.

W9, owner rows run by the agent with owner approval (criterion 9),
2026-09-29. Two disposable `hy-home.realm` users were created with `kcadm.sh`
inside the Keycloak container, `sso-test-outsider` in `/users` and
`sso-test-admin` in `/admins`; the flows ran with `curl` through the gateway
at `192.168.0.13`, and both users were deleted afterwards (realm back to one
user). Passwords and cookies stayed in `0600` scratch files, never printed,
and were deleted.

| Row | Result |
| --- | --- |
| User outside `/admins` | pass: after the Keycloak sign-in the flow ended at `/oauth2/callback` with `403`, no upstream content, and one OAuth2 Proxy `unauthorized` line for the user; the `/admins` user reached the Prometheus UI |
| Logout | pass: `/oauth2/sign_out` answered `302`, and the next request to `prometheus` went `302` to the Keycloak authorization endpoint |
| Role removal | pass: right after removal from `/admins` the existing Proxy cookie still reached Prometheus, as the 1 h `cookie_refresh` allows; after sign-out and a new sign-in the flow ended with `403` |
| Native OIDC signed in | pass for all eight apps; the last four by the owner's browser check of 2026-09-29. `/users` user: Gatus API `401` (subject allowlist), Open WebUI back at `/auth` with API `401` (sign-up off, no account made), Grafana login error with API `401` (strict role mapping), Kafbat `VIEW` and `MESSAGES_READ` only (readonly), Airflow API `403`. `/admins` user: Kafbat all 12 actions, Airflow API `200`. Grafana, Open WebUI and OpenBao were not signed in as the `/admins` user because each would keep a local account or entity after the Keycloak user is deleted; OpenBao binds `groups=["/openbao-admins"]`. Dozzle v11.1.0's OIDC start path was not found from its login page. The owner then signed in to Dozzle, and to Grafana, Open WebUI and OpenBao as an `/admins` user, and reported each check complete |

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

2026-10-04 source review validation against
`origin/main=0460795abf6da9203e38f30291a8f20118c6ab88`:

| Command | Exit / evidence | Scope |
| --- | --- | --- |
| Pinned `markdownlint-cli2 --fix` on selected current Spec/Plan/Task files | 0, errors 0 | Document formatting only |
| `check-document-metadata.py --mode check-changed --base-ref origin/main` with seven explicit changed document paths | 0, selected 7, violations 0 | Current 0182/0193 document lifecycle; no transition override |
| `check-document-links.py --mode traceability` | 0, failures 0, warnings 0 | Registered traceability |
| `check-document-links.py --mode alignment` | 0, failures 0, warning 1 | Existing 2870 legacy archive links without capture source remain unverified |
| `check-document-corpus-lifecycle.py --base-ref origin/main` | 0, lifecycle and archive recovery violations 0 | Existing frozen packages unchanged |
| `git diff --check` | 0 | Task-owned working-tree diff |

The attempted profile name `validation-changed` was not registered (exit 1);
its registered name is `changed`, whose selection was inspected with
`run-ci-gate.py --profile changed --explain` (exit 0). No full gate result is
claimed from that explanation or from historical test counts.

### 2026-10-04 W8 measurement and W7 evidence correction

W8/criterion 8 measurement completed for the approved 168-hour window above.
Read-only preflight: Docker context `default`, server `29.8.1`, existing
`infra-prometheus` healthy. No container, volume, network, credential or HOME
configuration was changed. Queries used the existing container's `wget` and
Prometheus instant API at `time=1790953200`; all executed queries returned
process exit 0 and API `status=success`. This is observation, not a deployment
or recovery test. The two previously recorded sample gaps remain; percentiles
cover available 5-minute observations, not uninterrupted 168-hour coverage.

This table preserves the observed literal infra container names from the tracked
Compose files (including services later moved to LAB). It is a historical
window receipt, not a current root inventory. Disposable test/job identities
and unnamed container IDs are excluded; no sample means no observed value,
not zero utilization.

| Container | CPU p95 / max (cores, 5-minute rate) | Working set p95 / max (MiB) |
| --- | --- | --- |
| airflow-apiserver | 0.0050 / 0.5474 | 258.2799 / 347.1094 |
| airflow-dag-processor | 0.8419 / 0.9429 | 426.4439 / 628.9297 |
| airflow-scheduler | 0.0502 / 0.1313 | 256.3164 / 353.1250 |
| airflow-statsd-exporter | 0.0073 / 0.0075 | 21.9791 / 22.5898 |
| airflow-triggerer | 0.2150 / 0.2293 | 227.7289 / 233.6641 |
| airflow-worker | 0.2433 / 0.2973 | 648.0881 / 771.5820 |
| cadvisor | 0.0870 / 0.0960 | 271.2119 / 313.6836 |
| comfyui | 0.0027 / 0.0030 | 33.2266 / 41.7891 |
| dcgm-exporter | 0.0089 / 0.0093 | 37.3736 / 38.2578 |
| dozzle | 0.0340 / 0.0444 | 50.0664 / 57.3320 |
| flower | 0.0042 / 0.0052 | 241.4855 / 242.6445 |
| gatus | 0.0025 / 0.0026 | 22.2639 / 25.4766 |
| infra-alertmanager | 0.0047 / 0.0052 | 35.8982 / 38.8398 |
| infra-alloy | 0.0297 / 0.0331 | 284.8814 / 295.6172 |
| infra-grafana | 0.0211 / 0.0418 | 380.5064 / 732.2070 |
| infra-loki | 0.0171 / 0.0223 | 164.0912 / 208.3164 |
| infra-prometheus | 0.0599 / 0.0779 | 1052.2773 / 1474.5547 |
| infra-pyroscope | 0.0304 / 0.0346 | 155.1396 / 250.4883 |
| infra-tempo | 0.0170 / 0.0315 | 289.3248 / 369.4648 |
| jupyterlab | 0.0015 / 0.0017 | 15.5742 / 19.3672 |
| kafbat-ui | 0.0039 / 0.0102 | 350.9848 / 352.2070 |
| kafka-1 | 0.2488 / 0.3285 | 770.1762 / 833.8906 |
| kafka-connect | 0.0131 / 0.3067 | 998.5508 / 1404.4336 |
| kafka-exporter | 0.0045 / 0.0050 | 10.8213 / 14.8906 |
| kafka-rest-proxy | 0.0035 / 0.0101 | 227.6250 / 231.6367 |
| keycloak | 0.0068 / 0.3900 | 551.3477 / 783.8516 |
| mlflow | 0.0086 / 0.0142 | 327.1133 / 335.2070 |
| mng-pg | 0.0969 / 0.1479 | 131.1945 / 174.9062 |
| mng-pg-exporter | 0.0056 / 0.0061 | 11.4400 / 15.8086 |
| mng-valkey | 0.0073 / 0.0076 | 19.9883 / 24.2070 |
| mng-valkey-exporter | 0.0047 / 0.0053 | 10.1613 / 10.7695 |
| n8n | 0.0068 / 0.0138 | 239.9555 / 282.3320 |
| n8n-task-runner | 0.0017 / 0.0018 | 4.6002 / 8.2734 |
| n8n-task-runner-worker | 0.0014 / 0.0015 | 3.9375 / 8.1875 |
| n8n-worker | 0.0017 / 0.0071 | 146.5469 / 146.5820 |
| node-exporter | 0.0152 / 0.0176 | 16.2564 / 17.8281 |
| oauth2-proxy | 0.0014 / 0.0021 | 18.5977 / 23.9023 |
| ollama | 0.0100 / 0.0201 | 196.0898 / 330.1484 |
| ollama-exporter | 0.0016 / 0.0018 | 34.9219 / 36.9648 |
| open-webui | 0.0065 / 0.0230 | 1377.1016 / 1377.3398 |
| openbao | 0.0205 / 0.9972 | 104.1859 / 116.1523 |
| openbao-agent | 0.0017 / 0.1971 | 16.0945 / 22.1758 |
| qdrant | 0.0029 / 0.0032 | 38.6041 / 38.6875 |
| redisinsight | 0.0012 / 0.0024 | 75.4205 / 77.1602 |
| registry | 0.0022 / 0.0027 | 27.2760 / 52.6016 |
| schema-registry | 0.0065 / 0.0779 | 265.4357 / 266.9023 |
| seaweedfs-filer | 0.0098 / 0.0143 | 193.0127 / 208.3477 |
| seaweedfs-master | 0.0045 / 0.0109 | 99.8828 / 101.6172 |
| seaweedfs-s3 | 0.6144 / 0.9427 | 136.8732 / 227.4688 |
| seaweedfs-volume | 0.0054 / 0.0086 | 60.2258 / 88.9531 |
| traefik | 0.0127 / 0.0253 | 89.0404 / 119.0039 |

Container queries are the four p95/max expressions in the corrected W8
contract. Original `sum by(name)` counted overlapping old/new identities:
the triggerer's 354.16 MiB apparent peak exceeded its 256 MiB limit. Pointwise
`max by(name)` removes that overlap; it represents one observed instance, not
a sum of replicas. This HOME measurement is not a multi-replica capacity plan.

Host CPU p95/max: 58.6823%/93.0787%. Host memory p95/max:
67.6499%/73.5278%, using `max(1-node_memory_MemAvailable_bytes/
node_memory_MemTotal_bytes)` before temporal aggregation to deduplicate target
labels. GPU utilization observed p95/max 0%; this does not prove absence of
GPU workloads during missing samples. Framebuffer counter maximum was 2508 MiB, following the
[NVIDIA exporter counter contract](https://github.com/NVIDIA/dcgm-exporter/blob/main/etc/default-counters.csv)
checked on 2026-10-04.

Disk endpoint subtraction joined start/end samples by the same mountpoint and
filesystem type. `/` used bytes changed 179310456832 -> 175795908608
(-3514548224); `/home/hyunyoun/storage` changed 182384209920 -> 189968408576
(+7584198656); `/boot` grew 4096 bytes and `/boot/efi` stayed unchanged. The
original `offset 168h` expression produced no matched series after target
labels changed; an empty result was not interpreted as zero growth. Neither
logical filesystem identity nor growth proves physical disk redundancy.

Supplemental throttling queries used the pointwise per-name maximum of
5-minute CFS throttled-period increases divided by CFS period increases, then
p95/max over the same window. Fractions: OpenBao 0.006559/0.978041,
management Valkey exporter 0.244898/0.324324, node exporter 0.650000/0.703704,
Airflow triggerer 0.673094/0.873326, SeaweedFS S3 0.003959/0.594921. These are
throttled-period fractions, not CPU utilization or proof of a required CPU
limit. The window spans historical budget changes; SPEC-0193 owns source
budget decisions and a separately approved rollout/re-measurement.

W7/criterion 7 is not closed by the historical PostgreSQL PASS row above.
That row is preserved as the 2026-09-25 report, but the current
[POL-0021](../../../05.operations/policies/0021-backup-and-restore.md) and
[RUN-0021](../../../05.operations/runbooks/0021-backup-and-restore.md)
supersede its time-target/RPO claim. SPEC-0201 W7.4 Phase A was held before
repository verification or scratch creation; the later owner hold superseded
the earlier verification approval. Verify, restore and PITR remain NOT_RUN. A new isolated
recovery, consistency checks and measured recovery time remain NOT_RUN and
require the separately scoped operational approval. The bounded MLflow,
synthetic CDC and owner-accepted empty JupyterLab evidence remain historical
receipts. W10 R2 scratch restore/offline key custody also remain open; the
Task and Spec package remain in progress/active.

## Review Evidence

2026-10-04 independent read-only review: Task 0002 completion receipts PASS;
Task 0003 W8 aggregates and current W7/W10 holds PASS with the scope of
observed service rows made explicit. No current recovery or rollout was
accepted from historical tests.

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
| #279 | Revert #277 until the R2 setup | merged |
| #280 | W7, W9, W10 and W11 records | merged |
| #281 | Task 0001 completed; RUN-0021 data-disk scratch; RUN-0088 rehearsal path | merged |

## Rulings

See the Plan.

- 2026-09-25, owner: criterion 7 asks for a JupyterLab restore on real
  content, but the production work directory holds no files. The
  2026-09-22 synthetic-notebook rehearsal (RUN-0089) stands as the W7
  JupyterLab evidence; a real-content rehearsal follows once the directory
  holds work.

## Deferred Items

| Item | Owner | Trigger or date |
| --- | --- | --- |
| R2 restore rehearsal into scratch (RUN-0021 8.3) with elapsed time, before offsite recovery is claimed as verified; copy BKP-003 to offline custody | @buenhyden | Before criterion 10 is closed |
| Monthly remote `forget-prune` (RUN-0021 8.5) and the Metrics tab reading (8.6) | @buenhyden | Monthly, or when `HyhomeOffsiteRepoNearFreeTier` fires |
| W7 management PostgreSQL restore evidence | @buenhyden | Current POL-0021/RUN-0021: actual isolated recovery remains NOT_RUN; approve the exact recovery phase separately |

### Current prerequisite review — 2026-10-04

The owner approved the implementation plan for immediately solvable prerequisite
work in SPEC-0182/0193/0204/0206 on 2026-10-04. This Task is the sole writer of this recovery review;
its Spec/Plan and existing POL/RUN-0021 recovery contract remain unchanged.
Baseline main/origin-main is `ebeb83521c768fedc620380b0c2e92db10a6fcdc`.

Read-only host counters: `/` and `/home/hyunyoun/data` each reported
266918543360 total bytes and 79943307264 free bytes; MemTotal was
33575424000 bytes, MemAvailable 14069882880 bytes, and 12 logical CPUs were
reported. These point-in-time counters reserve no resources and do not prove
physical redundancy, selected scratch capacity, repository size, or recovery
fit. The exact approved data-disk target must be rechecked before execution.

The Docker context is default with the local Unix socket. No image was pulled
and no container, backup lock, scratch, network or volume was created. The
existing BKP-001 owner and read-only bind approval remain usable inputs; their
values were not read by this review. Phase A never ran: the owner held it before
verify or scratch creation, superseding its earlier execution approval. Future
verify, step 5 time-target PITR and step 5a immediate restore each need their
exact execution scope approved. The step 5a
`app_db` temporary-table probe tests restored ACL/consistency only; the owner's
no-business-data statement does not make it an application cutover test.

The next actual recovery contract still requires a named selected backup,
recovery time/timezone and continuous WAL for PITR, original-compatible image,
owned empty target/device/inode, capacity budget, bounded lock/time window,
application invariants and separately approved cleanup. R2 additionally needs
an exact host/state snapshot pair, limited remote access and offline BKP-003
custody. Do not substitute `latest`, current Compose pins, synthetic recovery,
capacity counters or historical Phase A for these inputs. W7/W10 remain open;
Task, Plan and Spec stay active/in-progress, so the package is not archivable.

The prerequisite source checks passed 24 tests; the approved implementation
then passed 25 focused backup/auth/observability/runtime tests, exit 0, using the
four named modules recorded in the SPEC-0193 completion receipt.
No real repository restore, HOME mutation, secret issuance/rotation, private
log inspection, data deletion or remote snapshot operation ran. This receipt
closes prerequisite inspection only. Changed metadata14, corpus/archive recovery,
links (one legacy warning), Markdown14 and diff checks exited 0; independent
source/lifecycle review returned PASS. Recovery is a scoped documentation correction.
