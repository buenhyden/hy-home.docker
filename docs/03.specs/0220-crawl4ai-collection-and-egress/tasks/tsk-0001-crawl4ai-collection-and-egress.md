---
title: "Crawl4AI Collection and Egress Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0220-TSK-0001"
parent_ids:
- "SPEC-0220-PLAN-0001"
created: "2026-10-09"
---

# Crawl4AI Collection and Egress Task

## Objective

Enforce Crawl4AI egress outside its container, define the source rights
registry and consumer admission, ship a reference adapter with a bounded job
model, and prove the path with local fixtures and an isolated rehearsal of the
real image.

## Inputs and Authorization

The current user request on 2026-10-09 asks to execute prompt 07 of the
analysis pack (Crawl4AI collection, provenance, egress and reprocessing) with
per-unit commits and a per-Spec PR merge. Baseline `main` `5f4832a74`
(SPEC-0219 and its follow-up merged). SPEC-0212 routes request item 04
("Crawl4AI use") to this prompt; SPEC-0204 TSK-0001 still lists the Crawl4AI
egress-deny runtime evidence as `NOT_RUN`, which this Task supplies from an
isolated rehearsal. Starting `crawl4ai` on HOME, admitting a consumer,
collecting real data and changing host firewall rules are not part of this
request.

## Work Log

### Starting State

`infra/08-ai/crawl4ai/docker-compose.yml` pins `unclecode/crawl4ai:0.9.4` by
tag on the `crawl4ai_net` bridge, as `appuser` with a read-only root, tmpfs
state, `mem_limit` 4g, `pids_limit` 512, `shm_size` 1gb and a token read from
a secret file and checked for length. The bridge is not internal, so the
container reaches the host, the LAN and the internet directly. Open Notebook
mentions Crawl4AI only in commented settings; no consumer is connected, and no
source registry, job model or adapter exists.

### W1 Baseline and Contracts

Official facts, read on 2026-10-09 from the GitHub advisory APIs, the `v0.9.4`
tag (`133e1d92e37885dfccc03ea2e3687d06c98b7ceb`) and the registry:

- 19 repository advisories; none has an affected range that includes 0.9.4.
  GHSA-6qhc-x826-342c (CVE-2026-53755, proxy settings bypass the URL check)
  affects `<=0.8.8`, fixed in 0.8.9. GHSA-5w5p-vcv6-mm3f (untrusted config
  gate), GHSA-wh5w-hmj3-vgg7 (link preview SSRF) and GHSA-f77g-77vp-r96v
  (robots fetch SSRF) affect `<=0.9.3`, fixed in 0.9.4.
- Index `sha256:9021b3cb5c6f12570bbcd5395638495e0a06969b3148e377b953d174af2ebc9b`,
  `linux/amd64` `sha256:048848e5…`, `linux/arm64` `sha256:5370d96c…`,
  released 2026-09-23.
- In-image controls: `deploy/docker/egress_broker.py` refuses non-global
  addresses after unwrapping transition forms and pins one answer; Chromium
  goes through a local pinning proxy; untrusted bodies may not set proxies,
  `extra_args`, scripts or deep crawl strategies; webhooks re-check each
  redirect; `CRAWL4AI_UPSTREAM_PROXY` chains the pinning proxy upstream with
  `CONNECT <pinned-ip>:<port>`, so an upstream proxy sees addresses, not
  hostnames. The job API has `processing`, `completed` and `failed` states, a
  one-hour Redis TTL and no cancel endpoint.
- On this host (Docker 29.8.2) a container on an internal-only network cannot
  resolve external names; with `dns` set to a forwarder on the same internal
  network it can.

The Spec records the contracts, and the Plan compares the three project
candidates.

### W2 Egress Gateway

`crawl4ai` now joins only `crawl4ai_net` and `crawl4ai_egress_net`, both
`internal: true`, with `dns` and `CRAWL4AI_UPSTREAM_PROXY` set to
`10.250.200.2`, and its image is pinned by the 0.9.4 index digest. The new
`crawl4ai-egress` service runs `infra/08-ai/crawl4ai/egress_gateway.py` on the
repository's `python:3.13.15-alpine` image as `65534:65534`, read-only, with
`cap_drop: ALL` and `net.ipv4.ip_unprivileged_port_start=53` instead of a
capability; it alone joins `crawl4ai_outbound_net`, an ordinary bridge. The
gateway allows only global unicast IPv4 on ports 80 and 443, refuses every
IPv6 form, dials the address it checked, sends one request per plain HTTP
connection, strips proxy headers and logs host and address only. The DNS relay
answers AAAA with no records and forwards other queries to Docker's resolver.

`tests/validation/test_crawl4ai_egress.py` (11 tests) covers the address rule
(private, loopback, link-local, metadata, shared, documentation, multicast,
reserved and every IPv6 form), port and literal refusals, integer and hex
loopback forms through the real resolver, mixed DNS answers, a rebinding
answer that changes after the check, CONNECT tunnelling, plain HTTP header
handling, malformed requests, the AAAA answer and the relay, and the Compose
contract. The existing runtime test now reads the version before the digest.
The tech-stack registry, POL-0078, GDE-0091's service binding, the Grafana
coverage table and the m0021 inventory list `crawl4ai-egress`; the gate
contract runs the new module in `leaf.compose-baseline-regressions`.

### W3 Reference Adapter

`projects/crawl4ai/adapter/crawl_jobs.py` is a standard-library module that a
consuming workspace pins. Its registry check refuses a source without
provider, access mode, exact hosts, terms, license, robots observation, rate,
daily quota, the three rights flags, retention, deletion owner and consumer,
and a `web-fallback` without its reason; admission refuses unknown sources,
unregistered hosts, other ports, sources that forbid processing and sources
whose robots file disallows. Jobs move through the six states in SQLite with
a unique idempotency key, exponential backoff from 30 s capped at 15 min, a
deadline, a 5-minute lease that `recover()` returns to the queue with the
attempt counted, a per-source rate and daily quota that defer without
spending attempts, a response byte limit and a request time capped by the
deadline. Raw records keep source, URL, final URL, SHA-256, `retrieved_at`,
registry revision, license and a retention expiry; derived records reference
their raw hash with `ON DELETE CASCADE` and their own TTL. A redirect off the
registry keeps nothing. Extractions must use declared, typed fields that
quote the raw text, and `evaluate()` scores a golden set.

`tests/validation/test_crawl4ai_adapter.py` (15 tests) runs against a local
synthetic Crawl4AI endpoint: provenance on success, blocked admission without
any call, a redirect off the registry, oversize, malformed and mismatched
results, a bad token, 5xx retry to success and to exhaustion, a timeout, a
deadline, idempotency, cancel before and during a run, lease recovery, rate
deferral, TTL and source deletion, and the extraction checks, including a
golden case whose text tries to inject an instruction. The example registry
uses the reserved `example.org` domain. The gate contract runs the module.

### W4 Isolated Rehearsal

`Crawl4AIEgressRehearsalTests` (opt-in with `HYHOME_CRAWL4AI_REHEARSAL=1`,
registered as an optional runtime skip) ran the pinned image
(`linux/amd64` pulled by the index digest; `appuser` is uid 999, matching the
Compose tmpfs owners) with the Compose command, user, tmpfs, memory, pids and
shm values, behind the real gateway. All four networks were internal: an API
network with a probe, the gateway network `10.250.201.0/29`, a
"world" network `11.200.0.0/24` whose fixture `public.fixture` has the
globally routable form `11.200.0.10`, and a LAN network `10.250.202.0/24` with
`lan.fixture`; the token was generated per run.

Six tests passed on 2026-10-09:

| Case | Result |
| --- | --- |
| `/health` without token; `/crawl` without token | 200; 401 |
| Allowed page with `check_robots_txt` | 200 with its marker; the gateway logged `GET 11.200.0.10` (the broker sends the pinned address) |
| `http://lan.fixture/secret`; `http://169.254.169.254/` | 400; 400 |
| Redirect to the LAN host; redirect to the metadata address | No marker in the result; the LAN fixture logged no request |
| Page with a LAN image (subresource) | The LAN fixture logged no request for it |
| Meta refresh to `127.0.0.1:11235/health` | No health document in the result |
| Caller `proxy_config`; `extra_args` with `--proxy-server` | 400; 400 |
| Crawler connecting directly to `11.200.0.10:80` or the LAN host | No route (`OSError`) |
| Crawler `CONNECT` through the gateway to `11.200.0.10:80`; to `lan.fixture:80`; to port 22 | 200; 403; 403 |
| Crawler container | 4 GiB, 512 pids, 1 GiB shm, read-only root, `cap_drop: ALL`, `appuser` |

The first runs failed in the test itself: the Compose command's `$$` escape
reached `docker create` unchanged, a class attribute shadowed
`TestCase.run`, an interrupted run left networks that overlapped the next
run's subnets (removed), and the gateway logs the pinned address rather than
the name. No rehearsal container or network remained after the passing run.
Host firewall rules were not part of this rehearsal; the enforcement shown is
the network topology plus the gateway.

### W5 Operations Documents

POL, GDE and RUN-0091 (Korean) and both READMEs describe the internal
networks and gateway, consumer admission, the source rights registry, the
remaining risks and the rehearsal step. The first changed gate failed six
links: READMEs outside `docs/` may link only to `docs/README.md`, so they now
cite stage documents by path (`27895b78b`).

### W6 Independent Review

A security audit and a correctness review read `5f4832a74..27895b78b`
independently and ran nothing. Neither found a high or critical issue; the
gateway's address and port rules held against bracketed, mapped, integer,
octal, short and trailing-dot forms, userinfo, mixed answers and rebinding.
Every finding was fixed or recorded:

| Finding | Resolution |
| --- | --- |
| Plain HTTP passed later client bytes to the origin, so "one request per connection" did not hold | Only the declared `Content-Length` body is forwarded; `Transfer-Encoding`, duplicate or invalid lengths and bodies over 1 MiB get 400 (`af59f6daf`) |
| Per-direction idle timeouts cut long responses; a client half-close dropped the response | One idle timer for both directions, `write_eof` on half-close, a 15-minute connection limit (`af59f6daf`) |
| DNS relay: unbounded tasks; any sender's datagram accepted | 64 queries in flight; a connected upstream socket and a matching query id (`af59f6daf`) |
| Listeners on `0.0.0.0` also served `crawl4ai_outbound_net` | The gateway binds to `10.250.200.2` only, and its healthcheck uses that address (`af59f6daf`) |
| Gateway image pinned by tag | Pinned by the `python:3.13.15-alpine` index digest (`af59f6daf`) |
| No evidence for the crawler reaching a consumer on `crawl4ai_net` | The rehearsal adds a consumer fixture beside the crawler; a direct crawl got 400 and an embedded image reached nothing (`af59f6daf`); the residual risk stays in the Spec |
| Rehearsal token on the `docker` command line; a failed fixture start could leave a container | The token goes through the process environment; names are recorded before create (`af59f6daf`) |
| Adapter: `\`, userinfo or an invalid port could make the adapter and the browser disagree, and an empty `redirected_url` fell back to the request URL | Such URLs are blocked and a missing final URL is malformed (`42b719d22`) |
| Adapter: queued jobs were not re-admitted, and a removed source raised `KeyError` | The registry is checked again at claim time; the job is blocked (`42b719d22`) |
| Adapter: raw records deduplicated by hash shared provenance, retention and deletion across sources | One raw record per job; derived rows reference its id (`42b719d22`) |
| Adapter: rate and quota counted jobs, not requests | An `attempts` row per claim is counted, and purged after a day (`42b719d22`) |
| Adapter: an unchecked claim could fetch twice; `http.client` errors escaped | A lost claim returns without fetching; those errors are retryable (`42b719d22`) |
| `__main__` before the rehearsal class; Task placeholders | Moved to the end of the file; placeholders replaced |
| The host's own public or NAT-loopback address passes the global rule | Recorded in the Plan's risks |

Every new test failed against the code before its fix: four gateway tests
(six failures with subtests) and six adapter tests. After the fixes the gateway
module runs 21 tests (six rehearsal tests skipped without opt-in) and the
adapter module 21, all passing, and the rehearsal passed six of six again with
the consumer cases and left nothing behind.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline and contracts | 4, 5 | W1 | Advisory and tag reads; DNS probe | `5f4832a74` | PASS | W1 Baseline and Contracts | accepted |
| Egress gateway | 1 | W2 | Gateway, relay and Compose unit tests; catalog checks | `8cd81db4b` | PASS | W2 Egress Gateway | accepted |
| Reference adapter | 3 | W3 | Adapter tests against a synthetic endpoint | `b72476aed` | PASS | W3 Reference Adapter | accepted |
| Isolated rehearsal | 2 | W4 | Real image behind the gateway, six tests | `f20f626ce` | PASS | W4 Isolated Rehearsal | accepted |
| Operations documents | 5 | W5 | Link, metadata and catalog checks | `27895b78b` | PASS | W5 Operations Documents | accepted |
| Independent review | 1, 2, 3 | W6 | Security and correctness review; fix tests; rehearsal rerun | `42b719d22` | PASS | W6 Independent Review | accepted |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
