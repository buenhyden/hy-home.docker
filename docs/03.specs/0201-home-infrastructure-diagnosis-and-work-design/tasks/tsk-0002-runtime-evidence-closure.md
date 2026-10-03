---
title: "Home Infrastructure Runtime Evidence Closure Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-02"
layer: "specs"
artifact_id: "SPEC-0201-TSK-0002"
parent_ids:
- "SPEC-0201"
- "SPEC-0201-PLAN-0001"
created: "2026-10-02"
---

# Home Infrastructure Runtime Evidence Closure Task

## Objective

Close the SPEC-0201 runtime evidence gaps required for Prompt 02 source
work, and preserve deferred recovery evidence as an explicit later gate. The user approved the Spec amendment and W7.1-W7.3 read-only observations
on 2026-10-02. This does not approve an isolated restore. TSK-0001's W1-W6
source diagnosis and its approval remain unchanged. Prompt 02 source work may
proceed using W7.1-W7.3's accepted evidence under its own Spec, Plan, and Task.

## Inputs

- Approved amendment to SPEC-0201 and W7 in SPEC-0201-PLAN-0001, plus
  written approval for W7.1-W7.3 read-only observation. W7.4 isolated restore
  still requires separate written execution approval.
- Current main, worktree SHA, and TSK-0001 source inventory; do not infer live
  state from Compose, tests, historical counts, or a prior backup declaration.
- Approved read-only service inventory and query route that consumes existing
  credentials without displaying or recording their values.
- For restore only: named existing backup source and recovery point; verified
  Docker context, distinct project, image digest/platform, no host ports,
  isolated network and target volume, CPU/memory/disk budget, and exact cleanup
  ownership. Never mount HOME PGDATA as the restore target.

## Work Log

| Work unit | State | Evidence and completion rule |
| --- | --- | --- |
| W7.1 `app_db` owner and contents | PASS: no current business-app owner | The owner reports no current app uses `app_db` and no data is stored; the live catalog nevertheless shows one technical heartbeat row and a dbt view, with no observed business table. Future projects use dev-db. This does not authorize dropping `app_db` or migrating its infra objects without a separate Task. |
| W7.2 external consumers and traffic | PASS: scoped inventory and aggregate traffic | The owner identifies DBeaver over SSH as a management PostgreSQL administrative client and no current business app. Bounded 90-second and 24-hour `app_db` aggregate traffic was observed. DBeaver's selected database and each commit origin remain unverified limits; zero sampled sessions do not prove client absence. |
| W7.3 host capacity | PASS: point-in-time capacity | Record CPU, RAM, filesystem and Docker headroom as sanitized numbers and compare with existing policy floors. Prompt 02 later sets dev/LAB budgets and checks their margin against a fresh snapshot. Do not print mount paths or environment values into the Task. |
| W7.4 restore measurement | DEFERRED / NOT_RUN by owner | Verify backup integrity, restore the approved backup into a new isolated disposable target, start only that isolated target if needed, check database/extension/role inventory and count consistency, and record duration, recovery point and failure behavior. Distinguish backup verification from successful restore and PITR. Preserve any failed target; exact scratch cleanup requires separate approval after review. No HOME stop/restart, data deletion, or real migration. |
| W7.5 Prompt 02 start gate | DRAFT CONTRACT | Record a binding handoff: at actual Prompt 02 source implementation, recheck registry digest by platform, PostgreSQL/Timescale/pgBackRest compatibility, extension package and license revision against official sources. Prompt 02 Task owns the dated result; a present lookup cannot preapprove a future image. |

### Approved read-only observation, 2026-10-02

The observed baseline remained `e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d`;
Docker context was `default`, Compose project `hy-home-infra`, and `mng-pg`
reported healthy. No service was started, stopped, restarted, or reconfigured.
The existing local PostgreSQL socket and container-configured user were used;
no password, row contents, or query payload entered the evidence.

- **W7.1:** `app_db` exists, is 8,001,215 bytes, and its catalog database owner
  matches the declared `app_user` role. It has no `public` business table, no
  materialized/foreign table or large object, one declared Debezium heartbeat
  table with one row owned by the declared Debezium role, and one tracked dbt
  connectivity view. The declared CDC slot and publication are absent. The
  observed persisted row belongs to the Kafka/Debezium infrastructure path;
  there is no observed business table, materialized view, or large object,
  and no unexpected user schema. The owner confirmed in this conversation
  that no current app uses `app_db` and reports no stored data; future
  projects will use dev-db. The observed heartbeat row is technical
  infrastructure data, so the report of no data is not treated as zero rows.
  There is no current external business-data owner or business dataset to
  assign to a migration; the heartbeat and view remain
  infrastructure-owned objects. W7.1 passes for this limited ownership
  finding. Source owners are the mng-pg init SQL, Debezium provision SQL, and
  tracked dbt connectivity model under `infra/04-data/mng-db`,
  `infra/05-messaging/kafka`, and `infra/12-analytics/dbt`.
- **W7.2:** Kafka Connect REST reported zero installed connectors; the declared
  CDC slot/publication were absent. A 90-second `pg_stat_database` interval
  (11:38:54-11:40:24 UTC) increased by two committed transactions while 91
  one-second `pg_stat_activity` samples caught no `app_db` client. Prometheus
  reported about 2,884 `app_db` committed transactions over 24 hours, zero
  inserted/updated/deleted tuples, 2,880 healthy exporter samples, and no
  sampled connection in its 30-second cadence. These are observed traffic,
  not client attribution. The owner confirmed no current business app uses
  `app_db`, consistent with the active tracked project source search. The
  owner also confirmed DBeaver connects by SSH to management PostgreSQL.
  That identifies an external administrative tool but not its selected
  database or the source of the observed `app_db` commits. W7.2 passes
  only the external consumer inventory and bounded aggregate traffic
  requirement. Origin attribution remains an explicit risk, without
  inventing an external business app.
- **W7.3:** At 11:43:51 UTC, the host reported 12 CPUs, 31.27 GiB RAM total,
  13.55 GiB available, 32.72 GiB free on the root/backup filesystem, and
  2,572.89 GiB free on the Docker/data filesystem. Existing 4 CPU, 4 GiB RAM,
  8 GiB Docker-free, 25 GiB root-free warning, and 20 GiB backup-free floors
  pass as a snapshot. `mng-pg` used about 99 MiB of its 512 MiB limit and
  `mng-valkey` about 8 MiB of 256 MiB at one sample. No approved dev-pg,
  dev-valkey or full LAB budget exists yet; Prompt 02 must calculate those
  margins from a fresh snapshot. W7.3 passes for measured current capacity
  and existing floors only. The proposed isolated restore has a separate 2 GiB
  scratch planning budget below the observed Docker-free headroom.
- **W7.4 preflight only:** pgBackRest `mng` catalog status was 0 with eight
  backups; the latest was a differential backup ending 2026-10-01 18:51:49
  UTC with database size about 125 MB. This proves neither chain/WAL continuity
  nor successful restore. RUN-0021 marks isolated PITR action readiness
  BLOCKED until exact backup/recovery point, original compatible image,
  isolation resources, and separate execution approval are fixed. No restore
  command ran and no scratch volume/network/container was created.

### W7.4 selected-backup restore approval packet, not executed

This packet selects an **engine-only consistency restore** of the approved
management PostgreSQL backup. The original SPEC-0201 criterion 10 requested an
isolated restore result; the owner later deferred that result without treating
it as PASS. The deferred engine-only check needs no post-backup PITR target. The
[pgBackRest recovery type reference](https://pgbackrest.org/command.html)
defines `--type=immediate` as recovery only until the database is consistent.
This rehearsal will not establish the five-minute WAL RPO, time-target PITR,
offsite recovery, or recovery of n8n, Keycloak, Airflow, and other management
applications. Those remain separate RUN-0021/RUN-0028 checks.

The selected stanza is `mng`, differential set
`20260926-185114F_20261001-185139D`, ending 2026-10-01 18:51:49 UTC. Its
catalog status was 0 and its database size was about 125 MB at the prior
read-only check; neither is an integrity or restore result. The local image ID
was `sha256:0abb5ce5c0ad00a254862c8bf5afc5250d752e637b2d3768b0cc37eb05ee6da0`
(`linux/amd64`, PostgreSQL 18, pgBackRest 2.58.0). The selected label,
cluster system ID, image ID/platform/version, available backup chain, Docker
context `default`, and controller ownership must be rechecked immediately
before any action. An image mismatch stops the action; no pull or rebuild is
part of this packet. At 2026-10-02 12:44 UTC the repository occupied 679,596
KiB (about 664 MiB), and the host backup timer reported its next run at
2026-10-03 03:48:55 KST. These are planning snapshots, not future guarantees.

1. **Source and mutual exclusion.** Resolve the existing repository bind at
   `/var/lib/pgbackrest` and BKP-001 cipher-secret bind at
   `/run/secrets/pgbackrest_cipher_pass` from the live container's exact mount
   destinations; give the isolated executors only these two read-only mounts.
   Never attach HOME PGDATA, `mng_postgres_password`, another secret, a HOME
   network, or `--volumes-from`. Select the existing host backup lock used by
   `hyhome-backup.sh`: the controller opens its symbolic
   `$BACKUP_STATE_REPO_DIR/.hyhome-backup.lock`, acquires `flock -n`, and owns
   the file descriptor until clone recovery is complete. A busy lock or a
   concurrent backup/expire indication stops before any container starts.
   Release on every normal/failure/signal path; process death releases the
   descriptor. Maximum hold is two hours. A scheduled backup may exit 75 if
   it fires during this interval; that effect requires explicit operational
   approval. Continuous WAL archive-push may add later segments. Only if
   step 2 exits 0 will the rehearsal use the selected backup's verified
   consistency range.
2. **Integrity before restore.** With the lock held, the separate verify
   executor uses the exact local image ID, default secret-aware entrypoint,
   read-only repository/secret mounts, `/tmp/pgbackrest` 0700 tmpfs,
   `PGBACKREST_CONFIG_INCLUDE_PATH=/tmp/pgbackrest/conf.d`, `--network none`,
   `--pull=never`, and the resource limits below. Pass `sh -ec` as its command;
   run `gosu postgres pgbackrest --stanza=mng
   --set=20260926-185114F_20261001-185139D --output=none verify` and require
   exit 0. Verify checks the selected backup chain and associated archives;
   it does not prove a successful restore. Record only status, exit code,
   observation time, and artifact ID. An error stops before scratch creation.
3. **Owned target and resource guard.** The approved execution tool holds the
   actual data-disk `SCRATCH_ROOT` outside tracked evidence. It creates an
   empty target with `mktemp -d -p "$SCRATCH_ROOT"
   spec0201-restore.XXXXXXXX`, records its private path and opaque ID, sets
   UID/GID 70 and mode 0700, and checks device/inode differ from HOME PGDATA.
   No existing volume or directory may be reused. Fresh preflight must cover
   CPU, RAM, source filesystem, data-disk free space, image, names, ports,
   network, and mount identities. A dedicated monitor using the pinned image,
   `--entrypoint sh`, UID 70, `--network none`, no secret, and scratch mounted
   read-only samples `du -sk` and `df -k` at least every 10 seconds. Monitor
   failure, scratch above 2 GiB, data-disk free below 8 GiB, or two-hour
   deadline stops the exact owned containers. This sampling is not a hard
   quota and can overshoot. No new host port or HOME network is used.
4. **Executor and recovery.** Use controller ID
   `hyhome-spec0201-restore-20261002`; backup-verify, restore, clone, and
   monitor container names add `-backup-verify`, `-restore`, `-clone`, and
   `-monitor`. Check all names are absent, record each Docker-generated ID
   after creation, and label created artifacts
   `SPEC-0201/TSK-0002`. Every executor, including the clone, uses
   `--network none`, `--pull=never`, `--restart=no`, at most 2 CPUs, 2 GiB
   RAM, 256 MiB SHM, and 128 PIDs. No network or host port is created.
   The restore executor keeps
   the default secret-aware entrypoint and tmpfs/config include above, mounts
   only the owned scratch at `/var/lib/postgresql/data`, sets
   `PGDATA=/var/lib/postgresql/data/pgdata`, and passes `sh -ec` to run
   `gosu postgres pgbackrest --stanza=mng
   --set=20260926-185114F_20261001-185139D --type=immediate
   --target-action=promote --archive-mode=off restore`. There is no `--target`.
   The clone uses the same scratch PGDATA read/write, repository and cipher
   secret read-only, default entrypoint, tmpfs and include path. It starts
   `postgres -c archive_mode=off` and must reach consistency before the host
   backup lock is released. It never pushes WAL to the HOME repository.
5. **Acceptance, evidence, and stop.** The Phase A evidence must seal the
   selected set's DB list and source cluster system ID. Clone startup requires
   exact DB-list and system-ID equality, including `app_db` and `mlflow`.
   Assert the observed `app_user`, heartbeat-table owner, and dbt-view owner
   roles still exist; `plpgsql`, `public`, `debezium_heartbeat`, the tracked
   dbt schema/view, and their expected owner identities must be queryable.
   Enumerate sequence names/counts and extension names per restored DB;
   these are observation-only unless Phase A supplies a backup-time comparator.
   Query counts for MLflow experiments/runs, Debezium heartbeat, and the
   tracked dbt view twice in one repeatable-read snapshot; each count must be
   a nonnegative integer and equal to its repeat. These management counts
   are observation-only against the live source because the backup is older.
   A missing named object, failed count query, or mismatch in a same-snapshot
   repeat fails the rehearsal. Never claim backup-time row equality from a
   later live count. Use `docker exec --user 70 <clone-name>` with the
   sanitized restored admin role over the clone's local socket; stop if
   local authentication fails. That administrator creates a random short-lived
   LOGIN restricted to
   `NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS`
   with no direct grants or memberships except `CONNECT,TEMP` on restored
   `app_db`. Check effective `PUBLIC` privileges on `app_db`, `public` schema,
   and tested objects; stop if they permit persistent schema/object mutation
   outside the temporary-table probe. Generate and use its
   plaintext password only within the isolated process; do not log, echo,
   or persist plaintext outside that process. The clone persists a password
   verifier until role deletion, possibly in its retained scratch WAL. From
   `psql` inside the `--network none` clone, authenticate via
   `127.0.0.1:5432` as
   that LOGIN, create a temporary table, insert one synthetic row, assert
   count 1, roll back, and assert the temporary object is absent. Drop the
   LOGIN as the local administrator and assert the role is absent. This is
   an engine/infra read/write smoke check under POL-0021, not recovery of
   any management application; no business app currently uses `app_db`.
   Record backup-end bound, clone readiness, elapsed restore time, exit codes,
   sanitized inventory/count outcomes, and the unverified WAL RPO separately.
   POL-0021's four-hour RTO is a planning objective; engine-only duration is
   not proof of whole-HOME RTO. Release the host backup lock immediately
   after the clone reaches consistency under step 4; later cleanup closes it
   only if still held. On success, stop/remove the exact four owned container
   names and recorded IDs after evidence capture; retain only the mode 0700
   scratch PGDATA and sanitized evidence for owner review. The proposed review
   deadline is seven days after evidence capture; @buenhyden owns expiry
   escalation, while deletion still needs separate approval. On any failure,
   stop/remove only exact ephemeral containers, release the lock if held,
   preserve scratch PGDATA
   and sanitized evidence, record any surviving clone-only role name/status,
   and escalate to @buenhyden. Scratch deletion needs separate exact identity
   and owner approval. No source repository write, HOME service stop/restart,
   cutover, data migration, HOME credential rotation, time-target PITR, or
   offsite restore is authorized.

The owner approved POL-0021 v1.4.4's factual correction and RUN-0021
v1.4.3's immediate-rehearsal draft, and approved a narrow W7.4 Phase A.
Before `verify` or scratch creation, the owner directed Phase A and later
recovery work to be deferred so Prompt 02 source work can proceed. Two
read-only preflight attempts exited 1: the first encountered an inaccessible
Docker volume data path; the second reached the same path while trying to
compare device IDs. No lock was acquired, container created, secret value
read, backup verified, scratch created, or restore run. The data-disk parent
was separately confirmed to have about 2,573 GiB free. Future preflight must
compare against an accessible Docker-root ancestor rather than stat the
private volume leaf. The earlier Phase A approval is superseded by the later
deferral and is not standing execution authority.

The proposed implementer is agent `/root`; independent stateful reviewer is
agent `/root/w7_restore_packet_review`; @buenhyden is the separate human
approver and retained-scratch owner. The owner confirmed @buenhyden is
BKP-001's offline custodian and that the existing Docker secret bind is the
approved read-only consumption route; do not display key material. This
confirmation is not W7.4 execution approval. [SPEC-0182-TSK-0003](../../0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md)
records an owner-approved isolated PITR of actual HOME pgBackRest data on
2026-09-25, using a 2026-09-24 differential set and named management-table
count checks. This is dated prior restoreability evidence, not verification of
the currently selected 2026-10-01 set. [POL-0021](../../../05.operations/policies/0021-backup-and-restore.md)
proposed correction distinguishes those boundaries. RUN-0021 version 1.4.3
(`docs/05.operations/runbooks/0021-backup-and-restore.md`) now contains a
draft immediate-rehearsal branch alongside the existing time-target PITR
procedure; owner acceptance and focused document checks are required before
its use.
`W7.4` remains `DEFERRED / NOT_RUN`; revised SPEC-0201 criterion 10 permits
Prompt 02 source work on the accepted W7.1-W7.3 evidence.

## Verification Evidence

W7.1-W7.3 read-only queries ran after the user approval. No Docker restore,
image pull, secret value output, or HOME service action ran. `BLOCKED` and
`NOT_RUN` are not completion claims. Before W7.1-W7.4 can pass, evidence must
name the command or approved tool, UTC time/window, exit code, sanitized
aggregate result, caveat, and durable owner. If a source is
unavailable, record `BLOCKED` and identify the specific missing authorization or
instrumentation; do not convert it to PASS. A failed restore remains FAIL until
repaired and rerun under the same approved scope.

| Approved read-only command or API | Exit | Sanitized evidence |
| --- | --- | --- |
| `docker context show`; project-label `docker ps` | 0; 0 | `default`; `hy-home-infra` mng-pg healthy |
| `docker exec -u postgres mng-pg ... psql` read-only catalog/statistics queries | 0 | W7.1 object, role, row-count, slot, publication and W7.2 90-second counter/connection aggregates above |
| `docker exec kafka-connect ... GET /connectors` | 0 | HTTP 200; zero connectors |
| `docker exec infra-prometheus wget ... /api/v1/query` | 0 | W7.2 1-hour/24-hour transaction, write, connection and scrape aggregates above |
| `/proc/meminfo`, `statvfs`, `docker info`, `docker stats --no-stream` | 0 | W7.3 timestamped numeric capacity and one-sample service usage above; host paths suppressed |
| `docker exec -u postgres mng-pg pgbackrest --stanza=mng --output=json info` | 0 | Eight backups and latest differential metadata; no restore proof |
| `docker exec -u postgres mng-pg sh -c 'du -sk /var/lib/pgbackrest'`; `systemctl show hyhome-backup.timer`; `docker context show` | 0; 0; 0 | Repository 679,596 KiB at the observed time; next timer 2026-10-03 03:48:55 KST; context `default`; none is future capacity or restore proof |
| [SPEC-0182-TSK-0003](../../0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md) existing acceptance record | historical PASS | Actual HOME repository isolated PITR on 2026-09-25; selected older backup and limited counts, not current-set verification |
| `python3 scripts/validation/check-document-links.py --mode all` | 0 | 10,983 links; failures 0; one pre-existing archive-catalog warning |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD` with the seven changed Stage documents plus registry path | 0 | selected 7; violations 0; no lifecycle override |
| `git diff --check`; targeted new-SPEC trailing-whitespace scan | 0; 0 | No whitespace error across tracked diff or four new SPEC documents |
| Isolated restore command | NOT_RUN | Requires separate source, target, isolation, and recovery approval; current-set `verify` is also NOT_RUN |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 10, revised by owner | W7.1-W7.3 source gate; W7.4 later recovery | ACCEPTED for Prompt 02 source: W7.1 no-app ownership, W7.2 consumer inventory/aggregate traffic, W7.3 capacity snapshot scoped PASS. W7.4 deferred/NOT_RUN; no current-backup recovery claim | TSK-0002; later Stage 05 recovery Task and Prompt 02 runtime/migration gate |
| 11 | W7.5 | DRAFT contract; PASS requires reviewed handoff, not a future digest lookup | Prompt 02 Spec/Task and image/version owner |

## Review Evidence

Independent evidence review accepted W7.1's no-business-app finding, W7.2's
bounded consumer/traffic inventory, and W7.3's point-in-time capacity as
scoped PASS. Transaction origin and DBeaver's selected database remain
unknown. Restore-packet review separated selected-backup engine consistency
from post-backup PITR and application recovery. The historical real-data PITR
record in SPEC-0182-TSK-0003 closes the claimed absence of any HOME-data
restore evidence; it does not validate the current set. POL-0021 version
1.4.4 (`docs/05.operations/policies/0021-backup-and-restore.md`) proposes to
correct its stale no-HOME-data-restore entry using that source. Independent rules-engineer
semantic review found the bounded statement accurate and no first-restore
exception necessary. The owner accepted POL-0021 and RUN-0021 drafts and the
focused metadata/link checks exited 0. W7.1-W7.3 are accepted for Prompt 02
source-work entry; W7.4 is deferred/NOT_RUN and current-backup restoreability
remains unproven. Any future Phase A or restore needs renewed approval and
fresh preflight. SPEC-0201's diagnosis/design package is accepted under the
owner's revised criterion 10; this is not an operational recovery receipt.

## Commit Ledger

W7.1–W7.3 evidence and the W7.4 deferral were committed in
`b867eb7d466000ed8d49f6a8eb6410f1db646268` and reached local `main` at
`5f99e0e51b41b912f128daafb4a3d41539b77560`. The original observation
approval did not authorize remote or operational changes; remote delivery is
now a separately approved action. The TSK-0001 receipt remains preserved.

## Rulings

- Read-only catalog and aggregate telemetry queries were used; raw SQL
  statement text, row values, addresses, logs, auth files, and secret values
  are excluded from output and documents.
- A real-backup restore is an isolated execution using approved source and
  disposable target. It does not authorize actual HOME recovery or data move.
- The owner reports no current app uses `app_db` and no stored data; the
  catalog found one technical heartbeat row and a dbt view. W7.1 business
  ownership is resolved. DBeaver connects by SSH to
  management PostgreSQL. Its selected database and each `app_db` commit
  origin remain unverified limits on W7.2's scoped PASS.
- Future image digest and compatibility must be checked at Prompt 02 start;
  the check is not satisfiable in advance by a dated tag or digest observation.

## Deferred Items

Prompt 02 implementation, HOME deployment, service stop/restart, data migration
or deletion, credential rotation, remote mutation, and DNS/firewall change stay
outside this Task. The owner deferred W7.4 after two safe preflight aborts and accepted the
revised SPEC-0201 source-work gate. Prompt 02 can now open its own Spec/Plan/Task;
future recovery or operational migration still needs separate evidence and approval.
