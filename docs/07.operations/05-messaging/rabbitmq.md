# RabbitMQ Operations Policy

: Operational standards for RabbitMQ message broker.

---

## Overview (KR)

이 문서는 RabbitMQ 서비스의 안정적인 운영을 위한 정책을 정의한다. 보안 관리, 리소스 할당, 백업 전략 및 성능 모니터링 기준을 수립하여 시스템의 신뢰성을 보장한다.

## Policy Info

- **Owner**: SRE Team
- **Status**: `Active`
- **Last Updated**: 2026-03-26

## Core Policies

### 1. Security & Access Control

- **Credential Management**: 모든 접속 계정은 `scripts/gen-secrets.sh`를 통해 관리되어야 하며, `rabbitmq_user` 및 `rabbitmq_password` 시크릿 파일을 사용해 환경 변수로 주입한다.
- **TLS Configuration**: 외부 노출되는 Management UI는 Traefik을 통해 HTTPS로 강제 전환된다.
- **Permission**: 애플리케이션 계정은 원칙적으로 필요한 VHost와 Queue에 대해서만 권한을 부여하는 최소 권한 원칙을 준수한다.

### 2. Resource Management

- **Memory Watermark**: 기본 메모리 임계치는 가용 메모리의 40%로 설정되어 있으며, 이를 초과할 경우 모든 퍼블리셔의 메시지 전송이 일시 중단된다.
- **Disk Space**: 디스크 여유 공간이 50MB(기본값) 이하로 떨어지면 서비스가 중단될 수 있으므로, 상시 2GB 이상의 여유 공간 확보를 권장한다.

### 3. Queue Management

- **Max Length**: 메시지 폭주를 방지하기 위해 중요도가 낮은 큐에는 `x-max-length` 설정을 적용하여 무한 성장을 방지한다.
- **TTL**: 불필요한 메시지 체류를 방지하기 위해 큐 레벨 또는 메시지 레벨 TTL 설정을 권장한다.

### 4. Backup & Persistence Strategies

- **Volume Persistence**: `rabbitmq-data-volume`은 호스트의 `${DEFAULT_MESSAGE_BROKER_DIR}/rabbitmq`에 마운트되어 데이터 지속성을 보장한다.
- **Definition Export**: RabbitMQ 관리자 UI 또는 API를 통해 주기적으로 브로커 정의(Definitions - Users, VHosts, Queues, Exchanges)를 백업해야 한다.

## Monitoring Standards

- **Metrics**: Grafana를 통해 다음 지표를 상시 모니터링한다.
  - Number of Connections / Channels
  - Queue Length & Unacknowledged Messages
  - Erlang Process Count
  - Memory & Disk Usage

## Related Documents

- **Usage**: `[../07.operations/05-messaging/rabbitmq.md]`
- **Procedure**: `[../07.operations/05-messaging/rabbitmq.md]`

---

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/05-messaging/rabbitmq.md` during the 2026-05-10 operations taxonomy consolidation.

### RabbitMQ Service Usage

> Standardized AMQP message broker for task queuing and asynchronous messaging.

---

#### Overview (KR)

이 문서는 RabbitMQ 메시지 브로커에 대한 기술 가이드를 제공한다. `hy-home.docker` 환경에서 RabbitMQ를 연동하고 관리하는 방법, 큐 관리 정책 및 메시지 안정성 확보 방안을 설명한다.

#### Usage Type

`system-guide`

#### Target Audience

- Backend Developer
- SRE

#### Purpose

- RabbitMQ 서비스 연결 및 인증 설정
- Management UI 사용법 및 모니터링
- 큐(Queue) 및 익스체인지(Exchange) 설계 가이드

#### Prerequisites

- `infra/05-messaging/rabbitmq` 서비스가 실행 중이어야 함.
- AMQP 클라이언트 라이브러리 (pika, amqplib 등) 설치.

#### Step-by-step Instructions

##### 1. 연결 정보 및 인증

- **Endpoint (External)**: `amqp://rabbitmq.${DEFAULT_URL}:5672`
- **Management Console**: `https://rabbitmq.${DEFAULT_URL}`
- **Internal API**: `rabbitmq:5672`
- **Username/Password**: `rabbitmq_user` 및 `rabbitmq_password` 시크릿 파일에서 주입됨.

##### 2. Management UI 접속

웹 브라우저에서 `https://rabbitmq.${DEFAULT_URL}`에 접속하여 브로커 상태를 모니터링할 수 있다.

- **Connections**: 활성 클라이언트 연결 확인
- **Channels**: 활성 채널 및 처리량 확인
- **Exchanges**: 메시지 라우팅 규칙 설정
- **Queues**: 대기 중인 메시지 수 및 소비자 상태 확인

##### 3. 주요 설정 가이드

- **VHost**: 기본 VHost는 `/`를 사용하며, 서비스별로 분리 시 별도의 VHost 생성을 권장한다.
- **Quorum Queues**: 데이터 일관성이 중요한 경우 일반 큐 대신 Quorum 큐를 사용한다.
- **Message Durability**: 서비스 재시작 시에도 메시지를 보존하려면 `durable: true` 설정을 활성화해야 한다.

##### 4. 클라이언트 연동 예시 (Python/pika)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
connection.close()
```

#### Common Pitfalls

- **Default Credentials**: `guest/guest`는 보안상 비활성화되어 있다. 반드시 Vault/Secrets를 통해 생성된 계정을 사용해야 한다.
- **OOM Kill**: RabbitMQ는 메모리 사용량이 임계치에 도달하면 메시지 수신을 차단한다. 모니터링 대시보드에서 `Memory Workflow`를 상시 확인해야 한다.

#### Related Documents

- **Operation**: `[../07.operations/05-messaging/rabbitmq.md]`
- **Procedure**: `[../07.operations/05-messaging/rabbitmq.md]`

## Procedure

> Migrated from `docs/07.operations/05-messaging/rabbitmq.md` during the 2026-05-10 operations taxonomy consolidation.

### RabbitMQ Recovery Procedure

: Emergency procedures for RabbitMQ service failures.

---

#### Overview (KR)

이 런북은 RabbitMQ 서비스 장애 시 장애 복구 절차를 정의한다. 메시지 누적(Message Backlog), 메모리 부족(Memory Alarm), 서비스 응답 없음 등의 상황에서 즉각적인 복구 단계를 제공한다.

#### Purpose

- RabbitMQ 메시지 처리 성능 회복
- 장애 노드 복구 및 데이터 정합성 유지
- 메시지 폭주 상황에서의 시스템 보호

#### Canonical References

- `[../../../infra/05-messaging/rabbitmq/README.md]`
- `[../07.operations/05-messaging/rabbitmq.md]`

#### When to Use

- "Message Backlog": 큐에 메시지가 수만 개 이상 쌓여 처리가 지연될 때.
- "Memory Alarm": RabbitMQ가 메모리 부족으로 인해 퍼블리셔 차단 상태일 때.
- "Service Down": 컨테이너 장애로 인해 서비스에 접속할 수 없을 때.

#### Procedure or Checklist

##### Checklist

- [ ] RabbitMQ Management UI 접속 가능 여부 확인.
- [ ] `docker exec rabbitmq rabbitmqctl list_queues` 명령으로 큐 상태 확인.

##### Procedure

1. **Service Downtime (서비스 중단 시)**
   - 컨테이너 상태 확인: `docker compose ps rabbitmq`
   - 로그 확인: `docker compose logs -f rabbitmq`
   - 서비스 재시작: `docker compose restart rabbitmq`

2. **Memory Alarm (메모리 경고 시)**
   - 메모리 소모가 심한 큐 식별.
   - 불필요한 연결 강제 종료: UI 또는 `rabbitmqctl close_connection [connection-name]`
   - 중요도가 낮은 큐의 메시지 퍼지(Purge) 검토: `rabbitmqctl purge_queue [queue-name]`

3. **High CPU / Message Backlog (메처리 지연 시)**
   - Consumer 수 확인 및 확장 검토.
   - 메시지 처리 로직의 병목 지점(DB connection, external API call 등) 확인.
   - `x-max-priority` 설정이 있는 큐의 우선순위 처리 상태 점색.

#### Verification Steps

- [ ] `rabbitmq-diagnostics check_running`: 서비스 정상 실행 확인.
- [ ] `rabbitmqctl status`: 메모리 및 디스크 알람 해제 여부 확인.
- [ ] 웹 콘솔 (`https://rabbitmq.${DEFAULT_URL}`) 접속 및 대시보드 정상 출력 확인.

#### Related Operational Documents

- **Operation Policy**: `[../07.operations/05-messaging/rabbitmq.md]`
- **System Usage**: `[../07.operations/05-messaging/rabbitmq.md]`

---

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
