---
title: "SeaweedFS"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2025-12-06"
---

# SeaweedFS

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

이 패키지는 HOME S3 오브젝트 스토어인 SeaweedFS를 정의합니다. SPEC-0180 S07에서
MinIO를 대체했습니다.

###### Audience
<!-- core-payload-level:4 -->

오브젝트 저장소의 operator와 maintainer를 대상으로 합니다.

###### Scope
<!-- core-payload-level:4 -->

[`docker-compose.yml`](docker-compose.yml)이 `seaweedfs-master`,
`seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`를 정의합니다. `seaweedfs`,
`storage-seaweedfs` profile과 모든 S3 소비자 profile(`storage`, `obs`, `logs`,
`tracing`, `mlops`, `data-science`, `lakehouse`)이 `seaweedfs-buckets`와
함께 이들을 선택합니다. Iceberg table bucket job은 SPEC-0262에서
[lakehouse LAB](../../../labs/lakehouse/docker-compose.yml)으로 옮겼고, root `lakehouse`는 SeaweedFS만 선택합니다.
S3가 유일한 인터페이스입니다. FUSE mount는 S04에서 제거되었고 master와
filer에는 route가 없습니다.

###### Structure
<!-- core-payload-level:4 -->

| Path | Role |
| --- | --- |
| `docker-compose.yml` | 4개 서비스, 데이터 디스크 bind volume, secret |
| `config/hyhome-seaweedfs.sh` | 시작 스크립트: secret으로 JWT, gRPC mTLS, S3 identity 설정을 구성함 |
| `config/s3-identities.conf` | bucket 범위의 소비자 identity(loki, tempo, mlflow, terrakube, lakehouse, prefix 한정 `opsflow-worker`) |
| `config/seaweedfs-buckets.sh` | `seaweedfs-buckets` job: admin identity로 수행하는 idempotent bucket 생성 |
| `bin/gen-grpc-certs.sh` | 호스트 스크립트: SeaweedFS 전용 gRPC CA와 인증서를 발급함 |

상태는 `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}` 아래에 있으며 UID
1000이 소유합니다. Master, volume, filer는 `seaweed_internal`과 Prometheus만 함께 쓰는 metric 전용 `seaweedfs_metrics_net`(9324-9326)에 있습니다.
S3는 client용 `object_net`과 route용 `edge_net`에도 참여합니다. S3 메트릭 포트 `9327`은
Prometheus·Alloy만 함께 붙는 `seaweedfs_s3_metrics_net`에서 scrape하며, 이 망은 master·volume·filer API에
닿지 않습니다(SPEC-0266). 메트릭 listener는 `-metricsIp`로 이 망의 `10.250.41.2`에만 bind합니다(SPEC-0267).

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `seaweedfs-s3` S3 API (`object_net`, `edge_net`) | `seaweedfs-s3` | bucket 범위 identity 소비자 loki, tempo, mlflow, terrakube, lakehouse, prefix 한정 `opsflow-worker` | S3만 제공하며 소비자별 bucket identity를 쓰고 호스트 게시 포트는 없다. | 최초 활성화·백업·복구는 RUN-0024를 따른다. |
| S3 메트릭 포트 `9327` (`seaweedfs_s3_metrics_net`) | `seaweedfs-s3` | Prometheus·Alloy | `-metricsIp`로 `10.250.41.2`에만 bind하며 master·volume·filer API에 닿지 않는다. | 이 README는 실패 처리를 기록하지 않는다. |
| master·volume·filer 메트릭 `9324-9326` (`seaweedfs_metrics_net`) | `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer` | Prometheus | `seaweed_internal`과 Prometheus만 함께 쓰는 metric 전용 망에서 노출한다. | 이 README는 실패 처리를 기록하지 않는다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

호스트로 게시하는 포트 선언이 없다. 연결 네트워크는 `edge_net`, `object_net`, `seaweed_internal`, `seaweedfs_metrics_net`, `seaweedfs_s3_metrics_net`이다. (출처: `infra/04-data/seaweedfs/docker-compose.yml`의 `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` 서비스)

###### Security Boundary
<!-- core-payload-level:4 -->

Compose가 참조하는 secret은 `seaweedfs_jwt_filer_key`, `seaweedfs_jwt_volume_key`, `seaweedfs_s3_admin_secret_key`, `seaweedfs_s3_lakehouse_secret_key`, `seaweedfs_s3_loki_secret_key`, `seaweedfs_s3_mlflow_secret_key`, `seaweedfs_s3_opsflow_worker_secret_key`, `seaweedfs_s3_tempo_secret_key`, `seaweedfs_s3_terrakube_secret_key`이며 값은 저장소에 두지 않는다. 호스트로 게시하는 포트 선언은 없다. (출처: `infra/04-data/seaweedfs/docker-compose.yml`의 `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` 서비스)

#### Usage

##### Prerequisites

런타임은 `infra/04-data/seaweedfs/docker-compose.yml`의 `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-buckets` 서비스로 정의되며, 이미지와 태그는 해당 Compose 선언이 소유한다. 활성화 프로파일은 `data-science`, `lakehouse`, `logs`, `mlops`, `obs`, `seaweedfs`, `storage`, `storage-seaweedfs`, `tracing`이다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest \
  tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests
```

#### Checks

##### Readiness

루트에서 `HYHOME_COMPOSE_PROFILES`를 지정해 `scripts/validation/validate-docker-compose.sh`로 구성을 검증한다. 개별 leaf Compose는 루트 network와 secret 선언에 의존하므로 leaf 단독으로 검증하지 않는다(`infra/README.md` 참조).

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

이 서비스의 런북은 다음과 같다.

- RUN-0024: `docs/05.operations/03.runbooks/05.databases-and-storage/0024-seaweedfs.md`

###### Related Documents
<!-- core-payload-level:4 -->

[문서 진입점](../../../docs/README.md)에서 Stage 05 subject
`docs/05.operations/01.guides/05.databases-and-storage/0024-seaweedfs.md`와 POL-0021을 찾으십시오. 공식 소스:
[data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup),
[security](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration),
[license](https://github.com/seaweedfs/seaweedfs/blob/master/LICENSE).

###### Observability and Recovery
<!-- core-payload-level:4 -->

최초 활성화, 백업, 복구는 RUN-0024를 따릅니다. 일일 백업은 filer metadata와
volume/master 트리를 순서 있는 한 세트로 담습니다(RUN-0021).

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
