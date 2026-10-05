---
title: "SeaweedFS"
version: "1.2.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-12-06"
---

# SeaweedFS

## Overview

이 패키지는 HOME S3 오브젝트 스토어인 SeaweedFS를 정의합니다. SPEC-0180 S07에서
MinIO를 대체했습니다.

## Audience

오브젝트 저장소의 operator와 maintainer를 대상으로 합니다.

## Scope

[`docker-compose.yml`](docker-compose.yml)이 `seaweedfs-master`,
`seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`를 정의합니다. `seaweedfs`,
`storage-seaweedfs` profile과 모든 S3 소비자 profile(`storage`, `obs`, `logs`,
`tracing`, `nginx`, `mlops`, `data-science`, `lakehouse`)이 `seaweedfs-buckets`와
함께 이들을 선택합니다. `lakehouse`는 `seaweedfs-table-bucket`도 선택합니다.
S3가 유일한 인터페이스입니다. FUSE mount는 S04에서 제거되었고 master와
filer에는 route가 없습니다.

## Structure

| Path | Role |
| --- | --- |
| `docker-compose.yml` | 4개 서비스, 데이터 디스크 bind volume, secret |
| `config/hyhome-seaweedfs.sh` | 시작 스크립트: secret으로 JWT, gRPC mTLS, S3 identity 설정을 구성함 |
| `config/s3-identities.conf` | bucket 범위의 소비자 identity(loki, tempo, mlflow, terrakube, lakehouse)와 익명 CDN 읽기 |
| `config/seaweedfs-buckets.sh` | `seaweedfs-buckets` job: admin identity로 수행하는 idempotent bucket 생성 |
| `config/seaweedfs-table-bucket.sh` | `seaweedfs-table-bucket` job(`lakehouse`): Iceberg table bucket, 범위 정책, `dev`/`test` namespace |
| `bin/gen-grpc-certs.sh` | 호스트 스크립트: SeaweedFS 전용 gRPC CA와 인증서를 발급함 |

상태는 `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}` 아래에 있으며 UID
1000이 소유합니다. Master, volume, filer는 `seaweed_internal`에만 있습니다.
S3는 client용 `object_net`과 route용 `edge_net`에도 참여합니다.

## Usage

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest \
  tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests
```

최초 활성화, 백업, 복구는 RUN-0024를 따릅니다. 일일 백업은 filer metadata와
volume/master 트리를 순서 있는 한 세트로 담습니다(RUN-0021).

## Related Documents

[문서 진입점](../../../docs/README.md)에서 Stage 05 subject
`docs/05.operations/guides/0024-seaweedfs.md`와 POL-0021을 찾으십시오. 공식 소스:
[data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup),
[security](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration),
[license](https://github.com/seaweedfs/seaweedfs/blob/master/LICENSE).
