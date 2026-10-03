---
title: "Development Data Secret Issuance and Isolated Acceptance Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0202-TSK-0002"
parent_ids:
- "SPEC-0202"
- "SPEC-0202-PLAN-0001"
created: "2026-10-03"
---

# Development Data Secret Issuance and Isolated Acceptance Task

## Objective

Finish the owner-approved Prompt 02 private credential issuance and bounded
isolated checks before Prompt 03. Deliver the verified source to local `main`.
Do not start or restart HOME services, rotate an existing credential, move or
delete real data, perform the deferred management restore, or mutate a remote.

## Inputs

- Owner's 2026-10-03 instruction to issue the 20 new dev/LAB files and merge
  Prompt 02 into `main`, followed by the explicit selection to hold HOME
  start/restart. The source base is `e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d`;
  source head is `0a2de6c3758f4805c2be31cb6bd3976f60b8eb43`.
- SPEC-0202 and TSK-0001's source/static evidence. Archived SPEC-0199/0200
  and an earlier no-data report confer no runtime approval or proof.
- Public registry's 20 exact manual IDs: PG-032–035, CACHE-021, BKP-006,
  LAB-001–006, LAB-008–015. Each was absent in the owner checkout at the pre-issuance check.
- Docker context `default` and the current HOME container inventory must be
  rechecked immediately before any isolated container action.

## Work Log

| Unit | State | Evidence and remaining boundary |
| --- | --- | --- |
| W7.1 | PASS | The 20 exact new manual IDs (PG-032–035, CACHE-021, BKP-006, LAB-001–006, LAB-008–015) were exclusively issued in the owner checkout on 2026-10-03. Path-only postflight: 20 files, zero mode/ownership/ignore failures; mode `0640`, UID/GID `1000:1000`. Existing credentials were neither read nor rotated. |
| W7.2 | PARTIAL | The public registry records the issuance dates and purposes; the private 138-ID projection was previously aligned without changing value cells. Recheck private metadata and root/LAB env pairs after local main landing. Rollback compatibility keys remain until consumer and rollback review. |
| W7.3 | PASS (selected) | Docker context `default`, project `hyhome-p02-p8gkg7zv`, internal network `hyhome-p02-net-p8gkg7zv`, zero host ports, synthetic secrets, no HOME mount. Image build and both service healthchecks passed. Platform provision and rerun returned 0; Timescale `2.30.2` loaded. Role/reader DDL and write denials passed; Valkey A/B prefix and admin/DB1 denials passed. pgBackRest stanza-create returned 0; online backup correctly refused with 87 while `archive_mode=off`; stopped offline full backup with stale-PID `--force` returned 0; separate-volume restore returned 0 and returned one probe row, extension `2.30.2`, DB owner `platform_owner`. Timescale late/null/duplicate/unique-partition checks passed. Other LAB topologies were not started. |
| W7.4 | PENDING | Path-aware checks, independent review, source commit, private projection reconciliation, and clean local `main` fast-forward remain. Remote and HOME operations remain excluded. |

## Verification Evidence

The isolated dev image ID was `sha256:19ffce2ca8d8eb820b0ea784c869ea20afe24e526594e7d4267b18ea22ca43f2`; Valkey image ID was `sha256:a0dbf4c1d5708782907c10e2c72deff317518518b5288a58416981d9db95d30b`. The build used the pinned linux/amd64 Timescale child digest from the Dockerfile. The isolated host had 12 CPUs, 31 GiB RAM, about 32 GiB root free and 2.5 TiB Docker storage free at preflight. These are capacity observations, not benchmarks.

The exact test volumes were `hyhome-p02-p8gkg7zv_dev-pg-data`, `hyhome-p02-p8gkg7zv_dev-valkey-data`, and `hyhome-p02-p8gkg7zv_restore-pg-data`; all were removed after the test. The two isolated service containers, restore checker and internal network were removed. A first cleanup invocation omitted the selected profiles and left the service containers; the corrected `--profile '*' down` plus explicit volume removal passed, and container/network/volume absence was checked. The private scratch directory under `/tmp/hyhome-p02-iso-p8gkg7zv` remains until evidence review; it contains only synthetic test material and sanitized local output.

The first SQL denial harness expected `psql -c` to return 3, but it returned 1 for permission errors. The corrected harness required exit 1 and `permission denied` and passed all four cases. The first Valkey Compose preflight omitted `dev-data` and excluded the service; the corrected profile-aware render returned 0 with two isolated bind sources and zero host ports. Neither harness error was a source defect.

The following uses shell variables only to shorten repeated absolute, synthetic test paths. They contain no credential values. The backup/restore invocations were executed via Python `subprocess` with these argument lists, with full output kept only in private scratch and summarized here.

```bash
ISO=/tmp/hyhome-p02-iso-p8gkg7zv
SRC=/tmp/hy-home-spec-0202-finish-20261003
DC=(docker compose --env-file "$ISO/isolation.env" -p hyhome-p02-p8gkg7zv -f "$SRC/infra/04-data/dev-db/docker-compose.yml" -f "$ISO/compose.override.yml")
"${DC[@]}" --profile '*' config --format json
"${DC[@]}" --profile dev-data up -d --build dev-pg dev-valkey
"${DC[@]}" run --no-deps --rm dev-platform-provision
"${DC[@]}" run --no-deps --rm dev-platform-provision
docker exec --user postgres hyhome-p02-p8gkg7zv-pg psql -XAt -d platform_dev -c "select extname, extversion from pg_extension where extname='timescaledb'"
docker exec --user postgres hyhome-p02-p8gkg7zv-pg pgbackrest --stanza=dev stanza-create
docker exec --user postgres hyhome-p02-p8gkg7zv-pg pgbackrest --stanza=dev --type=full backup
docker stop hyhome-p02-p8gkg7zv-pg
```

The offline backup and restore used these complete argument lists (the private config file contains only the synthetic cipher input; no value is shown). The first offline attempt without `--force` returned 38 because the stopped source left `postmaster.pid`; no other container held the source volume. The second attempt returned 0.

```bash
docker run --rm --name hyhome-p02-p8gkg7zv-offline-backup --network none --cpus 2 --memory 2g \
  --mount type=volume,source=hyhome-p02-p8gkg7zv_dev-pg-data,destination=/var/lib/postgresql \
  --mount type=bind,source="$ISO/backup/dev-pgbackrest",destination=/var/lib/pgbackrest \
  --mount type=bind,source="$ISO/offline-conf",destination=/run/offline-conf,readonly \
  -e PGBACKREST_CONFIG_INCLUDE_PATH=/tmp/pgbackrest/conf.d --entrypoint /bin/sh \
  hy-home/dev-pg:18.6-ts2.30.2-pgbackrest2.57 -ec \
  'mkdir -p /tmp/pgbackrest/conf.d; cp /run/offline-conf/cipher.conf /tmp/pgbackrest/conf.d/cipher.conf; chown -R postgres:postgres /tmp/pgbackrest; chmod 0700 /tmp/pgbackrest /tmp/pgbackrest/conf.d; chmod 0600 /tmp/pgbackrest/conf.d/cipher.conf; exec gosu postgres pgbackrest --stanza=dev --no-online --force --type=full backup'

docker run --rm --name hyhome-p02-p8gkg7zv-restore-job --network none --cpus 2 --memory 2g \
  --mount type=volume,source=hyhome-p02-p8gkg7zv_restore-pg-data,destination=/var/lib/postgresql \
  --mount type=bind,source="$ISO/backup/dev-pgbackrest",destination=/var/lib/pgbackrest,readonly \
  --mount type=bind,source="$ISO/offline-conf",destination=/run/offline-conf,readonly \
  -e PGBACKREST_CONFIG_INCLUDE_PATH=/tmp/pgbackrest/conf.d --entrypoint /bin/sh \
  hy-home/dev-pg:18.6-ts2.30.2-pgbackrest2.57 -ec \
  'mkdir -p /tmp/pgbackrest/conf.d /var/lib/postgresql/18/docker; cp /run/offline-conf/cipher.conf /tmp/pgbackrest/conf.d/cipher.conf; chown -R postgres:postgres /tmp/pgbackrest /var/lib/postgresql; chmod 0700 /tmp/pgbackrest /tmp/pgbackrest/conf.d; chmod 0600 /tmp/pgbackrest/conf.d/cipher.conf; exec gosu postgres pgbackrest --stanza=dev restore'
```

| Check command or SQL | Exit | Evidence |
| --- | ---: | --- |
| `docker context show`; `docker compose ... --profile '*' config --format json` | 0, 0 | `default`; three selected services, zero host ports, internal network, six synthetic secret binds, two scratch data binds |
| `docker compose ... --profile dev-data up -d --build dev-pg dev-valkey`; `docker inspect` for both healthchecks | 0, 0 | both healthy; image IDs above |
| `docker compose ... run --no-deps --rm dev-platform-provision` twice | 0, 0 | `platform_dev` and four restricted roles created, rerun preserved them |
| `docker exec ... psql` role attributes, reader/runtime DDL and write denials | 0 | four expected denials each returned `psql -c` exit 1 and `permission denied` |
| `docker exec ... valkey-cli` with synthetic A/B secret files | 0 | own-prefix read/write passed; cross-prefix, admin, DB1 and anonymous access denied |
| `docker exec ... pgbackrest --stanza=dev stanza-create` | 0 | encrypted synthetic repository stanza created |
| `docker exec ... pgbackrest --stanza=dev --type=full backup` | 87 expected | refused online backup because `archive_mode=off` |
| isolated `docker stop`; offline pgBackRest `--no-online --force --type=full backup` | 0, 0 | stopped source, stale PID explicitly handled; full backup completed |
| fresh-volume `pgbackrest --stanza=dev restore`; isolated restored PostgreSQL `SELECT` | 0, 0 | one row, Timescale `2.30.2`, `platform_owner` |
| isolated Timescale SQL: late/NULL insert, duplicate insert, invalid partition key | 0 | accepted late/NULL; duplicate and invalid unique key rejected |
| `docker compose ... --profile '*' down`; `docker volume rm` for the three exact test volumes; absence checks | 0, 0, 0 | isolated containers, network and volumes absent |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | 1 | only two temporary worktree script modes were `775` while Git mode was `100755`; source checks before those cases passed |
| `chmod 755` on the two temporary worktree scripts; `python3 -m unittest tests.validation.test_openwebui_oidc_entrypoint tests.validation.test_gatus_oidc -q` | 0, 0 | 19 focused tests passed; Git tree has no mode change |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 2–4, 7 | W7.1–W7.3 | PASS in synthetic isolation for issuance, dev engines, role ACL, backup and restore; HOME `NOT_RUN` | GDE/POL/RUN-0100 and POL/RUN-0021 |
| 6 | W7.3 | Owner-attested empty Influx source; live inventory and data migration `NOT_RUN` | GDE/POL/RUN-0100 |
| 8–9 | W7.2–W7.4 | Source and static LAB isolation complete; LAB runtime topologies `NOT_RUN` | POL-0078 and LAB package documents |
| 10 | W7.4 | Pending Prompt 03/04/06 handoff and local main SHA | SPEC-0202 TSK-0001 handoff |

## Review Evidence

Independent review and any failures or waivers will be recorded after execution.
Static checks do not prove operational deployment or real-data migration.

## Commit Ledger

PENDING. The owner requested a local main merge. No remote publication is
within this Task.

## Rulings

The user selected HOME start/restart **hold**. Existing HOME secret paths and
credentials remain untouched. The 20 new paths are new issuance, not rotation.
A local `main` merge is recorded separately from hosted PR checks and runtime
activation. A no-data migration route does not delete InfluxDB or `app_db`.

## Deferred Items

HOME activation, management W7.4 restore, real CDC registration/LSN cutover,
real Influx export/import, old `app_db` technical-object removal, retention
activation, offsite backup and remote publication remain separate gates.
