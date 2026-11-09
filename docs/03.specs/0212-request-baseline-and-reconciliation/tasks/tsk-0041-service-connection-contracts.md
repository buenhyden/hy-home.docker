---
title: "Service Connection Contracts Task"
version: "0.1.41"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-09"
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
| ComfyUI-Manager security level HOME apply | 57 | W62 | Approved HOME edit and restart, then file, health, network and device readback | RUN-0081 0.5.0, container `78dbdf9f0021` | PASS | `weak` to `normal`; healthy in about 120 s; `comfyui_ingress_net` only; backup under `~/storage/backups/comfyui-manager-20261108/` | required | - |
| D03 Valkey memory cap HOME apply | 59 | W64 | Approved `mng-valkey` recreate, then config, AOF, keyspace, client and consumer readback | `main` `4bb6c0295`, container `a9e9b49ba896` | PASS | `maxmemory` 134217728 `noeviction`; 82 keys; consumers healthy, restart counts unchanged; Valkey errors only during the 7-second restart window; backup under `~/storage/backups/mng-valkey-maxmemory-20261108/` | required | - |
| D03 DEV/MNG render isolation | 59 | W64 | All-profile renders with synthetic DEV and MNG values | `main` `f5ab642ef` plus this test | PASS | Each side leaves the other unchanged; an injected cross reference fails it; new class 2/2; data-tier suites 146 OK (4 declared skips) before it | required | - |
| D03 n8n named-user switch | 59 | W64 | HOME client and ACL readback | Live `n8n`, `n8n-worker`, `mng-valkey` | NOT_RUN | BLOCKED: default user in use; `mng_valkey_n8n_password` not issued or mounted; needs the secret owner and a drain/backup approval | optional | - |
| D03 named Valkey user durable native rehearsal | 59 | W64 | Opt-in native class with AOF restart on port 16379 | Pinned 9.1.2-alpine, synthetic secrets, network-less labelled container | PASS | 3/3 OK in 77.5 s; key and wait list survive restart; denials and WRONGPASS hold after it; tmpfs variant fails; residue 0 | required | - |
| D03 n8n named-user HOME switch, first attempts | 59 | W64 | Approved recreate of `mng-valkey`, `n8n` and `n8n-worker`, then readback | `main` `6ac20f161`, `.env` named-user selection and `COMPOSE_FILE` | FAIL | Stale image entrypoint refused the pair (rolled back), then the rebuilt image hit NOPERM on `getdel` and `mget` (rolled back); `mng-valkey` keeps the added user; backup under `~/storage/backups/mng-valkey-n8n-user-20261108/` | required | - |
| D03 n8n cache and registry ACL commands | 59 | W64 | Static RED/GREEN and opt-in native class | n8n 2.43.6 code reading; pinned 9.1.2-alpine | PASS | Seven commands added; `keys` and `flushdb` still denied; native 3/3 in 74.1 s, residue 0 | required | - |
| D03 n8n named-user HOME switch after the ACL fix | 59 | W64 | Approved recreate, then health, ACL LOG, log and client readback | `main` `9939431c3`, image `f1493a20a2ff`, containers `435672289f3b` and the recreated `n8n`/`n8n-worker` | PASS | Healthy, no restarts; 19 `user=n8n` connections incl. worker `brpoplpush`; no `NOPERM`/`WRONGPASS` over three minutes; other consumers unchanged | required | - |
| D03 live job through the named user | 59 | W64 | Next workflow execution observed on `user=n8n` | HOME n8n after the switch | NOT_RUN | No execution in the watch window; confirm on the next run | optional | - |
| D03 live job through the named user, observed | 59 | W64 | Next workflow execution observed on `user=n8n` | HOME n8n after the switch, execution 127 | PASS | Enqueued by main, run by the worker, `success` in the n8n database; no `NOPERM` or `WRONGPASS` | optional | D03 live job through the named user |
| n8n Assistant model and SearXNG configuration | 60 | W65 | Compose render, `N8nAssistantSearchContractTests`, hardening pin, operations catalog | Branch base `ab34255ae` plus this change | PASS | Model and search URL on main only; `searxng` has no ports, route or privilege; the search network holds only `n8n` and `searxng`; no Anthropic key variable | required | - |
| n8n Assistant search live | 60 | W65 | Create `searxng`, ask the Assistant a web question, check `/healthz` and the JSON API from `n8n` | HOME | NOT_RUN | No container was created; the stack needs its own approval and the apply order in the report | required | - |
| n8n Assistant code sandbox | 60 | W65 | Firecracker runner without `privileged` | `n8nio/n8n-sandbox-service-runner-firecracker:1.8.1` | NOT_RUN | BLOCKED: the runner needs netns, veth, TAP, iptables, mount and jailer rights close to `privileged`, and a possible enterprise license; not added | required | - |
| n8n code sandbox (privileged DinD) configuration | 60 | W65 | Compose render, `N8nCodeSandboxContractTests`, `compose_controls.py`, Conftest verify, hardening pins | Branch base `4f91fa0da` plus this change | PASS | One privileged service; no ports, routes or Docker socket; runner on two distinct internal and outbound networks; digest-pinned 1.8.1 images; keys from secret files; exceptions recorded | required | - |
| n8n code sandbox secret metadata | 60 | W65 | `test_secret_metadata_sync` against the public secret metadata | `secrets/SENSITIVE_ENV_VARS.md.example` | FAIL | Two tests fail until three rows for the sandbox secret files are added to the metadata source and the OpenBao catalog; that file is denied to this session | required | - |
| n8n code sandbox live | 60 | W65 | Create the three secret files, start profile `n8n-sandbox`, check API health, runner registration, one sandbox and an Assistant code step | HOME | NOT_RUN | No container was started; DinD under `no-new-privileges` and `cap_drop: ALL`, mTLS registration and the image pull are unverified | required | - |
| SEC01 root source re-binding and crawl4ai-loopback row | 60 | W65 | `test_update_gates` | Clean `main` `b4d09cbd7` | PASS | 51 failures before (50 stale file hashes, 1 missing `crawl4ai-loopback` row); 39 tests OK after; image, build and the other membership unchanged | required | - |
| n8n 2.46.6 source pin and digests | 60 | W65 | Read-only Docker Hub registry, GitHub release and npm lookups | Branch base `0220de58a`; `n8nio/n8n:2.46.6`, `n8nio/runners:2.46.6` | PASS | Index digests `sha256:8602f5df…92b3ae` (n8n) and `sha256:b1fe87a5…322612` (runners); `stable`, `latest` and the tag agree; release `n8n@2.46.6` published 2026-11-04, not a prerelease; recorded in the SEC01 lookups and ledger | required | - |
| n8n 2.46.6 signature, full-image scan, build, native and HOME | 60 | W65 | Publisher signature, SBOM or scan, `hyhome/n8n` build, native queue and HOME recreate | Same inputs | NOT_RUN | Out of this source unit; the local image build and every recreate wait for their own approval | required | - |
| n8n router without gateway SSO | 57 | W62 | Static Compose label, Compose render, `RouteAuthContractTests`, `SsoOnlyIngressContractTests`, hardening gate | Branch base `0220de58a` plus this change | PASS | `traefik.http.routers.n8n.middlewares` is `gateway-standard-chain@file`; `docker compose --env-file .env.example config -q` exits 0; `check-all-hardening.sh` ALL PASS; `hermes-webhook.yml` unchanged | required | - |
| n8n live login without gateway SSO | 57 | W62 | Browser or HTTP check after the Traefik reload | HOME `n8n` host | NOT_RUN | No Traefik reload or recreate performed; confirm the n8n login page answers without a Keycloak redirect after the approved apply | required | - |
| n8n router exclusions for `/metrics` and the Hermes path | 57 | W62 | Static Compose rule, Compose render, hardening gate pins, `RouteAuthContractTests`, catalog check | Branch HEAD `1899263f4` plus this change | PASS | Rule excludes both prefixes; `docker compose --env-file .env.example config -q` exits 0; `check-all-hardening.sh` ALL PASS; Prometheus targets `n8n:5678` directly | required | - |
| n8n router exclusions live behaviour | 57 | W62 | Request to `/metrics`, a GET and a trailing-slash request to the Hermes path through Traefik | HOME gateway | NOT_RUN | No Traefik reload or recreate performed | required | - |
| OpsflowSmtp `n8n-workflow` pin and node tests | 60 | W65 | `npm ci`, `npm test` and `npm run test:coverage` in a scratch copy of the node | Branch HEAD `1899263f4` lock (zod 3.25.76, no zod override) | PASS | 38 of 38 pass; coverage 97.51 percent lines, 95.56 branches, 88.57 functions | required | - |
| OpsflowSmtp `npm audit` | 60 | W65 | `npm audit --package-lock-only` full and `--omit=dev` | Same lock | FAIL | Full audit: 3 high through GHSA-mrhx-c7xc-m3w5 on the `n8n-workflow` dev path; production audit: 0. No exception recorded; the failure is stored in `package-lookups.json` | required | - |
| OpsflowSmtp `npm audit` gate decision | 60 | W65 | `npm audit --package-lock-only` full and `--omit=dev` | Same lock; owner chose the production-only CI gate on 2026-11-09 | PASS | `leaf.opsflow-smtp-npm-audit` removed; `leaf.opsflow-smtp-npm-production-audit` stays and reports 0. The dev-tree finding remains and is no longer gated. | required | OpsflowSmtp `npm audit` |
| Dockerfile `n8n --version` and node load check | 60 | W65 | Build-time `RUN` check | `hyhome/n8n` image | NOT_RUN | Image not built; the node's `npm test` loads `n8n-workflow` 2.46.5 from the lock, which is not the image check | required | - |
| n8n OpenTelemetry configuration | 60 | W65 | Module source at `n8n@2.46.6`, Compose render, hardening pin, operations catalog | Branch base `e8631262b` plus this change | PASS | Default module, no license flag for tracing; `n8n` and `n8n-worker` render the three `N8N_OTEL_*` settings; worker also on `obs_net`; no credential or payload attribute in the constants | required | - |
| n8n spans reach Tempo | 60 | W65 | Recreate `n8n` and `n8n-worker`, run a production workflow, search Tempo for service `n8n` and `n8n-worker` | HOME | NOT_RUN | No recreate; also confirm the worker reaches `alloy:4318` over `obs_net` | required | - |
| n8n router case-insensitive exclusions | 57 | W62 | Compose render, `RouteAuthContractTests.test_n8n_router_exclusions_ignore_letter_case`, hardening pins | Branch base `e8631262b` plus this change | PASS | Rule uses `PathRegexp` with `(?i)` for `/metrics` and the Hermes prefix; plain `PathPrefix` fails the test | required | - |
| n8n router letter-case behaviour live | 57 | W62 | `GET /METRICS`, `/Metrics` and a mixed-case Hermes POST through Traefik | HOME gateway | NOT_RUN | Live finding before the fix: `/METRICS` and `/Metrics` returned metrics inside the container; the fix needs the `n8n` recreate | required | - |
| n8n documentation and catalog checks | 57 | W62 | `check-operations-catalog.py`, `check-document-metadata.py --mode check-changed --base-ref origin/main`, `check-document-links.py --mode alignment` | Branch base `0220de58a` plus this change | PASS | Catalog PASS after patching the stale n8n router cell in `m0021`; metadata 12 selected, 0 violations; links 0 failures | required | - |
| n8n consumer test suites | 60 | W65 | 41 modules naming n8n, `2.43.6` or `sso-auth`, plus `test_p02_service_contracts` and `test_compose_baseline_gates` | Branch base `0220de58a` plus this change, venv on `PATH` | FAIL | 1069 tests, 51 failures, 83 declared skips; the same 51 fail on a clean checkout of `0220de58a` (`test_update_gates` stale `source_input_sha256` for 50 rows and the root census); none is new and the n8n rows, `test_workflow_version_bundle`, `test_sec01_next_tool_candidates` and `test_p08_ci_routing` pass | required | - |
| Traefik v3.7.17 pin and digests | 60 | W65 | Anonymous Docker Hub registry API and GitHub latest-release API, release notes and v3.7 migration guide read | Branch base `be3cab6a6`; `traefik:v3.7.17` | PASS | Index `sha256:f4bb143d…86f5a` (raw SHA256 equals `Docker-Content-Digest`), linux/amd64 manifest `sha256:e15b8921…81511a`, config `sha256:d848e658…bcb2e21`; release `v3.7.17` published 2026-10-30, not a prerelease; recorded in the SEC01 files | required | - |
| Traefik v3.7.17 signature, scan, config boot and HOME | 60 | W65 | Publisher signature, SBOM or scan, config boot, recreate | Same inputs | NOT_RUN | The image was not pulled or inspected; the running Traefik is unchanged and every recreate waits for its own approval | required | - |
| Traefik v3.7.17 consumer checks | 60 | W65 | `test_update_gates`, `test_compose_baseline_gates`, `test_p02_service_contracts`, `test_tech_stack_version_contract`; `docker compose --env-file .env.example config -q`; `check-all-hardening.sh 01-gateway` | Branch base `be3cab6a6` plus this change | PASS | 286 tests OK, 31 declared skips; Compose render exits 0; `check-all-hardening.sh 01-gateway` ALL PASS | required | - |

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

### 2026-11-08 ComfyUI-Manager security level HOME apply

The `yanwk/comfyui-boot` bundle seeds `user/__manager/config.ini` with
`security_level = weak`; ComfyUI-Manager 3.41 defaults to `normal`. RUN-0081
0.5.0 (#816) sets `normal` as the target. With approval, the HOME file was
backed up to `~/storage/backups/comfyui-manager-20261108/`, set to `normal`
with the RUN-0081 command, and `comfyui` was restarted (same container
`78dbdf9f0021`). It returned healthy in about 120 seconds on
`comfyui_ingress_net` only; the file reads `security_level = normal`, and the
Manager log loads that path. `[ComfyUI-Manager] PyTorch is not installed` also
appeared on the previous start; torch 2.14.0+cu126 imports in the container and
`/system_stats` lists a `cuda` device. Rollback restores the saved file and
restarts the container.

### 2026-11-08 shared Valkey memory cap HOME apply

The D03 cap above stayed source-only: on 2026-11-08 Prometheus still reported
`redis_memory_max_bytes` 0 for `mng-valkey` (started 2026-11-02, before the
change) and 134217728 for `dev-valkey`. With approval, the pre-state and a
`docker cp` of `/data` (AOF and RDB, 18 MB) were saved to
`~/storage/backups/mng-valkey-maxmemory-20261108/`. The rendered service at
`main` `4bb6c0295` differed from the live container only by the 32 MiB memory
reservation; image, entrypoint, secrets, `mng_data_net` and the
`192.168.0.13:26379` binding matched. Only `mng-valkey` was recreated
(`up -d --no-deps --force-recreate`, profile `mng`): container `53cf5cdf0b4c`
became `a9e9b49ba896` and was healthy in about 10 seconds.

Afterwards `maxmemory` is 134217728 with `noeviction`, AOF is enabled with
`aof_last_write_status:ok`, the dataset loaded with 82 keys in db0, and 39
clients reconnected. n8n, n8n-worker, the worker runner, the five Airflow
services, oauth2-proxy and the exporter stayed healthy with unchanged restart
counts. Their only Valkey errors were `connection refused` and `LOADING`
between 05:39:33 and 05:39:40 UTC, during the restart; none appeared
afterwards. One oauth2-proxy session lookup in that window failed to load.
Rollback is to stop the container, restore the saved `/data` and recreate from
the previous source.

### 2026-11-08 D03 re-verification

A direct user request on 2026-11-08 re-ran D03 on clean `main`
`f5ab642ef`, Docker context `default`, branch
`test/d03-dev-mng-render-isolation`. Since the 2026-11-04 run at `73ccd9930`
the data-tier Compose diff is resource reservations (D09), the SeaweedFS S3
metrics bind and the removed lakehouse table-bucket job; no database, Valkey
mode, credential or data path changed. The data-tier suites (DEV boundary,
DEV/MNG Valkey ACL, MNG init SQL, Valkey mount scope, restore, upgrade and
rehearsal boundary) ran 146 tests: OK, four declared skips.

**T01 gap.** Only one direction was pinned: DEV consumers do not read the MNG
PostgreSQL variables. `DevMngRenderIsolationTests` now renders every profile
from `.env.example` with synthetic DEV and then MNG values. DEV values change
only `dev-*` services and the `dev-pg` provision consumers; MNG values change
no DEV-side service, and RedisInsight keeps its `dev-valkey:6379` connection
while only its `mng-valkey` port follows. Adding a `${POSTGRES_PORT}` reference
to `dev-pg` made the test fail; the source was restored. One fixed `HOME`
keeps `$HOME` binds (OpenTofu) from showing as a difference.

**T02/T03.** The per-application default mode is unchanged: n8n and Airflow
use shared `mng-valkey`, `dedicated-valkey` is opt-in (ADR-0007). HOME `n8n`
and `n8n-worker` run with host `mng-valkey`, empty username, Secret
`mng_valkey_password` and DB 0; `mng-valkey` has no `MNG_VALKEY_N8N_ENABLED`
and no `mng_valkey_n8n_password` mount. The named-user switch in RUN-0053 is
therefore BLOCKED on secret issuance by the secret owner and a separate
drain/backup approval. The opt-in native rehearsal runs with AOF off and an
ephemeral port, so restart, AOF reload and a nondefault port for the named
user remain NOT_RUN. Airflow's `connection_uri.py` admits only
(host, secret) broker pairs and builds no username, so no Airflow named user is
introduced. The exporter checks from the 2026-11-04 run still pass.

**T04.** Docker data-root `~/storage/docker-root` is on the HDD (`sdb`,
rotational, 2.7T, 10% used); `/` is on the SSD (`sda`, 52% used). The four
database volumes are named volumes there. `mng-pg` keeps PGDATA
`/var/lib/postgresql/data/pgdata` inside `mng-pg-data`; the extra anonymous
volume at `/var/lib/postgresql` comes from the image `VOLUME` and holds no
data. `dev-pg` keeps PGDATA under its `/var/lib/postgresql` volume. No
bottleneck was measured, so the accepted placement stays and nothing moved.

**T05.** The store set equals the 2026-11-04 record: one MNG and one DEV
PostgreSQL 18, shared `mng-valkey`, Prometheus as the single time-series
store, no InfluxDB or clusters; OpenSearch, Neo4j and RedisInsight stay
OPTIONAL in the `infra/04-data` README table.

Official pages read 2026-11-08T05:56Z: Valkey ACL SETUSER (database rules
since 9.1.0, so the declared 9.1.2 supports `db=0`; no memory or process
isolation claim) and Airflow Connections (documents 3.4.0, installed 3.3.2;
environment connections resolve on the worker and do not appear in the UI).
Runtime change, restore and Hosted CI for this run are NOT_RUN.

### 2026-11-08 named Valkey user durable native rehearsal

With the owner's approval on 2026-11-08, the opt-in native class gained
`test_named_queue_user_survives_restart_and_aof_reload_on_nondefault_port`.
It starts the pinned `valkey/valkey:9.1.2-alpine` image with the rendered n8n
ACL, AOF with `appendfsync always` on a temporary host directory, and port
16379 on a network-less, labelled container. As user `n8n` it writes a job key
and a wait list, sees no listener on 6379, restarts the container and reads
both back. After the restart the ACL still refuses `CONFIG`, a foreign key,
`SELECT 1`, `FLUSHDB` and a wrong password. With `HYHOME_N8N_ACL_REHEARSAL=1`
at 2026-11-08T06:12:57Z the class ran 3 tests OK in 77.5 seconds, including
the pinned Bull retry/delay/lock rehearsal; container and network residue was
zero. With the data directory switched back to tmpfs the new test failed on
the lost key and list, so it detects a non-durable broker. This is isolated
evidence; the HOME switch is separate.

### 2026-11-08 n8n named-user HOME switch, first attempts

With the owner's approval, the secret owner issued
`secrets/db/mng-valkey/n8n_password.txt` (group-readable by Valkey, one
link), set `N8N_VALKEY_USERNAME=n8n` and `N8N_VALKEY_SECRET` in `.env`, and
fixed the overlay set with `COMPOSE_FILE` (base, `docker-compose.n8n-acl.yml`,
`docker-compose.ollama-local.yml`). Before the switch the n8n queue was empty
(no wait, active, delayed, paused or prioritized key), every n8n key used the
`n8n:` prefix, and `mng-valkey` `/data` plus the three containers' state were
saved to `~/storage/backups/mng-valkey-n8n-user-20261108/`.

At 06:34 UTC `mng-valkey` was recreated with the overlay (`351ac5de090c`,
healthy; users `default`, `mnginspector`, `mngmonitor`, `n8n`; 84 keys,
`noeviction`, AOF ok). The n8n recreate at 06:35 FAILED: `n8n` restarted 12
times with `unsupported n8n broker/secret selection`, because the running
`hyhome/n8n:2.43.6-local` image (built 2026-10-20) still carried an
entrypoint that knew only the default and dedicated pairs. n8n was rolled back
to the default user by shell override at 06:40 (about five minutes down, queue
empty). The image was then rebuilt from `main` `6ac20f161` (new
`f1493a20a2ff`, entrypoint equal to the source, previous image kept as
`hyhome/n8n:2.43.6-local-pre-20261108`). The second switch at 07:02 came up
healthy with eight `user=n8n` connections, but the n8n cache store hit
`NOPERM` on `getdel` and `mget`, so n8n was rolled back to the default user
again at 07:04 on the rebuilt image (healthy, no restarts, 41 `default`
connections).

Reading the installed n8n 2.43.6 code, its Valkey users are Bull, pub/sub,
leader election, the lock, the instance registry, chat-hub and the
`@n8n/backend-services` cache store. The cache store also calls `mget`, `mset`,
`getdel`, `hexists`, `hkeys` and `hvals`, and the instance-registry Lua
script calls `PEXPIRE`. Its `keys` and `flushdb` paths have no caller and stay
denied on the shared DB0. The ACL now grants those seven commands. The static
test failed before the change; the opt-in native class (approved, run
2026-11-08T07:07Z) passed 3/3 in 74.1 seconds, with residue zero. It now
exercises the new commands, including `MGET` from Lua, and refuses `MGET` and
`GETDEL` on a foreign key. `test_secret_metadata_sync` fails 15 tests locally on
both this branch and clean `main` and is unrelated to this change; the hosted
CI result is the record for it.

### 2026-11-08 n8n named-user HOME switch after the ACL fix

After #821 merged (`main` `9939431c3`), the queue was empty again and
`mng-valkey` `/data` was saved again (`data-0715`, 2.1 MB). At 07:33 UTC
`mng-valkey` was recreated with the overlay (`435672289f3b`, healthy in about
30 seconds; the `n8n` user now carries the cache and registry commands; 85
keys, 128 MiB `noeviction`). At 07:34 `n8n` and `n8n-worker` were recreated
from `.env` without any override, on the rebuilt image `f1493a20a2ff`. Both
were healthy in about 75 seconds with no restarts. During a three-minute watch
neither log showed `NOPERM` or `WRONGPASS`, and `ACL LOG` held no `n8n` entry
(its only row is the existing `mngmonitor` `slowlog|get` denial). 19
connections authenticate as `n8n`, among them the worker's `brpoplpush` on the
jobs queue and a successful `getdel`; the other 20 consumers stay on
`default`, and oauth2-proxy, the Airflow worker and scheduler, the exporter and
the task runner stayed healthy. No workflow ran in the window (job id counter
126, no completed or failed entry), so a live job through the named user is
NOT_RUN until the next execution. RUN-0053 now records the entrypoint check,
the fixed overlay set and the override rollback. Rollback: recreate `n8n` and
`n8n-worker` with the default-user override; the saved `/data` restores the
broker if needed.

### 2026-11-08 live job and local metadata-suite failure

Execution 127, a manual run, was enqueued by `n8n`, started and finished by
`n8n-worker`, and reported finished to main at 07:51 UTC. The n8n database
records `status = success` (07:51:10 to 07:51:15). All of it ran over
`user=n8n` connections with no `NOPERM` or `WRONGPASS`, so the live job row is
now PASS. The switch backup and the rollback image tag were deleted on the
owner's instruction.

`test_secret_metadata_sync` failed 15 tests locally but passed in hosted CI.
The system `python3` 3.12.3 carries Ubuntu's `jsonschema` 4.10.3, below the
`scripts/requirements.txt` floor of 4.23, so `secret_catalog.validate_catalog`
could not import `referencing`. `gen-secrets.sh` turned that import error
into its generic "unsafe input" rejection. The documented ignored `.venv`
now holds the declared requirements (`jsonschema` 4.26.0, `referencing`
0.37.0), and the suite passes with it on `PATH`. The catalog and metadata
blocks of `gen-secrets.sh` now name a missing module and point to the
requirements file, without printing any value; the new test failed before
that change.

### 2026-11-09 root source re-binding and crawl4ai-loopback

On clean `main` `b4d09cbd7`, `test_update_gates` failed 51 times: 50 rows of
`test_current_rows_match_root_compose_source` and
`test_current_root_census_excludes_relocated_lab_history`. Every hash failure
was a stale file hash: the image and build assertions passed for all 96 rows.
Nine root Compose inputs had changed after their rows were last bound (dev-db,
mng-db, kafka, observability, airflow, ComfyUI, crawl4ai, open-webui and
storybook). The census failure was the `crawl4ai-loopback` service added to
`infra/08-ai/crawl4ai/docker-compose.yml` (`f816150a6`), which had no row.

A new `source_refreshes` entry keeps the previous include inputs and the
previous binding of each of the 50 rows, re-binds the include hashes and those
rows' `source_input_sha256`, and lists `crawl4ai-loopback` under
`added_services`. `source_refreshed_at` of the re-bound rows is unchanged. The
new row is BLOCKED: its image is the same digest pin as `crawl4ai-egress`, and
every release, signature, scan, compatibility, runtime and recovery field says
`UNKNOWN`, `NOT_RUN` or `NOT_OBSERVED`. The `p08_public_release_observations`
denominator moves to 97 and the row joins `services_without_related_source`,
with an `added_root_service_mapping` record; the observation rows are
unchanged. The n8n rows were not touched. No test code was stale, so none
changed. Afterwards `test_update_gates` ran 39 tests: OK.

### 2026-11-09 n8n 2.46.6 and native login only

The owner asked: "n8n 최신 안정판(2.46.6)으로 업데이트하고, n8n 로그인만 유지." and
"이중 로그인은 불가하다." The `n8n` Traefik router therefore drops `sso-errors@file`
and `sso-auth@file` and keeps `gateway-standard-chain@file`; n8n's own login is the
only login. The `hermes-webhook.yml` exact-path router is unchanged. The n8n UI and
API are now reachable through the gateway without SSO, so n8n's own authentication
and `N8N_PAYLOAD_SIZE_MAX` are the only controls in front of them. The router test
list `ROUTES_WITHOUT_SSO` gained `n8n: native-login`, because it encoded the old
decision; no other test asserted `sso-auth` on n8n.

The same day the owner withdrew the time-boxed acceptance of the runtime Zod
advisory: "정책에 걸려 있어(POL-0053, 11월 26일까지) -> 폐기한다." POL-0053 no longer
carries the "런타임 Zod advisory 기한부 수용" section, and no replacement policy was
written. The facts stay recorded here. n8n 2.46.6 still depends on zod 3.25.76
(npm metadata), inside the range of GHSA-mrhx-c7xc-m3w5 (zod below 4.6.6; memory
exhaustion from large arrays, availability only). `N8N_PAYLOAD_SIZE_MAX` (default
4 MiB) remains in the Compose file. The 2026-10-27 acceptance and the 2026-11-26
deadline in the TSK-0009 and TSK-0008 records are history and are not edited.

The pin moves `n8n`, `n8n-worker` and `n8n-task-runner-worker` from 2.43.6 to 2.46.6
in both Dockerfiles, the Compose file, `infra/tech-stack.versions.json` and the
version-bundle and runner-isolation tests. The base digests are the OCI index
digests of `n8nio/n8n:2.46.6` and `n8nio/runners:2.46.6`, read from the Docker Hub
registry on 2026-11-09 and also pulled by digest to the local image store. The
GitHub release notes for 2.44 through 2.46.6 list no breaking change for this
deployment. Changes worth a canary: queue jobs go to one idle worker in turn
(2.46.2); JavaScript task runners disable Node web storage (2.46.0); workflows with
deprecated nodes can no longer be created or updated through the API (2.44.0) and
the editor blocks them (2.46.0); Webhook and MCP Trigger nodes can authenticate
through trusted sources (2.46.0); `N8N_SCHEDULER_MIN_INTERVAL` was removed
(2.45.0) and is not set here. None of the queue-mode, external-runner,
`N8N_METRICS` or webhook-path settings changed. The patched versions of
GHSA-prmc-fg87-r4gh and several High advisories from 2026-10-28 are 2.45.5 on the
2.45 line and 2.46.1 on the 2.46 line, so 2.43.6 was inside their ranges and 2.46.6
is not.

The SEC01 evidence package follows the pin. The n8n rows, the ledger and
build-input source bindings, the release, image and package lookups and the
`include_inputs` Compose hash were rewritten; the previous candidate (2.45.7), the
previous source bindings and the previous lookups are archived inside the same files.
`test_update_gates` still fails for 50 rows and the root census on a clean
`0220de58a` because other root Compose files changed after their last re-binding
(see the 2026-11-08 root source re-binding); this change neither fixes nor worsens
that set. Signatures, a full-image
scan, the `hyhome/n8n` build, native and HOME acceptance are `NOT_RUN`.

Follow-up on the same day, on PR #849. The owner asked that the n8n versions be
unified ("n8n-workflow도 업데이트. n8n 관련 버전은 통일한다."), so the OpsflowSmtp
package and lock pin `n8n-workflow` 2.46.5, which 2.46.6 bundles. The `zod: 4.6.6`
override was removed because `n8n-workflow` 2.46.5 does not load under Zod 4
(`zod.string().ip is not a function`); the axios override stays (the lock resolves
axios 1.20.0). The lock now resolves zod 3.25.76 in the dev tree. In a scratch copy
`npm test` passes 38 of 38 and the coverage script passes (97.51 percent lines, 95.56
branches). `npm audit` on the full lock now reports three high findings, all through
GHSA-mrhx-c7xc-m3w5 (`zod`, `@n8n/expression-runtime`, `n8n-workflow`); the production
audit reports zero. The owner withdrew the Zod acceptance, so no exception or new
acceptance is recorded: the package-lookups record shows the failing full audit as
observed, and the previous zero-finding audits are archived beside it. This is the
open item to decide: either an `n8n-workflow` release on Zod 4 or a separate owner
decision. The runtime image is unaffected, because the deployable package carries no
`node_modules`.

Two router fixes follow from removing SSO. The `n8n` router rule is now
``Host(`n8n.${DEFAULT_URL}`) && !PathPrefix(`/metrics`) && !PathPrefix(`/webhook/hermes-blog-ingestion`)``.
`N8N_METRICS` serves unauthenticated `/metrics` on the app port, which the Host-only
router would now publish; Prometheus scrapes `n8n:5678` on the internal network and is
unaffected. A trailing-slash, non-POST or wrong-source request to the Hermes path
used to miss the exact-path Hermes router and fall through to the general router,
skipping its source allowlist, body limit and rate limit; the exclusion closes that.
The Hermes router keeps priority 1000 and is unchanged apart from its header comment,
which no longer claims an `sso-auth` chain. The hardening gate pins both exclusions.
The stale n8n statements in AD-0007 and AD-0022 now say n8n uses its own login. ADR-0059
(accepted) still says Flower and n8n keep the SSO chain in its decision text. The
architecture guide forbids rewriting an accepted decision body and requires a separately
approved new ADR to replace it, so it is left unchanged and reported.

### 2026-11-09 n8n OpenTelemetry tracing and a case-bypass fix

The owner asked to configure and apply n8n OpenTelemetry. In `n8n@2.46.6` the `otel`
module is a default module for `main`, `worker` and `webhook` instances, has no license
flag, and is switched on by `N8N_OTEL_ENABLED`. Only custom span attributes are
license-gated (`isOtelCustomSpanAttributesLicensed`), and those are not used here.
In queue mode main and the worker each export their own `workflow.execute` span per
segment and the worker exports the node spans, so both get the settings. The Compose
file sets `N8N_OTEL_ENABLED=true` and `N8N_OTEL_EXPORTER_OTLP_ENDPOINT` to
`http://alloy:${ALLOY_OTLP_HTTP_PORT:-4318}` in the shared env block and
`N8N_OTEL_EXPORTER_SERVICE_NAME` per service (`n8n`, `n8n-worker`). Every other option
keeps its n8n default: production executions only, sample rate 1.0, node spans on, no
start-marker spans, protocol `http/protobuf`, path `/v1/traces`, no exporter headers.
`n8n-worker` was not on `obs_net`, where Alloy listens, so it gained `obs_net`, the
least network change; it adds no new listener, because the worker's task broker is bound
to its runner network address and its health listener is not enabled. Alloy forwards OTLP
traces to Tempo, and Alloy is not a hard dependency: if it is down n8n logs a startup
connection error and tracing is skipped.

The running n8n already had tracing switched on through the UI: its `features.otel`
settings row holds enabled with the default endpoint `http://localhost:4318`, and the
startup log reports the failed OTLP connection. `OtelSettingsService.loadSettings` in
`n8n@2.46.6` decides per field. A field whose `N8N_OTEL_*` variable (or its `_FILE`
form) is set is env-managed and takes the environment value, whatever the row says;
every other field takes the row value, then the default. The Compose env therefore
overrides the stored endpoint, enabled flag and service name once `n8n` and `n8n-worker`
are recreated, and no Settings change is needed for them. The worker runs the same
module and reads the same row from the shared metadata database, so it behaves the same.
The fields Compose does not set (protocol, path, headers, sample rate, node spans,
start markers, outbound injection, production-only) still follow the stored row, which
the UI save writes in full. Check Settings, OpenTelemetry after the recreate that those
values are the defaults listed above; the settings API marks env-managed fields. The
database was not read or written.

Exported data, from `otel.constants.ts`, `execution-level-tracer.ts` and
`gen-ai-attributes.ts`: instance id and role, workflow id, name, version and node count,
execution id, mode, status, retry fields and error type, node id, name, type and version,
input and output item counts, and project id and, for team projects only, name. AI
agent nodes add agent name and id, model names and token counts. No credential, header
or execution payload is an attribute. Two things still leave n8n: a failed workflow or
node span records the error message and stack as an exception event, and n8n error
messages can quote data, and with `N8N_OTEL_TRACES_INJECT_OUTBOUND` at its default each
outbound HTTP request n8n makes carries a W3C `traceparent` header. Neither was
changed because the owner asked for defaults.

The same day a live check inside the n8n container showed `GET /METRICS` and
`/Metrics` returning metrics, because Express routes paths case-insensitively and
Traefik `PathPrefix` is case-sensitive, so the exclusions merged in PR #849 were
bypassable by letter case. The router rule is now
``Host(`n8n.${DEFAULT_URL}`) && !PathRegexp(`(?i)^/metrics`) && !PathRegexp(`(?i)^/webhook(-test)?/hermes-blog-ingestion`)``.
`PathRegexp` is a Traefik v3 matcher and the pinned v3.7.16 supports it; the Compose
render keeps the backticks and `(?i)` unchanged. The Hermes router keeps priority 1000
and its exact case-sensitive path, so a mixed-case Hermes POST now matches no router and
gets 404. The same `!PathPrefix(`/metrics`)` pattern exists on the Gatus router
(`infra/06-observability/docker-compose.yml`); it was not changed here and is noted for
the Gatus owner. A route contract test now fails on `PathPrefix` in the n8n rule, and
the hardening gate pins both `PathRegexp` exclusions.

The SEC01 rows and include hash were re-bound with `python3 -m
scripts.lib.supply_chain.ledger_rebind` (hash-only, six rows), and the n8n source
binding was rehashed in the ledger and build inputs. The `m0021` n8n and n8n-worker
inventory cells were refreshed from `render_service_inventory`. Nothing was recreated, so
neither the spans nor the router change are live.

### 2026-11-09 n8n Assistant: model and web search, code sandbox held

The owner asked to configure the n8n Assistant (Instance AI) with Web search through
SearXNG and Code sandbox through n8n-sandbox, model `anthropic/claude-sonnet-5`, with a
Firecracker runner and never privileged Docker-in-Docker. The Anthropic key is already a
provider connection in the UI, so Compose sets only the model and carries no key.

Done. `N8N_INSTANCE_AI_MODEL` and `N8N_INSTANCE_AI_SEARXNG_URL=http://searxng:8080` are set
on `n8n` main. `searxng` is a HOME service in `infra/07-workflow/n8n/docker-compose.yml`
(profiles `workflow`, `workflow-n8n`), digest-pinned to
`searxng/searxng:2026.11.9-57ff753ad`, on `template-infra-readonly-med` (1 CPU, 512 MiB,
512 pids, reservation 0.05 CPU and 192 MiB), read-only with `cap_drop: ALL`,
`no-new-privileges`, user 977, tmpfs for `/tmp`, `/run` and `/var/cache/searxng`, a
healthcheck on `/healthz`, no host port and no Traefik route. Its settings file
`infra/07-workflow/n8n/searxng/settings.yml` turns JSON output on. It needs no secret
file: the image refuses the default `server.secret_key`, so the entrypoint wrapper
generates a random key at each start; nothing here keeps sessions or signed links.
Networks: `n8n_search_net` is internal and holds only `n8n` and `searxng`, so n8n
reaches SearXNG and SearXNG reaches no other service; `n8n_search_outbound_net` is a plain
bridge that only `searxng` joins and is its way to the public internet. Its egress is
therefore unrestricted by port or destination, like any bridge container, and it can
reach the host LAN through NAT; unlike `crawl4ai` it has no address filter, because
SearXNG queries a fixed set of search engines and does not fetch arbitrary URLs for its callers. Nothing
reaches it from outside.

Held. The code sandbox is not configured. The Firecracker runner image
`n8nio/n8n-sandbox-service-runner-firecracker:1.8.1` (index
`sha256:d73156fe…971bcf`, linux/amd64 only) was inspected without running it. Its binary builds
network namespaces, veth pairs, TAP devices, `iptables` FORWARD and NAT rules, bind
mounts and a Firecracker jailer, and needs `/dev/kvm` and `/dev/net/tun` (both exist on
the host). That set needs `SYS_ADMIN` and `NET_ADMIN` plus mount, chroot, mknod and
uid/gid changes, and Docker's default AppArmor profile blocks the mount calls. The smallest capability list that works is therefore close to
`privileged`, cannot be shown to work without starting the container, and was not added. The
Go package path of the runtime is `firecracker.ee`, an enterprise-edition tree in the
sandbox service source, so whether the runner needs an n8n license is a question for the
owner; the binary shows no license variable. The n8n reference stack
(`docker/get-n8n.sh`, sandbox service 1.8.1) uses the privileged Docker-in-Docker runner
instead, which the owner ruled out. The API (`n8n-sandbox-service-api:1.8.1`,
`sha256:3ac19681…d00e7e`) and sandbox (`n8n-sandbox-service-sandbox:1.8.1`,
`sha256:b397f4b5…f664ba1233`) images exist; sandbox service 1.14.0 is the newest release, and 1.8.1
is the version tested with n8n 2.46.6. No sandbox secret is created; if the owner lifts the
hold, the API key, the runner registration token and the runner API key are needed and n8n's
config reads `N8N_SANDBOX_SERVICE_API_KEY` and accepts a `_FILE` form.

The SEC01 ledger has a BLOCKED `searxng` row (registry descriptors only, everything else
UNKNOWN or NOT_RUN), added through a source refresh; the other six n8n rows were
re-bound with `ledger_rebind`, and the n8n source binding was rehashed. The
tech-stack projection, POL-0078 (`workflow`, `workflow-n8n`), the `m0021` inventory
(`render_service_inventory`), GDE-0053 `implementation_services` and its Assistant
paragraph, the n8n README, AD-0026 network table and the Grafana coverage README were
updated. Nothing was started, so neither SearXNG nor the Assistant settings are live.

### 2026-11-09 dedicated Valkey removal (ADR-0062 decision 10)

The owner accepted ADR-0062, whose decision 10 removes the per-app Valkey and exporter
sets of airflow, n8n and oauth2-proxy (`dedicated-valkey` profile, never created in
HOME). Airflow, n8n and OAuth2 Proxy keep the shared `mng-valkey`; `mng-valkey`,
`dev-valkey` and their exporters stay.

Done in source only; no container, volume or image was touched. Six services left their
Compose files (`airflow-valkey`, `airflow-valkey-exporter`, `n8n-valkey`,
`n8n-valkey-exporter`, `oauth2-proxy-valkey`, `oauth2-proxy-valkey-exporter`) with the
three `docker-compose.monitor-acl.yml` overlays, the `airflow-valkey-data`,
`n8n-valkey-data` and `oauth2-proxy-valkey-data` volume declarations, the optional
`depends_on` entries, the `dedicated-valkey` profile (POL-0078, operations catalog), the
three exporter scrape comments, the exporter names in the `ObservationValkeyBackendMetricMissing`
selection, and the root Secret declarations `airflow_valkey_password`, `n8n_valkey_password` and
the three `*_valkey_monitor_password`. The n8n entrypoints no longer accept the
`n8n-valkey::n8n_valkey_password:0` selection and `connection_uri.py` no longer accepts
the `airflow-valkey` pair; the shared pair and the shared named-account pair stay. The
OpenBao secret catalog lost CACHE-008, CACHE-009, CACHE-028, CACHE-029 and CACHE-030;
their IDs are not reused. The SEC01 ledger archived the six rows in a `source_refreshes`
record (`removed_services`, `removed_entries`), adjusted the P08 observation counts
(denominator 97 to 91, services with a related source 83 to 80), re-bound 15 rows and 5
include hashes with `ledger_rebind`, and rehashed the n8n source binding identically in
`update-ledger.json` and `build-inputs.json` with the old binding archived. The tech-stack
projection and the `m0021` inventory were regenerated, and Stage 05 guides, policies and
runbooks, AD-0002, AD-0007, AD-0022 and the service READMEs were updated.
`oauth2_valkey_password` stays: the alternative `Dockerfile` entrypoint of oauth2-proxy
reads it, and the secret file lives under `secrets/db/mng-valkey/`.

Held. The public registry `secrets/SENSITIVE_ENV_VARS.md.example` still lists CACHE-008,
CACHE-009, CACHE-028, CACHE-029 and CACHE-030, and `secrets/README.md` still names
`db/n8n-valkey/`; the project permissions deny agent edits under `secrets/`, so the owner
removes those five rows and that clause. Until then the secret catalog contract and the
secret metadata sync tests report `catalog_public_source_drift`.

Owner decisions that remain: the volumes `hy-home-infra_airflow-valkey-data` and
`hy-home-infra_n8n-valkey-data` (and any stopped container or image of the six services)
are untouched and need separate approval to remove; the private files under
`secrets/db/airflow-valkey/`, `secrets/db/n8n-valkey/`, `secrets/db/oauth2-valkey/` and
`secrets/db/mng-valkey/airflow_password.txt` are not deleted; and the now unmounted
`infra/04-data/mng-db/valkey/scripts/start-dedicated.sh` and `render-monitor-acl.sh`
(with their script-level tests and `test_p02_secret_presentation_native`) are kept for a
separate retirement.

### 2026-11-09 n8n Assistant code sandbox: privileged Docker-in-Docker runner

The owner overrode the earlier exclusion for this one service and chose n8n's privileged
Docker-in-Docker runner for the Assistant code sandbox ("privileged DinD"). The
Firecracker runner stays unused (see the preceding section).

Services, in `infra/07-workflow/n8n/docker-compose.yml`, all in the opt-in profile
`n8n-sandbox` and none selected by `workflow` or `workflow-n8n`. Sandbox service 1.8.1 is
the release the n8n 2.46.6 installer pins; the newest tag seen on Docker Hub is 1.14.0.

- `n8n-sandbox-certs`: one-shot job from `n8nio/n8n-sandbox-service-api:1.8.1`
  (`sha256:3ac19681…d00e7e`) that runs the image's `bootstrap-mtls.sh` into the volume
  `n8n-sandbox-tls`, hands the API key files to the API user (`cap_add: CHOWN`, the
  only added capability, with an exception) and deletes the CA key. No network.
- `n8n-sandbox-api`: the same image, read-only, `cap_drop: ALL`, tmpfs state (sandbox
  metadata is lost on restart; sandboxes are disposable), healthcheck on `/healthz`.
- `n8n-sandbox-runner-1`: `n8nio/n8n-sandbox-service-runner-dind:1.8.1`
  (`sha256:b7444719…29a117`), `privileged: true`, the only privileged service in the
  file. The sandbox image is `n8nio/n8n-sandbox-service-sandbox:1.8.1`
  (`sha256:b397f4b5…f664ba1233`), named by digest in `SANDBOX_RUNNER_DOCKER_SANDBOX_IMAGE`; the
  inner Docker daemon pulls it from Docker Hub on first use into the dedicated volume
  `n8n-sandbox-docker`. The host Docker socket is never mounted. Renovate does not see the
  sandbox image because it is an environment value, so a test checks that it stays on
  the API's release.

`n8n` main gets `N8N_INSTANCE_AI_SANDBOX_ENABLED=true`, provider `n8n-sandbox`,
`N8N_SANDBOX_SERVICE_URL=http://n8n-sandbox-api:8080` and
`N8N_SANDBOX_SERVICE_API_KEY_FILE=/run/secrets/n8n_sandbox_api_key`. Because that
secret is mounted into `n8n` itself, **`n8n` will not start until the file exists**, even
if the profile is not selected.

Networks (each a distinct bridge, no host port and no Traefik route on any of the three
services). The reference stack uses one default network for everything. Here
`n8n_sandbox_net` (10.250.210.0/24, internal) holds only `n8n` and the API;
`n8n_sandbox_runner_net` (10.250.211.0/24, internal) holds only the API and the runner;
`n8n_sandbox_outbound_net` (10.250.212.0/24) holds only the runner. This departs from a
single network holding n8n, the API and the runner on purpose: sandboxed code leaves the
inner Docker network through the runner, so a shared network would let it reach n8n
main's UI and API directly. The runner joins no data, `n8n_net`, `obs_net`, edge or
`n8n_search_net` network.

Egress, stated exactly. The runner's only external path is `n8n_sandbox_outbound_net`, a
plain bridge with no destination or port filter. Sandbox code runs in an inner container
that the runner NATs onto that path, so it, like the runner, can reach the public
internet and, through the host's NAT, the host LAN and any host service listening on the
bridge gateway address. It can also reach the API on `n8n_sandbox_runner_net`, which
needs the API key. It cannot reach n8n or any data network. The inner dockerd needs the
internet to pull the sandbox image, and the Assistant's workflow builder may need it to
install packages (not verified). A host `DOCKER-USER` rule is the way to
narrow it if the owner wants; it was not added.

Budget: runner 3 CPU, 4 GiB, 4096 pids (reservation 0.05 CPU, 512 MiB); API 0.5 CPU,
256 MiB, 256 pids; certs job 0.5 CPU, 256 MiB for seconds. The sandbox image is 1.35 GB
unpacked, so the `n8n-sandbox-docker` volume grows by at least that.

Exception record: `infra/common-optimizations.exceptions.json` has `privileged` for
`n8n-sandbox-runner-1` and `cap_add CHOWN` for `n8n-sandbox-certs`, each citing the
owner decision of 2026-11-09, reviewed 2026-11-09 and due 2027-05-09. The Conftest
allow-list (`compose.rego`) now names `cadvisor` and `n8n-sandbox-runner-1`, with
tests. `N8nCodeSandboxContractTests` fails if any other service in the n8n file is
privileged, if a sandbox service gets a port, route or Docker socket, if the networks
change shape, or if an image leaves digest pinning or the 1.8.1 release.

Secrets, three Docker Secret files, none created or read here. The images read the API
key list, the runner registration token and the runner API key only from the
environment, so the API and runner entrypoints load them from the files and `exec` the
image command; n8n reads its copy through its `_FILE` form. The owner creates these files
before recreating `n8n`:

- `secrets/automation/n8n/n8n_sandbox_api_key.txt`: n8n main and the API.
- `secrets/automation/n8n/n8n_sandbox_runner_registration_token.txt`: the API and the runner.
- `secrets/automation/n8n/n8n_sandbox_runner_api_key.txt`: the API and the runner.

Suggested command (writes files only, prints nothing): `umask 027; for f in
n8n_sandbox_api_key n8n_sandbox_runner_registration_token n8n_sandbox_runner_api_key; do
openssl rand -hex 32 > "secrets/automation/n8n/$f.txt"; done`, then give the files the
group of `SECRETS_GID` like the other secret files. The OpenBao catalog and
`secrets/SENSITIVE_ENV_VARS.md.example` still need three rows for these files. That
metadata file is outside what this session may read or edit, so two tests in
`test_secret_metadata_sync` fail until someone adds them; this is the only open gate.

Records: SEC01 BLOCKED rows for the three services (registry descriptors only), the
refresh entry with `added_services`, the rebound hashes and the n8n source binding,
`tech-stack.versions.json`, POL-0078 (profile row and rule), the `m0021` inventory rows,
the Grafana coverage README, AD-0026, GDE-0053 (a security note) and
`secret-file-support.json`, which now lists the new `_FILE` key and the twelve certificate-path
keys. Nothing was started: the DinD start, the mTLS registration between API and runner,
the first sandbox creation, the `no-new-privileges` and `cap_drop` defaults under an
inner dockerd, and the sandbox image pull are all unproven.

### 2026-11-09 Traefik v3.7.17 for GHSA-xv5x-242w-7hf7

The owner approved prioritizing security-relevant updates. GHSA-xv5x-242w-7hf7 (High,
published 2026-11-02) affects Traefik v3.7.14 through v3.7.16: an `Authorization` header with the
`NTLM` or `Negotiate` scheme makes Traefik allocate a dedicated backend transport to the client
connection without any valid credential, and the transport, its idle backend connection and its
goroutines are not released when the client closes. An unauthenticated client can exhaust memory,
file descriptors and backend connections whether or not NTLM or Kerberos backends exist. The
patched version is v3.7.17. HOME declared v3.7.16 in Compose, so the source pin moves to
`traefik:v3.7.17@sha256:f4bb143d…86f5a`, the OCI index digest read from the Docker Hub registry on
2026-11-09. The running container still uses the image it ran before (recorded in the SEC01 ledger)
and was not touched.

The v3.7.17 release notes and the v3.7 migration guide list three changes. Traefik is built with
Go 1.27, which removes the `tlsrsakex`, `tls10server` and `tls3des` `GODEBUG` settings; the tracked
configuration sets no `GODEBUG`, `minVersion` or `cipherSuites`. Go 1.27 rejects requests with more
than 500 header values with 431 unless `maxHeaderValueCount` is raised; no entry point sets it, and a client that sends more is
rejected before routing and absent from the access logs. The Ingress-NGINX provider generates new names; that provider is not enabled.
The release also fixes an NTLM/Kerberos backend connection leak and bumps `quic-go`, `x/net`,
`lego` and `go-jose`. No breaking change touches this configuration.

Changed: `infra/01-gateway/traefik/docker-compose.yml`, `infra/tech-stack.versions.json` (through
`sync-tech-stack-versions.sh --write`), the pinned Traefik image in
`tests/validation/test_p02_native_contracts.py`, the Traefik README and Guide, and the SEC01
files. The traefik ledger row carries the new image, digests, advisory, applicability and a
`superseded_pin_2026_11_09` archive of the v3.7.16 binding; `previous_adopted_pin_assessment` (the
v3.7.14 scan) is unchanged. `ledger_rebind` re-bound the include hash. The release, image and
vendor-channel lookups gained the v3.7.17 responses. Signatures, a scan, the config boot and the HOME
recreate are `NOT_RUN`.

Unchanged on purpose: the v3.7.13 rollback overlay `infra/01-gateway/traefik/compose.window-ca.override.yml`
(SPEC-0243 rollback image), the digest-only `traefik@sha256:24841fe2…20e344a0` guard image in
`examples/operations/compose-core-readiness/`, `scripts/lib/ops/compose-core-readiness.sh` and the
quality-path guard (Renovate PR #853 touches it), and historical records that name v3.7.16 (TSK-0021,
POL-0013, the workspace inventory data).

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

### 2026-11-09 n8n code sandbox: vfs storage for the inner Docker

The Assistant workspace setup failed with `install-dependencies: canceled`. On the host
kernel `overlay.redirect_dir` is off, so `npm install` over the image-layer `node_modules`
hits `EXDEV` on directory renames and exceeds n8n's 120 s budget. The same install took
6 s on a copy of that tree. IPv6, dependency versions and sandbox 1.14.0 were tested and
ruled out. The runner now sets `SANDBOX_RUNNER_DOCKER_STORAGE_DRIVER=vfs`. The guide and
AD-0026 now state the measured egress limits of sandbox containers.

### 2026-11-09 dedicated Valkey leftovers retired

Owner-directed follow-up to the dedicated Valkey removal. `start-dedicated.sh` and
`render-monitor-acl.sh` were unmounted and used by no live service, so both are deleted
with their script-level tests (`DedicatedValkeyWrapperTests`, `ValkeyMonitorRendererTests`)
and `test_p02_secret_presentation_native`, whose only subject was the renderer. The
workflow contract, its test and the CI gate plan test drop that opt-in module (optional
selectors 33 to 32). The `start.sh` write-refusal check stays. The renderer entry in the
`local_source_rebindings` record of `build-inputs.json` is history and stays.

The alternative `Dockerfile` entrypoint of oauth2-proxy now reads `mng_valkey_password`
like `docker-entrypoint.dev.sh`. `oauth2_valkey_password` is removed from the oauth2-proxy
Compose file and the root `docker-compose.yml`, and catalog entry CACHE-012 is removed from
`secret-catalog.json` (its ID is not reused). The hardening script, the `sec01` entrypoint
test, the guide, the service README and the `m0021` inventory follow.

Held. The public registry `secrets/SENSITIVE_ENV_VARS.md.example` still lists CACHE-012;
the owner removes that row. The secret catalog contract and metadata sync tests report
the drift until then. The private file `secrets/db/mng-valkey/oauth2_password.txt` is not
deleted.

### 2026-11-09 Renovate image bumps keep the SEC01 ledger in sync

Renovate image PRs failed `candidate-quality` because the SEC01 update ledger and several
tests pinned the old image. `scripts/operations/sync-update-ledger.sh --write` is now a
Renovate post-upgrade task beside `sync-tech-stack-versions.sh --write` (allowlisted in
`config.js`; `update-ledger.json` and `build-inputs.json` added to `fileFilters`). It runs
`ledger_rebind --accept-image-updates`, which accepts only a full `name:tag@sha256:<64 hex>`
reference of the same repository on an existing row. A new or removed service, a repository
change, a reference without a digest and a build change exit 2 and write nothing. An accepted
row keeps `UNKNOWN` target digests, `NOT_RUN` review, scan and acceptance fields,
`BLOCKED`, and `UNBOUND_CURRENT_TARGET`; the replaced values stay in
`source_refreshes[].previous_service_images`. Nothing contacts a registry, so the digest,
signature and provenance are not verified. An n8n input change now rehashes
`n8n_source_preparation.source_binding` identically in both documents.

Tests that pinned a Renovate-owned version now check the repository, the full digest form
and the ledger row instead: `test_sec01_version_contract`, `test_sec01_next_stable_candidates`,
`test_sec01_next_tool_candidates`, `test_service_wiring_contracts`, `test_crawl4ai_egress`,
`test_workflow_version_bundle` and the updater contract in
`test_tech_stack_version_contract`. Replaying the open PRs 854, 857, 859, 860, 861, 864, 865,
872, 876 and 877 in throwaway copies passed the gating suites and the second run changed
nothing. PRs 856, 858 and 866 change tag-only images and are refused, as designed. The step
has not run inside the Renovate container; its Python version and the noexec `/tmp` behavior
are unobserved.

### 2026-11-09 n8n code sandbox: per-principal mTLS mounts

A security review found that `n8n-sandbox-api` and `n8n-sandbox-runner-1` both mounted the
whole `n8n-sandbox-tls` volume, so each could read the other's private keys. Each service
now mounts only its own subpath (`api`, `runner`) read-only.

### 2026-11-09 n8n code sandbox: CA key removal on every exit path

A security review noted that a failure between certificate generation and the final `rm`
would leave `ca.key` in `n8n-sandbox-tls`. The job now removes it through a shell `trap` on
exit. Reproduced on the pinned image: the key stayed before the change and is gone after it.
