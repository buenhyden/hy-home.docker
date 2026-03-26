# n8n System Guide

: Apache n8n (07-workflow)

---

## Overview (KR)

이 가이드는 n8n 로우코드 자동화 시스템의 아키텍처, UI 접근 방식 및 핵심 운영 절차를 설명한다. n8n은 워크플로우를 노드 기반으로 시각화하여 설계하며, 외부 서비스와의 통합을 가속화하는 역할을 한다.

## Architecture and Components

n8n은 확장성을 위해 분산형 큐 아키텍처를 사용하며, 주요 컴포넌트는 다음과 같다:

- **n8n Main**: 사용자 인터페이스(UI), API 서버, 워크플로우 엔진.
- **n8n Worker**: 대규모 비동기 작업 처리를 담당하는 작업 실행기.
- **n8nio/runners**: 특정 복잡한 연산을 격리 수행하여 메인 프로세스의 안정성을 확보.
- **Valkey Broker**: 메인과 워커 간의 메시지 전달을 위한 메시지 브로커.
- **Metadata DB**: 워크플로우 레시피 및 사용자 자격 증명(`Credentials`)을 저장하는 PostgreSQL 데이터베이스.

## Access and Integration

- **Web UI**: `https://n8n.${DEFAULT_URL}` 에 접속하여 시각적으로 자동화 로직을 설계한다.
- **Public API**: 필요한 경우 `N8N_PUBLIC_API_BASE_URL`을 통해 프로그래밍 방식으로 워크플로우를 제어할 수 있다.
- **Webhook**: 외부 서비스로부터의 이벤트를 수신할 수 있도록 `WEBHOOK_URL`이 명시적으로 구성되어 있다.

## Critical Procedures

### 1. 워크플로우 배포 및 테스트

- 새 워크플로우 설계 시 `Manual Execution`으로 개별 노드의 데이터 입출력을 검증한다.
- 검증 완료 후 `Active` 모드로 전환하여 자동 실행되도록 설정한다.

### 2. 자격 증명(Credentials) 관리

- 모든 인증 정보는 n8n 내부의 `Credentials` 탭에서 관리한다.
- 자격 증명은 메타데이터 DB에 암호화되어 저장되며, `N8N_ENCRYPTION_KEY`를 통해 보호된다.

### 3. 노드 라이브러리 확장

- 필요한 경우 `./custom` 디렉터리에 사용자 정의 노드를 추가하여 엔진 기능을 확장할 수 있다.

## Development and Verification

- **Local Runner**: 새로운 노드나 복잡한 JS 코드는 n8n 내부의 `Code` 노드에서 직접 실행하여 즉시 결과를 확인할 수 있다.
- **Instance Report**: `Admin > Settings`에서 인스턴스의 상태와 리소스 사용 현황을 모니터링한다.

## Operational Controls

- **Resource Monitoring**: 워커(`n8n-worker`)의 CPU 및 메모리 사용량을 Grafana 알람을 통해 모니터링한다.

## Known Limitations and Context

- 대규모 병렬 데이터 처리가 필요한 경우 Airflow 사용을 권장하며, n8n은 주로 API 기반의 경량 연동 자동화에 활용한다.
- 워크플로우가 너무 많은 노드를 포함할 경우 `Sub-workflows`로 분리하여 유지보수성을 높여야 한다.

## AI Agent Guidance

1. **Modularization**: 복잡한 로직은 `Sub-workflows`를 활용하여 분리하고 재사용성을 확보하십시오.

## Appendix: Links

- ARD: [07-workflow Architecture](../../02.ard/0007-workflow-architecture.md)
- Recovery: [n8n Recovery Runbook](../../09.runbooks/07-workflow/n8n.md)
- Specialized Guide: [02.n8n-automation.md](./02.n8n-automation.md) (Detailed usage)
