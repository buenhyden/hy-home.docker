---
title: "SSO-Only Backend Ingress Task"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-11-07"
layer: "specs"
artifact_id: "SPEC-0266-TSK-0001"
parent_ids:
- "SPEC-0266-PLAN-0001"
created: "2026-11-07"
---

# SSO-Only Backend Ingress Task

## Overview

### Objective

Execute W1–W5 of the Plan: confirm the SSO-only backends and their flows, move
them to dedicated ingress networks, test the isolation, update the documents
and, under separate approval, apply the change in HOME.

## Inputs and Authorization

The owner asked on 2026-11-07 to start this Spec after the D02 finding in
SPEC-0212 TSK-0041. The Spec and Plan are `draft`; no implementation starts
until both are approved. The 2026-11-07 render inputs are `main`
`56104a49ec2ee6b3756408d73520363080c9b55a` with the public `.env.example`.
HOME recreation (W5) needs its own approval.

## Work Log

### Draft inputs (2026-11-07)

A value-free render of every profile from `.env.example` listed 38 `edge_net`
members. Traefik holds `10.250.1.2` and the aliases `keycloak.hy.home.arpa`
and `auth.hy.home.arpa` on `edge_net`, so OIDC clients on it reach Keycloak
through Traefik; the SSO-only backends are not OIDC clients and do not need
those aliases. A text match of each member's environment, command and mounted
configuration against the other members' names, filtered to pairs that share
no network but `edge_net`, found three `edge_net`-only flows: Alloy and
Prometheus to `seaweedfs-s3`, and Grafana to Ollama. The match is approximate
(it also counts public host names and unused references), so W1 replaces it
with a source-read inventory before any change.

### W1 source inventory (2026-11-07)

Two read-only `code-reviewer` subagents each read half of the 38 `edge_net`
members (compose block, mounted configuration, wrapper scripts) and cited a
source line per claim. The orchestrator spot-checked six of those lines (the
Prometheus lifecycle flag, Loki `auth_enabled`, the Qdrant API keys, both
`seaweedfs-s3:9327` scrapes and the Traefik provider network); every other row
rests on the reviewer's citation. Own authentication means the listener Traefik routes
to enforces a credential without the gateway; product default-off auth counts
as absent.

| Service | Own auth | Source | Decision |
| --- | --- | --- | --- |
| alertmanager | ABSENT | `infra/06-observability/docker-compose.yml:757` (no `--web.config.file`) | Move |
| alloy | ABSENT | `infra/06-observability/docker-compose.yml:268`; `alloy/config/config.alloy:98-104` | Move; joins `seaweedfs_metrics_net` |
| cadvisor | ABSENT | `infra/06-observability/docker-compose.yml:590-600` (no auth file; privileged) | Move |
| comfyui | ABSENT | `infra/08-ai/comfyui/docker-compose.yml:80` | Move |
| flower | ABSENT | `infra/07-workflow/airflow/docker-compose.yml:444` | Move |
| kafka-connect | ABSENT | `infra/05-messaging/kafka/docker-compose.yml:172,220-222` | Move |
| kafka-rest-proxy | ABSENT | `infra/05-messaging/kafka/docker-compose.yml:326,331` | Move |
| loki | ABSENT | `infra/06-observability/loki/config/loki-config.yaml:1` (`auth_enabled: false`) | Move |
| mailpit | ABSENT | `infra/11-quality/mailpit/docker-compose.yml:30-36` | Move |
| mlflow | ABSENT | `infra/08-ai/mlflow/docker-compose.yml:105-113` (no basic-auth app) | Move |
| ollama | ABSENT | `infra/08-ai/ollama/docker-compose.yml:40-51` | Move |
| prometheus | ABSENT | `infra/06-observability/docker-compose.yml:76-83` (`--web.enable-lifecycle`, no web config) | Move |
| pushgateway | ABSENT | `infra/06-observability/docker-compose.yml:788-821` | Move |
| pyroscope | ABSENT | `infra/06-observability/pyroscope/pyroscope.yaml:1-26` | Move |
| schema-registry | ABSENT | `infra/05-messaging/kafka/docker-compose.yml:118` | Move |
| tempo | ABSENT | `infra/06-observability/tempo/config/tempo.yaml:1-96` | Move |
| terrakube-ui | ABSENT | `infra/09-platform-ops/terrakube/docker-compose.yml:88-94` (static SPA) | Move |
| qdrant | PRESENT | `infra/04-data/qdrant/docker-compose.yml:51-66` (API keys) | Keep; was in the draft list |
| dozzle | PRESENT | `infra/06-observability/dozzle/docker-compose.yml:48-52` (OIDC) | Keep |
| keycloak | PRESENT | `infra/02-auth/keycloak/docker-compose.yml:62,68,72` | Keep |
| neo4j | PRESENT | `infra/04-data/neo4j/scripts/neo4j-entrypoint-with-secrets.sh:11-20` | Keep |
| open-webui | PRESENT | `infra/08-ai/open-webui/docker-compose.yml:44-62` (OIDC only) | Keep |
| open_notebook | PRESENT | `infra/08-ai/open-notebook/docker-compose.yml:37` (password) | Keep |
| openbao | PRESENT | `infra/03-security/openbao/docker-compose.yml:68` (token over TLS) | Keep |
| opensearch | PRESENT | `infra/04-data/opensearch/opensearch/config/opensearch.yml:11,15` | Keep |
| opensearch-dashboards | PRESENT | `opensearch-dashboards/config/opensearch_dashboards.yml:16-17` | Keep |
| storybook-mcp | PRESENT | `infra/13-experience/storybook/docker-compose.yml:37-40,56-59` | Keep |
| terrakube-api | PRESENT | `infra/09-platform-ops/terrakube/docker-compose.yml:32-34,37-38,47` | Keep |
| terrakube-executor | PRESENT | `infra/09-platform-ops/terrakube/docker-compose.yml:132-133` | Keep |
| airflow-apiserver | PARTIAL | KeycloakAuthManager `infra/07-workflow/airflow/docker-compose.yml:6-7,127-135`; open health `:163` | Keep |
| gatus | PARTIAL | OIDC `gatus/config/config.oidc.yaml:11-22`; open `/metrics` | Keep |
| grafana | PARTIAL | OAuth `infra/06-observability/docker-compose.yml:347-398`; open `/metrics`, pprof `:409-411` | Keep |
| kafbat-ui | PARTIAL | OAuth2 `kafka/kafbat-ui/dynamic_config.template.yaml:9-27`; open actuator health | Keep |
| n8n | PARTIAL | User login and API key `infra/07-workflow/n8n/docker-compose.yml:72-127`; open `/metrics`, broker `5679` | Keep |
| oauth2-proxy | PARTIAL | The authenticator `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg:5,11,27`; metrics `44180` | Keep |
| seaweedfs-s3 | PARTIAL | SigV4 `seaweedfs/config/s3-identities.conf:5-12`; metrics `9327` open | Keep; joins `seaweedfs_metrics_net` |
| nginx | PARTIAL | Opt-in LAN gateway, not a Traefik backend, `nginx/config/nginx.conf:117-207` | Keep |
| traefik | PARTIAL | Gateway; metrics entrypoint `8082` open `traefik/config/traefik.yml:23-26` | Joins each new ingress network |

**Flows.** Only two flows of the moved services use `edge_net` as their sole
shared network: Prometheus scraping `seaweedfs-s3:9327`
(`prometheus/config/prometheus.dev.yml:232-234`) and Alloy's pprof scrape of the
same port (`alloy/config/config.alloy:158-161`). The draft's Grafana-to-Ollama
flow is not a call; every Ollama caller in source shares `ai_net`. None of the
moved services is an OIDC client, so none needs Traefik's `keycloak`/`auth`
aliases. Moving Ollama also removes n8n main's possible runtime path to it over
`edge_net`, which matches the worker-only overlay. Nginx reaches Keycloak and
OAuth2 Proxy only over `edge_net`; both stay there. Traefik's Docker provider
defaults to `edge_net` (`traefik/config/traefik.yml:30-33`), so each moved
service needs `traefik.docker.network`.

**Open secondary listeners that stay on `edge_net` (out of scope, recorded for
a separate decision):** Grafana pprof `0.0.0.0:6060` and `/metrics`, the n8n task
broker `5679` and `/metrics`, Traefik `8082`, OAuth2 Proxy `44180`, the Keycloak
management port `9000`, Gatus `/metrics` and the `seaweedfs-s3` metrics port.
Loki, Tempo and Alloy also publish on the host LAN under the POL-0096 exception,
which this package does not change.

**Subnets.** `10.250.9.0/24` and `10.250.12.0/24` are free in source but held
the retired `lab_net` and the Supabase network; a stale host network could still
use them, so W2 allocates from `10.250.24.0/24` upward.

### Approval and start (2026-11-07)

After reviewing the W1 inventory the owner approved the Spec and Plan and the
W2–W4 implementation in one branch on 2026-11-07, with ADR-0061 accepted in the
same change; W5 keeps its own approval. The package first landed as `draft`
(PR #784), as new Stage 03 documents must.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0266 | draft | approved | #approval-and-start-2026-11-07 |
| SPEC-0266-PLAN-0001 | draft | approved | #approval-and-start-2026-11-07 |
| SPEC-0266-TSK-0001 | draft | ready | #approval-and-start-2026-11-07 |
| SPEC-0266-TSK-0001 | ready | in-progress | #approval-and-start-2026-11-07 |
| SPEC-0266-TSK-0001 | in-progress | completed | #owner-acceptance-2026-11-07 |

### W2–W4 implementation (2026-11-07)

W3 came first: `SsoOnlyIngressContractTests` in
`tests/validation/test_p02_service_contracts.py` renders every profile from
`.env.example` and failed on all 17 backends before any network change. W2 then
replaced each backend's `edge_net` with `<service>_ingress_net`, set
`traefik.docker.network`, attached Traefik to the 17 networks, and declared them
in the root Compose in the RedisInsight pattern (internal, isolated gateway,
`/24` from `10.250.24.0` to `10.250.40.0`, dynamic range `.128/25`).

The plan to put the two `seaweedfs-s3:9327` scrapes on the existing
`seaweedfs_metrics_net` was dropped during W2: that network reaches the
master's write-JWT and collection-delete APIs and trusts only Prometheus with
them, so adding Alloy would have widened that trust. A new internal
`seaweedfs_s3_metrics_net` (`10.250.41.0/24`) carries only `seaweedfs-s3`,
Prometheus and Alloy, and the test asserts Alloy is not on
`seaweedfs_metrics_net`. Spec 0.3.0 records the change and sharpens criterion 4
to the ingress conditions the test checks; other networks of those services
stay, so isolation from their non-ingress peers is out of this package's scope.

The existing `test_routed_services_join_edge_net` required every routed service
except Storybook and RedisInsight to be on `edge_net`; it now accepts a dedicated
`*_ingress_net` instead. The m0021 current-service inventory was re-rendered with
`render_service_inventory`, which changed exactly the 19 Network cells of the
moved services, Traefik and `seaweedfs-s3`. W4 updated AD-0026, GDE-0077, eleven
service READMEs and accepted ADR-0061. No container was recreated.

### W5 HOME apply (2026-11-07)

The owner approved W5 on 2026-11-07 together with the remaining work. Before
the apply, the owner asked to check ComfyUI's outbound access: on `main`
`c28fce98a` ComfyUI's only network is the internal `comfyui_ingress_net`, the
only one of the 17 with no outbound-capable network, so model downloads,
Manager updates and package installs would stop, and a throwaway probe on an
internal-only network showed Docker 29.9.2 does not publish its host port, so
`127.0.0.1:8188` would stop too. ComfyUI already fails external DNS today (its
resolver file has no external servers) although outbound IP works. Its seven
declared volumes are empty; the data lives in the image's undeclared anonymous
`/root` volume. The owner chose to hold ComfyUI until a sole-member egress
network is added, and to move its volume paths in SPEC-0267.

The apply ran from `main` `c28fce98a` in project `hy-home-infra` with
`up -d --no-deps`, after confirming all 15 container ids matched the recorded
pre-change snapshot. Backups were taken first under
`~/storage/backups/spec0266-w5-20261107/` with SHA256 sums: the ComfyUI `/root`
volume (live copy, 8,117 entries) and the Pyroscope anonymous `/data` volume
(with Pyroscope stopped, 24 entries). Traefik was recreated first and all 15
route codes stayed as before. Alertmanager, Alloy, cAdvisor, Flower, Loki,
Mailpit, MLflow, Prometheus, Pushgateway and Tempo were recreated next, then
Ollama with its two-file set, then `seaweedfs-s3`. The four stopped backends
were not started.

Pyroscope's crash loop (7,493 restarts since 2026-11-02 03:53) was a corrupt
`/data/v2/metastore/data/metastore.boltdb`; the pages named in the panic exist
only in that file. The owner approved a raft restore: the file was renamed to
`metastore.boltdb.corrupt-20261107`, not deleted, and Pyroscope was recreated
on the same anonymous volume. It restored the 2026-11-02 02:35 snapshot
(`applied_index=4373076`), wrote a new `metastore.boltdb`, became healthy with
no panic, and a query for 14 to 6 days ago returned 11 service names. Its route
changed from 404 to 302 because the backend is back.

Ollama took about six minutes to listen because its start command first reads
the CUDA libraries from a cold cache; it then turned healthy.

Flower failed to start. The recreate also applied an undeployed `main` change
(`e14ebe0fd`, 2026-11-02) whose `_CMD` readers call
`/opt/airflow/bin/connection_uri.py`, which the 2026-10-20 image lacks. The
owner chose to rebuild the image, and the rebuild exposed a second defect:
`COPY --chmod=0444` also gave the created `/opt/airflow/bin` mode 0444, so the
`airflow` user cannot reach the helper and every Airflow service would fail on
its next recreate. PR #787 changes the mode to 0555 with a test. The deploy tag
was restored to the previous image (`b7c57ce073b4`, also tagged
`3.3.2-keycloak-pre-20261107`); the other Airflow containers were not touched.
Flower stays down until #787 merges and its image is rebuilt.

After the apply, an unrelated `edge_net` container (`storybook-mcp`) could no
longer resolve any of the 12 moved backends, compared with 12 of 13 reached
before; ComfyUI, held, still answered. Traefik reached 11 of the 12 over their
ingress networks (Flower down). Prometheus scraped `seaweedfs-s3:9327` as up.
Its other down targets were stopped or absent services and Flower, plus Gatus,
which has crash-looped since before W5 (7,263 restarts): the bind-mounted
`config.oidc.yaml` from `0592303d1` expands `${POSTGRES_PORT}`, which the
2026-10-28 container does not have, and the render from `main` does.

The rollback was rehearsed on Pushgateway with the previous revision
`fa6135043`: it returned to `edge_net` and `obs_net`, stayed healthy with route
302 and was reachable directly again; recreated forward from `main`, it
returned to `pushgateway_ingress_net` and `obs_net`, healthy with route 302,
and direct access was refused.

### W5 completion (2026-11-07)

PR #787 (`6c8452ab3`) set the Airflow helper mode to 0555. The image was
rebuilt from `main` `5064cf6f7` and only Flower was recreated: healthy with no
restarts, connected to its broker, route 302, refused from `storybook-mcp` and
reached by Traefik. The other Airflow containers keep the previous image until
their own recreate.

The owner approved recreating Gatus. The previous image was tagged
`hy/gatus:local-pre-20261107`, and Gatus was recreated from `main` without a
rebuild: it went from 7,287 restarts to healthy, now receives `POSTGRES_PORT`,
and all 15 probes in its first minute succeeded. `status.hy.home.arpa/`
returned 200, and `/metrics` 404 because the route excludes it. Prometheus then
had 30 of 38 targets up; the eight down are stopped or absent services.

PR #789 (`78461aef1`) added the sole-member, non-internal
`comfyui_egress_net`. ComfyUI was recreated from `main` `ec9124c5a` on the same
anonymous `/root` volume (`8c60682fd5a7`; Manager, 62M of models and 20M of
user data present). It is healthy, its resolver lists the host upstream again,
`github.com` resolves, `huggingface.co` and the Manager catalog return 200,
`127.0.0.1:8188` publishes and returns 200, the route returns 302, it is
refused from `storybook-mcp` and reached by Traefik, and `comfyui_egress_net`
has no other member.

The four stopped backends (Kafka Connect, Kafka REST Proxy, Schema Registry,
Terrakube UI) were not started; their next start uses the new networks, and the
render test covers their configuration.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | Draft reachability and flow scan | `56104a49e`, public render | NOT_RUN | Approximate draft input only; the source-read inventory is W1 | optional | - |
| E2 | 1 | W1 | Source-read authentication and flow inventory of 38 `edge_net` members | `56104a49e` | PASS | Inventory above with a source line per row; in-scope list and flows corrected in Spec 0.2.0 | required | - |
| E3 | 4 | W3 | `SsoOnlyIngressContractTests` before and after W2 | `15be6a84f` then this branch | PASS | All 17 subtests failed before W2; 3 tests OK after | required | - |
| E4 | 2, 3 | W2 | All-profile public render, `validate-docker-compose.sh`, `check-all-hardening.sh` | This branch | PASS | 65 selections valid; all hardening tiers pass; `test_p02_service_contracts` 29 OK | required | - |
| E5 | 2, 3 | W2 | Network regression suites (baseline gates, wiring, runner isolation, runtime compatibility, port, P02 native/Prometheus, compose_start, port inventory, connections, tier layout, Crawl4AI) | This branch | PASS | 311 tests OK, 39 declared skips, after the `edge_net` routing test accepted dedicated ingress | required | - |
| E6 | 5 | W4 | Metadata, link, lifecycle and operations-catalog checks | This branch | PASS | See the PR validation block | required | - |
| E7 | 6 | W5 | HOME recreation of Traefik, `seaweedfs-s3`, Pyroscope, Ollama and ten backends; route codes; direct reach from `storybook-mcp`; Traefik reach; `seaweedfs-s3:9327` scrape | `c28fce98a` | PASS | Work log "W5 HOME apply"; routes unchanged except Pyroscope 404→302 and Flower; all 12 recreated backends refused directly; Traefik reached 11 (Flower down) | required | - |
| E8 | 6 | W5 | Flower recreate | `c28fce98a` | FAIL | Image lacks `connection_uri.py`; the rebuild is unreadable by `airflow` (PR #787) | required | - |
| E9 | 6 | W5 | ComfyUI recreate | - | NOT_RUN | Held by the owner until a sole-member egress network lands | required | - |
| E10 | 6 | W5 | Rollback rehearsal on Pushgateway | `fa6135043` then `c28fce98a` | PASS | Previous networks and direct reach restored, then refused again | required | - |
| E11 | 6 | W5 | Pyroscope metastore raft restore | `c28fce98a` | PASS | Snapshot `applied_index=4373076` restored; healthy; 11 services queryable for 14–6 days ago | optional | - |
| E12 | 6 | W5 | Flower recreate | `5064cf6f7` | PASS | Rebuilt image; healthy; route 302; refused directly; reached by Traefik | required | E8 |
| E13 | 6 | W5 | ComfyUI recreate | `ec9124c5a` | PASS | With `comfyui_egress_net`; data volume kept; DNS and HTTPS egress; host port 200; route 302; refused directly; sole egress member | required | E9 |
| E14 | 6 | W5 | Gatus recreate (owner-approved, outside the package) | `5064cf6f7` | PASS | Crash loop ended; 15 of 15 probes succeeded | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | E2 | Accepted by the owner on 2026-11-07 | @buenhyden |
| 2 | accepted | E4, E5 | Accepted by the owner on 2026-11-07 | @buenhyden |
| 3 | accepted | E4, E5 | Accepted by the owner on 2026-11-07 | @buenhyden |
| 4 | accepted | E3 | Accepted by the owner on 2026-11-07 | @buenhyden |
| 5 | accepted | E6 | Accepted by the owner on 2026-11-07 | @buenhyden |
| 6 | accepted | E7, E10, E11, E12, E13 | Accepted by the owner on 2026-11-07 | @buenhyden |

## Review and Completion

W1–W5 are done and every criterion has PASS evidence.

### Owner acceptance (2026-11-07)

The owner accepted SPEC-0266 on 2026-11-07 after the W5 completion evidence
merged (#790), and the Task closed as `completed`. The four stopped backends
take the new networks on their next start. Two follow-ups moved to SPEC-0267:
the undeclared ComfyUI and Pyroscope data volumes and the secondary listeners.
ComfyUI's unrestricted outbound access through `comfyui_egress_net` remains an
open owner decision (egress allowlist or accepted risk).

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [ADR-0061](../../../02.architecture/decisions/0061-dedicated-ingress-for-sso-only-backends.md)
