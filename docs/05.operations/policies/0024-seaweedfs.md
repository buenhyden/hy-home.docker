---
title: "SeaweedFS Operations Policy"
version: "1.5.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0024"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# SeaweedFS Operations Policy

## Overview

이 정책은 현재 소스 구성을 데이터 보호, 보안, 리소스, 생명주기와 독립적으로 검증 가능한
운영 통제에 묶는다.

## Policy Scope

SeaweedFS는 S3 object store이며 SPEC-0180 S07에서 MinIO를 대체했다. HOME 대상이다.
S3 consumer를 선택하는 모든 profile(`storage`, `obs`, `logs`, `tracing`, `nginx`,
`mlops`, `data-science`, `lakehouse`)은 4개 서비스와 `seaweedfs-buckets`도 함께
선택하며, `seaweedfs`와 `storage-seaweedfs` profile도 마찬가지다. `lakehouse`는
`seaweedfs-table-bucket`도 함께 선택한다. Terrakube(`iac`, HOME이 제외하는 자동화
profile)는 `storage`와 함께 동작한다.

## Controls

- **영속 세트.** Master(`-mdir=/data`), volume(`-dir=/data`)과 filer의 내장
  leveldb2 store(`/data/filerldb2`)는 각각 `${DEFAULT_DATA_DIR}/seaweedfs` 아래
  bind volume을 갖는다. 내장 store를 외부 database 대신 선택한 이유는 시작이나
  복구 의존성을 추가하지 않고 filer metadata export가 이식 가능한 형태이기
  때문이다. `/data` mount만으로는 경로를 증명하지 못하며, rehearsal이 파일이
  실제로 그 위치에 있는지 확인한다.
- **S3 identity.** `seaweedfs-s3`는 secret으로 구성된 명시적 identity(admin:
  `SEAWEEDFS_S3_ADMIN_ACCESS_KEY`와 STRG-010)로만 시작한다. Identity 구성은 scoped 인증을 요구하며 명시된 CDN anonymous-read 예외만 허용한다. S07에서 추가된 모든 consumer는
  `config/s3-identities.conf`에 자신의 bucket(loki, tempo, mlflow, terrakube,
  lakehouse)으로 범위가 한정된 identity를 갖는다. 어떤 consumer도 admin을 쓰지
  않으며, `anonymous`는 `cdn-bucket`의 객체만 읽을 수 있다. Bucket은 consumer가
  아니라 `seaweedfs-buckets`가 생성한다.
- **IAM 우회 금지.** Volume과 filer HTTP는 읽기/쓰기 모두 STRG-008과 STRG-009로
  서명된 JWT를 요구한다. S3 route만 있고 master와 filer에는 Traefik route가
  없다. CDN은 S3를 통한 public-read bucket이며 filer를 거치지 않는다.
- **내부 전송.** 모든 gRPC port는 SeaweedFS 전용 CA(`bin/gen-grpc-certs.sh`; CA
  key는 발급 후 폐기)로 mutual TLS를 사용한다. S3는 `object_net`에서 SigV4
  서명을 사용한 plain HTTP이며, host client에는 Traefik을 통한 HTTPS를
  제공한다. Master, volume, filer는 `seaweed_internal`(internal)에만 있으며
  master의 인증되지 않은 `/dir/assign`은 그곳에서만 접근할 수 있다.
- **최소 노출면.** Lance listener와 내장 IAM API는 꺼져 있다. Iceberg REST
  catalog는 `object_net`에서만 접근 가능해야 하며 route/host port를 두지 않는다. **현재 구현 미준수**: `seaweedfs-s3`의4.47 listener는 `0.0.0.0:8181`로 edge_net/seaweed_internal/object_net 모두에서 도달 가능하다. host port와 catalog router는 없고 데이터 관리 route는 인증 middleware를 사용한다. 단순 `expose` 제거로 격리되지 않으며 별도 source 변경과 network별 부정 접근 검증이 필요하다. 예외는 승인되지 않았다. 동일 identity(SigV4)를 사용한다. Table bucket은 `lakehouse`
  하나뿐이며 admin이 소유한다. 해당 policy는 `lakehouse` identity에 catalog와
  table action만 부여한다(policy 변경이나 bucket 삭제는 불가). Run마다
  `seaweedfs-table-bucket`이 이를 재작성하므로 수동 편집한 policy는 유지되지
  않는다.
- **Metrics.** `seaweedfs-s3`만 `9327`에서 metrics를 제공하며 Prometheus가
  job `seaweedfs-s3`로 수집한다. Listener는 게시되지 않고 Traefik route도
  없지만, 어떤 `edge_net` 서비스든 접근할 수 있다. Request counter와
  latency만 담고 있어 민감도가 낮으므로 이를 허용한다. Master, volume, filer는
  scraping에 노출되지 않는다. `SeaweedFSS3Down`과 `SeaweedFSDataDiskLow`는
  `alert_rules.local.datastores.yml`에 있다. Disk rule은 data-disk 파일시스템의
  node-exporter mountpoint를 고정하며, `DEFAULT_MOUNT_VOLUME_PATH`가 이동하면
  함께 갱신해야 한다.
- **용량.** Volume server는 data disk의 여유 공간이 20 GiB 아래로 내려가면
  쓰기를 중단한다(`-minFreeSpace`, POL-0035). 동일 host replica는 host
  가용성이 아니므로 replication은 `000`이다.

### Backup and restore

일일 orchestrator(RUN-0021)는 vacuum을 멈추고 `fs.meta.save`로 filer metadata를
저장한 뒤, Restic이 volume과 master tree를 읽게 하고 종료 시 vacuum을 다시
활성화한다. Needle은 append-only이므로 metadata export 이전에 작성된 객체는
온전히 복원된다. Restic이 volume 파일을 읽는 동안 덮어쓰거나 삭제된 객체는
누락으로 복원될 수 있고, data 파일 이후 복사된 volume index는 그 끝을 넘어선
needle을 나열할 수 있다(복원 시 `volume.fsck`로 확인). 따라서 recovery point는
export 시각에서 Restic 창 안에서 변경된 객체를 뺀 시점이다. 세트는 다른
물리 디스크의 암호화된 Restic state repository에 5 GiB 예산(POL-0021) 안에서
보관된다. 일일 세트는 30일, 주간 세트는 90일 보관한다. 목표는 RPO 24시간,
RTO 8시간이며, isolated rehearsal은 HOME 타이밍이 아니라 방법을 증명한다.

동일 버전의 빈 대상으로 복원한다. Volume과 master tree를 제자리에 두고, filer
store를 비운 뒤 `fs.meta.load`를 실행하고 S3 읽기를 확인한다. HOME에서의
cutover, 삭제, state 재사용은 별도 승인이 필요하다.

### Change policy

Image 갱신에는 공식 release와 license 검토, 통과한 `SeaweedfsRehearsalTests`
실행이 필요하다. Identity, key, certificate 교체는 모든 구성 요소를 재시작하며
승인이 필요하다. 새 consumer identity는 해당 consumer의 cutover와 같은
change에서 추가한다.

### Accountable lifecycle boundary

적용 identity: `seaweedfs-buckets`, `seaweedfs-filer`, `seaweedfs-master`, `seaweedfs-s3`, `seaweedfs-volume`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

FUSE mount는 별도 승인이 필요하다. 예외는 runtime mutation, plaintext secret,
raw active storage 복사, 동일 host 가용성 주장을 허용하지 않는다.

## Verification

Root 구성과 범위가 지정된 static policy check를 검증한 뒤, 승격이나 cutover
전에 application 수준 acceptance를 갖춘 isolated compatible restore를
요구한다. 검증되지 않은 runtime 속성은 명시적으로 기록한다.

## Review Cadence

Profile, image, volume, credential, consumer, retention 또는 upstream
lifecycle 변경 후, 그리고 보관되는 동안 최소 연 1회 검토한다.

## Traceability

- Runtime source: [SeaweedFS Compose](../../../infra/04-data/seaweedfs/docker-compose.yml).
- Artifact: `POL-0024`; parent: `AD-0004`.
- Runtime 권한은 연결된 Compose/소스 파일에 남아 있으며, 정확한 pin도 그곳에 있다.

### References

- [Data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup)
- [Security configuration](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration)
- [Runbook](../runbooks/0024-seaweedfs.md)

## Related Documents

- [Domain catalog](../README.md)
