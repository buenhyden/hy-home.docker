---
title: "Cross-tier Contracts Second Round Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0005"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-08"
---

# Cross-tier Contracts Second Round Task

## Objective

Re-run prompt 04 against the current tree: observe authentication, workflow,
CDC and backup state on the HOME host, close the source gaps that can be
proven with tests, and name each remaining gap with the owner action it needs.

## Inputs and Authorization

The current user request on 2026-10-08 asks to execute prompt 04 of the
analysis pack ("connect authentication, variables, workflows and backup
across tiers") with per-unit commits and a per-Spec PR merge, reusing
SPEC-0204. The request takes precedence over this package's earlier
source-only limits, so read-only HOME observation and isolated containers
are in scope. HOME data changes, realm changes, credential issuance and
image pulls onto a 90%-full disk are not. Baseline `main` `f88eb6601`; the
branch was rebased onto `670b39e53` after PR #386 (SPEC-0215) merged.

## Work Log

### W8 Baseline, Owner Map and HOME Observations

Files this round writes, and the owners whose work it must not overwrite:

| File | Owner it touches | Reason |
| --- | --- | --- |
| `infra/09-platform-ops/restic/bin/hyhome-backup.sh`, RUN-0021 | SPEC-0204 TSK-0003 | Adds the dev-valkey export next to mng-valkey |
| `infra/02-auth/keycloak/docker-compose.yml` | SPEC-0204 TSK-0001 | Wrapper refuses empty secrets |
| `infra/secret-file-support.json` | New | Per-image verdicts |
| `tests/validation/test_service_runtime_compatibility.py`, `test_compose_baseline_gates.py` | SPEC-0204 | New regressions |
| RUN-0070 | SPEC-0204 contract 10 | Mail outcome states |

SPEC-0213 (DEV data), SPEC-0214 (quality) and SPEC-0215 (LAB, merged as
PR #386) own none of these files. POL-0078 is read, not written.

HOME observations, read-only, 2026-10-08:

- **OIDC.** From inside `oauth2-proxy`, the discovery issuer equals its
  configured issuer, `S256` is offered, JWKS holds two keys (RS256 `sig`,
  RSA-OAEP `enc`) and an end-session endpoint exists. The realm also offers
  `plain` PKCE and the implicit and password grants. Of the nine `home-*`
  clients, all are confidential with implicit off; only `home-airflow`
  allows the password grant; `home-airflow`, `home-dozzle`, `home-grafana`,
  `home-kafbat` and `home-proxy-client` have service accounts; none enforces
  PKCE on the server. Client fields were read with a field-limited `kcadm`
  query; no secret was printed.
- **Browser and machine paths.** Unauthenticated Grafana returns 302 to
  `/login` in a browser and 401 JSON on its API. Airflow's root returns 200
  with its own login page, which is not API success. User A to B denial was
  not run: no test users exist.
- **n8n.** `n8n`, `n8n-worker` and both runners run 2.41.6 in queue mode
  with `N8N_RUNNERS_TASK_TIMEOUT=300`. Compose, both Dockerfiles and the
  tech-stack row already share one version, and an existing test pins it;
  Renovate is off for both images. Upstream stable is 2.42.5, released the
  same day; the pin is kept.
- **Airflow.** The worker, not only the scheduler, resolves its metadata DB,
  broker, result backend, Fernet key and API JWT secret through `_CMD`; the
  API server resolves the Keycloak client secret. No DEV DB or S3
  connection and no DAG is tracked, and `AIRFLOW__CORE__LOAD_EXAMPLES` is on.
- **CDC.** `cdc` is not in the HOME selection. `dev-pg` has no
  `platform_dev` database, Kafka Connect has no connector, and Schema
  Registry holds four heartbeat subjects under the old `hyhome.app` prefix,
  while the tracked connector uses `hyhome.platform`. The connector and
  provisioning names are already pinned by an existing test.
- **Backup.** `dev-valkey` had no backup. OpenBao has no snapshot job, and
  OpenSearch has no snapshot repository.
- **Images.** No active Compose file, LAB or Dockerfile uses a Bitnami image.

### W9 Dev-valkey Snapshot and Queue Replay

The nightly run now exports a `dev-valkey` RDB as the `devadmin` ACL user
under the same 300 s in-container limit as `mng-valkey`, drops a partial
file and fails the run on error, and skips a stopped DEV. An export from
HOME `dev-valkey` returned 212 bytes (the DEV store is empty). In an
isolated `valkey/valkey:9.1.2-alpine` pair with no network, a key and a
stream with a consumer group were exported with `--rdb`, loaded into a new
container, and came back with both stream entries and the one pending
entry; `XAUTOCLAIM` handed that entry to a new consumer. RUN-0021 states
that replay is at-least-once. The new assertion failed against the previous
script (RED) and passes now. Commit `abcc1d7a7`.

### W10 Secret File Support Matrix

`infra/secret-file-support.json` gives each of the 73 image and key pairs
in the rendered root a verdict:

| Verdict | Pairs | Evidence |
| --- | --- | --- |
| native | 23 | Upstream source at the pinned tag, or a HOME runtime signal: `pg_up 1`, a Grafana admin login with the file password, Airflow values resolved non-empty |
| wrapper | 5 | The repository entrypoint or Compose command that reads the file |
| unsupported | 45 | The Supabase stack (35, Kong and PostgREST included), Terrakube (9) and SonarQube (1) images ignore the key |

The Supabase stack also gives GoTrue, Storage and Supavisor no database URL,
so it cannot start as declared; PostgREST's native form is `@file`, and
Terrakube's is Spring `configtree`. These services are outside the HOME
selection, and the new test keeps every unsupported key there and fails on a
key without a row. Two mutations, a removed row and a HOME service marked
unsupported, each fail the test.

The Keycloak wrapper now refuses an empty admin or database password; with
an empty mounted file the exact image exits 1 before `kc.sh`. Commit
`e1ee268b0`.

### W11 Image Residue and Mail Outcomes

A test refuses any `bitnami/` image across tracked Compose, LAB and
Dockerfiles; it failed after a Bitnami base was injected. Commit
`ea6c69d59`. RUN-0070 separates accepted, delivered, failed and unknown per
recipient, ties retries to a fixed `Message-ID`, and keeps Mailpit as
capture only. Commit `841bf4eb6`.

### W12 Validation and Handoff

The changed-profile local gate ran in a throwaway worktree holding the
branch diff against `670b39e53` as staged changes, with the checkout's group
write bits cleared. It selected the docs-traceability, supply-chain fixture,
conftest, Compose baseline and repository integrity leaves and exited 0
(689 tests, including the four new ones). Its 23 skips are the opt-in Docker
rehearsals; the backup rehearsal covers pgBackRest and Restic round trips,
not the Valkey export, so it was not run for this change.
`pre-commit run --from-ref origin/main --to-ref HEAD` exited 0.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ledger rows | 1 | W8 | SPEC-0212 TSK-0002 items 03, 04 and 08 updated | This branch | PASS | W8 Baseline, Owner Map and HOME Observations | accepted |
| Owner map and HOME observations | 1 | W8 | Read-only probes and file map | HOME host 2026-10-08 | PASS | W8 Baseline, Owner Map and HOME Observations | accepted |
| Dev-valkey snapshot and replay | 7, 9 | W9 | Test RED then GREEN; HOME export; isolated restore | `abcc1d7a7` | PASS | W9 Dev-valkey Snapshot and Queue Replay | accepted |
| Secret file matrix | 4, 9 | W10 | Matrix test with two mutations; exact-image empty secret run | `e1ee268b0` | PASS | W10 Secret File Support Matrix | accepted |
| Residue and mail | 3, 6 | W11 | Mutation of the Bitnami test; runbook text | `ea6c69d59`, `841bf4eb6` | PASS | W11 Image Residue and Mail Outcomes | accepted |
| Validation | 8 | W12 | Changed gate in a clean worktree; pre-commit over the range | `8dc35b198` | PASS | W12 Validation and Handoff | accepted |

## Review and Completion

Not complete. These remain open, each with its owner action:

- Fix or retire the Supabase stack, SonarQube and Terrakube secret wiring
  before any of them is selected.
- Decide whether `home-airflow` needs the password grant and which service
  accounts are used; enforce server-side PKCE `S256` per client after its
  login is checked.
- Run user A to B denial, n8n queue, manual, scheduled, webhook, Code and
  cancel paths, and CDC Avro decode and replay in isolated fixtures with
  synthetic users and data.
- Give Airflow a DEV dataset, connection and DAG before testing watermark,
  backfill, retry, dead letter and quality gates.
- Add OpenBao and OpenSearch snapshots with a snapshot identity and
  repository; free host disk below 90% first.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
