---
title: "D02 v8 Network and Gateway Authentication Task"
version: "0.1.10"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0117"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-25"
---

# D02 v8 Network and Gateway Authentication Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion173/W189 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply D02 of the lifecycle v8 task prompts: reuse the accepted Traefik, DNS,
TLS and machine-route contracts, observe every route from server A, close the
GDE-0079 route-table drift, and route the B-side acceptance and open host
items to their owner.

##### Inputs and Authority

On 2026-11-25 the user directly requested D02 from
`_workspace/workspace_task_prompts_20261125_lifecycle_v8/` (prompt
`02_network_auth_gateway.md`), limited to that prompt's scope, with commit,
push, PR and merge after checks. In this chat the owner chose to record the
host Hermes webhook listener as an open item rather than change it. Work ran
on branch `docs/d02-route-auth-matrix` in the linked worktree
`.claude/worktrees/d02` from `main` `0bc8e76de`; brief
`d02-agent-health-restore` revision 2 bound the paths before the first edit.
This session has no shell on 192.168.0.22 and no root on server A. Direct
user authorization is authority; this record is not.

On 2026-11-27 the user directly requested D02 again from
`_workspace/workspace_task_prompts_20261127_progress_v9/`, limited to that
prompt's scope: reuse the accepted result, record only the differences, and
commit, push, PR and merge. Work ran in the primary checkout on branch
`docs/d02-v9-network` from clean `main` `6284c1222`; brief `d02-v9-network`
revision 1 bound this file only.

#### Execution Log

##### Work Performed

###### Route census and A-side probes

Every `traefik.http.routers.*.rule` in the rendered Compose labels (all
profiles) and every router in `infra/01-gateway/traefik/dynamic/*.yml` was
collected: 47 routers and 38 distinct hosts, equal to the package's static
count. Each host was requested once from server A as
`https://<host>/` with `--resolve <host>:443:192.168.0.13`, the public
`rootCA.pem`, no credentials and no TLS bypass:

| Result | Hosts |
| --- | --- |
| TLS verified (`ssl_verify_result=0`) | all 38 |
| 302 to the Keycloak realm (SSO chain) | alertmanager, alloy, cadvisor, hermes, loki, mailpit, mlflow, ollama, prometheus, pyroscope, qdrant, redisinsight, searxng, storybook, tempo |
| Native login redirect or page | airflow 200, dozzle 307 `/login`, grafana 302 `/login`, kafbat-ui 302 OAuth2, keycloak 302 `/admin/`, n8n 200, openbao 307 `/ui/`, status (Gatus) 200 |
| Gateway or app credential refusal | dashboard 401, s3 403 |
| 404, no running backend or no root route | auth (oauth2-proxy serves `/oauth2/*`), blog-export `/`, comfyui, flower, neo4j, open-notebook, opensearch, opensearch-dashboard, pushgateway, storybook-mcp `/`, terrakube-api, terrakube-executor, terrakube-ui |

Targeted machine paths and negatives from server A:

| Request | Result | Reading |
| --- | --- | --- |
| `searxng/search` and `prometheus/api/v1/…` without `Authorization` | 302 to SSO | `searxng-api` and `prometheus-api` match only `Authorization: Basic`; others fall to the SSO router |
| `searxng/search` with an invalid Basic credential | 401 | Traefik basic auth refuses |
| `storybook-mcp/mcp` without a token | 401 | Bearer resource server refuses |
| `blog-export/v1/exports` from A | 403 | Export routes allow only 192.168.0.22 |
| `n8n/webhook/hermes-blog-ingestion` with GET | 404 | Exact POST route only |
| `s3/` with a forged `X-Forwarded-For: 192.168.0.22` | 403 | No credential, no bypass |
| Unknown host `nonexistent-route` | 404 | No backend is selected |
| Default certificate for an unknown SNI | `*.hy.home.arpa`, `hy.home.arpa` | Single-label wildcard only |
| Listeners on :80/:443 | `192.168.0.13:80`, `192.168.0.13:443` only | LAN bind as declared |

###### GDE-0079 route-table drift

`ROUTES_WITHOUT_SSO` in `tests/validation/test_compose_baseline_gates.py`
named `searxng-api`, but the GDE-0079 table did not, and only a comment tied
the two. The new `test_guide_route_table_names_exactly_the_exempt_routers`
failed on exactly `searxng-api` before the guide change and passes after it;
the guide row now also states that the two Basic API routers match only
requests with that header.

###### Host observations on server A

- `hermes-gateway.service` and `hyhome-hermes-dashboard.service` run as user
  units; `hermes-attester.timer` is active. Hermes OTLP listens on
  `127.0.0.1:4320`.
- The host Hermes Agent's own `webhook` platform listens on `0.0.0.0:8644`
  and `[::]:8644`, outside Traefik and the repository, and answers HTTP on
  `192.168.0.13:8644`. Its routes include `homeassistant`. The host firewall
  could not be read without root. Owner choice: record it as open. Check from
  192.168.0.22: `curl -sS -o /dev/null -w '%{http_code}' http://192.168.0.13:8644/`.
  Fixes: bind the platform to `127.0.0.1` if nothing on the LAN posts to it,
  or allow only the Home Assistant address in the host firewall.
- Follow-up on 2026-11-25: the owner set the rule that the listener binds to
  loopback if nothing on the LAN posts to it. No webhook route is configured,
  the gateway logs hold no inbound request, no Home Assistant runs on this
  host, and `homeassistant` is only the platform's toolset. The owner set
  `platforms.webhook.extra.host: 127.0.0.1` in `~/.hermes/config.yaml`
  (backup `~/.hermes/backups/config.yaml.pre-webhook-loopback`) and restarted
  `hermes-gateway`. It now listens on `127.0.0.1:8644` only; `192.168.0.13:8644`
  refuses the connection and loopback answers 404.
- 192.168.0.22 answers ICMP; no B process, resolver, CA store or OpenClaw
  configuration was observable from this session.

###### Not done here and why

| Item | State | Owner and precondition |
| --- | --- | --- |
| B resolver, TCP, TLS, browser login and API calls for all 38 hosts | NOT_RUN | Owner on 192.168.0.22 (Windows and WSL accounts) |
| B OpenClaw and A Hermes Agent consuming supported services through Traefik | NOT_RUN | Owner; installed versions and credentials on each host |
| Old SearXNG credential refused after rotation | NOT_RUN | Owner rotation of AI-011/INFRA-008 (TSK-0116) first |
| Hermes webhook listener on 0.0.0.0:8644 | closed | Bound to 127.0.0.1 (E07); B-side refusal check stays with the owner |
| Webhook and gateway integrity (D02-T04) | REUSE | SPEC-0204 TSK-0022 records the exact routes, IP allow-lists and live deliveries; no new defect observed |
| Minimal network design (D02-T03) | REUSE | No new caller or reachability defect observed; no network change |

###### v9 difference pass (2026-11-27)

Criterion173 and the rows above are reused. Only routes and consumers that
changed after `0bc8e76de` were re-observed, from server A at `6284c1222`.

| Task | Observed | Versus v8 | State |
| --- | --- | --- | --- |
| T01 routes | 45 routers (39 Docker label, 6 file provider) and 35 distinct hosts; the file provider spells three hosts as `<name>.{{ env "DEFAULT_URL" }}` | `terrakube-api`, `terrakube-executor`, `terrakube-ui` routers and hosts removed (SPEC-0263 TSK-0004); router `ollama-api` added on the existing `ollama` host | REUSE with the difference |
| T01 A probes | 35/35 hosts TLS verified with the public CA, same codes as E02 for every remaining host; `terrakube-ui` now 404 (no router) | 38 → 35 hosts | PASS |
| T01 listeners | `192.168.0.13`: 80, 443 (Traefik), 3100 (Loki), 3200 (Tempo), 4317 and 4318 (Alloy OTLP), 26379 (`mng-valkey`); every other host port on `127.0.0.1`, including 8644 and 11434 | E03 read only 80/443 | REUSE: the five non-gateway LAN ports are the owner-accepted exposure of POL-0096-R22 (SPEC-0267, 2026-11-07), not a new defect |
| T02 `ollama-api` | No credential 302 (SSO); wrong Basic 401; wrong Basic on `/api/pull` and `DELETE /api/delete` 302 (unlisted paths fall to SSO); Bearer on `/v1/models` 302; forged `X-Forwarded-For: 192.168.0.22` 302 | New router; positive call reused from TSK-0118 E24 | PASS for the negatives; positive REUSE |
| T02 A Hermes | All Hermes Agent profiles call local Ollama at `http://127.0.0.1:11434/v1` (TSK-0118 E30, E32); the `ops-console` profile starts MCP containers with `docker run --network` on `ai_net` (Qdrant), `obs_net` (Grafana) and `dev_data_net` (DEV Valkey), and reaches MNG Valkey on `192.168.0.13:26379` and the DB loopback ports; its secret fields are environment references and the file is mode 0600 | Not observed in v8 | Owner decision 2026-11-27: loopback Ollama stays as the approved same-host exception; it is local function evidence and is not counted as Traefik evidence |
| T03 | No new caller or network; the MCP joins above are host-side `docker run` choices outside the repository | - | REUSE for Compose; owner decision 2026-11-27: the MCP joins stay as a recorded residual risk |
| T04 | Exact routes, allow-lists and rate limits unchanged since SPEC-0204 TSK-0022 | - | REUSE |
| T05 | GDE-0079 lists `ollama-api` with the Basic-header rule; `RouteAuthContractTests` pass | - | REUSE |

Correction to E16: the server B probes (E09 to E13) covered the 38 hosts and
port 8644 only. "Only 80 and 443 answer" holds for those probes, not for every
port; the POL-0096-R22 ports above are published on the LAN by design and were
not probed from server B.

###### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0117 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0117 | ready | in-progress | #work-performed |
| SPEC-0212-TSK-0117 | in-progress | completed | #criterion-decisions |

##### Blockers and Decisions

Server B and root on server A are unavailable to this session, so B-side and
firewall evidence stays NOT_RUN rather than inferred from A-side results.

v9: the prompt routes host consumers' supported functions through
authenticated Traefik, while the owner-accepted A Hermes configuration calls
Ollama on loopback and joins shared Docker networks for MCP. Changing
`~/.hermes` is a host change outside this repository, so the owner chose in
this chat on 2026-11-27:

| Item | Decision | Residual and resume condition |
| --- | --- | --- |
| A Hermes local Ollama at `127.0.0.1:11434` | Keep loopback as the approved same-host exception; the `local` profile and its empty fallback chain stay unchanged | None; resume only if Ollama leaves server A or the owner asks for gateway-only access, then route through `ollama-api` with a D07 machine credential |
| `ops-console` MCP containers on `ai_net`, `obs_net`, `dev_data_net` | Keep; record as residual risk | Each MCP container can reach every peer on its shared network, not only its target; resume on a separate owner request (Grafana can move to the gateway with its service-account token; Qdrant needs a new machine route) |

No host file was changed.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 173 | W189 | method=observation; tool=docker compose, PyYAML; command=router rules from rendered labels and dynamic files | `main` 0bc8e76de | PASS | 47 routers, 38 hosts | required | - |
| E02 | 173 | W189 | method=observation; tool=curl; command=unauthenticated GET per host via 192.168.0.13 with the public CA | Server A, 2026-11-25 | PASS | 38/38 TLS verified; classes above | required | - |
| E03 | 173 | W189 | method=observation; tool=curl, openssl, ss; command=machine paths, negatives, default certificate, listeners | Server A, 2026-11-25 | PASS | Table above | required | - |
| E04 | 173 | W189 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_compose_baseline_gates.RouteAuthContractTests | Change before the guide edit | FAIL | Guide table lacks `searxng-api` | required | - |
| E05 | 173 | W189 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_compose_baseline_gates.RouteAuthContractTests | Change after the guide edit | PASS | OK | required | E04 |
| E06 | 173 | W189 | method=observation; tool=-; command=- | Server B and A firewall | NOT_RUN | Owner items above | required | - |
| E07 | 173 | W189 | method=observation; tool=ss, curl, systemctl; command=ss -ltn sport 8644; curl LAN and loopback; is-active hermes-gateway | After the owner's config change and restart, 16:44 KST | PASS | `127.0.0.1:8644` only; LAN `000`, loopback 404; gateway active | required | - |
| E08 | 173 | W189 | method=observation; tool=Windows browser; command=- | 192.168.0.22, owner, 2026-11-25 | PASS | Owner reported successful login to Grafana, Keycloak, n8n, OpenBao and Gatus from server B | required | - |
| E09 | 173 | W189 | method=observation; tool=curl in WSL; command=unauthenticated GET per host with the public CA; `curl http://192.168.0.13:8644/` | 192.168.0.22 WSL, owner, 2026-11-25 | FAIL | 31 of 38 hosts return the same codes as server A with `tls=0`; `8644 000`; opensearch-dashboard, opensearch, pyroscope, s3, terrakube-api, terrakube-executor and terrakube-ui do not resolve in WSL (`000`), whose hosts list names only some hosts | required | - |
| E10 | 173 | W189 | method=observation; tool=PowerShell 7 Invoke-WebRequest; command=GET per host without redirect following; `GET http://192.168.0.13:8644/` | 192.168.0.22 Windows, owner, 2026-11-25 | FAIL | Codes 200, 401 and 404 match server A; hosts that redirect on server A raise the PowerShell 3xx exception, with no TLS error; 8644 closed; the same seven names fail with "no such host", so the Windows hosts list (which WSL copies) lacks them | required | - |
| E11 | 173 | W189 | method=observation; tool=curl in WSL; command=unauthenticated GET per host with the public CA; `curl http://192.168.0.13:8644/` | 192.168.0.22 WSL after the owner added the seven names to the Windows hosts list, 2026-11-25 | PASS | All 38 hosts return the same codes as server A with `tls=0` (opensearch and terrakube 404, pyroscope 302, s3 403); `8644 000` | required | E09 |
| E12 | 173 | W189 | method=observation; tool=curl in WSL; command=SearXNG `/search?format=json` with the new credential from a 0600 file | 192.168.0.22 WSL, owner, 2026-11-25 | PASS | 200 with a JSON `results` list (RUN-0110 step 7) | required | - |
| E13 | 173 | W189 | method=observation; tool=PowerShell 7 Invoke-WebRequest; command=GET per host without redirect following; `GET http://192.168.0.13:8644/` | 192.168.0.22 Windows after the hosts change, owner, 2026-11-25 | PASS | All 38 hosts connect with no TLS or name error: 200, 401, 403 and 404 match server A and the hosts that redirect on server A raise the PowerShell 3xx exception; the port 8644 probe was not repeated (closed in E10 and E11) | required | E10 |
| E14 | 173 | W189 | method=observation; tool=PowerShell 7, curl; command=loopback SearXNG proxy on server B: `GET /other`, `/search?format=json`, listener address, proxy log | 192.168.0.22 Windows, owner, 2026-11-25 | PASS | `other 404`; 53 results through `http://127.0.0.1:8889/search`; listens on 127.0.0.1 only; upstream 200 twice | required | - |
| E15 | 173 | W189 | method=observation; tool=OpenClaw 2026.11.309.0 SearXNG plugin; command=web search with `baseUrl` set to the HOME URL, then to the loopback proxy | 192.168.0.22 Windows, owner, 2026-11-25 | PASS | With `https://searxng.hy.home.arpa` the search fails (no Basic header, SSO redirect); with `http://127.0.0.1:8889` OpenClaw searches through SearXNG successfully | required | - |
| E16 | 173 | W189 | method=observation; tool=-; command=- | Server B checks E08, E11 to E15 and the server A listener readout, 2026-11-25 | PASS | Server B side done; from server B only 80 and 443 answer on 192.168.0.13 and 8644 is closed; the server A host firewall rules were not read (no root), so exposure is judged from the listeners and the server B probes | required | E06 |
| E17 | 173 | W189 | method=observation; tool=PowerShell 7 ScheduledTasks; command=task action through `conhost.exe --headless`, listener, search through the proxy, task state | 192.168.0.22 Windows, owner, 2026-11-25 22:02 KST | PASS | No console window; listens on 127.0.0.1 only; 53 results; task `Running` and set to start at logon | optional | - |
| E18 | 173 | W189 | method=observation; tool=docker compose 5.6.1, PyYAML; command=router rules from rendered labels and dynamic files | `main` 6284c1222 | PASS | 45 routers, 35 hosts | optional | - |
| E19 | 173 | W189 | method=observation; tool=curl; command=unauthenticated GET per host via 192.168.0.13 with the public CA | Server A, 2026-11-27 | PASS | 35/35 TLS verified; codes equal E02 | optional | - |
| E20 | 173 | W189 | method=observation; tool=curl, ss; command=ollama-api negatives (none, wrong Basic, unlisted path, Bearer, forged XFF); listeners | Server A, 2026-11-27 | PASS | 302, 401, 302, 302, 302; LAN ports as in the v9 table | optional | - |
| E21 | 173 | W189 | method=automated; tool=Python3.12.3; command=python3 -m unittest tests.validation.test_compose_baseline_gates.RouteAuthContractTests | `main` 6284c1222 | PASS | OK | optional | - |
| E22 | 173 | W189 | method=observation; tool=Python3.12.3; command=URL hosts and network arguments from `~/.hermes` profile configs, values redacted | Server A, 2026-11-27 | PASS | Loopback Ollama in every profile; `ops-console` MCP on `ai_net`, `obs_net`, `dev_data_net` | optional | - |

##### Resolution Links

E05 resolves E04; E11 resolves E09; E13 resolves E10; E16 resolves E06.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 173 | accepted | E01,E02,E03,E05,E07,E08,E11,E12,E13,E14,E15,E16 | Owner @buenhyden accepted on 2026-11-25 in this chat after the server A census, the route-table fix, the Hermes loopback bind, every server B check and OpenClaw searching through the server B loopback proxy; the server A host firewall rules were not read, and exposure is judged from listeners and server B probes | @buenhyden |

##### Remaining Conditions

None for criterion173. The v9 A Hermes path (E22) was decided by the owner on
2026-11-27 (Blockers and Decisions); the MCP network joins stay a recorded
residual risk, not a remaining condition.

#### Handoff

##### Promotion Receipt

GDE-0079 carries the corrected route table; the regression keeps it aligned
with the route contract.

##### Next Owner

The B-side checks and the 8644 listener are done (E07, E16), and the A Hermes
path is decided. The MCP residual resumes only on a separate owner request;
D06 owns the Hermes model profile and D07 any new machine credential. No
other prompt is started automatically.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
