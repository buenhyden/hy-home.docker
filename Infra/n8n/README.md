# n8n Workflow Automation

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 노드 기반의 워크플로우 자동화 도구입니다. 다양한 앱과 서비스를 시각적으로 연결하여 자동화 파이프라인을 구축합니다.

**주요 기능 (Key Features)**:
- **Queue Mode**: 메인 인스턴스와 별도의 워커 인스턴스로 분리하여 대용량 처리 지원.
- **Webhook**: 외부 트리거 수신을 위한 웹훅 기능.

**기술 스택 (Tech Stack)**:
- **Image**: `n8nio/n8n:2.1.4`
- **DB**: PostgreSQL (`n8n` DB)
- **Queue**: Redis (Job 관리)

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**구조**:
- **Editor/Webhook (Main)**: UI 제공 및 웹훅 수신, 작업을 Redis 큐에 적재.
- **Worker**: Redis 큐에서 작업을 가져와 실제 실행.
- **Redis**: 작업 큐 저장소.

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수**:
- `N8N_ENCRYPTION_KEY`: 민감 정보 암호화 키 (분실 시 복구 불가).
- `EXECUTIONS_MODE`: `queue` 모드로 설정됨.
- `WEBHOOK_URL`: 외부에서 접근 가능한 URL (`https://n8n.${DEFAULT_URL}`).

**네트워크 포트**:
- **Internal**: 5678
- **External**: `https://n8n.${DEFAULT_URL}` via Traefik.

## 5. 통합 및 API 가이드 (Integration Guide)
**API**: `N8N_PUBLIC_API_DISABLED=false`로 설정되어 REST API 사용 가능.

## 6. 가용성 및 관측성 (Availability & Observability)
**모니터링**:
- `N8N_METRICS=true` 설정으로 메트릭 수집 활성화.
- `n8n-redis-exporter`를 통해 큐 상태 모니터링 가능.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- PostgreSQL 데이터 백업.
- `n8n-data` 볼륨(설정 파일 등) 백업.
- **중요**: 암호화 키(`N8N_ENCRYPTION_KEY`) 별도 보관 필수.

## 8. 보안 및 강화 (Security Hardening)
- 워크플로우 내 Credential 정보는 암호화되어 DB에 저장됩니다.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Webhook Error 404**: `WEBHOOK_URL` 환경 변수가 실제 프록시 도메인과 일치하는지 확인.
