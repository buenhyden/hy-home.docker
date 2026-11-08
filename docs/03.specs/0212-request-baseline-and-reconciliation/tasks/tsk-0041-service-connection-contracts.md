---
title: "Service Connection Contracts Task"
version: "0.1.21"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0041"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-02"
---

# Service Connection Contracts Task

## Overview

### Objective

Implement P02.01–P02.05 as a bounded local source and isolated-test unit. This
Task owns the current connection-contract routing and evidence. It is distinct
from the completed historical P02 secret catalog in SPEC-0204. It does not
grant operating, host, credential, external-repository or remote-CI authority.

## Inputs and Authorization

The direct user request of 2026-11-02 authorizes the approved P02 plan,
including local source, documentation, test and logical-commit work. The source
starts at `b79cbb9f3f49af8cd0e654c2ca1c4b9ea7632af0`. The issuing observation
was on `codex/p01-workspace-inventory`; implementation is on the separately
observed clean branch `codex/p02-integration-network-auth-valkey`. The current
P01 inventory and DATA-0096 are bounded inputs;
they do not replace canonical Compose, Secret, port or version ownership.

At `2026-11-01T22:20:38Z`, the read-only query
`git ls-remote --exit-code origin refs/heads/main` first failed in the default
sandbox with DNS exit 128. The same query then succeeded through the approved
scoped execution path and returned
`ac573aaa1c0db602e16cdb6e68678ea4d6cfb14d`. No fetch, pull, reset, push or
remote mutation was performed. The remote result is a comparison receipt; P02
implements from the separately recorded local baseline.

Shared MNG Valkey remains the selected default. Existing named n8n ACL and
dedicated broker configurations are opt-in contracts, not a topology change.
The approved Grafana exception is only GET/HEAD on `/favicon.ico` and
`/robots.txt`; unsafe methods must end at `noop@internal` with `418` before the
normal Grafana route. Existing Grafana RBAC and the documented rate limit of
100 requests/second with burst 200 remain unchanged. Its policy owner is
`@buenhyden`; reconsider by 2026-12-02 or immediately after route widening,
authentication changes or a relevant advisory.

## Work Log

### Issued writer leases

This Task is issued before implementation changes. Each writer must compare the
current fingerprint recorded in the P02 local curation receipt before editing;
a changed shared input pauses only its dependent slice.

The registered metadata gate identified a narrow shared-package correction in
the current draft `TSK-0040`: before SHA-256
`a946e47cac814437da5418f941333e76a5bc321548d11d2797d79c07013b7073`.
`p02_docs_impl` changes only the five `FAIL` evidence rows at lines 315–319 and
the five later `PASS` selected-check rows at lines 320–324 so each `Resolves`
value is `-`. A failing row cannot resolve a gate, and a selected-check PASS
cannot resolve a distinct full-gate FAIL. Inputs, locations, results, failure
history and Check labels remain unchanged. This is a metadata correction, not a
P01 acceptance change or validator/baseline waiver.

| Scope | Writer | Review role | Boundary |
| --- | --- | --- | --- |
| All `infra/` source and its exact service READMEs | `p02_infra_impl` | independent code/IaC review | Single integration writer for Compose, gateway, readiness and Valkey source |
| `scripts/operations/workspace-inventory.py`, its library and source tests | `p02_connections_impl` | independent code/security review | Adds public connection evidence only; no private-value read or hash |
| Native, synthetic and contract-test source | `p02_contract_tests` | independent QA/security review | Exercises declared contracts without operating a HOME service |
| This package, DATA-0096 README and local P02 curation/review receipts | `p02_docs_impl` | independent document review | Records evidence and handoffs; DATA-0096 generation remains coordinator-owned |
| CI manifest, selectors, their tests and `scripts/hardening/check-all-hardening.sh` shared-URL assertion | `p02_ci_impl` | independent CI review | Registers only existing verified checks and keeps the OAuth2 Proxy MNG Valkey assertion aligned with the transport contract |

Acceptance owner, data owner and operating accepter are not inferred from these
writer labels. P03 owns model/product registration, P04/P05 own Airflow/n8n
consumer behavior, P06 owns secret issuance and custody, P07 owns observations,
and P08 owns the Valkey update/advisory decision. A service source change stays
under the infra lease even when those owners receive a handoff.

### 2026-11-02 residual follow-up lease

At `2026-11-02T10:40:48+09:00`, the direct user request authorizes a local
cause analysis of three retained residuals: the full SSO class not run, the
broad Compose-baseline aggregate timing out at 600 seconds, and the
supply-chain fixture failure. The follow-up starts from clean commit
`0592303d1f7d96b46019be7a730c115c53cbbcab`; it neither reclassifies the
earlier observations nor authorizes a HOME service, host, credential, external
repository, remote-CI or dependency-lock change.

| Scope | Writer | Review role | Local objective and stop boundary |
| --- | --- | --- | --- |
| Full SSO isolated fixture, helpers and exact baseline-gate test | `p02_residual_sso` | independent code/security review | Find the bounded first-start cause; fix and rerun only a synthetic, isolated class when it is a P02 source/test defect. Stop before a HOME Keycloak/OAuth2 Proxy or stored client. |
| Exporter candidate assertion regression | `p02_residual_exporter_tests` | independent code review | Correct only the stale literal exporter-argv contract in `tests/validation/test_sec01_next_stable_candidates.py`; prove default and nondefault dynamic ports while preserving image/security invariants. |
| CI selector, runner plan, DATA generation, integration and normal commit | `p02_residual_ci` | independent CI review | Determine why the broad aggregate exceeded its 600-second budget; make a bounded local orchestration correction only when the cause belongs to P02. Do not treat selected P02 PASS results as the aggregate result. |
| Supply-chain fixture and ownership classification | `p02_residual_supply_review` | independent security review | Read the exact fixture failure and its declared inputs. It may not mutate an image declaration, provenance ledger, controller lock or service. |
| This Task, P02 curation and owner handoffs | `p02_residual_docs` | independent document review | Record commands, input/output fingerprints, time, exit status, recovery and the separate source/static/isolated/history/current-operation/rotation/restore/remote-CI/final-acceptance axes. DATA generation remains `p02_residual_ci`-owned. |

The work-unit mapping remains unchanged: W61 provides the selected port-source
context, W62 owns the SSO class, W63/W64 delimit readiness and synthetic
Valkey evidence, and W65 owns the bounded ledger, review and handoff record.
The prior historical operation evidence stays historical; direct operation,
credential rotation, independent restore, remote CI and final acceptance stay
`NOT_RUN` unless their separately authorized owners execute them.

The follow-up uses the official [Keycloak container guidance](https://www.keycloak.org/server/containers)
and [configuration reference](https://www.keycloak.org/server/configuration),
retrieved on 2026-11-02, only for the observed distinction between a `kc.sh`
build and an optimized start. The matching test image's tracked `26.7.4-0`
runtime help must be verified before applying that guidance; the current pages
do not establish a version-support claim. The CI child-process change is
bounded by Python's [subprocess](https://docs.python.org/3.14/library/subprocess.html)
and [unittest](https://docs.python.org/3.14/library/unittest.html) semantics:
the implementation records completed child output only, bounds captured bytes,
and preserves a timeout as a timeout rather than synthesizing a test result.

### Contract decisions and residual boundaries

P02 reconciles four port locations separately: process listener, service DNS,
host publication and gateway backend. It rejects using host publications from a
container or adding a public port to repair a private caller. `DEV` and `MNG`
variables must remain separately evidenced. Process liveness, initialization,
dependency readiness and functional/product readiness remain separate results.

No source inspection, route test or connection census proves a stored product
credential, model registration, successful external delivery, a current
operator run, credential rotation, recovery or remote CI result. Those items
remain explicitly routed to their owning task.

### D02 re-verification at current main

A direct user request on 2026-11-04 re-ran this contract as D02 on clean
`main` `d3f1cfaac3d1237331fa59786948c4e4dbabc9be`, branch
`fix/compose-start-host-port-conflict`. The focused P02 port, service, native,
Valkey-mount, Prometheus, port-inventory and Hermes gate suites ran 131 tests:
OK, one declared skip. A value-free all-profile render shows only Traefik
(`core`/`dev`/`local`) and opt-in Nginx (`nginx`) publish 80/443 on
`HOST_LAN_BIND_IP`. The Loki, Tempo, Alloy and `mng-valkey` LAN publications are
the owner-approved POL-0096 exception and are preserved unchanged.

POL-0011 forbids selecting Nginx with the Traefik profile, but nothing enforced
it: `compose_start.create_plan` accepted `--profile core --profile nginx` and
`--target traefik --target nginx`, which would bind the same host 80/443. The
plan now rejects any selection in which two services publish the same unrendered
host binding expression (`host_port_conflict`). A new regression failed before
the fix and passes after; the module runs 20 tests OK. On the real source, HOME
and every one of the single profiles still plan, and the gateway pair is
refused with CLI exit 2. Different variables resolving to one value are a stated
limit of this source-expression check. No container, route, credential or
authentication setting was changed; runtime and Hosted CI for this delta are
NOT_RUN, as the D02/D03 runtime and Hosted CI row records.

Official pages re-read on 2026-11-04: Traefik routing rules (redirected to the
v3.7 reference; declared image `v3.7.16`), Compose networking (service-to-service
traffic uses the container port, host ports only from outside), OIDC Core
§3.1.3.7 ID Token validation and RFC 8725. They match the existing P02 contract;
no new authentication change was adopted from them.

### D02 re-verification after the LAB moves (2026-11-07)

A direct user request on 2026-11-07 re-ran D02 on clean `main`
`636c9191cc92e5bb04ea9c35a967aabde2a1f5e7`, equal to read-only `git ls-remote`
main, Docker context `default`, branch `fix/d02-host-publication-invariant`.
Since the 2026-11-04 run at `d3f1cfaac` (321 commits), `infra/01-gateway` and
`infra/02-auth` are unchanged; the root Compose lost only the moved LAB
includes and secrets, and the n8n and Ollama diffs are an image pin and
resource reservations. No network, port or authentication declaration changed.

**Reuse.** The P02 gateway-port, native, OAuth, Prometheus, secret
presentation, service, Valkey-mount, port-contract, P11 Hermes gate, Gatus OIDC
and Open WebUI OIDC suites ran 90 tests OK with 4 declared skips; runner
isolation, service wiring, `compose_start` and port inventory ran 75 OK with 1
declared skip. The rendered host publications equal the 2026-11-04 record: on
`HOST_LAN_BIND_IP` only Traefik and opt-in Nginx 80/443 and the POL-0096
Loki/Tempo/Alloy/`mng-valkey` exception; eleven loopback publications.

**T01 gap.** Hardening pinned loopback for only Open Notebook, WireMock,
Pact Broker and Mailpit; nothing stopped another service (Ollama, ComfyUI,
the PostgreSQL ports, Kafka, Pyroscope, Registry) from moving to a wildcard or
LAN address, and the POL-0096 LAN list was not enforced as an exact set.
`HostPublicationContractTests` now renders every profile from `.env.example`
with `HOST_LAN_BIND_IP` set to the RFC 5737 address `198.51.100.7` and requires
each publication to be loopback or an approved (service, container port) on
that address; Ollama, Open Notebook, Pact Broker and WireMock must stay on
`127.0.0.1` for their host callers. Synthetic wildcard, omitted, IPv6-wildcard,
unapproved-LAN and wrong-port cases are rejected; dropping `mng-valkey` from
the allowlist makes the real render fail with `mng-valkey:6379`.

**T03 access matrix (value-free render, all profiles).** The Ollama overlay
adds only `n8n-worker` and `ollama` to internal `n8n_ollama_net`; `n8n` main and
both runners cannot reach Ollama, and each runner is alone with its parent on
an internal network (pinned by `test_p03_runner_isolation` and
`test_service_wiring_contracts`). Crawl4AI joins only internal `crawl4ai_net`,
which has no consumer until a POL-0091 change adds one, and internal
`crawl4ai_egress_net` with its egress proxy. Storybook shares its internal
ingress network only with Traefik. RedisInsight is on both data networks for
its Valkey connections, but `RI_APP_HOST` binds its listener to the
Traefik-only `redisinsight_ingress_net` address, so data-network peers cannot
reach it (pinned by `test_compose_baseline_gates`). SeaweedFS master, volume and
filer are internal only; the S3 API on `edge_net` requires SigV4 credentials.

**Handed-off gap: shared `edge_net` bypasses SSO.** Every Traefik backend except
RedisInsight and Storybook shares `edge_net` (37 peers). A container on it can
call any other backend by service DNS without passing Traefik, so services that
rely only on the `sso-auth` middleware are reachable without SSO by every other
`edge_net` member. Among the routed services with `sso-auth` these are
Alertmanager, Alloy, cAdvisor, ComfyUI, Flower, Kafka Connect, Kafka REST Proxy,
Loki, Mailpit, MLflow, Ollama, Prometheus, Pushgateway, Pyroscope, Qdrant,
Schema Registry and Tempo; whether each also enforces an application-level
credential was not verified per service. ADR-0055 states that a compromised
container reaches only its wired peers but does not address this shared
ingress path, and the Traefik v3.7 Docker provider reference makes no
isolation claim. The owner chose record-and-handoff on 2026-11-07: the fix
needs a new ADR (an accepted ADR body is not edited) and its own Spec that
classifies each backend's own authentication, designs per-backend ingress
networks or listener binds like RedisInsight's, orders the recreation and
defines rollback. No network was changed here.

**T02/T04.** Gateway, Keycloak and OAuth2 Proxy sources are unchanged since the
2026-11-04 run, whose isolated SSO 3/3 and interruption cleanup 1/1 records
stay the evidence; the P11 Hermes gate (exact webhook route, size limit, rate
limit and source range) passes in this run, and no new authentication change
was needed. Official pages read on 2026-11-07: the Traefik Docker provider
reference (v3.7; `exposedByDefault`, and `network` only chooses Traefik's path,
with no isolation claim) and `docker compose up` (`--wait` means running or
healthy only, not function proof). Runtime, restore and Hosted CI for this run
are NOT_RUN.

### D03 data-tier re-verification at current main

A direct user request on 2026-11-04 re-ran the data, Valkey and storage
contract as D03 on clean `main` `73ccd9930c64e38b4a51d4bb191b061ecf1c9b95`,
branch `fix/valkey-maxmemory-noeviction`. Data-tier suites (DEV boundary,
DEV/MNG Valkey ACL, MNG init SQL, mount scope, write rate, restore and upgrade
rehearsals) ran 155 tests: OK, four declared skips. Value-free renders with
`VALKEY_PORT=16379` and `POSTGRES_PORT=15432` show every `mng-valkey` and
`mng-pg` consumer, exporter and health check following the nondefault port;
RedisInsight keeps the fixed `dev-valkey` 6379 by design. The store set is
already consolidated: one MNG and one DEV PostgreSQL 18.6, shared `mng-valkey`
with opt-in `dedicated-valkey`, Prometheus as the single time-series source, no
PG or Valkey cluster or InfluxDB, and graph/search/NoSQL stores only in opt-in
profiles. Eight bind volumes of opt-in profiles have no host directory, which
fails closed instead of creating an empty data directory. The shared n8n named
account secret is not issued; issuance stays with the secret owner.

Read-only `docker stats` showed `mng-valkey` at about 5 MiB of its 256 MiB limit,
with no `maxmemory`, while `dev-valkey` already used `128mb`/`noeviction`. A
full queue would therefore OOM-kill the process shared by n8n, Airflow,
oauth2-proxy and Terrakube. The shared and dedicated start scripts now pass
`--maxmemory 128mb --maxmemory-policy noeviction`. A labelled, network-less
container of the pinned `valkey/valkey:9.1.2-alpine` image reported 134217728
and `noeviction`; with the cap lowered it refused write 12 with the OOM error,
still answered PONG and kept earlier keys; residue was zero. The new static
regression failed before the change. The pinned dedicated-wrapper argv test was
updated to the intended arguments; Valkey suites run OK with three declared
skips. The running containers were not recreated, so the live servers keep the
old arguments until an approved operator recreates them.

Official pages re-read on 2026-11-04: Valkey ACL (database index is not an
isolation boundary; channels start empty for new users), Valkey persistence
(AOF `everysec` default, safe AOF copy procedure), PostgreSQL backup (current
major 18) and Docker volumes (removing a service keeps its volumes).

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Issued baseline and leases | 56 | W61 | Read-only branch, source and ownership readback | Initial HEAD and public P01 ledger | PASS | Inputs and Authorization; Issued writer leases | required | - |
| Port contract regression | 56 | W61 | Focused isolated source/configuration suites | Public changed Compose inputs, listed in local P02 hash packet | PASS | `p02_infra_impl`: contract suite 24/24; port/renderer suite 20/20; root and monitor-overlay rendering selected 57 Traefik/55 Nginx services | required | - |
| Authentication boundary regression | 57 | W62 | Controlled loopback OAuth2 Proxy ID-token verifier and isolated Traefik method check (bounded scope) | Official v7.15.5 asset, checksum and synthetic signed tokens | PASS | `_workspace/repo-support/analysis/p02/oauth2-proxy-oidc-native-20261102.txt`, 2026-11-02T07:23:00+09:00, 2 methods pass; isolated Traefik method check, 1 method passes; stored Keycloak client and API access-token acceptance excluded | required | - |
| Full SSO exact-class rehearsal | 57 | W62 | Browser 302, JSON 401 and group-denial 403 full-stack class | Matching Keycloak test image | NOT_RUN | `_workspace/repo-support/analysis/p02/sso-rehearsal-residual-20261102.txt`: first-start provider build exceeded 300 seconds; cleanup passed. Resume with a pre-built matching Keycloak test image or bounded `kc.sh` build preparation | required | - |
| Full SSO exact-class rehearsal, isolated rerun | 57 | W62 | Synthetic Keycloak 26.7.4-0 fixture with separately bounded preparation and optimized start | Cached base (`--pull never`), synthetic realm/users and no HOME client or credential | PASS | `tests/validation/test_compose_baseline_gates.py` SHA-256 `da5d64a34c63cccff58312a81e506525ceadcbec88ae8771a4889e8e400c2590`; full authentication 3/3 passes in 235.019 seconds (preparation 129.004, start 37.966): browser 302, JSON 401, member login/logout and nonmember 403. This receipt is bound to that exact source fingerprint and is not transferred to a later cleanup fix. The prior NOT_RUN observation remains historical. | required | - |
| Full SSO interruption cleanup, isolated rerun | 57 | W62 | Runner-style hard-timeout cancellation of the same synthetic fixture | Cached base, labelled temporary resources, no HOME target | PASS | Same `da5d64a…` fixture: native interruption 1/1 passes in 17.378 seconds after exact parent recovery; container, network and image residue count is zero. Static ownership tests are 9 PASS and one opt-in SKIP. Independent code review found no open defect at this fingerprint. The receipt is not evidence for a later source fingerprint. | required | - |
| Full SSO source-equivalent runtime proof | 57 | W62 | Synthetic Keycloak fixture, bounded preparation and optimized start | e537 source, cached base, synthetic realm/users and no HOME target | PASS | `tests/validation/test_compose_baseline_gates.py` source SHA-256 `e537232d3147d62d122ea4d5c2822fe421f1502f439b715d9bd4f97edb9d8b76`: traced authentication 3/3 passes in 272.773 seconds (preparation 169.443, start 36.078), and native hard-timeout cleanup 1/1 passes in 25.719 seconds. Browser 302, JSON 401, member login/logout, nonmember 403, teardown and owned residue zero are isolated-only evidence. Main added executable coverage is 85.46%. | required | - |
| Final SSO cleanup-only source proof | 57 | W62 | Static/default fixture contract and immutable-ID postcondition | Final b565 source; static contract plus separately recorded prior owned-digest/residue proof | PASS | `tests/validation/test_compose_baseline_gates.py` SHA-256 `b565757557918244acd0321acb76b08b7624ee8537e6aadf9ae6be4c3d664ecd`: static/default 16/16 passes (0.613 seconds independent security run), 1 registered optional skip, focused cleanup-delta coverage 80.65%, and a separately recorded prior immutable-ID absence/residue-zero proof. The b565 delta is cleanup-only and SOURCE_EQUIVALENT to the e537 runtime packet, not a direct b565 runtime run. Independent code review passed at 2026-11-02T11:27:55+09:00; security review found no Critical, High or Medium finding. | required | - |
| SSO hook-compatibility-only delta | 57 | W62 | Identical synthetic run ID bound to a local variable before test call | Current `2470477a…` test source; no fixture, runtime or assertion-contract change | PASS | `tests/validation/test_compose_baseline_gates.py` SHA-256 `2470477aafad41d441472c5e08c72eab628e0d6e93d321eaf720b55522944b3f`: focused 2/2 passes in 0.002 seconds; Ruff, gitleaks and diff check pass. Independent code review (`/root/p02_residual_ci/gitleaks_delta_review`, 2026-11-02T11:54:53+09:00) and security review (`/root/p02_residual_ci/gitleaks_delta_security`, 2026-11-02T11:54:56+09:00) found no issue. This is a hook-compatible call-expression refactor only; e537 runtime and b565 cleanup proof remain separately source-bound. | required | - |
| Registered SSO module and runner selection | 57 | W62 | Frozen module through the corrected selector adapter | Declared opt-in selection only; no new allowed environment key | PASS | 135 total cases at historical `da5d64a…`: 104 PASS and 31 exact declared skips in 43.275 seconds; independent CI code/security review, gate contract 45/45, plan 60/60 and validator checks pass. This is local registered-selection evidence only. | required | - |
| Registered broad Compose baseline leaf | 60 | W65 | `leaf.compose-baseline-regressions` through the corrected per-selector adapter | 75 unique registered selectors; unchanged 600-second budget | FAIL | Exit 1 in 250.959 seconds, with 1,330 discovered cases, 95 declared skips, 1,234 executed PASS, one FAIL and no ERROR. The only failure is `WorkflowVersionBundleTests.test_n8n_source_receipt_does_not_reuse_previous_native_acceptance`: stored n8n `8792a345…` differs from current `afe7eabe…`; P05/P08 owns that provenance receipt transaction. `_workspace/repo-support/analysis/p02/broad-leaf-final.log` is the sanitized local log. This replaces neither operational nor remote-CI evidence. | required | - |
| Environment and readiness regression | 58 | W63 | Focused isolated source/configuration suites (source/isolated scope) | Public changed Compose inputs | PASS | `p02_infra_impl`: contract suite 24/24 and port/renderer suite 20/20; Open Notebook `/health` remains limited liveness/startup evidence | required | - |
| Valkey contract regression | 59 | W64 | Synthetic ACL, secret-delivery and topology source checks (source/isolated scope) | Synthetic values only | PASS | `p02_infra_impl`: contract suite 24/24; hardening suite reports ALL PASS | required | - |
| Exporter candidate assertion regression, corrected | 59 | W64 | Rendered Compose and synthetic exporter wrapper checks | Default 6379 and nondefault 16379; synthetic secret only | PASS | `tests/validation/test_sec01_next_stable_candidates.py` SHA-256 `f3231f6c5a45dc9b402ad7574e4edb0dec93c07e770e5b4c8ee7ef6dd4f6fb23`: focused 2/2 and full module 12/12 pass. It verifies exact host/port argv while the password remains environment-only. The prior four literal-argv failures remain historical. | required | - |
| Native secret-presentation contract | 59 | W64 | Synthetic Compose secret ownership and permission modes | Cached image and synthetic secret only | PASS | `_workspace/repo-support/analysis/p02/compose-secret-native-20261102.txt`, 2026-11-01T22:56:55.947414+00:00; `test_p02_secret_presentation_native.py` SHA-256 `97faf10b437f6ba89ed7c1141a455f7d77574d74096ebe01478440cf8b678e1e`; 1 test, 4 modes, 74.684s | required | - |
| Connection ledger and handoff validation | 60 | W65 | Public extractor and handoff curation (bounded public-source scope) | 67 public sources, 22 connection rows, 1 explicit unknown gap; 10 extracted sources and 1 unhandled source | PASS | Frozen helper `dfefebaa…`, test `261067…`; 50 tests pass with main branch 86%, helper 85% and combined 87%; Superset has four rows, including source-declared Trino with actual registration `UNKNOWN`; generated DATA-0096 records 22 rows and validates | required | - |
| Current direct operation C56 | 56 | W61 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Current direct operation C57 | 57 | W62 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Current direct operation C58 | 58 | W63 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Current direct operation C59 | 59 | W64 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Current direct operation C60 | 60 | W65 | HOME service operation | No approved target/operator/window | NOT_RUN | Out of this local source unit | optional | - |
| Credential rotation and independent restore | 59 | W64 | Actual credential and state recovery | No approved secret/data owner or recovery window | NOT_RUN | P06 and actual data owner handoff | optional | - |
| Hosted CI C56 | 56 | W61 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| Hosted CI C57 | 57 | W62 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| Hosted CI C58 | 58 | W63 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| Hosted CI C59 | 59 | W64 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| Hosted CI C60 | 60 | W65 | Remote CI execution | No remote publication | NOT_RUN | Out of this local source unit | optional | - |
| D02 focused regression | 56 | W61 | P02 port/service/native/Valkey/Prometheus/port-inventory/Hermes suites | HEAD d3f1cfaac | PASS | 131 tests OK, 1 declared skip | required | - |
| D02 gateway exclusivity | 56 | W61 | compose-start host binding conflict regression and real-source plans | HEAD d3f1cfaac plus this delta | PASS | New test RED before fix, 20/20 after; HOME and all single profiles plan; Traefik+Nginx refused (exit 2) | required | - |
| D03 data-tier regression | 59 | W64 | Data-tier suites and nondefault-port renders | HEAD 73ccd9930 | PASS | 155 tests OK, 4 declared skips; all MNG consumers follow 16379/15432 | required | - |
| D02 2026-11-07 reuse regression | 56 | W61 | P02/P11/OIDC, isolation, wiring, compose_start and port-inventory suites | HEAD 636c9191c | PASS | 90 OK (4 declared skips) and 75 OK (1 declared skip) | required | - |
| D02 host publication invariant | 56 | W61 | All-profile public render against loopback/approved-LAN allowlist | HEAD 636c9191c plus this delta | PASS | Synthetic violations rejected; removing an allowlist entry fails the real render | required | - |
| D02 shared edge_net SSO bypass | 57 | W62 | Value-free all-profile reachability matrix | HEAD 636c9191c | FAIL | SSO-only backends reachable from 37 edge_net peers; owner chose record-and-handoff to a new ADR and Spec | optional | - |
| D02/D03 runtime and Hosted CI | 56 | W61 | Live service and remote CI for the D02/D03 delta | HEAD 73ccd9930 | NOT_RUN | No container recreated and no remote run recorded for this delta | optional | - |
| D03 Valkey memory cap | 59 | W64 | Static regression and pinned-image native probe | 9.1.2-alpine, labelled network-less container | PASS | RED before change; 128 MiB noeviction; write refused with OOM, PONG, keys kept, residue 0; live servers not recreated | required | - |
| SEC01 root source re-binding | 60 | W65 | `test_update_gates` and the three other ledger consumers | Clean `main` `6361e93b5` | PASS | 57 hash-only failures before; 63 tests OK (2 declared skips) after; image, build and membership unchanged | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 56 | pending | Port contract regression | SOURCE_READY: corrected source passes selected contract/render suites; direct operation, restore and remote CI remain separate | SPEC-0212 TSK-0041 |
| 57 | pending | Authentication boundary regression, Full SSO exact-class rehearsal | SOURCE_READY: current OAuth2 Proxy verifier rejects wrong issuer, audience and expiry without a session cookie, an isolated Traefik method check passes, and the synthetic `SsoRehearsalTests` realm covers browser 302, JSON 401, permitted-user login/logout and nonmember 403. The shared `SsoStack` Storybook/TLS issuer native variants were not run in this follow-up; existing Storybook operating acceptance remains reused only within its recorded scope. This is not a stored Keycloak client, real API access-token, HOME operation, rotation, restore or remote-CI result. | SPEC-0212 TSK-0041 |
| 58 | pending | Environment and readiness regression | SOURCE_READY: corrected source passes isolated checks; liveness, dependency initialization and product readiness remain separate | SPEC-0212 TSK-0041 |
| 59 | pending | Valkey contract regression | SOURCE_READY: selected shared-MNG/default and opt-in topology source checks pass; credential issue, rotation, queue drain and restore remain unexecuted | SPEC-0212 TSK-0041 |
| 60 | pending | Connection ledger and handoff validation | SOURCE_READY: 67-source census yields 22 connection rows, one explicit unknown gap, 10 extracted sources and one unhandled source; generated DATA-0096 is validated, while broader metadata/QA and final acceptance remain separate | SPEC-0212 TSK-0041 |

## Review and Completion

Independent code, security, IaC and document review must cover the exact changed
fingerprints. Required local tests, metadata, link and changed-file checks must
be recorded here with their actual result. Run `graphify update .` after source
integration. Preserve separate observations for source, static, isolated,
historical operation, current operation, rotation, restore, remote CI and final
acceptance. A logical local commit may follow these checks; push, PR, merge,
release and deployment remain unapproved.

### Bounded review records

The current curation contains 56 `complete: false` partial review records: two
retained P01 records, 29 IaC records, six code records, 13 README records,
five CI records and one generated-operations-catalog record. They record changed-section review only and do not grant a
full-file review result. The CI changed-section review was performed by
`root_ci_review` at `2026-11-01T22:59:14Z` for P02 workflow-contract,
manifest, `test_ci_gate_plan` and hardening source assertions; it reported no
Important or Critical finding. Final metadata, link, registry and selected-leaf
gate results are recorded only after their frozen execution receipts exist.

The authoritative broad Compose baseline regression aggregate timed out at its
ten-minute budget (exit 124) without a captured module result, so unrelated
modules remain unproven. It is not a P02 feature failure and is not promoted
from the P02-owned selected slice: 58/58 pass in 38.607 seconds (service
contracts 24, Prometheus 3, gateway 3, service wiring 20, datastore scrape
labels 5 and route-auth contracts 3). A workload/budget mismatch was only an
initial hypothesis. The later split measurement includes a deliberately
aborted 300.105-second selector and does not establish that the ten-minute
budget is inadequate.

The residual follow-up located a local orchestration defect, then corrected it
without changing the mandatory selector set or the 600-second policy. The old
adapter ran all 75 registered selectors (1,312 discovered cases) in one Python
child and emitted captured stdout/stderr only after child completion. Its
outer timeout therefore killed the process group at 600 seconds and discarded
the active module's diagnostic output. The updated adapter runs one child per
registered selector, writes a safe selector breadcrumb before spawn, emits
only completed child payloads, bounds aggregate stdout/stderr (including
markers) to 1 MiB, preserves zero-case and optional-skip validation, retains
the first nonzero result, withholds active-child payload at an outer timeout,
and cleans up child and grandchild processes. Its SHA-256 is
`d5a5a26e3a085db9e00f749a28c1e7f1d5cadbae86d0b0cc49fcc9d88f15342b`;
the adapter and execution-context regressions are
`6677b8eb9c7046a80e91ea3ae31c0d0a825d443fb2b2a31ab2203af7a37a3b34` and
`881e059414bc9911949ad41c6d2e832470179a880a1a736ec79980337b2d6c3b`.
Independent code and security reviews each passed 41 focused cases (3.275 and
3.823 seconds respectively); this is a partial review of the orchestration
change.

The modular measurement attributed all 75 selectors separately, with a split
wall sum of 479.213 seconds. It is not an uninterrupted aggregate PASS:
62 selectors passed and 13 were nonzero. The slowest passing selectors were
`openbao_agent_contract` (50.834 seconds), `compose_baseline_gates` (44.969),
`service_wiring` (22.004), `openbao_tls` (9.175), `infra_tier` (7.202) and
`lab_isolation` (6.527). `tests.validation.test_crawl4ai_egress` timed out at
300.105 seconds because
`AddressRuleTests.test_pin_refuses_ports_literals_mixed_answers_and_integer_forms`
stalls in its asyncio `getaddrinfo` executor: the isolated
`system_resolve('2130706433')` exceeds five seconds while synchronous
`socket.getaddrinfo` returns immediately. Its owner/environment classification
is provisional until the scoped unsandboxed reproduction; it is not treated as
a P02 source failure. The other nonzero selectors are `locust_telemetry`,
`storybook_image`, `crawl4ai_adapter`, `datastore_observation_rehearsal`,
`datastore_rehearsal_boundary`, `openbao_protected_maintenance`,
`openbao_token_operations`, `openbao_raft_snapshot`,
`sec01_next_stable_candidates`, `workflow_version_bundle`,
`opsflow_adapters` and `opsflow_airflow_contract`. Resume their own
owner/environment classification and investigation from their completed
checkpoints; do not
extend the ten-minute policy or present the split measurement as a green broad
aggregate. Rollback restores only the three orchestration files and preserves
both the original exit-124 observation and its completed selector checkpoints.

The scoped valid-local-context rerun resolves the provisional execution-context
classification: the exact Crawl4AI method passed in 0.006 seconds and its
module recorded 15 PASS and six declared opt-in skips in 1.556 seconds. The
then-current valid-context recheck had ten PASS results and two failures:
`sec01_next_stable_candidates` (four subtests) and
`workflow_version_bundle` (one failure). The former was an initial P02
test-contract failure, not a P08 residual; its later P02 correction is
recorded below. Only the latter remains the current P05/P08 provenance
residual.
The valid-context default-leaf attribution is about 180.7 seconds, below the
unchanged ten-minute budget. The frozen historical `da5d64a…` SSO module then
recorded 135 total cases in 43.275 seconds: 104 PASS and 31 exact declared
skips. CI registration's independent
code/security reviews passed, as did the gate contract (45), plan (60) and
validator checks. These results validate the P02 runner correction and its
registered isolated SSO path; they do not turn the original interrupted broad
run into an uninterrupted aggregate PASS.

The persistent valid-context failures split by actual ownership. The four
`NextStableCandidates` subtest failures are a P02-owned test-contract gap, not
a P08 handoff: the literal assertion rejects P02's legitimate quoted dynamic
exporter argument. `p02_residual_exporter_tests` owns only
`tests/validation/test_sec01_next_stable_candidates.py`; it subsequently added
meaningful default/nondefault argv coverage while preserving image and security
invariants. The corrected SHA `f3231f6c5a45dc9b402ad7574e4edb0dec93c07e770e5b4c8ee7ef6dd4f6fb23`
passed focused 2/2 and full-module 12/12 checks and received a narrow
independent code review. The original four-failure receipt remains dated RED
history.

`tests/validation/test_sec01_next_stable_candidates.py` SHA-256
`47ad9fdb73812aa4aa0810b6ac111148590a12205f8f996ec5f761a50f48b58d`
has four failing subtests for OAuth2 Proxy
(`6a3bbb2dd657e2a975b2c7da1e8e7297acc599f7f18c9baf8e90c040cb4bd22a`),
MNG DB (`b02261123e7fc867598b02a1bf9254f6d364e5df75359cf6776edb653ac8b471`),
Airflow (`b3ddab42b06ae41a332b6b683ffb2846f9a40110903feb6d44727a162e05ecb9`)
and n8n (`afe7eabe63e19a889ec608fb76900ff908b0da32faf261f99099fb0e5b6009f7`).
It expects a literal `-redis.addr=redis://` in `service["command"][0]`, while
the current safety wrapper supplies a quoted dynamic
`-redis.addr="redis://…:$$port"`; this is a stale P02 assertion, not a
P02 runtime failure or a supply-manifest change. The separate P05/P08 handoff
is
`tests/validation/test_workflow_version_bundle.py` SHA-256
`c649be9f22b6dd3e3a4bc94d4ab1f6c6da9e26e8ccea87294d1da57f3e1b91c2`,
where stored n8n Compose `8792a345bd2ead857d108fc2eb100b8be19a9c5012caa5e457829b978b2adcc3`
does not equal current `afe7eabe63e19a889ec608fb76900ff908b0da32faf261f99099fb0e5b6009f7`.
P08 must update the canonical manifest/receipt transaction and its test
together; P02 does not edit those sources.

The P02 assertion correction is frozen at test SHA-256
`f3231f6c5a45dc9b402ad7574e4edb0dec93c07e770e5b4c8ee7ef6dd4f6fb23`.
It renders each Compose configuration at the default `6379` and nondefault
`16379` ports, executes synthetic exporter wrappers, checks exact host/port
argv and verifies that a password remains environment-only. Its focused run
passed 2/2 and the full module passed 12/12. This does not erase the original
four-failure observation or prove a running exporter.

The final registered `leaf.compose-baseline-regressions` run confirmed the
adapter correction under the unchanged 600-second budget: it exited 1 after
250.959 seconds, rather than exit 124, and emitted all 75 unique selector
summaries. It discovered 1,330 cases, declared 95 skips, executed 1,234 PASS
cases and had one failure with no ERROR. That single failure is the n8n
source-receipt mismatch owned by P05/P08; it is not an SSO, exporter, port or
CI-adapter defect. The sanitized log was born at
`2026-11-02T11:29:04.153+09:00` and last modified at
`2026-11-02T11:33:15.112+09:00` at
`_workspace/repo-support/analysis/p02/broad-leaf-final.log`. This is a
registered local leaf result, not current operation, credential rotation,
restore, remote CI or final acceptance.

The restricted repository-integrity run reported 767 tests with 9 failures and
77 errors. Its scoped-permission rerun completed 767 tests in 305.595 seconds
with 763 pass, 4 fail and no errors. P02 native reachability is fixed/passing,
the original three secret-metadata failures were caused by P02's overbroad
dedicated-broker mount, not missing P06 grants. The observed failures remain
historical evidence; after narrowing to the two required read-only files,
`PublicSecretSchemaTests` passed 21/21 in 55.806 seconds. P06 custody,
issuance and rotation remain `NOT_RUN`. P08 must refresh the nested SEC01 n8n
source-binding from `8792a345…` to the current
`afe7eabe63e19a889ec608fb76900ff908b0da32faf261f99099fb0e5b6009f7`
through its owned provenance transaction; its exact test is
`tests/validation/test_workflow_version_bundle.py` SHA-256
`c649be9f22b6dd3e3a4bc94d4ab1f6c6da9e26e8ccea87294d1da57f3e1b91c2`.
These are failures, not `NOT_RUN`, and no actual secret, provenance ledger or
operating service was changed here.

### Lifecycle comparator closure lease

The registered gate exposed a semantic conflict: the schema requires a
non-PASS evidence row to use `Resolves: -`, while the lifecycle comparator was
preserving that later relation cell as part of a failed observation identity.
The approved CI lease is a semantic projection, not a path-specific waiver.
For generation 7 it preserves `row[:8]`; for legacy generation 6 it preserves
`row[:7]`. Thus Criteria, Work Unit, Check, Input, Result, Location and known
Required data remain immutable while only the later-PASS relationship cell is
excluded. The five full-gate FAIL observations remain unresolved and criteria
51–55 stay pending; selected PASS rows have a different Check and do not
resolve or promote those full-gate failures.

`p02_ci_impl` owns the narrow comparator and regression source:
`scripts/lib/document_governance/spec_packages.py` SHA-256
`9f6dd115886c397043052904edbf525ff89d7ade7e110ac37db2c7274dee7a03`
and its generation-7 regression
`tests/lib/document_governance/test_generation7.py` SHA-256
`c0e9ab3a415f5eb8c587c74343d8fbf0f12ad3527d4f11657b0fbe4df237b420`.
The packet against baseline `b79cbb9f3f49af8cd0e654c2ca1c4b9ea7632af0`
is SHA-256 `12c5c0874436b43356a5b9af1e3ac4c4750cc3b1138c0c5ff4a4d5e80655c440`.
Rollback restores the comparator and its regression source together, then
leaves the gate blocked rather than rewriting a historical observation.

At `2026-11-02T08:29:15+09:00`, independent code review recorded 11/11
focused tests passing in 11.768 seconds with no findings; narrow security and
rules reviews also passed. CI focused tests passed. Earlier the changed-profile
run passed 6 leaves, then leaf 7 failed with exactly five failed-observation
differences. The registered routes subsequently ran; they do not form an
uninterrupted aggregate PASS. The metadata fixture leaf passed 152/152. The
original library leaf remains an observed 787-case split of 784 PASS, one FAIL
and two ERROR; the approved taxonomy target reran 1/1 PASS and the
permission-caused identity-history methods reran 2/2 PASS. Those component
receipts do not erase the original leaf failure.

Earlier CI/reachability checks passed workflow contract 45, runner/plan 86 and
GitHub workflow contract 44 at the dated fingerprints `3dfe252…`, `d1bdaa7…`
and `f7894c9…`. After mount-module registration, the current workflow,
plan-test and workflow-contract-test SHA-256 fingerprints are
`46c15badd836003aff16c6da43eb810a030225c9ec2011eb89952e05ccb6ae87`,
`4798f34350767ab35bffae92f5357c4db5f952dd55199b01f6ae7c30f24296d4` and
`6e2c504c7d746aa2a38b1e5d584eb27e0415fb465d6ca96f8f2507d7013eba2a`.
Current CI impact reruns passed gate contract 24/24, plan 60/60, GitHub workflow
44/44 and the executable checker. The mount regression SHA-256 is
`13096d677d46913f8a11795bd14e99f6e759ea4da90ff6b834aa7db5b0e623b8`; its
three new service subtests were RED before the fix and the final QA run was
GREEN at 13 PASS in 28.577 seconds, with full SecretSchema 21 PASS in 55.806
seconds and the P02 static slice 59/59 PASS in 38.091 seconds. `root_ci_review`
at `2026-11-02T00:54:54Z` reviewed the earlier scope. The current selector and
mount/wiring hashes were independently re-reviewed by `p02_code_review` at
`2026-11-02T01:12:52Z` with no findings; this is a partial review, not
full-file credit.

The dated pre-final-mount DATA-0096 scan/validate passed with files
41106/41106, partial reviews 53/2253, body 0/2253, render 0/17 and
runtime/restore 0/112. Its comparison saw 10 changed inputs and no
head/add/remove/connection delta. The final scan/validate then passed with
files 41169/41169, partial reviews 55/2254, body 0/2254, render 0/17 and
runtime/restore 0/112. The 56 ledger records and 54 coverage numerator differ
because self/excluded records do not enter that numerator. These census facts
do not change pending criterion acceptance or any operating, rotation, restore,
remote-CI or final-acceptance status.

The isolated official `pip-audit` 2.10.1 run against the unchanged,
hash-locked `scripts/requirements-controller.lock` is an actual `FAIL` (exit
1), not a P02 package change: two packages have 25 known vulnerabilities.
`filelock` 4.2.0 accounts for 17 findings (fix 4.2.1) and `virtualenv`
21.14.8 accounts for eight: seven reports specify 21.14.9, while
`CVE-2026-113713` specifies 21.14.10. A compatibility-reviewed 21.14.10 is
the minimum candidate covering all reported `virtualenv` IDs. The sanitized receipt
`_workspace/repo-support/analysis/p02/pip-audit-controller-lock-20261102.json`
has SHA-256 `740c466637b62722d779ba143be8503465f67c139c5890b6ebf5e18e8104c717`;
the lock remains byte-identical to baseline at SHA-256
`d05a5fb50e29e3d44587b34abacf2713eaea83c7c88ff84127d9cbfe96a193e2`.
P08 owns the canonical dependency input manifest(s), generated lock and
affected controller-gate transaction. The report states 4 High, 12 Medium and
9 Low findings, with no Critical; P02-specific exploitability and reachability
are not established. The baseline-equal lock establishes no P02-induced
dependency delta. Recovery reverts only the owned input-plus-lock delta,
appends corrective evidence, preserves the original FAIL receipt/history, and
reruns the exact hash audit and controller gates. `npm audit` is separately
`NOT_RUN` because P02 changed no npm dependency tree.

### Catalog synchronization and supply-chain residual

The generated inventory projection in
`docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`
was refreshed only between `current-service-inventory` markers using
`operations_catalog.render_service_inventory(ROOT)`. The prior SHA-256 was
`aa35b5b93c1719d1b3d82eaf18d200ede1b41ac804e99c0a22840c6875833b19` and
the refreshed SHA-256 is
`2e92d2bb86a2515591a29fe4c31ef28192933cb40fa3dcee13f95329ab53a6c7`.
The 25 added/25 removed lines are generated projection fields; authored
narrative remains outside the markers. `check-operations-catalog.py` passed.
The earlier 36-cell review at `2026-11-02T00:34:54Z` is retained as history.
At `2026-11-02T01:08:26Z`, `root_document_review` re-reviewed refreshed
SHA-256 `2e92d2bb86a2515591a29fe4c31ef28192933cb40fa3dcee13f95329ab53a6c7`:
exactly three generated mount-projection cells changed (Airflow, n8n and
OAuth2 Proxy), from the prior catalog SHA
`125c4cbd90f6ee72a9d11859519c361832788b0eb8a6d68d4b822de7e79bf281`.
It is `complete: false`, limited to P02 changed generated catalog cells, and
found no blocker or runtime, restore or acceptance promotion.

The registered supply-chain fixture leaf is an actual residual `FAIL`, not a
P02 feature failure or an unexecuted result: 266 cases ran, 265 passed and
`UpdateEvidencePackageTests.test_current_root_census_excludes_relocated_lab_history`
failed in 48.488 seconds. The test
`tests/lib/supply_chain/test_update_gates.py` and ledger
`infra/09-platform-ops/security-updates/update-ledger.json` both retain their
baseline SHA-256 values
`060dc243c5061c820636dab9429ea3b61505ae013d2c543fe026c783ac538f4e` and
`a25b4092a88dd088a56e97b947bd51f3c5ad206e352edb4fcf57f8e3aa4c1911`.

The follow-up exact bounded command was
`rtk proxy /tmp/hyhome-v28-toolchain-venv/bin/python -m unittest tests.lib.supply_chain.test_update_gates.UpdateEvidencePackageTests.test_current_root_census_excludes_relocated_lab_history tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests.test_n8n_source_receipt_does_not_reuse_previous_native_acceptance -v`.
It exited 1 after 1.966299674 seconds with two tests and two failures; the
execution timestamp and durable raw-log path were not recorded. The first
failure is not the only cause: the current root has 112 expected services and
the ledger has 111, because `blog-ingestion` has no truthful ledger entry.
Separately, both the root and ledger enumerate 44 include inputs, but 13
stored digests are stale. The current root input manifest is
`8ccf45441658f551de44e723af512bdd19666fce17b57654e78efdab684858df`.

| Input path | Stored SHA-256 | Current SHA-256 | Attribution |
| --- | --- | --- | --- |
| `docker-compose.yml` | `20b72108463e4883b4bed328507021a152436fd4a04fe163fe2bf26f9f18f411` | `95a797947e7be5954f7673a252170b16d94db562f9552016db73a5eb6f27559c` | Pre-existing root residual |
| `infra/01-gateway/nginx/docker-compose.yml` | `d719e16568e1d898bfc0978c405910e118b3bb58cf7f09dfe6615610546624bb` | `f4162f1ae131db51901127a22d52982134ac6c1668e0b4e5daabd8dbfb606c1e` | P02 change |
| `infra/01-gateway/traefik/docker-compose.yml` | `478c42e90ac88dcb49fee1e236836afe110d143bea4560206b8a4d30a54e6841` | `4b0c9a0d170c721bed25000a1b3f34ee2711b309edd2f78b063cc4dc995dde0b` | Pre-existing stale input plus P02 change |
| `infra/02-auth/keycloak/docker-compose.yml` | `4f54b5785bedf3f21046ba1abe91e3800302109cdede4b5baa9e371e4482e547` | `bda416f399d071abc554db5251b67e0e2228e98608cd80c0bb078e20792f9707` | P02 change |
| `infra/02-auth/oauth2-proxy/docker-compose.yml` | `b3dda3d3640c9e46ab59ee21168237956b04586fbadd5e5936d11d73af2cdeb3` | `6a3bbb2dd657e2a975b2c7da1e8e7297acc599f7f18c9baf8e90c040cb4bd22a` | P02 change |
| `infra/04-data/mng-db/docker-compose.yml` | `c840fc410ae8728f833db68802264b551d998b487cb3098bf9ffeb273c8bdee7` | `b02261123e7fc867598b02a1bf9254f6d364e5df75359cf6776edb653ac8b471` | P02 change |
| `infra/04-data/redisinsight/docker-compose.yml` | `1e2aae21929c1ba22fd3a18856d99ff9dcbef93bb500ade703505659867fd961` | `90f9e4145644e405499210e600eac652cd819707e248979a4837e4ce3b5cd23a` | P02 change |
| `infra/06-observability/docker-compose.yml` | `7300c76c56cd07dd965c84b08e524a723d14c20c9d6a5338722c259ec09560a7` | `555bbb09e3e05f1b9de005c2d7210a9931eceb6552f5855a7d524ac14d6d4aa4` | P02 change |
| `infra/07-workflow/airflow/docker-compose.yml` | `bba69bb08a7536c5e84e11302cb2fb518b781d1ecefba46d7c8dc78c8d4ad835` | `b3ddab42b06ae41a332b6b683ffb2846f9a40110903feb6d44727a162e05ecb9` | P02 change |
| `infra/07-workflow/n8n/docker-compose.yml` | `da77261cc68f3bf989ad571b93aa4c4d82872e7b9b44e1fc4f024e45bb71fe36` | `afe7eabe63e19a889ec608fb76900ff908b0da32faf261f99099fb0e5b6009f7` | Pre-existing stale input plus P02 change |
| `infra/08-ai/open-notebook/docker-compose.yml` | `780ebabe132c9c3c82041c2ce91fa11d78463e2c4abb6c8b9cc4a1c72f6998e4` | `a1d0b2c90982489a48c69198c1c785816246b42cf587fed8b6ac3b71e888b336` | P02 change |
| `infra/08-ai/open-webui/docker-compose.yml` | `831db636e40aad5be4f9805dfef81b91fc104693f1c790bc3625acc633065a53` | `718a214e0515b8befb42ed97c96e1f874725409470a17b6d272af4a23555b93b` | P02 change |
| `infra/09-platform-ops/terrakube/docker-compose.yml` | `49b086010504cc2f4a62983e658f5df3313019d47ae888e3381cbcc3c9037e81` | `9b812e0c04256d9f3f2144835d46b07b44f0c4ca6c42cc058a1512bbd97ca3ae` | P02 change |

P05/P08 owns resumption: add a truthful ledger identity/image/provenance entry
and expected service for `blog-ingestion`, then reconcile the root input set as
one owned provenance transaction before rerunning the exact methods. This is
not a blind hash replacement: the 12 P02-changed Compose inputs must be
distinguished from the root pre-existing residual, while Traefik and n8n have
both earlier and P02 deltas. Rollback affects only that owning
ledger/declaration transaction. P02 must not alter the service, invent
provenance or operate a runtime; the parsed `services.blog-ingestion`
declaration is unchanged from baseline.

The later durable bounded recheck preserves the same result without changing
its inputs: it started `2026-11-02T02:34:59.646222+00:00`, ended
`2026-11-02T02:35:00.712717+00:00`, exited 1 after 1.066466 seconds, and
reported two failures with no errors. Its value-free receipt is
`_workspace/repo-support/analysis/p02/supply-residual-rerun.json` SHA-256
`6cd886baa61573b33ace9d790e41a075e093aef1db3a3cc15da23d604fab43d3`; the
sanitized log SHA-256 is
`d31635fa415210ebd58cb22603a0696de60319e02841c5cdfbad4135b99cd783`.
The four test/ledger/build-input source fingerprints are byte-identical before
and after the run. This durable receipt supplements, and does not erase, the
earlier timestamp-unrecorded 1.966299674-second observation.

### 2026-11-08 root source re-binding

On clean `main` `6361e93b5`, `test_update_gates` failed 57 times: 56 rows of
`test_current_rows_match_root_compose_source` and
`test_current_root_census_excludes_relocated_lab_history`. Every failure was a
stale file hash. The same test's image and build assertions passed for every
row, and service membership matched the root census. Fourteen root Compose
inputs had changed after their rows were last bound, through these commits
since `ed67f3e7b`: resource reservations (`386074326`, `385aa1590`,
`4eadac40a`), SSO-only ingress networks (`a15876218`), ComfyUI egress
(`78461aef1`, `51008aa3c`), consumer-only listener networks (`7f3030a54`) and
the n8n main runner removal (`6792f6d30`). None changed an image, a build input
or the service set.

A new `source_refreshes` entry keeps the previous include inputs and the
previous binding of each of the 56 rows, then re-binds the include hashes and
those rows' `source_input_sha256`. `source_refreshed_at` is unchanged, and no
vendor lookup, signature, SBOM, scan, native, deployment or recovery result is
promoted. Afterwards `test_update_gates`, `test_sec01_next_tool_candidates`,
`test_p08_ci_routing` and `test_workflow_version_bundle` ran 63 tests: OK, two
declared skips.

## Handoff

| Target | Disposition | Current owner | Resume condition and recovery |
| --- | --- | --- | --- |
| P03 product/model registration | OUT_OF_SCOPE | P03 acceptance owner | Consume the exact P02 connection row; product-side registration and function proof remain separate |
| P04 Airflow URI encoding and native Celery behavior | TEST_RESIDUAL | P04 acceptance owner | Current frozen `infra/07-workflow/airflow/docker-compose.yml` SHA-256 `b3ddab42b06ae41a332b6b683ffb2846f9a40110903feb6d44727a162e05ecb9` has `_CMD` DSNs that interpolate passwords. Reproduce special-URI-character handling against the actual Celery provider before an encoding change; use a synthetic credential and preserve the current file before rollback. P02 changes only transport ports. The former `0bbb7e…` fingerprint is a dated pre-freeze observation, not current evidence. |
| P05 n8n consumer behavior | TEST_RESIDUAL | P05/P08 acceptance owners | Consume listener, MNG endpoint and Valkey ACL evidence; preserve accepted historical C19/C22 scope. Jointly add the truthful `blog-ingestion` identity/image/provenance and expected-service record, reconcile current root inputs and rerun the two recorded fail-closed methods. Do not fabricate vendor/native completion or operate the service. |
| P06 secret custody and issuance | OUT_OF_SCOPE | P06 acceptance owner | Issue or rotate only with actual secret owner, target and recovery boundary. P02's synthetic presentation contract permits group-readable `0440`/`0640` where the service has the group, or runtime-`999` owned `0400`/`0600`; it rejects `0444`, `0644`, symlinks and hardlinks. The earlier grant finding was corrected in P02 by narrowing an overbroad mount; P06 custody, issuance and rotation remain unexecuted. P02 records no value and does not issue a credential. |
| P07 observations | OUT_OF_SCOPE | P07 acceptance owner | Add measurements only after selected source topology and consumer evidence are stable |
| P08 Valkey 9.1.3 advisory, supply-chain provenance and dependency audit | IMPROVEMENT_CANDIDATE | P08 image/advisory owner | Assess declared 9.1.2 against the official advisory, client compatibility and rollback before any image update. Jointly with P05, own the blog identity/provenance and 13-input reconciliation transaction above. Archive the old n8n binding aggregate `57ad4d23833e8563576b9021ac3b4a8f67f8a2ecb04faefe41225d99cea7707a` and stored Compose `8792a345bd2ead857d108fc2eb100b8be19a9c5012caa5e457829b978b2adcc3`; mirror the current source-only aggregate `f791262bbd771759c5157b1c3c63e8993e8ca8d24f685d55dcd0f492b5933ca2` and Compose `afe7eabe63e19a889ec608fb76900ff908b0da32faf261f99099fb0e5b6009f7` across `update-ledger.json` and `build-inputs.json` on source base `0592303d1f7d96b46019be7a730c115c53cbbcab`. Then rerun `WorkflowVersionBundleTests.test_n8n_source_receipt_does_not_reuse_previous_native_acceptance` and its nested SEC01 route check. Signature, SBOM, Native, HOME operation and recovery evidence remain `NOT_RUN`. Rollback only the owned receipt transaction. Own the failed controller dependency transaction: update canonical dependency input manifest(s), generated lock and appended evidence together; verify affected controller gates. Recovery reverts only the input-plus-lock delta and preserves the original FAIL receipt/history. |

## Related Documents

- [SPEC-0212](../spec.md)
- [SPEC-0212 Plan](../plan.md)
- [Historical P03 service integration contracts](../../0204-service-integration-security-and-operations/tasks/tsk-0011-p03-service-integration-contracts.md)
- [Application authentication guide](../../../05.operations/guides/03-identity-and-access/0079-application-auth-integration.md)
- [Workspace inventory data](../../../90.references/data/0096-workspace-inventory/README.md)
