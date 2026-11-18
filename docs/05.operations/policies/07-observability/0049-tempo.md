---
title: "Tempo Operations Policy"
version: "1.3.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "operations"
artifact_id: "POL-0049"
parent_ids:
- "AD-0006"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Tempo Operations Policy

## Purpose and Scope

### Objective

이 정책은 Tempo distributed tracing backend의 trace ingestion, SeaweedFS S3
storage, block retention, metrics generator, secret boundary, protected route를
정의한다. 사용 흐름은 Tempo guide가, 장애 대응 절차는 Tempo runbook이
담당한다.

#### Authority

- Declared parent: [Observability Architecture Description](../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

### Applies To

이 정책은 current `infra/06-observability/tempo` compose와
`config/tempo.yaml`에 선언된 Tempo 운영 기준을 다룬다.

- **Systems**: compose service `tempo`, container `tempo`, image [hy/tempo image declaration](../../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/tempo/config/tempo.yaml`, volume `tempo-data`, SeaweedFS bucket `tempo-bucket`
- **Environments**: 로컬·개발·홈랩 운영

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0049-R1 | 항상 | 필수: `template-stateful-high`, `hy/tempo` image 선언, user `10001:10001`, read-only config mount, persistent `tempo-data` volume 유지 | none | none |
| POL-0049-R2 | 항상 | 필수: custom Tempo image는 upstream, non-root user `10001:10001`, `/docker-entrypoint.sh` secret guard 유지 | none | none |
| POL-0049-R3 | 항상 | 필수: OTLP receiver는 internal gRPC `4317`/HTTP `4318` endpoint 유지 | none | none |
| POL-0049-R4 | 항상 | 필수: HTTP/query/health surface는 `${TEMPO_PORT:-3200}`와 `/ready` healthcheck 기준 | none | none |
| POL-0049-R5 | 항상 | 필수: trace storage는 SeaweedFS S3 backend, bucket `tempo-bucket`, endpoint `seaweedfs-s3:8333`, `insecure: true` 사용 | none | none |
| POL-0049-R6 | 항상 | 필수: `S3_ACCESS_KEY`는 environment reference로, `S3_SECRET_KEY`는 Docker Secret `seaweedfs_s3_tempo_secret_key`로만 주입 | none | none |
| POL-0049-R7 | 항상 | 필수: block retention 값은 [POL-0048](0048-telemetry-retention.md) 기준 | none | none |
| POL-0049-R8 | 항상 | 필수: metrics generator는 `span-metrics`/`service-graphs` processors와 Prometheus `http://prometheus:9090/api/v1/write` remote_write 유지 | none | none |
| POL-0049-R9 | 항상 | 필수: Tempo 3 TraceQL metrics를 이전 `local_blocks` processor 요구와 구분 | none | none |
| POL-0049-R10 | 항상 | 금지: 검색/Drilldown capability를 processor 이름만으로 검증 | none | none |
| POL-0049-R11 | 항상 | 필수: route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` middleware chain 유지 | none | none |
| POL-0049-R12 | Development/debug 상황의 sampling 또는 log-level 변경 | 허용: plan/task evidence와 rollback note가 있을 때만 변경 | 수동 | plan/task evidence / rollback note |
| POL-0049-R13 | 장기 분석이 필요할 때 | 필수: retention policy와 SeaweedFS owning policy/runbook을 함께 갱신 | none | none |
| POL-0049-R14 | 항상 | 금지: PII/password/token/credential 값을 trace attributes에 기록 | none | none |
| POL-0049-R15 | 항상 | 금지: secret guard 없이 SeaweedFS-backed Tempo image나 entrypoint 변경 | none | none |
| POL-0049-R16 | 항상 | 금지: 승인 없이 bucket/retention/metrics generator processors/remote_write endpoint/route middleware/image version을 runtime에서 변경 | 수동 | none |
| POL-0049-R17 | 항상 | 필수: Tempo를 HOME으로 유지 | none | none |
| POL-0049-R18 | `tracing`을 빼는 대상으로 전환할 때 | 필수: Tempo를 명시적으로 중지 | none | none |
| POL-0049-R19 | 항상 | 필수: `tempo-bucket`/local WAL/temp state/config/대응 SeaweedFS credential을 하나의 조율된 recovery set으로 취급 | none | none |
| POL-0049-R20 | bucket backup/restore 시 | 필수: object-store owner가 수행 | none | none |
| POL-0049-R21 | consistency 캡처 전 | 필수: OTLP ingestion 중지 | none | none |
| POL-0049-R22 | 항상 | 필수: isolated bucket/path로 rehearse하고 WAL replay/historical·new trace query/metrics-generator 동작/Alloy·Grafana integration 검증 | none | none |
| POL-0049-R23 | 제거 시 | 필수: producer/exporter migration, retention 결정, credential/route 정리, object나 local data 삭제 전 명시적 승인 | 수동 | none |
| POL-0049-R24 | 항상 | 금지: Bucket/receiver에 일치한 `rg`를 retention 검증으로 간주 | none | none |
| POL-0049-R25 | retention 설정 누락 시 | 필수: 별도로 확인하고 누락을 통제 실패로 기록 | 수동 | none |
| POL-0049-R26 | 항상 | 필수: 버전에 맞는 별도 구현 수정으로 retention 결함 해소 | none | none |
| POL-0049-R27 | 항상 | 금지: Tempo 3 설정에 Tempo 2의 `compactor` 블록 복사 | none | none |
| POL-0049-R28 | 항상 | 필수: Traefik hostname에는 TLS/SSO middleware 유지 | none | none |
| POL-0049-R29 | Tempo HTTP `3200` LAN 게시 예외 | 필수: 예외는 지정 cluster 통합 목적과 설정된 LAN 인터페이스로 한정 | 수동 | none |
| POL-0049-R30 | Tempo HTTP `3200` LAN 게시 예외 | 필수: 사람은 보호된 hostname을, 기계 검증은 GDE-0096을 따름 | none | none |
| POL-0049-R31 | Tempo HTTP `3200` LAN 게시 예외 | 필수: 실제 log/trace payload 대신 상태와 시험 ID만 기록 | none | 상태와 시험 ID |
| POL-0049-R32 | 재바인딩/제거/인증·TLS 추가/노출 확대 시 | 필수: 통합 소유자와 조정한 별도 승인 변경으로 수행 | 수동 | none |
| POL-0049-R33 | 분산 모드 전환/외부 gRPC 소비자 추가/인증 도입 시 | 필수: gRPC `9095` listener 노출 수용(2026-11-12)을 다시 검토 | 수동 | none |

- **Required**:
  - Tempo service는 `template-stateful-high`, image
    [hy/tempo image declaration](../../../../infra/06-observability/docker-compose.yml), user `10001:10001`, read-only config mount,
    persistent `tempo-data` volume을 유지한다.
  - Custom Tempo image는 upstream [grafana/tempo image declaration](../../../../infra/06-observability/tempo/Dockerfile), non-root user
    `10001:10001`, `/docker-entrypoint.sh` secret guard를 유지한다.
  - OTLP receiver는 internal gRPC `4317`과 HTTP `4318` endpoint를 유지한다.
  - HTTP/query/health surface는 `${TEMPO_PORT:-3200}`와 `/ready` healthcheck를
    기준으로 한다.
  - Trace storage는 SeaweedFS S3 backend, bucket `tempo-bucket`, endpoint
    `seaweedfs-s3:8333`, `insecure: true`를 사용한다.
  - `S3_ACCESS_KEY`는 environment reference로, `S3_SECRET_KEY`는
    Docker Secret `seaweedfs_s3_tempo_secret_key`로만 주입한다.
  - Block retention 값은 [POL-0048](0048-telemetry-retention.md)을 기준으로 한다.
  - Metrics generator는 현재 `span-metrics`, `service-graphs` processors와
    Prometheus `http://prometheus:9090/api/v1/write` remote_write를 유지한다.
    Tempo 3 TraceQL metrics는 이전 `local_blocks` processor 요구와 구분한다.
    검색/Drilldown capability를 processor 이름만으로 검증하지 않는다.
  - Tempo route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
- **Allowed**:
  - Development/debug 상황의 sampling 또는 log-level 변경은 plan/task
    evidence와 rollback note가 있을 때만 허용한다.
  - 장기 분석이 필요하면 retention policy와 SeaweedFS owning policy/runbook을
    함께 갱신한다.
- **Disallowed**:
  - PII, password, token, credential 값을 trace attributes에 기록하는 행위
  - Secret guard 없이 SeaweedFS-backed Tempo image나 entrypoint를 변경하는 행위
  - 승인 없이 bucket, retention, metrics generator processors, remote_write
    endpoint, route middleware, image version을 runtime에서 변경하는 행위

#### Lifecycle and data controls

- Tempo는 `HOME`이다. SPEC-0182 W6에서 소유자가 `tracing`을 HOME에 추가했다(POL-0078). `tracing`을 빼는 대상으로 전환할 때는 `HOME up`이 이미 실행 중인 컨테이너를 제거하지 않으므로 Tempo를 명시적으로 중지한다.
- `tempo-bucket`, local WAL/temp state, config, 대응하는 SeaweedFS credential을 하나의 조율된 recovery set으로 취급한다; object-store owner가 bucket backup/restore를 수행한다.
- consistency 캡처 전에 OTLP ingestion을 멈춘다. isolated bucket/path로 rehearse하고 WAL replay, historical/new trace query, metrics-generator 동작, Alloy/Grafana integration을 검증한다.
- Removal은 producer/exporter migration, retention 결정, credential/route 정리, object나 local data를 삭제하기 전 명시적 승인이 필요하다.

#### Retention enforcement gap

[POL-0048](0048-telemetry-retention.md)은 block 24h, compacted block 1h를 요구하지만 현재 설정에는 둘 다 없다. 선언된 Tempo 기본값은 336h/1h이므로 24h 준수가 입증되지 않는다. Bucket/receiver에 일치한 `rg`를 retention 검증으로 간주하지 않는다. 별도로 확인하고 누락은 통제 실패로 기록한다. 버전에 맞는 별도 구현 수정이 필요하다. Tempo 3은 backend scheduler/worker compaction 설정을 사용하므로 Tempo 2의 `compactor` 블록을 복사하지 않는다. 소스 검증은 실제 삭제나 trace 복원 증거가 아니다.

#### Approved LAN integration boundary

Traefik hostname에는 TLS/SSO middleware를 유지한다. 별도로 [POL-0096](../10-platform-and-backup/0096-k8s-integration.md#rules)의 기존 k3d 예외에 따라 Tempo HTTP `3200`을 `HOST_LAN_BIND_IP`(공개 기본값 `192.168.0.13`)에 gateway 인증·서비스 TLS 없이 게시한다. 완료된 SPEC-0188 Task의 2026-09-29 owner 승인에 따른 것으로 W5가 만든 예외가 아니다. Loki `auth_enabled: false`는 사용자 인증이 아니며 Tempo에도 native 인증 계층이 없다. Gateway middleware는 직접 포트를 보호하지 않는다.

예외는 지정 cluster 통합 목적과 설정된 LAN 인터페이스로 한정한다. 소스에는 k3d만 식별하는 인증이 없으며 비공개 override, bind 성공, routing/firewall과 실제 도달성은 관찰하지 않았다. 사람은 보호된 hostname을, 기계 검증은 [GDE-0096](../../guides/10-platform-and-backup/0096-k8s-integration.md)을 따른다. 실제 log/trace payload 대신 상태와 시험 ID만 남긴다. 재바인딩·제거·인증/TLS 추가·노출 확대는 통합 소유자와 조정한 별도 승인 변경이다.

#### Internal gRPC listener

Tempo gRPC `9095`은 listen address를 지정하지 않아 모든 인터페이스에 인증 없이 bind하며 `tempo_ingress_net`, `obs_net`, `object_net`의 peer가 접근할 수 있다. 단일 바이너리 구성에서 이 포트는 Tempo 자신의 내부 호출에만 쓰이고 선언된 외부 소비자는 없다. 같은 서비스의 HTTP 포트도 인증이 없으므로 노출 수준이 같다. owner가 2026-11-12 이 노출을 수용했다. 이 listener는 REQ-0023-FR-0004가 다루는 metrics·관리·profiling·broker listener가 아니다. 분산 모드 전환, 외부 gRPC 소비자 추가, 인증 도입 때 다시 검토한다.

### Exceptions

#### Exception Conditions

- Retention, bucket, sampling, remote_write, route, secret reference 예외는
  사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Tempo runbook에서 최소 조치와 rollback
  evidence를 기록한다.

#### Approval and Review

- Tempo image, config, retention, SeaweedFS bucket, metrics generator,
  remote_write, route, secret reference, OTLP receiver가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Enforcement

### Mechanisms

- Compose service boundary:
  `rg -n 'service: template-stateful-high|image: hy/tempo:|user: .10001:10001.|tempo-data|TEMPO_PORT|seaweedfs_s3_tempo_secret_key|tempo.middlewares' infra/06-observability/docker-compose.yml`
- Tempo config:
  `rg -n 'metrics_generator:|remote_write:|url: http://prometheus:9090/api/v1/write|bucket: tempo-bucket|endpoint: seaweedfs-s3:8333|secret_key: \$\{S3_SECRET_KEY\}' infra/06-observability/tempo/config/tempo.yaml`
- Custom image secret guard:
  `rg -n 'FROM grafana/tempo:|USER 10001:10001|S3_SECRET_KEY_FILE is not set|missing secret:' infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
- Repository contracts:
  원격 PR public `changed` 검사 ([quality policy](../../../00.workspace/03.quality/quality-standards.md#canonical-delivery-phase-matrix))

### Limits

정책 본문이 이름 붙인 검사로 강제하는 규칙은 일부이며 아래 항목은 기계적으로 강제되지 않는다.

- 서비스/설정 경계: `POL-0049-R1`, `POL-0049-R2`, `POL-0049-R3`, `POL-0049-R4`, `POL-0049-R5`, `POL-0049-R8`, `POL-0049-R9`, `POL-0049-R10`, `POL-0049-R11`는 이름 붙은 검사가 지정되지 않았다.
- secret: `POL-0049-R6`는 이름 붙은 검사가 지정되지 않았다.
- retention: `POL-0049-R7`, `POL-0049-R24`, `POL-0049-R26`, `POL-0049-R27`는 이름 붙은 검사가 지정되지 않았다.
- 변경 절차: `POL-0049-R12`는 승인/검토 등 수동 절차에 의존한다.
- 변경 절차: `POL-0049-R13`는 이름 붙은 검사가 지정되지 않았다.
- 금지 행위: `POL-0049-R14`, `POL-0049-R15`는 이름 붙은 검사가 지정되지 않았다.
- 금지 행위: `POL-0049-R16`는 승인/검토 등 수동 절차에 의존한다.
- 수명주기/데이터: `POL-0049-R17`, `POL-0049-R18`, `POL-0049-R19`, `POL-0049-R20`, `POL-0049-R21`, `POL-0049-R22`는 이름 붙은 검사가 지정되지 않았다.
- 수명주기/데이터: `POL-0049-R23`는 승인/검토 등 수동 절차에 의존한다.
- retention: `POL-0049-R25`는 승인/검토 등 수동 절차에 의존한다.
- LAN 통합 예외: `POL-0049-R28`, `POL-0049-R30`, `POL-0049-R31`는 이름 붙은 검사가 지정되지 않았다.
- LAN 통합 예외: `POL-0049-R29`, `POL-0049-R32`는 승인/검토 등 수동 절차에 의존한다.
- gRPC 노출: `POL-0049-R33`는 승인/검토 등 수동 절차에 의존한다.
- 설정에 24h 블록 보존이 없고 선언 기본값은 336h/1h라 retention 준수는 입증되지 않으며 소스 검증은 실제 삭제나 trace 복원 증거가 아니다.
- `3200` LAN 게시는 gateway 인증과 서비스 TLS가 없고 비공개 override, bind 성공, routing/firewall과 실제 도달성은 관찰되지 않았다. gRPC `9095`는 인증 없이 모든 인터페이스에 bind하며 owner 수용에 의존한다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Triggers

- Subject peers: [Guide](../../guides/07-observability/0049-tempo.md) (`GDE-0049`), [Runbook](../../runbooks/07-observability/0049-tempo.md) (`RUN-0049`)

- [Operations index](../../README.md)
- [Usage guide](../../guides/07-observability/0049-tempo.md)
- [Recovery runbook](../../runbooks/07-observability/0049-tempo.md)
