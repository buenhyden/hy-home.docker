---
title: "Pyroscope Operations Policy"
version: "1.5.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "operations"
artifact_id: "POL-0047"
parent_ids:
- "AD-0006"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Pyroscope Operations Policy

## Purpose and Scope

### Objective

이 정책은 Pyroscope continuous profiling service의 ingestion, filesystem
storage, capacity boundary, label/cardinality, route, health 기준을 정의한다.
사용 흐름은 Pyroscope guide가, 장애 대응 절차는 Pyroscope runbook이
담당한다.

#### Authority

- Declared parent: [Observability Architecture Description](../../../02.architecture/01.descriptions/0006-observability-architecture.md) (`AD-0006`)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

### Applies To

이 정책은 현재 `infra/06-observability/pyroscope` compose와
`config/pyroscope.yaml`에 선언된 Pyroscope 운영 기준을 다룬다.

- **Systems**: compose service `pyroscope`, container `pyroscope`, image [grafana/pyroscope image declaration](../../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/pyroscope/config/pyroscope.yaml`, volume `pyroscope-data`, `pyroscope-metastore`
- **Environments**: 로컬·개발·홈랩 운영

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0047-R1 | 항상 | 필수: `template-infra-med`, image 선언, read-only config mount, persistent `pyroscope-data` volume 유지 | none | none |
| POL-0047-R2 | 항상 | 필수: v2 metastore/raft state를 named volume `pyroscope-metastore`(`/data`)에 보관하고 mount 유지 | none | none |
| POL-0047-R3 | 항상 | 필수: runtime command `-config.file=/etc/pyroscope/pyroscope.yaml`/`-config.expand-env=true` 유지 | none | none |
| POL-0047-R4 | 항상 | 필수: HTTP/query/health는 `${PYROSCOPE_PORT:-4040}`와 `profilecli ready` healthcheck 기준 | none | none |
| POL-0047-R5 | 항상 | 필수: host port는 `127.0.0.1`에만 게시 | none | none |
| POL-0047-R6 | 항상 | 필수: storage backend는 local filesystem `storage.filesystem.dir: /var/lib/pyroscope` 사용 | none | none |
| POL-0047-R7 | 항상 | 필수: Compactor data directory `/var/lib/pyroscope/compactor` 유지 | none | none |
| POL-0047-R8 | 항상 | 필수: `reporting_enabled: false` 유지 | none | none |
| POL-0047-R9 | 항상 | 필수: `self_profiling.disable_push: true`와 `multitenancy_enabled: false` 유지 | none | none |
| POL-0047-R10 | 항상 | 필수: 입력 제한 `ingestion_rate_mb: 16`/`ingestion_burst_size_mb: 32`/`max_label_name_length: 1024`/`max_label_value_length: 2048`/`max_label_names_per_series: 30` 유지 | none | none |
| POL-0047-R11 | 항상 | 금지: profile label에 cardinality가 높은 값이나 secret이 포함된 값 사용 | 수동 | none |
| POL-0047-R12 | 항상 | 필수: route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` middleware chain 유지 | none | none |
| POL-0047-R13 | 항상 | 필수: `limits.retention_period: 168h`(7일) 유지 | none | none |
| POL-0047-R14 | 보관 기간 변경 시 | 필수: config/capacity 검증과 retention policy 갱신을 함께 수행 | 수동 | none |
| POL-0047-R15 | 항상 | 필수: Alloy `pyroscope.scrape`는 `scrape_interval = "60s"`와 block/mutex profile off 유지 | 수동 | none |
| POL-0047-R16 | Alloy scrape 간격을 줄이거나 profile type을 켤 때 | 필수: 용량 근거 확보 | 수동 | 용량 근거 |
| POL-0047-R17 | Development/debug 상황 | 허용: 임시 고빈도 profiling | none | none |
| POL-0047-R18 | 임시 고빈도 profiling 시 | 필수: CPU/storage 영향과 rollback note 기록 | none | rollback note |
| POL-0047-R19 | 새 profile source 또는 Alloy forwarding 변경 시 | 필수: Pyroscope/Grafana datasource 확인과 함께 검증 | none | none |
| POL-0047-R20 | 항상 | 금지: PII/password/token/credential 값을 profile labels 또는 profile payload에 기록 | 수동 | none |
| POL-0047-R21 | 항상 | 금지: request ID/user ID 같은 high-cardinality 값을 label로 승격 | 수동 | none |
| POL-0047-R22 | 항상 | 금지: 승인 없이 route/storage backend/ingestion limits/image version/persistent volume/config path를 runtime에서 변경 | 수동 | none |
| POL-0047-R23 | 운영 환경 | 금지: 근거 없이 high-overhead block/mutex profiling 상시 활성화 | 수동 | none |
| POL-0047-R24 | 항상 | 필수: Pyroscope를 HOME으로 유지 | none | none |
| POL-0047-R25 | `profiling`을 빼는 대상으로 전환할 때 | 필수: Pyroscope를 명시적으로 중지 | none | none |
| POL-0047-R26 | 항상 | 필수: Gateway 인증과 로컬 filesystem 경계 유지 | none | none |
| POL-0047-R27 | 항상 | 금지: profile source 없이 쓰기 대상만 설정한 것을 수집 증거로 취급 | none | none |
| POL-0047-R28 | 항상 | 필수: 백업은 쓰기·서비스를 중지하거나 일관성을 검증한 snapshot으로만 수행 | none | none |
| POL-0047-R29 | 항상 | 필수: 격리 스토리지에서 rehearsal을 수행하고 과거·신규 조회와 producer label 확인 | none | none |
| POL-0047-R30 | 제거 전 | 필수: producer·Grafana 참조 정리, 보존 여부 결정, 경로 폐쇄 | none | none |
| POL-0047-R31 | `pyroscope-data`/`pyroscope-metastore` 삭제 시 | 필수: 명시적 승인 | 수동 | none |
| POL-0047-R32 | 수신 확인 시 | 필수: 선택 파일·target과 제한된 profile query로 수신 확인 | none | none |
| POL-0047-R33 | 수신 확인 시 | 금지: writer/receiver readiness만으로 판정 | none | none |
| POL-0047-R34 | probe 사용 시 | 필수: 선언된 `profilecli ready` probe 사용(wget 존재를 가정하지 않음) | none | none |
| POL-0047-R35 | retention 기간 변경 시 | 필수: 별도 승인된 설정·용량 검토 | 수동 | none |
| POL-0047-R36 | 항상 | 필수: Profile/config를 일관되게 보존하고 삭제는 POL-0048을 따름 | none | none |

- **Required**:
  - Pyroscope service는 `template-infra-med`, image
    [grafana/pyroscope image declaration](../../../../infra/06-observability/docker-compose.yml), read-only config mount, persistent
    `pyroscope-data` volume을 유지한다.
  - v2 metastore와 raft state는 named volume `pyroscope-metastore`가 `/data`에
    보관한다(`${DEFAULT_OBSERVABILITY_DIR}/pyroscope-metastore`). 컨테이너를
    재생성해도 index가 고아가 되지 않도록 이 mount를 유지한다.
  - Runtime command는 `-config.file=/etc/pyroscope/pyroscope.yaml`와
    `-config.expand-env=true`를 유지한다.
  - HTTP/query/health surface는 `${PYROSCOPE_PORT:-4040}`와 `profilecli ready`
    healthcheck를 기준으로 하며, host port는 `127.0.0.1`에만 게시한다.
  - Storage backend는 local filesystem backend
    `storage.filesystem.dir: /var/lib/pyroscope`를 사용한다.
  - Compactor data directory는 `/var/lib/pyroscope/compactor`를 유지한다.
  - Analytics reporting은 `reporting_enabled: false`를 유지한다.
  - `self_profiling.disable_push: true`와 `multitenancy_enabled: false`를
    유지한다.
  - 입력 제한은 `ingestion_rate_mb: 16`, `ingestion_burst_size_mb: 32`, `max_label_name_length: 1024`, `max_label_value_length: 2048`, `max_label_names_per_series: 30`을 유지한다.
  - Profile label에 cardinality가 높은 값이나 secret이 포함된 값을 쓰지 않는다.
  - Pyroscope route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
  - `limits.retention_period: 168h`(7일)를 유지한다. 개인 PC HDD에서 하루 약
    0.12 GB(30초 scrape 기준)가 쌓이므로 기본값 31일은 필요 이상으로 길다. 보관
    기간 변경은 config/capacity 검증과 [retention policy](0048-telemetry-retention.md)
    갱신을 함께 요구한다.
  - Alloy `pyroscope.scrape`는 `scrape_interval = "60s"`와 block/mutex profile
    off를 유지한다. 간격을 줄이거나 profile type을 켜는 변경은 용량 근거가 필요하다.
- **Allowed**:
  - Development/debug 상황에서 임시 고빈도 profiling을 사용할 수 있으나,
    CPU/storage 영향과 rollback note를 남긴다.
  - 새 profile source 또는 Alloy forwarding 변경은 Pyroscope/Grafana
    datasource 확인과 함께 검증한다.
- **Disallowed**:
  - PII, password, token, credential 값을 profile labels 또는 profile payload에
    기록하는 행위
  - Request ID, user ID 같은 high-cardinality 값을 label로 승격하는 행위
  - 승인 없이 route, storage backend, ingestion limits, image version,
    persistent volume, config path를 runtime에서 변경하는 행위
  - 운영 환경에서 근거 없이 high-overhead block/mutex profiling을 상시 활성화하는 행위

#### Lifecycle and data controls

- Pyroscope는 `HOME`이다. SPEC-0182 W6에서 소유자가 `profiling`을 HOME에 추가했다(POL-0078). `profiling`을 빼는 대상으로 전환할 때는 `HOME up`이 이미 실행 중인 컨테이너를 제거하지 않으므로 Pyroscope를 명시적으로 중지한다.
- Gateway 인증과 로컬 filesystem 경계를 유지한다. Profile source 없이 쓰기 대상만 설정한 것은 수집 증거가 아니다.
- 쓰기·서비스를 중지하거나 일관성을 검증한 snapshot으로만 백업한다. 격리 스토리지에서 rehearsal을 수행하며 과거·신규 조회와 producer label을 확인한다.
- 제거 전 producer·Grafana 참조를 정리하고 보존 여부를 결정하며 경로를 닫는다. `pyroscope-data`와 `pyroscope-metastore` 삭제에는 명시적 승인이 필요하다.

#### Profile storage and source limits

두 Alloy 설정에는 Go(11개 대상)와 별도 SeaweedFS pprof source가 있다. 선택 파일·target과 제한된 profile query로 수신을 확인하며 writer/receiver readiness만으로 판정하지 않는다. Pyroscope는 선언 volume의 로컬 filesystem과 ingestion/cardinality 한도를 사용한다. retention은 `limits.retention_period: 168h`로 고정하며 삭제는 block 단위·유예 이후다. 기간 변경은 별도 승인된 설정·용량 검토가 필요하다. wget 존재를 가정하지 않고 선언된 `profilecli ready` probe를 쓴다. Profile/config를 일관되게 보존하고 삭제는 POL-0048을 따른다.

### Exceptions

#### Exception Conditions

- Retention, storage backend, ingestion limits, profile source, route 예외는
  사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Pyroscope runbook에서 최소 조치와
  rollback evidence를 기록한다.

#### Approval and Review

- Pyroscope image, config, storage backend, ingestion limits, profile source,
  route, healthcheck, retention/capacity policy가 변경될 때 검토한다.
- 정기 검토는 분기마다 수행한다.

## Enforcement

### Mechanisms

- Compose service boundary:
  `rg -n 'service: template-infra-med|image: grafana/pyroscope:|pyroscope-data|PYROSCOPE_PORT|/ready|pyroscope.middlewares' infra/06-observability/docker-compose.yml`
- Pyroscope config:
  `rg -n 'http_listen_port: 4040|reporting_enabled: false|data_dir: /var/lib/pyroscope/compactor|ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|multitenancy_enabled: false|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml`
- Repository contracts:
  원격 PR public `changed` 검사 ([quality policy](../../../00.workspace/04.quality/quality-standards.md#canonical-delivery-phase-matrix))

### Limits

정책 본문이 이름 붙인 검사로 강제하는 규칙은 일부이며 아래 항목은 기계적으로 강제되지 않는다.

- 서비스/설정 경계: `POL-0047-R1`, `POL-0047-R2`, `POL-0047-R3`, `POL-0047-R4`, `POL-0047-R5`, `POL-0047-R6`, `POL-0047-R7`, `POL-0047-R8`, `POL-0047-R9`, `POL-0047-R10`, `POL-0047-R12`는 이름 붙은 검사가 지정되지 않았다.
- 금지 행위: `POL-0047-R11`, `POL-0047-R20`, `POL-0047-R21`, `POL-0047-R22`, `POL-0047-R23`는 승인/검토 등 수동 절차에 의존한다.
- retention/capacity: `POL-0047-R13`, `POL-0047-R36`는 이름 붙은 검사가 지정되지 않았다.
- retention/capacity: `POL-0047-R14`, `POL-0047-R15`, `POL-0047-R16`, `POL-0047-R35`는 승인/검토 등 수동 절차에 의존한다.
- 변경 절차: `POL-0047-R17`, `POL-0047-R18`, `POL-0047-R19`는 이름 붙은 검사가 지정되지 않았다.
- 수명주기/데이터: `POL-0047-R24`, `POL-0047-R25`, `POL-0047-R26`, `POL-0047-R28`, `POL-0047-R29`, `POL-0047-R30`는 이름 붙은 검사가 지정되지 않았다.
- 수신 판정: `POL-0047-R27`, `POL-0047-R32`, `POL-0047-R33`, `POL-0047-R34`는 이름 붙은 검사가 지정되지 않았다.
- 수명주기/데이터: `POL-0047-R31`는 승인/검토 등 수동 절차에 의존한다.
- 정책은 config 점검이 일부 key만 확인하며 `-config.expand-env`, `pyroscope-metastore` mount, retention 168h, label 길이 한도는 이름 붙은 점검에 없다고 명시한다.
- writer/receiver readiness만으로는 수집을 증명하지 못하며 백업과 rehearsal은 runbook 절차에 의존한다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Triggers

- Subject peers: [Guide](../../01.guides/07.observability/0047-pyroscope.md) (`GDE-0047`), [Runbook](../../03.runbooks/07.observability/0047-pyroscope.md) (`RUN-0047`)

- [Operations index](../../README.md)
- [Usage guide](../../01.guides/07.observability/0047-pyroscope.md)
- [Recovery runbook](../../03.runbooks/07.observability/0047-pyroscope.md)
- [Retention policy](0048-telemetry-retention.md)
- 이 문서는 SPEC-0267 secondary-listener hardening 결과를 담고 있다. 해당 패키지는 retire되었고 본문은 version history에 있다.
