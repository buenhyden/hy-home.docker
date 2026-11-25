---
title: "D02 v8 Network and Gateway Authentication Task"
version: "0.1.8"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-25"
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

##### Blockers and Decisions

Server B and root on server A are unavailable to this session, so B-side and
firewall evidence stays NOT_RUN rather than inferred from A-side results.

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

##### Resolution Links

E05 resolves E04; E11 resolves E09; E13 resolves E10; E16 resolves E06.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 173 | accepted | E01,E02,E03,E05,E07,E08,E11,E12,E13,E14,E15,E16 | Owner @buenhyden accepted on 2026-11-25 in this chat after the server A census, the route-table fix, the Hermes loopback bind, every server B check and OpenClaw searching through the server B loopback proxy; the server A host firewall rules were not read, and exposure is judged from listeners and server B probes | @buenhyden |

##### Remaining Conditions

None for criterion173.

#### Handoff

##### Promotion Receipt

GDE-0079 carries the corrected route table; the regression keeps it aligned
with the route contract.

##### Next Owner

The owner runs the B-side checks and decides the 8644 listener; no other
prompt is started automatically.

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
