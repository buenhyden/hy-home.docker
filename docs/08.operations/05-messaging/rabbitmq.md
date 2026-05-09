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

- **Guide**: `[../07.guides/05-messaging/rabbitmq.md]`
- **Runbook**: `[../09.runbooks/05-messaging/rabbitmq.md]`

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
