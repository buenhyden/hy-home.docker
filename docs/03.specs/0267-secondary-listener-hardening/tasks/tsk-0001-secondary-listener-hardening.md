---
title: "Secondary Listener Hardening Task"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0267-TSK-0001"
parent_ids:
- "SPEC-0267-PLAN-0001"
created: "2026-11-07"
---

# Secondary Listener Hardening Task

## Overview

### Objective

Execute W1–W5 of the Plan: inventory the six secondary listeners, bind them to
consumer-only addresses, add Grafana metrics authentication, declare the
Pyroscope and ComfyUI data volumes, test, document and, under separate approval, apply
the change in HOME.

## Inputs and Authorization

On 2026-11-07 the owner reviewed the secondary listeners recorded out of scope
by SPEC-0266 and chose: bind all six under a new Spec, add Grafana metrics
authentication, record n8n `/metrics`, Gatus `/metrics` and the POL-0096 LAN
listeners as accepted risks, and declare the Pyroscope metastore as a named
volume in a separate change. The Spec and Plan are `draft`; no
implementation starts until both are approved. The review read `main`
`fa6135043a4b770281400e5f7a6a7b4ceca66063` and the upstream documentation and source of each pinned
version. HOME recreation (W5) needs its own approval.

## Work Log

### Draft inputs (2026-11-07)

| Listener | Bind setting (upstream) | Consumers found in review | Note |
| --- | --- | --- | --- |
| SeaweedFS S3 `9327` | `-metricsIp` (4.48 `weed/command/s3.go:116`) | Prometheus, Alloy profiles | `seaweedfs_s3_metrics_net` already carries only these |
| OAuth2 Proxy `44180` | `OAUTH2_PROXY_METRICS_ADDRESS` (7.15) | Prometheus | Health check uses `4180` |
| Keycloak `9000` | `KC_HTTP_MANAGEMENT_HOST` (26.7.4 `ManagementOptions.java:66-69`) | Prometheus, Gatus, own health check on `127.0.0.1:9000` | Health check must move |
| n8n broker `5679` | `N8N_RUNNERS_BROKER_LISTEN_ADDRESS` (2.43.6 `runners.config.ts:32-33`) | `n8n-task-runner` over `n8n_main_runner_net` | Already token-protected; `n8n-worker` is not on `edge_net` |
| Grafana pprof `6060` | `GF_DIAGNOSTICS_PROFILING_ADDR` | Alloy `pyroscope.scrape` | A specific IP is implied, not stated, by the docs |
| Traefik `8082` | entrypoint `address: "<host>:8082"` (v3.7) | Prometheus, own `traefik healthcheck --ping` | Ping with a bound entrypoint is untested |

Main-port metrics: Grafana offers `[metrics] basic_auth_username` and
`basic_auth_password` (13.2.4 `conf/defaults.ini:2031-2033`); n8n documents
no metrics authentication; Gatus serves `/metrics` outside its OIDC router
and the repository patch test `metrics-remains-public-for-internal-scrape`
keeps it public. Loki and Tempo have no built-in authentication; Alloy's OTLP
receiver accepts an `auth` handler, but the senders run in LAB.

Pyroscope 2.4.0 keeps `-metastore.data-dir` and `-metastore.raft.dir` under
`./data/v2/metastore` with working directory `/`, so the metastore lives in
the image's anonymous `/data` volume (142.6M), not in the declared
`pyroscope-data` volume. A `down` or `rm` followed by `up` would give it an
empty volume and orphan the profile blocks.

### Approval and start (2026-11-07)

The owner approved the SPEC-0267 Spec and Plan on 2026-11-07, after the draft
package merged in #786. Spec 0.2.0 adds the ComfyUI state mounts the owner chose
during the SPEC-0266 apply. W1 starts now; W5 (HOME) keeps its own approval.
ComfyUI's unrestricted outbound access through `comfyui_egress_net` is not in
scope until the owner decides between an egress allowlist and an accepted risk.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0267 | draft | approved | #approval-and-start-2026-11-07 |
| SPEC-0267-PLAN-0001 | draft | approved | #approval-and-start-2026-11-07 |
| SPEC-0267-TSK-0001 | draft | ready | #approval-and-start-2026-11-07 |
| SPEC-0267-TSK-0001 | ready | in-progress | #approval-and-start-2026-11-07 |
| SPEC-0267-TSK-0001 | in-progress | completed | #owner-acceptance-2026-11-08 |

### W1 source inventory (2026-11-07)

Read from `main` `84170dde6` and the pinned upstream source of each image.
Every listener bound all interfaces. Prometheus loads `prometheus.dev.yml` by
default (`infra/06-observability/docker-compose.yml:90`) and carries the same
job lines as `prometheus.yml`, so both change together.

| Listener | Bind setting | Consumers | Health checks on it | Network, address, alias |
| --- | --- | --- | --- | --- |
| SeaweedFS S3 `9327` | `-metricsIp` (4.48 `weed s3 -h`); command at `infra/04-data/seaweedfs/docker-compose.yml:219` | Prometheus `prometheus.yml:232-234`; Alloy `config.alloy:158-160`, `config.home.alloy:265-267`, both over `seaweedfs_s3_metrics_net` only | None (`8333/healthz`) | `seaweedfs_s3_metrics_net`, `10.250.41.2`, name kept |
| OAuth2 Proxy `44180` | `OAUTH2_PROXY_METRICS_ADDRESS` (`infra/02-auth/oauth2-proxy/docker-compose.yml:44`; v7.15 `net.Listen`) | Prometheus `prometheus.yml:151-153` over `obs_net` | None (`4180/ping`) | `oauth2_proxy_metrics_net` `10.250.43.0/24`, `.2`, `oauth2-proxy-metrics` |
| Keycloak `9000` | `KC_HTTP_MANAGEMENT_HOST` (26.7.4 `kc.sh start --help`); port at `infra/02-auth/keycloak/docker-compose.yml:76` | Prometheus file_sd from `prometheus/scripts/start.sh:35,75-83`; Gatus `config.oidc.yaml:52`, `config.yaml:39` | Own check on `127.0.0.1` (`:113-114`) | `keycloak_management_net` `10.250.44.0/24`, `.2`, `keycloak-management` |
| n8n broker `5679` | `N8N_RUNNERS_BROKER_LISTEN_ADDRESS` in the shared anchor (`infra/07-workflow/n8n/docker-compose.yml:29`; 2.43.6 `runners.config.js:24,54`) | `n8n-task-runner` (`:212`) over `n8n_main_runner_net`; `n8n-task-runner-worker` (`:262`) over `n8n_worker_runner_net` | `n8n-worker` on `127.0.0.1:5679/healthz` (`:185-186`) | Existing runner networks, `10.250.22.2` and `10.250.23.2`, names kept |
| Grafana pprof `6060` | `GF_DIAGNOSTICS_PROFILING_ADDR` (13.2.4 `pkg/server/bootstrap/diagnostics.go:149`); `infra/06-observability/docker-compose.yml:416` | Alloy `config.alloy:146`, `config.home.alloy:254` over `obs_net` | None (`3000/api/health`) | `grafana_pprof_net` `10.250.45.0/24`, `.2`, `grafana-pprof` |
| Traefik `8082` | entrypoint `address` (`infra/01-gateway/traefik/config/traefik.yml:23-24`; v3.7.16 `[host]:port`) | Prometheus `prometheus.yml:139-141`, sharing `obs_net` and `prometheus_ingress_net` with Traefik | Own `traefik healthcheck --ping`; v3.7.16 `cmd/healthcheck/healthcheck.go:49-83` dials the entrypoint address as written | `traefik_metrics_net` `10.250.46.0/24`, `.2`, `traefik-metrics` |

Grafana 13.2.4 enforces `[metrics] basic_auth_username` and
`basic_auth_password` on `GET /metrics` (`pkg/api/http_server.go:755-773`), and
the image's `/run.sh:50-62` turns `GF_METRICS_BASIC_AUTH_PASSWORD__FILE` into
the password. Pyroscope 2.4.0 keeps its metastore and raft state under
`./data/v2/metastore` with working directory `/`, inside the image's anonymous
`/data` volume (205.8 MB at W1). ComfyUI runs `/root/ComfyUI` from the image's
anonymous `/root` volume; the Compose mounts at `/opt/comfyui` are empty.

UNKNOWN after W1: the embedded-DNS answer when a consumer shares several
networks with a target (avoided by the aliases); `traefik healthcheck --ping`
with a bound entrypoint has not run; Keycloak binding `/metrics` to the
management host rests on its `--help` text; LAB state of the runner networks.
HOME n8n does not match the tracked revision: `n8n_main_runner_net` and
`n8n_worker_runner_net` do not exist live and both containers sit on older
networks.

### W1 decisions (2026-11-07)

The owner chose: n8n broker binding in source only, with its HOME apply in a
separate n8n reconciliation; consumers address each bound listener by a
network-scoped alias; the Pyroscope metastore on a named volume at `/data`;
and the existing ComfyUI volumes remounted at `/root/ComfyUI/<dir>`. Grafana
metrics authentication needs a new secret and follows in a second change.

### Accepted risks (2026-11-07)

The owner accepted these exposures on 2026-11-07 instead of changing them.

| Exposure | Reachable from | Reason | Review trigger |
| --- | --- | --- | --- |
| n8n `/metrics` on the main port `5678` | Every peer of n8n on `edge_net`, `n8n_net`, `mng_data_net` and `obs_net` | n8n documents no metrics authentication and Traefik needs the same port; metrics carry no credential or write path | An n8n release that adds metrics authentication or a separate metrics listener |
| Gatus `/metrics` on the main port `8080` | Every peer of Gatus on `edge_net`, `mng_data_net` and `obs_net` | Upstream serves it outside the OIDC router, and the repository patch keeps it public for the internal scrape (`metrics-remains-public-for-internal-scrape`) | A Gatus bump that touches `oidc-hardening.patch`, or upstream metrics authentication |
| POL-0096 LAN publications of Loki `3100`, Tempo `3200` and Alloy `4317`/`4318` | The HOME LAN through `${HOST_LAN_BIND_IP}` | The senders run in LAB, which this package does not change; Loki and Tempo have no built-in authentication | Any LAB change that can carry a token or certificate to the senders, or a change to POL-0096 |

### W2–W4 implementation (2026-11-07)

W3 came first: `SecondaryListenerContractTests` in
`tests/validation/test_p02_service_contracts.py` failed on all seven listeners,
both health checks, every consumer reference and both volume contracts
(17 failures, 2 errors). W2 declared the four networks and added `ip_range` to
the two runner networks, set each bind option and fixed address with its alias,
moved the Keycloak and n8n-worker health checks to the bound address, pointed
Prometheus (both files), the Prometheus file_sd renderer, Gatus (both files)
and Alloy (both files) at the aliases, moved the n8n listen address out of the
shared anchor, added `pyroscope-metastore` at `/data`, and remounted the five
ComfyUI volumes. `compose_observation.TARGET_ALIASES` maps the aliases back to
their services, and a test pins it to the Compose aliases. Existing tests that
pinned the old Keycloak target, health check, runner-network IPAM and the
`edge_net` path of `seaweedfs-s3` were updated to the new contract. The n8n
source binding in `update-ledger.json` and `build-inputs.json` was rehashed and
its predecessor archived, as earlier n8n Compose changes did. W4 updated
GDE-0077, seven READMEs and the m0021 inventory. No container was recreated.

### Working-tree side effect (2026-11-07)

W2 was edited in the HOME working tree, which is also the bind-mount source of
the running services. Gatus reloaded the edited `config.oidc.yaml` and its
Keycloak probe failed against the not-yet-existing `keycloak-management` alias,
and `traefik healthcheck --ping` read the edited `traefik.yml` and marked
Traefik unhealthy for about 40 minutes; routes and the real ping kept working.
The single-file mounts are read-only and held the edited inode, so after the
commit the files were restored to `main` and, with the owner's approval,
Traefik and Gatus were restarted: both turned healthy, the route codes matched
the baseline and the Keycloak probe succeeded again. Prometheus and Alloy still
hold the edited inode but read it only at start or on an explicit reload; W5
recreates them. Further branch work uses a separate Git worktree, and the HOME
working tree stays on `main`.

### Grafana metrics authentication (2026-11-07)

The owner approved the second change on 2026-11-07. W3 first:
`test_grafana_metrics_require_basic_auth` failed on the current render. W2 set
`GF_METRICS_BASIC_AUTH_USERNAME=prometheus` and
`GF_METRICS_BASIC_AUTH_PASSWORD__FILE` in Grafana, declared the
`grafana_metrics_password` Compose secret for Grafana and Prometheus, added
`basic_auth` with `password_file` to the `grafana` job in both Prometheus files,
and catalogued the secret as `OBS-015`. The public registry row for `OBS-015`
lives in `secrets/SENSITIVE_ENV_VARS.md.example`, which the agent's permission
rules keep out of reach, so the owner adds it; until then three catalog and
metadata tests fail on the missing row. W5 generates the private value with
`scripts/operations/gen-secrets.sh` before Grafana and Prometheus are recreated.

### W5 HOME apply (2026-11-08)

The owner approved W5 on 2026-11-07 ("PR-2, Grafana metrics auth (criterion
3), W5, the HOME apply approval") and merged #793. The live tree was
fast-forwarded to `c669517df` with no local changes.

Secret: `gen-secrets.sh` under the system `python3` stopped with
`GENERATION rejected: invalid public catalog`. The cause was the distro
`jsonschema`, which lacks the `referencing` module, not the catalog. The owner
ran `--sync-metadata` and then the no-argument mode through
`uv run --no-project --with 'jsonschema>=4.18' --with pyyaml`. The dry run
planned five new files: `OBS-015` and the missing `CACHE-027` to `CACHE-030`,
which no recreated service uses. The new file is 16 bytes, mode `640`, owner
`1000:1000`, read through `group_add: 1000` like the existing Grafana secret.
No value was read or printed.

Data: `pyroscope` and `comfyui` were stopped, and their anonymous volumes were
archived to `~/storage/backups/spec0267-w5-20261108/` (`pyroscope-anon-data.tar`
from `788915f1746d`, `comfyui-root.tar` from `8c60682fd5a7`, `SHA256SUMS`,
`volumes.txt`, `pre-networks.txt` with each service's previous networks). The
Pyroscope `/data` content (260.3M, `v2/metastore` and `pyroscope-sync`, UID
10001) was copied with ownership to `${DEFAULT_OBSERVABILITY_DIR}/pyroscope-metastore`.
The ComfyUI `models`, `custom_nodes`, `input`, `output` and `user` directories
were copied into their empty bind directories. File counts matched for every
directory.

Recreate: a `--dry-run` showed only the four new networks and the
`pyroscope-metastore` volume being created. Then
`docker compose -p hy-home-infra up -d --no-deps --force-recreate` ran for
seaweedfs-s3, oauth2-proxy, keycloak, grafana, traefik, prometheus, alloy,
gatus, pyroscope and comfyui from 18:53:29 to 18:57:19 UTC. n8n was not
recreated.

Outage: the changed `KC_HTTP_MANAGEMENT_HOST` made Keycloak rebuild its server
image at start (`Changes detected in configuration. Updating the server
image.`). The host had 33–40% iowait, and the rebuild took until 19:05:25 UTC.
A thread dump showed the build writing the fast-jar, not deadlocked. Until
then oauth2-proxy and Gatus failed OIDC discovery and restarted, so SSO routes
were down for about 12 minutes. Both recovered on their own once Keycloak was
healthy. A later change to a Keycloak build-affecting option should expect the
same rebuild time, or start oauth2-proxy and Gatus after Keycloak is healthy.

Observations after the apply:

| Check | Result |
| --- | --- |
| Health of the ten services | All `healthy` |
| Prometheus targets `traefik-metrics:8082`, `oauth2-proxy-metrics:44180`, `keycloak-management:9000`, `seaweedfs-s3:9327`, `grafana:3000` (basic auth) | All `up` |
| Other down targets | kafka-1, kafka-connect, kafka-exporter, schema-registry exited 3 days earlier; opensearch and three Valkey exporters not deployed; none in scope |
| Grafana `/metrics` without credentials, from Prometheus | `401 Unauthorized` |
| From `storybook-mcp` on `edge_net`: `keycloak:9000`, `oauth2-proxy:44180`, `traefik:8082`, `grafana:6060`, `seaweedfs-s3:9327` | All `connection refused`; control `keycloak:8080` answers `200` |
| `traefik healthcheck --ping` | `OK: http://10.250.46.2:8082/ping` |
| Gatus `gatus_results_endpoint_success` | 8 endpoints, none failing, Keycloak `1` |
| Pyroscope `service_name` values in the last 10 minutes | `grafana` present, so Alloy reaches `grafana-pprof` |
| Pyroscope history 24 h to 1 h before the apply | Same 11 services as before; the 2–3 day window is empty, which predates the 2026-11-07 raft snapshot restore |
| Pyroscope `/data` mount | `hy-home-infra_pyroscope-metastore` |
| ComfyUI mounts and file counts | The five volumes at `/root/ComfyUI/<dir>`; 75, 182, 3, 2 and 18 entries, as in the source |
| SSO routes through `192.168.0.13:443` | `comfyui` 302 to the Keycloak realm; `grafana` 302 to its OIDC login |

Rollback rehearsal: both archives pass `sha256sum -c`. A detached worktree at
the pre-SPEC-0267 revision `57e2636d7` rendered a recreate of all ten
services with `--dry-run` and no error, and was removed. The live rollback was
not run, because it would repeat the Keycloak rebuild outage. A rollback of
Pyroscope also needs the archive restored into a new `/data` volume, because
the previous revision's anonymous volume is no longer attached; ComfyUI still
mounts its previous `/root` volume.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | Draft source and documentation review | `fa6135043`, upstream pins | NOT_RUN | Draft input only; the source-read inventory is W1 | optional | - |
| E2 | 1 | W1 | Source-read inventory of the six listeners | `84170dde6`, upstream pins | PASS | W1 table above with a source line per row | required | - |
| E3 | 5 | W3 | `SecondaryListenerContractTests` before and after W2 | `57e2636d7` then this branch | PASS | 17 failures and 2 errors before W2; 5 tests OK after | required | - |
| E4 | 2, 4 | W2 | All-profile public render, `validate-docker-compose.sh`, `check-all-hardening.sh` | This branch | PASS | 65 selections valid; all hardening tiers pass | required | - |
| E5 | 2, 4 | W2 | 76 suites naming the changed services | This branch | PASS | 1,468 tests; only `test_root_resource_assessment` fails to import (`referencing` absent locally, also on `main`) | required | - |
| E6 | 6 | W4 | Metadata, link and operations-catalog checks | This branch | PASS | 0 violations; all link modes PASS | required | - |
| E7 | 6 | W1 | Accepted-risk records | This branch | PASS | "Accepted risks" table with reason and review trigger | required | - |
| E8 | 3 | W2 | Grafana metrics authentication render test and catalog | This branch | PASS | `test_grafana_metrics_require_basic_auth` failed before, OK after; the registry row is the owner's step | required | - |
| E9 | 7 | W5 | HOME recreate of the ten services and live observations | `c669517df`, HOME | PASS | "W5 HOME apply" table; about 12 minutes of SSO outage during the Keycloak rebuild | required | - |
| E10 | 7 | W5 | Backup checksums and dry-run render of `57e2636d7` | Backups, `57e2636d7` | PASS | "W5 HOME apply", rollback rehearsal | required | - |
| E11 | 7 | W5 | Live rollback to `57e2636d7` | HOME | NOT_RUN | Not run, to avoid a second Keycloak rebuild outage; owner decision | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | E2 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 2 | accepted | E4, E5, E9 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 3 | accepted | E8, E9 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 4 | accepted | E4, E5, E9 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 5 | accepted | E3 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 6 | accepted | E6, E7 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 7 | accepted | E9, E10 | Accepted by the owner on 2026-11-08 | @buenhyden |

## Review and Completion

W1–W5 are done and every criterion has PASS evidence.

### Owner acceptance (2026-11-08)

The owner accepted criteria 1–7 on 2026-11-08 after the W5 evidence merged
(#794), including the dry-run rollback rehearsal in place of a live rollback
(E11 stays NOT_RUN), and the Task closed as `completed`. Two follow-ups stay
outside this Task: the n8n HOME reconciliation that applies the broker binding
proceeds as separate work, and ComfyUI's unrestricted outbound access through
`comfyui_egress_net` remains an open owner decision.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [SPEC-0266 Task](../../0266-sso-only-backend-ingress/tasks/tsk-0001-sso-only-backend-ingress.md)
