---
title: "SeaweedFS Stack Health Runbook"
version: "1.6.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "RUN-0024"
parent_ids:
- "GDE-0024"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# SeaweedFS Stack Health and Recovery Runbook

## Trigger and Scope

### Trigger

SeaweedFS 스택의 정적 진단, 경보 대응, 최초 활성화, 백업·격리 복구 절차를 다룬다.

이 subject의 승인된 static diagnosis, backup 계획, isolated recovery에
사용한다.

### Targets

- Runtime source: [SeaweedFS Compose](../../../../infra/04-data/seaweedfs/docker-compose.yml).
- Artifact: `RUN-0024`; parent guide: `GDE-0024`.
- isolated rehearsal은 2026-09-22에 실행했다(SPEC-0180 Task 0008 S06). HOME activation과 HOME restore는 아직 실행하지 않았다.

- [Domain catalog](../../README.md)
- [Policy](../../policies/05-databases-and-storage/0024-seaweedfs.md)
- [SeaweedFS data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup)

## Preflight

### Authority

live write, restore, cutover, cleanup, credential 변경은 별도로
승인된 task가 필요하다.

대상: `seaweedfs-buckets`, `seaweedfs-filer`, `seaweedfs-master`, `seaweedfs-s3`, `seaweedfs-volume`. table bucket 작업 `seaweedfs-table-bucket`은 lakehouse LAB의 [RUN-0094](../15-labs/0094-lakehouse.md)가 다룬다(SPEC-0262). 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../../guides/01-common/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../../policies/01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

### Environment

Steps의 첫 코드 블록에서 `config --quiet`는 렌더링만 검증하는 사전 점검이며, 그 아래 rehearsal은 별도 승인된 disposable runtime에서만 실행한다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | First activation: `gen-secrets.sh`로 STRG-008/009/010 생성하고 `.env`에 `SEAWEEDFS_S3_ADMIN_ACCESS_KEY` 설정 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 2 | First activation: `gen-grpc-certs.sh`로 gRPC certificate 발급 | 기본 `secrets/certs/seaweedfs`에 발급되고 Compose mount 경로와 일치 | 불완전한 세트면 중단 |
| 3 | First activation: data 디렉터리를 UID 1000으로 만든 뒤 `docker compose --profile seaweedfs up -d --wait` 실행 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 4 | First activation: admin identity로 disposable bucket 생성/삭제와 anonymous 요청 확인 | anonymous 보호 대상 요청이 403 반환 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 5 | Restore: Restic snapshot과 `seaweedfs-filer.meta` export를 동일 version의 빈 target에 복원 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 6 | Restore: 네 service를 시작하고 health 대기 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 7 | Restore: `fs.meta.load`와 `volume.fsck` 실행 | 문서에 기록 없음 | Restic window 동안 변경된 객체는 누락될 수 있음(POL-0024), 실패 target과 증거를 보존하고 escalation |
| 8 | Restore: 복구 범위 bucket을 S3로 읽어 manifest와 count/byte 비교 | manifest와 count/byte 일치, 제외된 telemetry 이력은 별도 기록, Loki/Tempo 신규 수집 확인 | client 전환 전 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |

repository root에서 실행한다.

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
# 별도 승인된 disposable runtime rehearsal만: 빌드·쓰기·삭제 효과가 있다.
HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest \
  tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests
```

rehearsal은 disposable data에서 실제 service를 렌더링한다. anonymous 및
wrong-credential 보호 대상 요청이 거부되는지, filer와 volume HTTP가 JWT를 요구하는지,
gRPC가 client certificate를 요구하는지, consumer S3 API, restart 후
persistence, volume server가 다운된 동안 read가 실패하는지, 빈 store로의
backup과 restore를 확인한다.

#### Alerts

- `SeaweedFSS3Down`: `docker compose --profile seaweedfs ps seaweedfs-s3`와 그 로그를 확인한다.
  metrics listener가 S3 프로세스를 공유하므로, target이 다운되었다면
  보통 S3가 다운되었거나 재시작 중이다.
- `SeaweedFSNodeMetricsDown`: master, volume, filer 중 하나의 metric target이
  down이다. `docker compose --profile seaweedfs ps seaweedfs-master seaweedfs-volume seaweedfs-filer`와
  해당 로그를 확인하고, 세 서비스와 Prometheus가 모두 `seaweedfs_metrics_net`에
  있는지 `docker network inspect`로 확인한다. metric listener는 각 프로세스를
  공유하므로 서비스가 정상인데 target만 down이면 network 구성원을 먼저 본다.
- `SeaweedFSDataDiskLow`: data-disk filesystem의 여유 공간이 15% 미만이다.
  20 GiB 미만이 되면 volume server가 write 수락을 멈춘다(`-minFreeSpace`).
  그 전에 공간을 확보하거나 escalation한다. 객체 삭제는 승인된 task가
  필요하다.

#### First activation (approved task)

1. `bash scripts/operations/gen-secrets.sh`가 STRG-008, STRG-009, STRG-010을
   생성한다. `.env`에 `SEAWEEDFS_S3_ADMIN_ACCESS_KEY`를 설정한다.
2. `bash infra/04-data/seaweedfs/bin/gen-grpc-certs.sh`가
   gRPC certificate를 기본 `secrets/certs/seaweedfs`에 발급한다(`--rotate`를
   쓰지 않는 한 기존 세트를 유지하고, 불완전한 세트면 중단한다). Compose는 이를
   `${DEFAULT_CERT_DIR}/seaweedfs`에서 `/certs`로 read-only mount하므로 두 경로가 같아야 한다.
3. `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}`를 UID 1000(host
   operator)으로 생성한 뒤
   `docker compose --profile seaweedfs up -d --wait`를 실행한다.
4. admin identity로 검증한다: disposable bucket을 만들고 삭제하며, anonymous
   보호 대상 요청이 403을 반환하는지 확인한다.

#### Retained MinIO data

Loki, Tempo, MLflow는 2026-09-22에 SeaweedFS로 이전했다(SPEC-0180 S07). 각
bucket에는 그 copy에서 나온 `hyhome-migration/<bucket>.cutover` marker가
있다. 그 뒤 source에서 MinIO를 제거했다. 2026-09-25에 SPEC-0182
W5는 데이터 디렉터리 `${DEFAULT_DATA_DIR}/minio/data-1`, volume
`hy-home-infra_minio-data`, 격리된 MinIO credential 파일, `quay.io/minio/minio`
image를 폐기했고 이로써 S07의 MinIO rollback 경로는 끝났다. 현재 복구에 사용할
수 있는 백업은 아래 범위와 해당 snapshot의 manifest를 따로 확인한다.

#### Backup (daily, RUN-0021)

`hyhome-backup.sh`는 `seaweedfs-master`를 통해 다음을 실행한다:
`volume.vacuum.disable`, 그 다음 `fs.meta.save -o /tmp/filer.meta /`를
staging export로 복사, 그 다음 Restic이 `data/seaweedfs/volume`과
`data/seaweedfs/master`를 읽고, 그 다음 EXIT trap에서
`volume.vacuum.enable`. script는 `weed shell`의 exit가 0이 아니거나 그
출력에 오류 텍스트가 있을 때, export가 비어 있을 때, master와 filer 중
하나만 실행 중일 때 run을 실패로 처리한다. stale export는 save 전마다
지운다. SeaweedFS가 아예 실행 중이 아니면 실패로 보지 않는다.
SIGKILL로 종료된 run(예: unit의 stop timeout)은 vacuum이 꺼진 채로 남는다.
`seaweedfs-master`에서 `hyhome-seaweedfs.sh shell`을 통해
`volume.vacuum.enable`을 실행한다.

[HOME 백업 정책](../../policies/10-platform-and-backup/0021-backup-and-restore.md)에 따라
`loki-bucket`과 `tempo-bucket` collection의 volume file은 state snapshot에서 제외된다.
Filer metadata가 복원되더라도 제외된 object 이력은 돌아오지 않는다.

#### Restore (isolated first)

1. Restic snapshot의 `data/seaweedfs/{volume,master}`와
   `seaweedfs-filer.meta` export(RUN-0021 step 6)를 동일한 version의 빈
   target에 빈 `filer` 디렉터리와 함께 복원한다.
2. 네 service를 시작하고 health를 기다린다.
3. export를 `seaweedfs-master`로 복사하고 `hyhome-seaweedfs.sh shell`을 통해
   `fs.meta.load`를 실행한 뒤 `volume.fsck`를 실행한다. backup의 Restic
   window 동안 변경된 객체는 누락될 수 있다(POL-0024).
4. client를 전환하기 전에 승인된 복구 범위에 포함된 bucket의 객체를 S3로 읽어
   manifest와 count/byte를 비교한다. 제외된 telemetry 이력은 별도로 기록하고
   Loki와 Tempo가 새 데이터를 수집하는지 확인한다.

### Stop Conditions

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Verification

### Expected Results

#### Service Checks

rehearsal은 anonymous 및 wrong-credential 요청의 거부, filer와 volume HTTP의 JWT 요구, gRPC의 client certificate 요구, consumer S3 API, restart 후 persistence, 빈 store로의 backup과 restore를 확인한다. 실제 복구 검증은 Restore 단계의 manifest와 제외 범위를 따른다.

#### Evidence

source revision/version, scope, timestamp, manifest/checksum 요약, command와
exit status, validation 결과, 관찰된 recovery point/time, 모든 미검증
gap을 기록한다. secret, raw payload, 비공개 resolved 경로는 제외한다.

### Unverified Conditions

이 runbook은 아래 항목을 아직 관측하지 않았다.

- disposable runtime rehearsal: 별도 승인된 경우에만 실행하며 이 문서에는 실행 결과가 기록되어 있지 않다. `HYHOME_SEAWEEDFS_REHEARSAL=1`의 `SeaweedfsRehearsalTests` 통과 결과가 있으면 보호 요청 거부, JWT/client certificate 요구, persistence, backup/restore가 검증된다.
- First activation: 승인된 task에서만 하는 live 변경이며 실행 결과가 기록되어 있지 않다. disposable bucket 생성/삭제와 anonymous 403 관측이 필요하다.
- Backup(RUN-0021)과 Restore: 이 문서에는 실제 backup/restore 실행 기록이 없다. 격리 target에서 `fs.meta.load`, `volume.fsck`, manifest 대비 count/byte 비교 결과가 있으면 검증된다.
- 알림 대응(`SeaweedFSS3Down`, `SeaweedFSNodeMetricsDown`, `SeaweedFSDataDiskLow`): 실제 알림 발생 시 대응한 기록이 없다. 해당 알림 시 `ps`/로그/network 확인 결과가 필요하다.

## Escalation

### Next Owner

filer metadata 누락, topology mismatch, 고아 volume, checksum 실패, 보안
노출, version 비호환이 있으면 중단한다. 동일 snapshot의 filer metadata
export 없이 volume tree를 절대 복원하지 않는다.

### Recovery or Forward Repair

실패한 cutover는 write boundary를 검증한 뒤 client를 보존된 원본 store로
되돌린다. coordinated artifact와 isolated target은 그대로 보존한다.
cutover는 owner approval, 최종 consistency capture, application validation,
보존된 rollback window를 거친 뒤에만 진행한다.
