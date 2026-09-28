---
title: "SeaweedFS Stack Health Runbook"
version: "1.4.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0024"
parent_ids:
- "GDE-0024"
created: "2026-05-17"
---

# SeaweedFS Stack Health and Recovery Runbook

## When to Use

이 subject의 승인된 static diagnosis, backup 계획, isolated recovery에
사용한다. live write, restore, cutover, cleanup, credential 변경은 별도로
승인된 task가 필요하다.

## Procedure

repository root에서 실행한다.

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest \
  tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests
```

rehearsal은 disposable data에서 실제 service를 렌더링한다. anonymous 및
wrong-credential 요청이 거부되는지, filer와 volume HTTP가 JWT를 요구하는지,
gRPC가 client certificate를 요구하는지, consumer S3 API, restart 후
persistence, volume server가 다운된 동안 read가 실패하는지, 빈 store로의
backup과 restore를 확인한다.

### Alerts

- `SeaweedFSS3Down`: `docker compose ps seaweedfs-s3`와 그 로그를 확인한다.
  metrics listener가 S3 프로세스를 공유하므로, target이 다운되었다면
  보통 S3가 다운되었거나 재시작 중이다.
- `SeaweedFSDataDiskLow`: data-disk filesystem의 여유 공간이 15% 미만이다.
  20 GiB 미만이 되면 volume server가 write 수락을 멈춘다(`-minFreeSpace`).
  그 전에 공간을 확보하거나 escalation한다. 객체 삭제는 승인된 task가
  필요하다.

### First activation (approved task)

1. `bash scripts/operations/gen-secrets.sh`가 STRG-008, STRG-009, STRG-010을
   생성한다. `.env`에 `SEAWEEDFS_S3_ADMIN_ACCESS_KEY`를 설정한다.
2. `bash infra/04-data/lake-and-object/seaweedfs/bin/gen-grpc-certs.sh`가
   gRPC certificate를 `secrets/certs/seaweedfs`에 발급한다(`--rotate`를
   쓰지 않는 한 유지된다).
3. `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}`를 UID 1000(host
   operator)으로 생성한 뒤
   `docker compose --profile seaweedfs up -d --wait`를 실행한다.
4. admin identity로 검증한다: disposable bucket을 만들고 삭제하며, anonymous
   요청이 403을 반환하는지 확인한다.

### Retained MinIO data

Loki, Tempo, MLflow는 2026-09-22에 SeaweedFS로 이전했다(SPEC-0180 S07). 각
bucket에는 그 copy에서 나온 `hyhome-migration/<bucket>.cutover` marker가
있다. 그 뒤 source에서 MinIO를 제거했다. 2026-09-25에 SPEC-0182
W5는 데이터 디렉터리 `${DEFAULT_DATA_DIR}/minio/data-1`, volume
`hy-home-infra_minio-data`, 격리된 MinIO credential 파일, `quay.io/minio/minio`
image를 폐기했고 이로써 S07의 MinIO rollback 경로는 끝났다. 이 bucket들의
유일한 copy는 SeaweedFS에 있다.

### Backup (daily, RUN-0021)

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

### Restore (isolated first)

1. Restic snapshot의 `data/seaweedfs/{volume,master}`와
   `seaweedfs-filer.meta` export(RUN-0021 step 5)를 동일한 version의 빈
   target에 빈 `filer` 디렉터리와 함께 복원한다.
2. 네 service를 시작하고 health를 기다린다.
3. export를 `seaweedfs-master`로 복사하고 `hyhome-seaweedfs.sh shell`을 통해
   `fs.meta.load`를 실행한 뒤 `volume.fsck`를 실행한다. backup의 Restic
   window 동안 변경된 객체는 누락될 수 있다(POL-0024).
4. client를 전환하기 전에 S3를 통해 모든 bucket의 객체를 읽어 manifest와
   count/byte를 비교한다.

## Evidence

source revision/version, scope, timestamp, manifest/checksum 요약, command와
exit status, validation 결과, 관찰된 recovery point/time, 모든 미검증
gap을 기록한다. secret, raw payload, 비공개 resolved 경로는 제외한다.

## Rollback or Recovery

실패한 cutover는 write boundary를 검증한 뒤 client를 보존된 원본 store로
되돌린다. coordinated artifact와 isolated target은 그대로 보존한다.
cutover는 owner approval, 최종 consistency capture, application validation,
보존된 rollback window를 거친 뒤에만 진행한다.

## Escalation

filer metadata 누락, topology mismatch, 고아 volume, checksum 실패, 보안
노출, version 비호환이 있으면 중단한다. 동일 snapshot의 filer metadata
export 없이 volume tree를 절대 복원하지 않는다.

## Traceability

- Runtime source: [SeaweedFS Compose](../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml).
- Artifact: `RUN-0024`; parent guide: `GDE-0024`.
- isolated rehearsal은 2026-09-22에 실행했다(SPEC-0180 Task 0008 S06). HOME activation과 HOME restore는 아직 실행하지 않았다.

### References

- [SeaweedFS data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup)
- [Policy](../policies/0024-seaweedfs.md)

## Related Documents

- [Domain catalog](../README.md)
