---
title: "Development Data Secret Issuance and Isolated Acceptance Task"
version: "0.1.1"
type: "sdlc/task"
status: "completed"
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
| W7.2 | PASS | The public registry records issued dates and purposes. After the first local main fast-forward, `--sync-metadata-check` returned 1 for one private metadata file, `--sync-metadata` returned 0 and preserved values, then the check returned 0 with zero changed files. Three private files were backed up under an ignored `0700` scratch directory; all 138 private Value cells and both private env files matched their pre-sync copies, then that temporary copy was removed. Rollback compatibility env keys remain until consumer and rollback review. |
| W7.3 | PASS (selected) | Docker context `default`, project `hyhome-p02-p8gkg7zv`, internal network `hyhome-p02-net-p8gkg7zv`, zero host ports, synthetic secrets, no HOME mount. Image build and both service healthchecks passed. Platform provision and rerun returned 0; Timescale `2.30.2` loaded. Role/reader DDL and write denials passed; Valkey A/B prefix and admin/DB1 denials passed. pgBackRest stanza-create returned 0; online backup correctly refused with 87 while `archive_mode=off`; stopped offline full backup with stale-PID `--force` returned 0; separate-volume restore returned 0 and returned one probe row, extension `2.30.2`, DB owner `platform_owner`. Timescale late/null/duplicate/unique-partition checks passed. Other LAB topologies were not started. |
| W7.4 | PASS (static) | Independent review findings were corrected; Spec metadata recheck returned 0 violations. The first path-aware gate returned 1 only for two group-writable scripts in the temporary worktree; chmod to Git mode `100755` and 19 focused tests returned 0. The complete changed gate retry returned 0, including 163 final unit tests. The source and both Task documentation commits reached local `main` at `5f99e0e51`; remote delivery remains separate. HOME operations remain excluded. |

## Verification Evidence

The isolated dev image ID was `sha256:19ffce2ca8d8eb820b0ea784c869ea20afe24e526594e7d4267b18ea22ca43f2`; Valkey image ID was `sha256:a0dbf4c1d5708782907c10e2c72deff317518518b5288a58416981d9db95d30b`. The build used the pinned linux/amd64 Timescale child digest from the Dockerfile. The isolated host had 12 CPUs, 31 GiB RAM, about 32 GiB root free and 2.5 TiB Docker storage free at preflight. These are capacity observations, not benchmarks.

The exact test volumes were `hyhome-p02-p8gkg7zv_dev-pg-data`, `hyhome-p02-p8gkg7zv_dev-valkey-data`, and `hyhome-p02-p8gkg7zv_restore-pg-data`; all were removed after the test. The two isolated service containers, restore checker and internal network were removed. A first cleanup invocation omitted the selected profiles and left the service containers; the corrected `--profile '*' down` plus explicit volume removal passed, and container/network/volume absence was checked. The private scratch directory under `/tmp/hyhome-p02-iso-p8gkg7zv` was removed after the final gate evidence was recorded; it contained only synthetic test material and local output.

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
| `python3 scripts/validation/run-ci-gate.py --profile changed` (first) | 1 | only two temporary worktree script modes were `775` while Git mode was `100755`; source checks before those cases passed |
| `bash scripts/operations/gen-secrets.sh --sync-metadata-check`; `--sync-metadata`; `--sync-metadata-check` in merged main | 1, 0, 0 | one metadata file reconciled, values preserved, secret files untouched |
| `chmod 755` on the two temporary worktree scripts; `python3 -m unittest tests.validation.test_openwebui_oidc_entrypoint tests.validation.test_gatus_oidc -q` | 0, 0 | 19 focused tests passed; Git tree has no mode change |
| `python3 scripts/validation/run-ci-gate.py --profile changed` (retry) | 0 | path-aware gate passed; last selected unit suite ran 163 tests, all OK |

| Criterion reference | Plan work unit | Evidence status | Follow-up owner |
| --- | --- | --- | --- |
| 2–4, 7 | W7.1–W7.3 | PASS in synthetic isolation for issuance, dev engines, role ACL, backup and restore; HOME `NOT_RUN` | GDE/POL/RUN-0100 and POL/RUN-0021 |
| 6 | W7.3 | Owner-attested empty Influx source; live inventory and data migration `NOT_RUN` | GDE/POL/RUN-0100 |
| 8–9 | W7.2–W7.4 | Source and static LAB isolation complete; LAB runtime topologies `NOT_RUN` | POL-0078 and LAB package documents |
| 10 | W7.4 | Prompt 03/04/06 handoff is in TSK-0001; final local main SHA is `5f99e0e51`. Remote delivery and operational handoff remain separate. | SPEC-0202 TSK-0001 handoff |

### Completion receipt for the approved source and synthetic scope

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: dated image, license, platform and PG/pgBackRest compatibility assumptions recorded | [source Task](tsk-0001-source-integration.md) |
| 2 | W2 | PASS: normal opt-in dev-pg/dev-valkey declarations preserve mng state and create no 07/08 resources | [source Task](tsk-0001-source-integration.md) |
| 3 | W2 | PASS: project provision checks and isolated A/B SQL denial, rerun and concurrency evidence recorded | [isolated acceptance Task](tsk-0002-issued-secrets-and-isolated-acceptance.md) |
| 4 | W2 | PASS: time-series and Valkey ACL source fixtures plus bounded isolated behavior checks recorded; retention remains inert | [isolated acceptance Task](tsk-0002-issued-secrets-and-isolated-acceptance.md) |
| 5 | W3 | PASS: dbt, CDC, mng init and Schema Registry source contract validated; live connector cutover is NOT_RUN | [source Task](tsk-0001-source-integration.md) |
| 6 | W4 | PASS: owner-attested empty Influx route and strict mapping validation recorded; real export remains NOT_RUN | [source Task](tsk-0001-source-integration.md) |
| 7 | W4 | PASS: dev backup/key source and separate-volume synthetic restore recorded; HOME PITR and offsite remain NOT_RUN | [isolated acceptance Task](tsk-0002-issued-secrets-and-isolated-acceptance.md) |
| 8 | W5 | PASS: normal and LAB dependency, port, network, volume, name and secret graphs statically separated | [source Task](tsk-0001-source-integration.md) |
| 9 | W6 | PASS: path-aware gate, version projection, metadata, links and focused checks recorded with exact limits | [isolated acceptance Task](tsk-0002-issued-secrets-and-isolated-acceptance.md) |
| 10 | W7 | PASS: scoped secret issuance, isolated acceptance and 03/04/06 handoff recorded; HOME and migration remain deferred | [isolated acceptance Task](tsk-0002-issued-secrets-and-isolated-acceptance.md) |

### 2026-10-03 Follow-up: Secret Layout and Environment Parity

The owner separately approved inspection and reorganization of the entire
`secrets/` tree, actual ignored credential-file moves, private/public registry
alignment and exact root/LAB env-key parity. This follow-up uses the current
main baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7` and isolated
source branch `codex/secrets-layout`. It does not authorize HOME restart,
credential rotation, remote publication or data movement. Before mutation,
path-only checks found 138 stable registry IDs (105 file paths, 33 env-only),
all 105 canonical files issued, and six legacy paths for five communication
credentials and one SurrealDB credential. All six were regular files with
mode `0640` and UID/GID `1000:1000`; the running Alertmanager had one old
`common/` bind source. The other top-level secret areas have distinct consumers
or artifact ownership, so their values and names were preserved.

Concrete target: move `secrets/common/{smtp_password,slack_webhook,smtp_username,stalwart_password,supabase_smtp_password}.txt`
to `secrets/communication/` and
`secrets/db/surreal_db/surreal_db_password.txt` to
`secrets/db/surrealdb/`. Six old paths remain as same-inode compatibility
hardlinks until a separately approved HOME cutover and rollback review. This is a path relocation, not a credential rotation. A
protected, Git-ignored `secrets/.backup-20261003-layout/` directory holds
mode `0600` copies of the six originals and the three private metadata/env
files; its directory mode is `0700`. Actual values and original file bodies
were never logged or committed. Hash equality and inode/alias equality were
checked without outputting hashes or contents.
Independent security review identified group-writable path directories. All 24
`0775` secret directories were tightened to `0750` for active credential paths
or `0700` inside protected backup/retired areas. The feature worktree's 27
group-writable secret directories were also tightened to `0750`. An ignored mode-only rollback
manifest is in the protected backup; value files and running mounts were not
changed. Group read/execute needed by the secret-file group remains available.

The value-preserving `gen-secrets.sh --sync-metadata-prune` operation on the
feature worktree aligned all 138 private rows and removed 17 legacy-only root
keys. The 212 retained root assignments have their original values; the only
intentionally empty root key is `_PIP_ADDITIONAL_REQUIREMENTS` (no extra pip
packages). `labs/.env` now has the same 48 keys as its example; nine Locust
keys were added. Five LAB inputs remain intentionally unset because no
isolated data root, Kafka cluster ID, OpenSearch certificate root or approved
Locust scenario/result directory has been selected. Such blanks are not
runtime readiness. The owner checkout's ignored private files were atomically
updated after comparing them with the protected backups. Public/private
registry metadata now differs only in Value cells; all 138 former private
Value cells were preserved. Private file modes remain `0600`.

Rollback before source cutover: verify each old hardlink and canonical path
share an inode, unlink the old hardlink, then rename the canonical file back
to its original path. Restore the ignored private files from the protected
copies only if they still match this Task's projection; otherwise stop for
operator review. After a HOME cutover, service restart and hardlink removal
require a separate service-specific operating plan. A rotation that replaces
only one hardlink path can split the two names; freeze credential rotation
until that plan. The source branch is separate from local `main`: the owner
checkout's private registry matches current-main public paths, while the
feature worktree's private registry matches candidate paths. Both
`--sync-metadata-prune-check` invocations returned 0. Existing main Compose
resolves through the hardlinks. No container was started, stopped or restarted.
After the tracked source branch is integrated into main, the main private
registry must be synchronized once with `--sync-metadata-prune` and verified
with `--sync-metadata-prune-check` before this follow-up is considered fully
landed. Keep the protected backup and hardlinks until that post-merge check
and the separately approved HOME cutover review. Pre-merge checks do not
substitute for post-merge alignment.

| Follow-up check | Exit | Evidence and limit |
| --- | ---: | --- |
| `python3 -m unittest -q tests.validation.test_secret_metadata_sync tests.validation.test_compose_baseline_gates` | 0 | 131 tests OK, 21 existing skips; source contract only |
| `bash scripts/validation/validate-docker-compose.sh` | 0 | 67 static selections, 321 summed service selections, HOME 45; no container start |
| `python3 scripts/validation/check-operations-catalog.py` | 0 | Current service projection in sync |
| `python3 scripts/validation/check-document-links.py --mode all` | 0 | 0 failures, one pre-existing historical archive warning |
| `bash scripts/operations/gen-secrets.sh --sync-metadata-prune-check` in feature worktree and current main | 0, 0 | Each private registry matches its own public paths; root/LAB env key sets aligned; values suppressed |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | 143 | Operator terminated after 15 minutes when path-aware selection expanded into an unrelated full document regression suite; earlier selected suites passed, but this gate is incomplete, not PASS |

## Review Evidence

Independent review found one forbidden Spec heading, one stale README main count, one Task tense mismatch, and missing durable command evidence. Each was corrected. `check-document-metadata.py --mode check-changed --base-ref 0a2de6c3758f4805c2be31cb6bd3976f60b8eb43` returned 0 with 20 selected documents and zero violations; README language/navigation and public secret schema checks returned 0. Static checks do not prove operational deployment or real-data migration.

## Commit Ledger

The source integration commit is `b867eb7d4`; the first Task ledger commit is `ae40cb4ff6a3aa7127dd55b5e185ad5455a3b679`. Both reached local `main` by fast-forward from baseline `e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d`. The final documentation commit `5f99e0e51b41b912f128daafb4a3d41539b77560` also reached local `main` by fast-forward. The source-only Task did not authorize remote publication; the owner approved it separately on 2026-10-03.

## Rulings

The user selected HOME start/restart **hold**. Existing HOME secret paths and
credentials remain untouched. The 20 new paths are new issuance, not rotation.
A local `main` merge is recorded separately from hosted PR checks and runtime
activation. A no-data migration route does not delete InfluxDB or `app_db`.

## Deferred Items

HOME activation, management W7.4 restore, real CDC registration/LSN cutover,
real Influx export/import, old `app_db` technical-object removal, retention
activation, offsite backup and remote publication remain separate gates.
