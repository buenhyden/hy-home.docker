# 05-Messaging Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `05-messaging` 계층의 최적화/하드닝 운영 정책을 정의한다. 게이트웨이 경계 제어, 관리 경로 보호, 이미지 태그 통제, CI 기준선 검증, 카탈로그 확장 승인 조건을 필수 통제로 규정한다.

## Policy Scope

- `infra/05-messaging/kafka/docker-compose.yml`
- `infra/05-messaging/kafka/docker-compose.dev.yml`
- `infra/05-messaging/rabbitmq/docker-compose.yml`
- `scripts/hardening/check-all-hardening.sh 05-messaging`

## Applies To

- **Systems**: Kafka/Kafbat/Schema Registry/Kafka Connect/Kafka REST/RabbitMQ
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 외부 노출 라우터는 `gateway-standard-chain@file`를 적용해야 한다.
  - 관리 UI 라우터(`kafka-ui`, `kafbat-ui-dev`, `rabbitmq`)는 SSO 체인을 포함해야 한다.
  - Kafka UI 이미지는 고정 태그를 사용해야 하며 부동 태그를 금지한다.
  - 메시징 변경은 `messaging-hardening` CI 게이트를 통과해야 한다.
  - 문서(PRD~Procedure)는 optimization-hardening 링크를 유지해야 한다.
- **Allowed**:
  - `messaging-option` 프로필 기반 RabbitMQ 선택 활성화
  - 카탈로그 확장 항목의 단계적 도입(DLQ/재처리/quorum queue)
- **Disallowed**:
  - 무검증 라우터 middleware 변경
  - 부동 태그 이미지 도입
  - 카탈로그/정책 미연계 확장 실행

## Exceptions

- 긴급 장애 대응 시 일시적으로 middleware 완화가 필요할 수 있다.
- 단, 조치 후 동일 릴리스 내 원상 복구 및 검증 증적 확보가 필수다.

## Verification

- `bash scripts/hardening/check-all-hardening.sh 05-messaging`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`
- `docker compose -f infra/05-messaging/kafka/docker-compose.yml config`
- `docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config`

## Review Cadence

- 월 1회 정기 검토
- 메시징 컴포넌트 주요 버전 변경/보안 이슈 발생 시 수시 검토

## Catalog Expansion Approval Gates

- **Kafka 확장 승인 조건**:
  - 토픽 거버넌스(보존/compaction/파티션 기준) 문서화
  - DLQ + 재처리 파이프라인 표준 운영 절차 확보
- **RabbitMQ 확장 승인 조건**:
  - quorum queue 적용 범위 및 예외 명시
  - dead-letter/retry 정책 + 소비자 재시도 기준 합의
- **Gateway 연계 승인 조건**:
  - 보안 헤더/접근 정책 템플릿 적용 계획 수립
  - 운영 자동화 경로의 접근 제어 영향 평가 완료

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: `messaging-hardening` + 공통 기준선 통과 필수
- **Log / Trace Retention**: `06-observability` 정책 준수
- **Safety Incident Thresholds**: 장기 healthcheck fail, 관리경로 인증 실패 급증, 메시지 지연 급증 시 runbook 즉시 전환

## Related Documents

- **PRD**: [../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md](../../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md](../../../02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../03.specs/05-messaging/spec.md](../../../03.specs/05-messaging/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Usage**: [../../05.operations/05-messaging/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/05-messaging/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Usage

> Migrated from `docs/05.operations/05-messaging/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 05-Messaging Optimization Hardening Usage

#### Overview (KR)

이 문서는 `05-messaging` 계층의 최적화/하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. Kafka/RabbitMQ 관리 경로의 게이트웨이 제어, 이미지 태그 고정, 개발 구성 정합성, CI 검증 절차를 제공한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Messaging Operator
- DevOps Engineer
- Platform Developer

#### Purpose

- 메시징 관리 경로를 게이트웨이 표준 정책으로 정렬한다.
- 예측 불가능한 이미지/구성 회귀를 사전에 차단한다.
- 카탈로그 기반 확장(DLQ/재처리/quorum queue) 준비 상태를 확보한다.

#### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/05-messaging` 및 `scripts/` 수정 권한
- Traefik 미들웨어(`gateway-standard-chain`, `sso-*`) 구성 존재

#### Step-by-step Instructions

1. 구성 변경 전 정적 상태 점검
   - `docker compose -f infra/05-messaging/kafka/docker-compose.yml config`
   - `docker compose -f infra/05-messaging/kafka/docker-compose.dev.yml config`
   - `docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config`
2. Kafka 하드닝 적용
   - `kafbat-ui` 이미지를 고정 태그로 유지한다.
   - `schema-registry`, `kafka-connect`, `kafka-rest`, `kafka-ui` 라우터에 `gateway-standard-chain@file`를 적용한다.
   - `kafka-ui`는 `sso-errors@file,sso-auth@file`를 체인에 포함한다.
3. Kafka dev 정합성 적용
   - 볼륨 마운트 경로를 compose 파일 디렉터리 기준 상대 경로로 유지한다.
   - dev 라우터에도 동일 체인/SSO 정책을 적용한다.
4. RabbitMQ 하드닝 적용
   - `rabbitmq` 관리 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
   - `messaging-option` 프로필을 유지해 선택적 활성화 모델을 보존한다.
5. 검증 자동화 및 CI 반영
   - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
   - CI workflow에 `messaging-hardening` job 반영 여부 확인
6. 문서 추적성 동기화
   - PRD~Procedure optimization-hardening 문서 링크를 점검한다.

#### Common Pitfalls

- UI 라우터에 SSO를 누락해 관리 경로가 과노출되는 실수
- 부동 태그(`:main`)를 재도입해 예측 불가능한 런타임 회귀를 유발하는 실수
- dev compose 경로를 repo-root 기준으로 작성해 파일 마운트 실패를 유발하는 실수
- 하드닝 스크립트와 문서 링크를 함께 갱신하지 않는 실수

#### Related Documents

- **PRD**: [../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md](../../../01.requirements/2026-03-28-05-messaging-optimization-hardening.md)
- **Spec**: [../../03.specs/05-messaging/spec.md](../../../03.specs/05-messaging/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)
- **Operation**: [../../05.operations/05-messaging/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/05-messaging/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Procedure

> Migrated from `docs/05.operations/05-messaging/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 05-Messaging Optimization Hardening Procedure

: Messaging Gateway/Compose Baseline Recovery

#### Overview (KR)

이 런북은 05-messaging 하드닝 항목에서 발생할 수 있는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. 관리 경로 middleware/SSO 누락, 이미지 태그 회귀, dev 경로 오류, CI 하드닝 실패를 중심으로 점검/복구 절차를 정의한다.

#### Purpose

- 메시징 관리 경로의 보안/안정성 기준을 신속히 복구한다.
- compose 정합성과 CI 기준선 회귀를 빠르게 차단한다.

#### Canonical References

- [Spec](../../../03.specs/05-messaging/spec.md)
- [Operations Policy](./optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md)

#### When to Use

- `messaging-hardening` CI가 실패할 때
- Kafka/RabbitMQ 관리 UI가 Traefik 경유로 비정상 응답할 때
- Kafka dev compose가 경로/네트워크 오류로 기동 실패할 때
- 부동 태그 이미지 회귀가 발견될 때

#### Procedure or Checklist

##### Checklist

- [ ] 실패 항목(이미지/라우터/경로/문서 링크) 식별
- [ ] 최근 변경 커밋과 영향 범위 확인
- [ ] 운영 영향도(관리 경로/데이터 평면) 평가

##### Procedure

1. 정적 구성 점검
   - `docker compose -f infra/05-messaging/kafka/docker-compose.yml config`
   - `docker compose -f infra/05-messaging/kafka/docker-compose.dev.yml config`
   - `docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config`
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
3. 증상별 복구
   - middleware 누락:
     - 대상 라우터에 `gateway-standard-chain@file` 재적용
   - 관리 UI 접근 제어 누락:
     - `kafka-ui`, `kafbat-ui-dev`, `rabbitmq` 라우터에 `sso-errors@file,sso-auth@file` 재적용
   - 이미지 회귀:
     - `kafka-ui` 이미지를 고정 태그로 복원
   - dev 경로 오류:
     - `./jmx-exporter`, `./kafbat-ui/dynamic_config.yaml` 경로로 복원
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 05-messaging`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`

#### Verification Steps

- [ ] 3개 compose `config` 검증 통과
- [ ] `check-messaging-hardening` 실패 0건
- [ ] optimization-hardening 문서 링크와 README 인덱스 최신화 확인

#### Observability and Evidence Sources

- **Signals**: CI `messaging-hardening` job 상태, Traefik 라우터 상태, 컨테이너 health
- **Evidence to Capture**:
  - 변경 전후 `check-messaging-hardening.sh` 출력
  - `docker compose config` 결과
  - 관련 compose/docs diff

#### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/05-messaging/kafka/docker-compose.yml`
  - `infra/05-messaging/kafka/docker-compose.dev.yml`
  - `infra/05-messaging/rabbitmq/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 05-messaging`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 운영 정책/가이드/태스크 문서 링크 재확인

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: 메시징 관리 자동화 작업 일시 중지(승인 필요)
- **Eval Re-run**: `check-messaging-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Trace Capture**: CI logs + compose config output + health 상태 스냅샷

#### Related Operational Documents

- **Usage**: [../../05.operations/05-messaging/optimization-hardening.md](./optimization-hardening.md)
- **Operation**: [../../05.operations/05-messaging/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
