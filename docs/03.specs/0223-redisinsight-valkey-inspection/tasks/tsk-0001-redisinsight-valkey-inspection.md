---
title: "RedisInsight Valkey Inspection Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0223-TSK-0001"
parent_ids:
- "SPEC-0223-PLAN-0001"
created: "2026-10-09"
---

# RedisInsight Valkey Inspection Task

## Objective

Give RedisInsight read-only inspector access to DEV and MNG Valkey, close the
direct UI path around SSO, and roll it out on HOME without breaking the
services that share MNG Valkey.

## Inputs and Authorization

On 2026-10-09 the owner asked to execute prompt 13 (RedisInsight access to
`dev-valkey`, ACL and readiness) and then asked that DEV and MNG Valkey receive
the same changes and that every service using them be reviewed for impact.
Baseline `main` `5e4398b6c`. Prompt 14 (exporter accounts and labels) follows
in its own package; this package is the single writer of both ACL renderers
until it merges.

## Work Log

### Measurement

An isolated RedisInsight 3.8.0 against Valkey 9.1.2 with ACL logging showed
that `+@read +@connection -@dangerous` covers the key browser, key details and
values, and that the overview needs `INFO`, which sits in `@dangerous`.
`CLUSTER NODES` is refused harmlessly. The image reads pre-set connections
from `RI_REDIS_HOST<n>`, `RI_REDIS_USERNAME<n>`, `RI_REDIS_PASSWORD<n>` and
`RI_REDIS_ALIAS<n>`, recreates them on every start and removes pre-set entries
that disappear. `RI_ENCRYPTION_KEY` encrypts stored passwords only while the
`encryption` agreement is on; auto-accepted terms turn it on for a new `/data`
only. `RI_APP_HOST` sets the listener and `/api/health/` returns
`{"status":"up"}`; the image has `wget` and runs as UID 1000. The first
database request after a start can exceed the 25 s request timeout while
start-up lookups fail on an internet-less network.

### W1 DEV Inspector

The DEV renderer builds service roles from one table, each with its own
secret, and refuses any two roles or projects sharing a secret. `devinspector`
joins `devadmin` and `devmonitor`; the inspector secret and the RedisInsight
encryption key are declared. ACL tests: 8 pass; secret metadata: 44 pass.

### W2 MNG ACL

MNG Valkey renders `default` (unchanged password, all commands) and
`mnginspector` into a tmpfs ACL at start instead of `--requirepass`. Its
renderer tests (4) cover the role lines, a shared secret, missing and
multi-line secrets, and the Compose start path.

### W3 RedisInsight

RedisInsight first listened on a fixed `edge_net` address; after the review
(below) it listens on `10.250.18.3` in the internal `redisinsight_ingress_net`,
which only Traefik shares. `edge_net`, `n8n_net` and `airflow_net` are gone, `DEV / dev-valkey` and
`MNG / mng-valkey` are pre-set with the inspectors, `start.sh` loads both
passwords and the encryption key from secrets, and the health check reads
`/api/health/`. The service inventory was re-rendered; operations catalog,
04-data hardening and Compose tests (116) pass.

### W4 Isolated Rehearsal

`tests.validation.test_redisinsight_rehearsal` runs the pinned images with the
repository scripts on internal networks: listener scope and health, a refused
bypass from a data-network peer, distinct named connections with separate
keys, reads, refused writes and ten refused commands per inspector, encryption
on with no plaintext secret in `/data`, a DEV outage error with MNG unaffected
and recovery, and rotation with the old secret refused. 8 pass.

### W5 HOME Rollout and Consumer Review

RedisInsight `/data` was copied owner-only to
`management/.redisinsight-backup-20261009` first. `dev-valkey` and
`mng-valkey` were recreated: both healthy, the inspectors answer `PONG`, a
wrong password answers `WRONGPASS`, and MNG kept its keys (234 before, 233
after, one expiry). RedisInsight was recreated and listens on `10.250.1.3:5540`
only. The `encryption` agreement was off on HOME; it was turned on and the
service restarted. Both pre-set connections answer `info` 200; an expiring DEV
test key was read through the UI; writes on both answer 403 `NOPERM`. The two
manual connections that used `devadmin` and the MNG `default` password were
deleted, and `VACUUM` removed their residual pages: integrity `ok`, and no
admin or inspector secret remains in the store. `/data` is now `700` and the
store `600` (it was world-readable). Without a session the UI and API answer
302 to Keycloak, and `dev-valkey` and `mng-valkey` get a refused connection to
the RedisInsight port on their networks. Stopping `dev-valkey` made the DEV
connection answer 424 while MNG answered 200; after the restart it reconnected.
Rotating the DEV inspector secret refused the old one and the UI reconnected.

The consumer review compared Compose references with `CLIENT LIST` on both
servers:

| Consumer | Account | Impact |
| --- | --- | --- |
| OAuth2 Proxy, n8n, n8n-worker, Airflow worker, Flower | MNG `default` | None; reconnected after the restart as before |
| Four go-redis clients from the `k3d-hyhome` cluster through the LAN port | MNG `default` | None; reconnected. An external consumer the repository does not declare |
| `mng-valkey-exporter`, Gatus TCP check | MNG `default`; no auth | None; healthy |
| `dev-valkey-exporter` | `devmonitor` | None; healthy |
| Terrakube API and executor (`iac`, not running) | `terrakube_valkey_password` | Pre-existing: that secret differs from the MNG password, so they fail to authenticate before and after this change; review when `iac` is activated |

### Review

The independent review found that the `edge_net` listener still let every
`edge_net` peer (27 Compose files, including JupyterLab and n8n, which run
user code or HTTP requests) and the host read MNG and DEV keys through the
RedisInsight API without SSO. RedisInsight moved to `redisinsight_ingress_net`
(internal, `10.250.18.0/24`) with Traefik as the only other member; a Compose
test pins that membership, the listener address and the label. Minor findings
fixed: the renderers' signal traps now exit instead of continuing to write; the
rehearsal bypass check has a positive control and covers MNG, the stored-secret
scan covers both inspectors and the key, the readiness loop sleeps, and a test
uses the password-only form the MNG consumers send; the MNG port follows
`VALKEY_PORT`; the MNG healthcheck passes its password through `REDISCLI_AUTH`
instead of argv; the RedisInsight README, Runbook and Policy match the pre-set
connections, and the MNG README describes Gatus as an unauthenticated TCP
check. Rehearsal: 9 pass.

On HOME the network was created, Traefik was attached with
`docker network connect` (no restart), and RedisInsight was recreated: a
throwaway `edge_net` container and `dev-valkey` and `mng-valkey` all get a
refused connection to the UI port while the same probe reaches Traefik on 443;
unauthenticated requests answer 302 to Keycloak and both connections answer
200. MNG Valkey still runs the previous healthcheck form until prompt 14
recreates it for its monitor account; the change does not alter behaviour.

The re-review confirmed every finding resolved and raised two Minor ones, and
a host probe found that host processes still reached the UI through the
bridge address Docker gives an internal network. The ingress network now uses
`gateway_mode_ipv4: isolated` (no host address) and `ip_range` `.128/25`, so
the fixed `.3` stays free while RedisInsight is stopped; the stored-secret scan
uses `grep -e` so a secret starting with `-` is not read as an option. A
throwaway network first showed isolated mode refusing the host while a peer
still connects. On HOME the network was recreated with Traefik detached and
reattached (no restart): the host now gets no connection, Traefik reaches
`/api/health/`, and the `edge_net` and both data-network probes are refused.
Rehearsal with a host check: 9 pass.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEV inspector | 1 | W1 | ACL and secret metadata tests | `878c2fa1d` | PASS | W1 DEV Inspector | accepted |
| MNG ACL | 1 | W2 | MNG renderer tests | `48d3d548d` | PASS | W2 MNG ACL | accepted |
| RedisInsight wiring | 2 | W3 | Catalog, hardening, Compose tests | `d635a67a0` | PASS | W3 RedisInsight | accepted |
| Isolated rehearsal | 2 | W4 | Eight rehearsal tests | `5a9562395` | PASS | W4 Isolated Rehearsal | accepted |
| HOME rollout | 3 | W5 | Probes, outage, rotation, store scan | `5a9562395` | PASS | W5 HOME Rollout and Consumer Review | accepted |
| Consumer review | 4 | W5 | Compose references; client inventory | `5a9562395` | PASS | W5 HOME Rollout and Consumer Review | accepted |
| Review fixes: renderers | 1 | W1 | Signal traps; MNG and DEV ACL tests | `ccfcb4db1` | PASS | Review | accepted |
| Review fixes: rehearsal | 2 | W4 | Nine rehearsal tests with controls | `f1c3360c2` | PASS | Review | accepted |
| Review fixes: ingress | 3 | W5 | Compose test; HOME bypass probes from `edge_net`, both data networks and the host | `7220fa247` | PASS | Review | accepted |
| Admin browser login | 3 | W5 | Owner signed in and saw only the two pre-set connections | `a34c96796` | PASS | W5 HOME Rollout and Consumer Review | accepted |
| Non-admin refusal | 3 | W5 | Owner confirmed a non-`/admins` account is refused | `a34c96796` | PASS | W5 HOME Rollout and Consumer Review | accepted |

## Review and Completion

Not complete: W6 validation and the merge remain. The owner signed in at
`https://redisinsight.hy.home.arpa/`, saw only `DEV / dev-valkey` and
`MNG / mng-valkey`, and confirmed that a non-administrator is refused. The
owner set the disposal of the owner-only `/data` copy, which holds the former
plaintext admin passwords, for 2026-10-09; the agent's delete was refused by
the session's permission settings, so the owner runs it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
