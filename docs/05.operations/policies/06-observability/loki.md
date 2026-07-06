---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/loki.md -->

# Loki Operations Policy

## Overview

이 정책은 Loki log aggregation service의 retention, MinIO storage,
cardinality, compactor, resource, secret boundary를 정의한다. 사용 흐름은
Loki guide가, 장애 대응 절차는 Loki runbook이 담당한다.

## Policy Scope

이 정책은 current `infra/06-observability/loki` compose와 config에 선언된
Loki 운영 기준을 다룬다.

- **Systems**: compose service `loki`, container `infra-loki`, image `hy/loki:3.7.3-custom`, MinIO bucket `loki-bucket`, config `infra/06-observability/loki/config/loki-config.yaml`
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Loki storage는 MinIO S3 backend와 `loki-bucket`을 사용한다.
  - Retention은 `retention_enabled: true`와 `retention_period: 168h`를
    기준으로 한다.
  - Compactor는 `compaction_interval: 10m`,
    `retention_delete_delay: 2h`, `retention_delete_worker_count: 15`
    설정을 따른다.
  - `minio_app_user_password`는 Docker Secret으로만 주입한다.
  - Service는 `template-stateful-high` 기준의 restart, security, resource
    cap(`cpus: "2.00"`, `mem_limit: 2g`)을 유지한다.
  - Loki route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
  - Label은 `service_name`, `env`, `stream`처럼 낮은 cardinality 값으로
    제한하고, user ID, IP address, request ID 같은 high-cardinality 동적
    값을 label로 승격하지 않는다.
- **Allowed**:
  - Dynamic log fields는 LogQL parser(`| json` 등)로 query time에 추출한다.
  - Long-term audit 보관이 필요하면 MinIO owning policy/runbook과 별도
    Stage 04 task evidence로 snapshot 또는 replication을 검토한다.
- **Disallowed**:
  - Retention 변경 없이 문서만 수정해 보관 정책이 바뀐 것처럼 선언하는 행위
  - `MINIO_APP_USER_PASSWORD` 또는 secret 값을 문서, 로그, task evidence에
    기록하는 행위
  - 승인 없이 Loki route, retention, compactor, MinIO bucket, resource cap을
    runtime에서 변경하는 행위

## Exceptions

- Retention, label cardinality, MinIO storage, resource cap 예외는 사용자
  승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Loki runbook에서 최소 조치와 rollback
  evidence를 기록한다.

## Verification

- Loki config:
  `rg -n 'bucketnames: loki-bucket|retention_enabled: true|retention_period: 168h|compaction_interval: 10m' infra/06-observability/loki/config/loki-config.yaml`
- Compose service boundary:
  `rg -n 'service: template-stateful-high|image: hy/loki:3.7.3-custom|minio_app_user_password|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml`
- Repository contracts:
  `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- Loki image, config, MinIO bucket, compactor, retention, resource cap, route,
  or secret reference가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/loki.md)
- [Recovery runbook](../../runbooks/06-observability/loki.md)
- [Retention policy](./retention.md)
