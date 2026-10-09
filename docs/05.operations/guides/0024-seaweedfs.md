---
title: "SeaweedFS Usage Guide"
version: "1.5.5"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "operations"
artifact_id: "GDE-0024"
parent_ids:
- "POL-0024"
implementation_services:
  infra/04-data/seaweedfs/docker-compose.yml:
  - 'seaweedfs-buckets'
  - 'seaweedfs-filer'
  - 'seaweedfs-master'
  - 'seaweedfs-s3'
  - 'seaweedfs-volume'
created: "2026-05-10"
---

# SeaweedFS Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

SeaweedFS는 S3 object store이며 SPEC-0180 S07에서 MinIO를 대체했다.
consumer profile을 통해 HOME에 속한다. `http://seaweedfs-s3:8333`
(path-style, region `us-east-1`)의 S3가 유일한 interface이다. privileged
FUSE mount는 S04에서 제거되었으며 master와 filer에는 route가 없다.

### Current implementation

[`infra/04-data/seaweedfs/docker-compose.yml`](../../../infra/04-data/seaweedfs/docker-compose.yml)은
`seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`를
정의한다. profile `seaweedfs`와 `storage-seaweedfs`가 네 service를 모두
선택한다. 각 service는 UID 1000으로
[`config/hyhome-seaweedfs.sh`](../../../infra/04-data/seaweedfs/config/hyhome-seaweedfs.sh)를
통해 시작한다. 이 script는 `security.toml`(volume과 filer JWT key, gRPC
mTLS)을 만들고 S3용 identity 파일은 Docker secret에서 만든다.
secret이나 certificate가 없으면 시작을 거부한다.

state는 data disk에 있다: `${DEFAULT_DATA_DIR}/seaweedfs/master`, `/volume`,
`/filer`(embedded leveldb2 store). master, volume, filer는
`seaweed_internal`과 metric 전용 internal network `seaweedfs_metrics_net`에
있다. S3는 `seaweed_internal`에 더해 client용 `object_net`과
`s3.${DEFAULT_URL}` route용 `edge_net`에도 join한다.

S3는 `-metricsPort=9327`로 metric을 제공하고 Prometheus가 `edge_net`을 통해
job `seaweedfs-s3`로 scrape한다. master, volume, filer는 각각 9324, 9325,
9326에서 metric을 제공하며 Prometheus가 `seaweedfs_metrics_net`을 통해 job
`seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`로 scrape한다. 이
network의 다른 구성원은 Prometheus뿐이며 Prometheus는 SeaweedFS 신뢰 경계
안에 있다([POL-0024](../policies/0024-seaweedfs.md)). Alert:
`SeaweedFSS3Down`(target down 2분), `SeaweedFSNodeMetricsDown`(master·volume·filer metric
target down 5분)과 `SeaweedFSDataDiskLow`(node-exporter 기준 data-disk
filesystem free 15% 미만 10분).

### Identity-specific behavior

master 는 topology/volume 배정, volume 은 객체 bytes, filer 는 metadata/leveldb2 를 보존한다. s3 는 secret 에서 생성한 tmpfs config 와 gRPC mTLS 를 쓰며 네트워크 3 개에 참여한다.4.47 catalog8181 도 같은 s3 process 의 0.0.0.0 에 bind 되어 edge_net/seaweed_internal/object_net peer 가 접근 가능하다. host mapping/catalog router 는 없고 데이터 관리 route 는 인증 middleware 로 감싼다. object_net-only 요구는 미준수로 별도 구현 수정이 필요하다. buckets job 은 admin 으로 bucket 을 생성하며 table-bucket 은 GDE0094 소유다. 익명 CDN read 예외를 전체 anonymous 거부로 설명하지 않는다. 인증서 교체는 모든 peer 의 새 CA/leaf 수용을 검증한 승인 작업이다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `seaweedfs-buckets` | admin bucket provisioning job; 기존 bucket 보존 | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/04-data/seaweedfs/docker-compose.yml) |
| `seaweedfs-filer` | filer metadata/leveldb2 보존 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/seaweedfs/docker-compose.yml) |
| `seaweedfs-master` | topology/volume 배정; master metadata 보존 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/seaweedfs/docker-compose.yml) |
| `seaweedfs-s3` | S3·Iceberg·metrics listener; 생성 config, 자체 durable data 없음 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/seaweedfs/docker-compose.yml) |
| `seaweedfs-volume` | object bytes 보존; 최소 여유 공간에서 write 거부 | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/seaweedfs/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Consumers, buckets and migration

| Consumer | Bucket | Identity (access key ID) | Secret |
| --- | --- | --- | --- |
| Loki | `loki-bucket` | `loki` | STRG-011 |
| Tempo | `tempo-bucket` | `tempo` | STRG-012 |
| MLflow | `mlflow-artifacts` | `mlflow` | STRG-013 |
| Terrakube | `tfstate` | `terrakube` | STRG-014 |
| Spark (Iceberg) | `lakehouse` table bucket | `lakehouse` | STRG-015 |
| Nginx `/cdn/` | `cdn-bucket` | `anonymous` (object reads only) | none |

`seaweedfs-buckets`(aws-cli, admin identity)는 다섯 개 bucket을 생성하고,
`lakehouse`에 한해 `seaweedfs-table-bucket`이 `lakehouse` table bucket과 그
policy, `dev`/`test` namespace를 모두 idempotent하게 생성한다. bucket을
소유한 모든 consumer는 이를 기다린다(Nginx는 `seaweedfs-s3`만 기다린다).
S07 cutover는 각 MinIO bucket을 S3 API를 통해 복사하고
`hyhome-migration/<bucket>.cutover` marker object를 남겼다. copy job은
MinIO와 함께 제거되었다. 보존되어 있던 MinIO data, volume, image는
2026-09-25(SPEC-0182 W5)에 폐기되어 S07 rollback path가
종료되었다.

### Images, configuration and resource controls

Compose 파일은 고정된 `chrislusf/seaweedfs` image를 소유한다. Renovate가
update를 제안할 수 있으며 version projection은 파생물이다. root의
`SEAWEEDFS_*_HTTP_PORT`와 `SEAWEEDFS_*_GRPC_PORT` key가 listener를 제어한다.
`SEAWEEDFS_S3_ADMIN_ACCESS_KEY`가 admin identity의 이름을 정한다. 그 secret
key(STRG-010)와 JWT key(STRG-008, STRG-009)는 secret 파일이며 gRPC
certificate는 `bin/gen-grpc-certs.sh`로 만든다. master와 filer는
`template-stateful-med`를, volume은 `template-stateful-high`를, S3는
`template-infra-med`를 extend한다. 모든 service에 health check가 있다.
volume server는 free 20 GiB 미만에서 write를 거부한다. flow: master →
volume, filer → master/volume, 그다음 S3 → filer.

### Static preflight and rehearsal

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest \
  tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests
```

repository root에서 실행한다. rehearsal은 Docker가 필요하며 disposable
data만 사용한다.

### Verified S3 behaviour (4.47, 2026-09-22 rehearsal)

| Area | Result |
| --- | --- |
| Anonymous PUT/list, wrong secret | 403; `SignatureDoesNotMatch` |
| Filer GET/PUT and volume POST without JWT | 401 |
| gRPC without a client certificate | TLS alert `certificate required` |
| PUT with content type, user metadata and tags; HEAD; tagging read | preserved (보존됨) |
| Range GET, list with prefix, URL-encoded key with space and `+` | correct bytes and key (정확함) |
| 20 MiB multipart upload | round trip identical; ETag has the `-N` part suffix, so it is not an MD5 (MD5가 아님) |
| Presigned GET | correct bytes (정확함) |
| Key `a` then `a/b` | both stored and readable with their own bytes (모두 저장 및 자체 바이트로 읽기 가능) |
| Volume server stopped | GET fails instead of returning data (data를 반환하는 대신 실패) |
| Restart; restore of volume and master trees plus `fs.meta.load` into empty stores | objects identical (동일함) |

Versioning, Object Lock, SSE, notification, lifecycle rule은 테스트하지
않았다. S07은 cutover 전에 consumer에게 필요한 것을 테스트한다.

### Recovery and lifecycle

backup set은 filer metadata export, volume tree, master tree로 이루어지며
vacuum을 일시 중지한 채 이 순서대로 수행한다
([RUN-0024](../runbooks/0024-seaweedfs.md), RUN-0021).

image를 upgrade하려면 공식 release를 검토하고 rehearsal을 통과해야 한다.
SeaweedFS의 license는 Apache-2.0이다.

### Official references

- [SeaweedFS data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup)
- [SeaweedFS security configuration](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration)
- [SeaweedFS repository and license](https://github.com/seaweedfs/seaweedfs)

### Common Checks

정확한 root profile, service, health/resource control, writable-state
ownership, secret reference, exposure, engine별 recovery boundary를
확인한다. static pass는 configuration 증거일 뿐이다. runtime과 restore는
별개로 남는다.

### Traceability

- Artifact: `GDE-0024`; governing policy: `POL-0024`.
- Runtime authority: `infra/04-data/seaweedfs/docker-compose.yml`.

## Related Documents

- [Operations policy](../policies/0024-seaweedfs.md)
- [Health and recovery runbook](../runbooks/0024-seaweedfs.md)
- [Backup policy](../policies/0021-backup-and-restore.md)
