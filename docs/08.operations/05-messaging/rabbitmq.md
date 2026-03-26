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
