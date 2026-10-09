---
title: "04-Data Backup Policy"
version: "1.5.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0021"
parent_ids:
- "AD-0004"
created: "2026-06-04"
---

# 04-Data Backup Policy

## Overview

### Overview

이 policy는 현재 source configuration을 data protection, security, resource,
lifecycle, 독립적으로 검증 가능한 operator control에 묶는다.

### Purpose

이 policy는 보존되는 모든 HOME state owner에 recoverability method를 배정한다.
Compose volume은 backup이 아니고, 단일 host 상의 replication은 host availability가
아니며, 성공적인 export가 restore evidence는 아니다. 날짜가 기록된 rehearsal
report가 달리 입증하기 전까지 모든 restore는 계획된 절차로 남는다.

`${DEFAULT_*}`로 시작하는 경로는 resolved host 값이 private operator state로
남는 bind-backed named volume이다.

## Scope

### Policy Scope

이 policy는 현재 source-backed package와 그 보존 state에 적용된다.

### HOME state-owner matrix

| 소유자와 data 분류 | 현재 상태가 저장되는 곳 | 필수 backup 방식과 저장 대상 | 암호화와 보존 | 계획 목표 | rehearsal·복구 소유자 |
| --- | --- | --- | --- | --- | --- |
| Management PostgreSQL: `postgres`, `n8n`, `keycloak`, `airflow`, `terrakube`, `sonarqube`, `${SERVICE_POSTGRES_DB:-app_db}` | `mng-pg-data` → `${DEFAULT_MANAGEMENT_DIR}/pg`; role과 grant는 cluster-wide | server image 내 pgBackRest: 일요일 full backup, 매일 differential, 지속적인 WAL archive(`archive_timeout`)를 system SSD의 `${BACKUP_STATE_REPO_DIR}/pgbackrest`로(예산은 control 2); globals-only export와 pgBackRest repository 자체는 state Restic set에 들어가 R2로 간다(control 1); live `PGDATA` tree는 절대 복사하지 않는다 | BKP-001로 `aes-256-cbc` repository; full backup 두 개와 그 WAL 보존; Restic daily 30 / weekly 13 / monthly 12 | WAL archive 기준 RPO 5분, RTO 4시간은 planning target; 2026-09-25 격리 PITR에서 선택 시점과 약 8분 18초를 관측했으나 지속 보장은 미검증 | Synthetic full/diff/PITR rehearsal(2026-09-22)과 실제 HOME pgBackRest 저장소의 격리 PITR(2026-09-25) 통과. 후자는 선택 backup/WAL과 제한된 MLflow·dbt·heartbeat count만 검증했다([SPEC-0182-TSK-0003](../../03.specs/0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md)); 현재 backup, 전체 앱, offsite, 실제 cutover 증거는 아니다. 절차: [RUN-0021](../runbooks/0021-backup-and-restore.md); service recovery: [RUN-0028](../runbooks/0028-management-database.md) |
| Development PostgreSQL: `dev-pg` and approved external project databases | `dev-pg-data` → `${DEFAULT_DATA_DIR}/dev-pg`; management `app_db` is a legacy empty default and is not a development-project shared database | separate stanza `dev` in `${BACKUP_STATE_REPO_DIR}/dev-pgbackrest`: continuous WAL archive (`archive_mode=on`, `archive_timeout=300`, `archive-push-queue-max=2GiB`), the same nightly scheduler as management (Sunday full, other days differential after `check`), globals/schema export and Restic inclusion; live `PGDATA` tree is never copied | `dev_pgbackrest_cipher_pass` is a distinct secret reference; `repo1-retention-full=2`, `repo1-retention-diff=6` with their WAL; Restic retention as the state set | planning target only: WAL archive bounds the loss window to about 5 minutes while archiving succeeds; no RTO is measured | Synthetic offline recovery passed on 2026-10-04. HOME stanza, WAL activation, first full backup and isolated restore canary are recorded in [SPEC-0213-TSK-0002](../../03.specs/0213-dev-data-and-influx-retirement/tasks/tsk-0002-dev-backup-activation-and-monitoring.md); PITR and offsite (R2) restore stay unverified until that Task records them. |
| Management Valkey: OAuth2 Proxy session과 Airflow/n8n broker/cache | `mng-valkey-data` → `${DEFAULT_MANAGEMENT_DIR}/valkey`; AOF 활성화 | Point-in-time RDB stream(`valkey-cli --rdb -`)을 export staging으로, 이후 Restic snapshot; live AOF 디렉터리는 제외; queued work를 replay할지 discard할지 기록 | BKP-002로 Restic encryption; daily 30 / weekly 13 / monthly 12 | RPO 24시간, RTO 4시간; queued-job semantics는 incident 승인 필요 | Synthetic RDB export/reload rehearsal 2026-09-22; HOME-data restore 없음. Recovery: [RUN-0028](../runbooks/0028-management-database.md) |
| OpenBao secrets와 Raft state | `openbao-data` → `${DEFAULT_SECURITY_DIR}/openbao/data` | 별도 offline custody로 authenticated Raft snapshot; seal/recovery material은 해당 security runbook을 따른다 | Barrier encryption은 encrypted backup custody를 대체하지 않는다; daily 30일, monthly 1년 | RPO 24시간, RTO 4시간; planning target, 미검증 | No rehearsal. OpenBao security operations가 recovery를 소유한다. `openbao-agent-data`와 `openbao-agent-out`은 생성된 secret material을 담으며 일반 archive 밖에 있다. |
| OpenBao Agent 생성 auth/render state | `openbao-agent-data` → `${DEFAULT_SECURITY_DIR}/openbao/agent`; `openbao-agent-out` → `${DEFAULT_SECURITY_DIR}/openbao/out` | rendered secret output은 일반적으로 backup하지 않는다. agent를 재인증하고 restore된 OpenBao에서 다시 render해 recovery한다; non-secret template source는 별도로 보존한다 | Output은 secret을 담고 source-at-rest encryption은 미검증; 일반 retention 없음 | derived output에는 data RPO가 적용되지 않는다; recovery target 4시간, 미검증 | No rehearsal. Security operations가 재인증, template 검증, stale output의 안전한 폐기를 소유한다. |
| Open WebUI application state | `open-webui` → `${DEFAULT_AI_MODEL_DIR}/open-webui` | `backup-sqlite-export`가 SQLite Online Backup API로 integrity check와 함께 `webui.db`를 복사; upload와 기타 파일은 Restic으로 직접; live database 파일과 cache는 제외 | BKP-002로 Restic encryption; daily 30 / weekly 13 / monthly 12 | RPO 24시간, RTO 8시간; planning target, 미검증 | Synthetic WAL-database export rehearsal 2026-09-22; HOME-data restore 없음. AI operations subject가 isolated validation을 소유한다. |
| SeaweedFS object와 filer metadata | `seaweedfs-{master,volume,filer}` → `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}` | Orchestrator가 vacuum을 일시 중지하고, `fs.meta.save`로 filer metadata를 export하며, Restic이 volume과 master tree를 읽고, 종료 시 vacuum을 재개한다; live leveldb2 filer store는 file-copy하지 않는다 | BKP-002로 Restic encryption; daily 30 / weekly 13 / monthly 12; 5 GiB state budget에 포함 | RPO 24시간, RTO 8시간; planning target | Isolated rehearsal 2026-09-22: 빈 store로의 restore가 동일한 object를 반환; 아직 HOME data 없음. GDE/RUN-0024가 validation을 소유한다. |
| Gatus availability history | `gatus-data` → `${DEFAULT_OBSERVABILITY_DIR}/gatus`; WAL mode의 `/data/gatus.db`에 SQLite | uncheckpointed WAL page를 포함한 `backup-sqlite-export` Online Backup API 복사, 이후 Restic | BKP-002로 Restic encryption; daily 30 / weekly 13 / monthly 12 | RPO 24시간, RTO 4시간; planning target, 미검증 | Synthetic WAL export rehearsal 2026-09-22; HOME-data restore 없음. Gatus operations subject가 validation을 소유한다. |
| Grafana database, plugin, mutable state | `grafana-data` → `${DEFAULT_OBSERVABILITY_DIR}/grafana`; 현재 Compose는 external PostgreSQL을 구성하지 않는다 | `grafana.db`의 `backup-sqlite-export` Online Backup API 복사, 이후 Restic; plugin은 provisioning과 plugin list로부터 rebuild 가능; provisioning 파일은 tracked source로 남는다 | BKP-002로 Restic encryption; daily 30 / weekly 13 / monthly 12 | RPO 24시간, RTO 4시간; planning target, 미검증 | Synthetic export rehearsal 2026-09-22; HOME-data restore 없음. Grafana operations subject가 validation을 소유한다. |
| Keycloak theme, provider, runtime configuration | `keycloak-themes` → `${DEFAULT_AUTH_DIR}/keycloak/themes`; `keycloak-providers` → `${DEFAULT_AUTH_DIR}/keycloak/providers`; `keycloak-config` → `${DEFAULT_AUTH_DIR}/keycloak/conf`; 서비스가 read-only로 mount | 가능하면 versioned source/build artifact에 quiesced file snapshot과 hash manifest를 더함; `keycloak` PostgreSQL database, 별도 custody된 secret과 pair | at-rest encryption 미선언; 어떤 backup이든 암호화; weekly 90일, upgrade 전 | RPO 7일, RTO 8시간; planning target, 미검증 | No rehearsal. Auth operations는 provider/theme 호환성과 restore된 database state 대비 realm login을 검증해야 한다. |
| Airflow schedule과 metadata | `airflow-config`, `airflow-dags`, `airflow-logs`, `airflow-plugins`, PostgreSQL database `airflow`, management Valkey | scheduler/worker 일시 중지 이후 조정된 PostgreSQL logical dump와 file snapshot; DAG/plugin/config 보존; log는 operational retention을 따른다 | Encrypted destination 필수; metadata/파일 daily 30일, log 14일 | RPO 24시간, RTO 8시간; planning target, 미검증 | No rehearsal. Airflow operations가 application validation과 Fernet/key custody를 소유한다. |
| n8n workflow, credential, runner | `n8n-data`, `n8n-task-runner-data`, `n8n-task-runner-worker-data`, `infra/07-workflow/n8n/custom`, PostgreSQL database `n8n`, management Valkey | producer/worker 일시 중지; 조정된 PostgreSQL dump와 file snapshot; encryption key는 별도 보존; Valkey restore 전에 queue replay 여부 결정 | Encrypted destination 필수; daily 30일 | RPO 24시간, RTO 8시간; planning target, 미검증 | No rehearsal. n8n operations가 workflow, credential, runner validation을 소유한다. |
| ComfyUI user asset과 workflow | `comfyui-custom-nodes`, `comfyui-input`, `comfyui-output`, `comfyui-user` | custom-node source/revision inventory를 포함한 quiesced file snapshot | source-at-rest encryption 미검증; encrypted destination 필수; input/user는 daily, output/custom node는 weekly, 30/90일 retention | RPO 24시간, RTO 24시간; planning target, 미검증 | No rehearsal. `comfyui-models`, Hugging Face, Torch cache는 model identifier, license, hash가 기록될 때만 rebuild 가능. |
| Ollama local model store | `ollama-data` → `${DEFAULT_AI_MODEL_DIR}/ollama` | custom Modelfile과 대체 불가능한 input 보존; 검증된 re-pull을 위해 다운로드한 model을 catalog화. `models/manifests`·`manifests-v2`는 state set에 포함하고 blob은 제외 | source-at-rest encryption 미검증; custom input weekly 90일 | Rebuild target 24시간; reproducibly sourced된 다운로드 blob은 data-loss RPO가 없다 | Catalog 격리 복원만 시험(SPEC-0226). Blob re-pull 미시험. Rebuild 예외는 source, version, license, hash evidence가 필요하다. |
| Qdrant vector collection | `qdrant-data` → `${DEFAULT_DATA_DIR}/qdrant/data` | Qdrant collection/full-storage snapshot을 별도 target으로 복사; live directory 복사를 snapshot으로 취급하지 않는다 | source-at-rest encryption 미검증; encrypted destination 필수; daily 30일 | RPO 24시간, RTO 8시간; planning target, 미검증 | No rehearsal. Qdrant operations가 isolated snapshot restore를 소유한다. |
| Prometheus metrics | `prometheus-data` → `${DEFAULT_OBSERVABILITY_DIR}/prometheus` | 지원되면 engine snapshot, 아니면 stopped filesystem snapshot; tracked scrape/rule configuration은 source에서 restore | source-at-rest encryption 미검증; encrypted destination 필수; daily 7일 | RPO 24시간, RTO 8시간; planning target, 미검증 | No rehearsal. Prometheus operations가 TSDB validation을 소유한다. |
| Loki logs | WAL/cache/rule용 `loki-data` → `${DEFAULT_OBSERVABILITY_DIR}/loki`, 그리고 SeaweedFS `loki-bucket` | Loki quiescence, local WAL/rule snapshot, SeaweedFS set(RUN-0024)을 조정; 양쪽을 동일한 recovery point로 restore | source-at-rest encryption 미검증; encrypted destination 필수; daily 14일 | RPO 24시간, RTO 8시간; planning target, 미검증 | No rehearsal. Loki operations와 [RUN-0024](../runbooks/0024-seaweedfs.md)가 validation을 공유한다. |
| Tempo trace(HOME 서비스, 보존되는 bucket state) | WAL/cache용 `tempo-data` → `${DEFAULT_OBSERVABILITY_DIR}/tempo`, 그리고 SeaweedFS `tempo-bucket` | trace가 보존될 때 Tempo quiescence, local WAL snapshot, SeaweedFS object backup을 조정 | source-at-rest encryption 미검증; encrypted destination 필수; daily 7일 | 선택 시 RPO 24시간, RTO 8시간; planning target, 미검증 | No rehearsal. Tempo operations와 [RUN-0024](../runbooks/0024-seaweedfs.md)가 validation을 공유한다. |
| Alertmanager silence/state | `alertmanager-data` → `${DEFAULT_OBSERVABILITY_DIR}/alertmanager` | Stopped 또는 application-consistent snapshot; tracked routing configuration은 source에서 restore | source-at-rest encryption 미검증; encrypted destination 필수; daily 7일 | RPO 24시간, RTO 4시간; planning target, 미검증 | No rehearsal. Alertmanager operations가 silence와 route validation을 소유한다. |
| Alloy ingestion cursor/WAL | `alloy-data` → `${DEFAULT_OBSERVABILITY_DIR}/alloy` | 중복 또는 누락된 ingestion이 허용되지 않을 때 stopped snapshot; 그렇지 않으면 loss window를 기록하고 tracked config로부터 rebuild | source-at-rest encryption 미검증; 보존 시 encrypted destination 필수; 7일 | RPO 24시간, RTO 4시간; planning target, 미검증 | No rehearsal. Rebuild는 telemetry gap을 수용할 때만 허용된다. |

### Traceability

- Artifact: `POL-0021`; parent: `AD-0004`.
- Runtime authority는 연결된 Compose/source 파일에 남는다; 정확한 pin도 그 파일에 있다.

### Official references

- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [SQLite Online Backup API](https://sqlite.org/backup.html) and [backup-copy hazards](https://sqlite.org/howtocorrupt.html)
- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Qdrant snapshots](https://qdrant.tech/documentation/concepts/snapshots/)
- [Grafana backup guidance](https://grafana.com/docs/grafana/latest/administration/back-up-grafana/)
- [OpenBao Raft operator commands](https://openbao.org/docs/commands/operator/raft/)
- [pgBackRest user guide](https://pgbackrest.org/user-guide.html) and [command reference](https://pgbackrest.org/command.html)
- [Restic repository preparation](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html) and [snapshot removal](https://restic.readthedocs.io/en/stable/060_forget.html)

## Rules

### Controls

전체 export·백업·검증 성공이 유효 복구 세트의 필수 조건이다. 현재 `restic_ok`는 Restic backup/check만 gate하므로 앞선 pgBackRest/globals/Valkey/SQLite/SeaweedFS 실패에도 partial snapshot/copy가 생길 수 있다. 종료1·성공 timestamp 부재를 실패로 유지하고 snapshot 존재로 승격하지 않는다. 자동 skip 강화는 별도 구현 사항이다. `archive_timeout`의 5분은 segment 전환 설정이며 성공 archive RPO 보장이 아니다.

1. destination은 source volume 밖에, 다른 physical disk에 있어야 한다.
   `BACKUP_STATE_REPO_DIR`(system SSD)는 data-disk state의 복사본을,
   `BACKUP_HOST_REPO_DIR`(data disk)는 `secrets/`와 `.env`의 복사본을 담는다;
   orchestrator는 자신의 source와 같은 filesystem에 있거나 그 안에 있는
   repository를 거부한다. 서로 다른 filesystem이 같은 physical disk일 수 있으므로 물리 매핑 검증은 별도 필수다. 오프사이트(ADR-0041): 로컬 backup과 check가
   성공하면 `restic-offsite`가 두 Restic repository의 snapshot을, state
   set 안의 pgBackRest repository까지 포함해 bucket lock이 걸린 Cloudflare R2
   repository 하나로 복사한다. host의 token은 object를 쓸 수 있지만 bucket을
   관리하거나 지우지 못한다. owner가 RUN-0021의 R2 설정을 마치고 첫 copy가
   성공하면 원격 사본이 생긴다. 전체 export 성공과 격리 restore를 별도로 확인하기 전 recoverability는 미검증이며 원격 RPO 하루는 계획 목표다. 원격 보존은 owner가
   매달 실행하는 `forget-prune`(최근 30일 전부와 월 1개씩 12개월)으로 R2 무료
   한도 초과 위험을 검토한다; 보존/과금 상한을 보장하지 않는다(RUN-0021 8.5, 8.6). 그 전까지는 모든
   복사본이 한 host에 있어 **offsite recovery는 제공되지 않는다**.
2. SSD repository의 크기 예산은 `BACKUP_STATE_MAX_GIB`(5 GiB, owner 2026-09-22)
   이다. pgBackRest와 export 이후 검사에서 초과하면 run이 실패하고 해당 Restic 단계를 건너뛴다. 실행 중 quota는 아니며 후속 쓰기로 초과할 수 있다;
   예산을 맞추려고 snapshot을 자동으로 삭제하지도 않는다.
3. Backup key BKP-001과 BKP-002, R2 secret BKP-003~005는 이 host 밖에
   offline 사본을 두고 OpenBao에는 절대 두지 않는다. Restic의 host
   repository는 key를 담지만 열려면 BKP-002가 필요하고, R2 repository는
   BKP-003이 필요하다.
4. backup을 소유하는 scheduler는 하나뿐이다: host의 `hyhome-backup.timer`.
   Airflow와 다른 scheduler는 backup을 실행하지 않는다. Snapshot 삭제
   (`forget-prune`)는 별도 승인을 받는 manual procedure다.
5. engine이 지원하는 export 또는 snapshot method를 사용한다. active
   PostgreSQL, SQLite, Valkey, SeaweedFS, Qdrant, Loki, Tempo storage의
   raw 복사본은 승인된 backup artifact가 아니다. SeaweedFS volume tree는
   needle이 append-only이고 vacuum이 일시 중지되며 filer metadata가 먼저
   export되기 때문에만 live로 읽는다. 그 set의 restore는 rehearsal을 거쳤다
   (GDE-0024); Restic이 읽는 동안 변경된 object는 그 set에서 누락될 수 있다
   (POL-0024).
6. service, engine/source version, timestamp, scope, 의미 있는 경우
   object/file count, byte size, cryptographic hash를 담은 manifest를
   기록한다.
7. password, unseal material, database dump, workflow credential, 또는
   secret-rendered agent output을 Git이나 generic evidence tree에 두지
   않는다.
8. Destructive recovery, cutover, cleanup, credential rotation, live service
   변경은 별도로 승인된 task가 필요하다. 이 policy는 이를 승인하지 않는다.

### Development backup chain

개발 pgBackRest 편입은 기존 state set과 예산·실패 경보를 재사용합니다.
`dev-pgbackrest/`는 read-only source이며 관리 stanza/key/PGDATA와 독립입니다.
개발 backup/check 실패·서버 중단·export 실패 시 전체 성공 timestamp를 기록하지
않습니다. 부분 snapshot/copy는 복구 PASS가 아닙니다. 연속 WAL archive는 `dev`
stanza가 먼저 만들어진 뒤에만 켭니다. stanza가 없거나 `archive_mode=off`이면
`check`가 실패하고 그 밤의 백업 실행 전체가 실패로 남습니다. archive가 계속
실패하면 `archive-push-queue-max=2GiB`를 넘는 WAL은 버려지고 그 구간은 PITR
공백입니다. 보존 정책 축소, offsite 쓰기, 실제 cutover restore는 별도 구체적
승인 대상입니다.

### Restore acceptance

Rehearsal은 isolated target, 호환되는 engine version, disposable credential을
사용한다. application-level read/write를 증명하고, planning RTO 대비
경과 시간을 기록하며, 관찰된 recovery point를 명시하고, 이후 test copy를
폐기하거나 안전하게 보관한다. Production 교체는 rollback을 갖추고 별도로
승인된 cutover다.

### Accountable lifecycle boundary

적용 identity: `restic`, `restic-offsite`, `backup-sqlite-export`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Verification

root configuration과 scoped static policy check를 검증한 다음, promotion
또는 cutover 전에 application-level acceptance를 갖춘 isolated compatible
restore를 요구한다. 미검증 runtime 속성은 명시적으로 기록한다.

### Review Cadence

profile, image, volume, credential, consumer, retention, 또는 upstream
lifecycle 변경 이후, 그리고 보존되는 동안 최소 연 1회 검토한다.

보존되던 MinIO data와 보존되던 Vault tree
(`${DEFAULT_MOUNT_VOLUME_PATH}/security/vault`)는 SPEC-0182 W5에 따라
2026-09-25에 폐기되었고 이로써 SPEC-0180 S07 rollback path가 종료되었다.
Restic은 더 이상 `security/vault`를 포함하지 않는다; 이를 담은 기존
snapshot은 위의 Restic retention에 따라 age out된다.

## Exceptions

### Exceptions

HOME state owner; rebuildable exception은 기록된 source evidence가 필요하다.
Exception은 runtime mutation, plaintext secret, active storage의 raw 복사,
또는 same-host availability 주장을 승인하지 않는다.

## Related Documents

- [Backup and Restore Guide](../guides/0021-backup-and-restore.md) and [Runbook](../runbooks/0021-backup-and-restore.md)
- Runtime sources: [Restic Compose](../../../infra/09-platform-ops/restic/docker-compose.yml), [pgBackRest image](../../../infra/04-data/mng-db/pg/backup/Dockerfile) and the [derived image projection](../../../infra/tech-stack.versions.json)
- [Data Architecture](../../02.architecture/descriptions/0004-data-architecture.md)
- [Data hardening policy](0030-data-optimization-hardening.md)
- [Storage exhaustion runbook](../runbooks/0035-storage-exhaustion.md)
