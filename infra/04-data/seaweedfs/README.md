---
title: "SeaweedFS"
version: "1.3.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-10"
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
함께 이들을 선택합니다. Iceberg table bucket job은 SPEC-0262에서
[lakehouse LAB](../../../labs/lakehouse/docker-compose.yml)으로 옮겼고, root `lakehouse`는 SeaweedFS만 선택합니다.
S3가 유일한 인터페이스입니다. FUSE mount는 S04에서 제거되었고 master와
filer에는 route가 없습니다.

## Structure

| Path | Role |
| --- | --- |
| `docker-compose.yml` | 4개 서비스, 데이터 디스크 bind volume, secret |
| `config/hyhome-seaweedfs.sh` | 시작 스크립트: secret으로 JWT, gRPC mTLS, S3 identity 설정을 구성함 |
| `config/s3-identities.conf` | bucket 범위의 소비자 identity(loki, tempo, mlflow, terrakube, lakehouse, prefix 한정 `opsflow-worker`)와 익명 CDN 읽기 |
| `config/seaweedfs-buckets.sh` | `seaweedfs-buckets` job: admin identity로 수행하는 idempotent bucket 생성 |
| `bin/gen-grpc-certs.sh` | 호스트 스크립트: SeaweedFS 전용 gRPC CA와 인증서를 발급함 |

상태는 `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}` 아래에 있으며 UID
1000이 소유합니다. Master, volume, filer는 `seaweed_internal`과 Prometheus만 함께 쓰는 metric 전용 `seaweedfs_metrics_net`(9324-9326)에 있습니다.
S3는 client용 `object_net`과 route용 `edge_net`에도 참여합니다. S3 메트릭 포트 `9327`은
Prometheus·Alloy만 함께 붙는 `seaweedfs_s3_metrics_net`에서 scrape하며, 이 망은 master·volume·filer API에
닿지 않습니다(SPEC-0266). 메트릭 listener는 `-metricsIp`로 이 망의 `10.250.41.2`에만 bind합니다(SPEC-0267).

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
`docs/05.operations/guides/05-databases-and-storage/0024-seaweedfs.md`와 POL-0021을 찾으십시오. 공식 소스:
[data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup),
[security](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration),
[license](https://github.com/seaweedfs/seaweedfs/blob/master/LICENSE).
