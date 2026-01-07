# n8n Workflow Automation

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 확장 가능한 노드 기반 워크플로우 자동화 도구입니다.  
본 인프라에서는 **Queue Mode**로 구성되어 있어, 웹 인터페이스(Editor)와 실행 작업자(Worker)가 분리된 고성능 아키텍처를 가집니다.

## 2. 주요 기능 (Key Features)
- **Workflow Automation**: HTTP 요청, 스케줄링, 이벤트 트리거 등을 통해 다양한 서비스를 연결하고 자동화합니다.
- **Queue Mode Architecture**: 무거운 작업 부하를 처리하기 위해 실행 요청을 Redis 대기열에 넣고 Worker가 비동기적으로 처리합니다.
- **Detailed Monitoring**: Prometheus용 메트릭을 노출하여 워크플로우 실행 성능과 노드별 사용량을 관측할 수 있습니다.
- **Secure**: 자격 증명(Credential) 데이터의 암호화 및 API Key 기반 접근 제어를 지원합니다.

## 3. 기술 스택 (Tech Stack)
- **Core Image**: `n8nio/n8n:2.1.4` (Main & Worker)
- **Database**: PostgreSQL (Metadata & Execution Logs)
- **Message Broker**: Redis (Job Queue)
- **Cache**: Redis

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 컴포넌트 구조
1.  **n8n (Main)**:
    - 웹 UI 제공 (`https://n8n.${DEFAULT_URL}`).
    - Webhook 요청 수신 및 Job 생성.
    - 생성된 Job을 Redis 큐에 적재.
2.  **n8n-worker**:
    - UI 없음.
    - Redis 큐에서 Job을 가져와 실제 워크플로우 실행.
    - CPU/Memory 집약적인 작업 담당.
3.  **n8n-redis**:
    - Job Queue 작업을 위한 브로커 역할.
4.  **Database (External)**:
    - 워크플로우 정의, 실행 기록, 사용자 정보 등을 `mng-pg`에 저장.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **참고**: `n8n-worker`는 `n8n` 메인 컨테이너와 동일한 암호화 키(`N8N_ENCRYPTION_KEY`)를 공유해야 올바르게 동작합니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 Web UI 사용
1.  **접속**: `https://n8n.${DEFAULT_URL}`
2.  **계정 생성**: 최초 접속 시 Owner 계정 설정 필요.
3.  **워크플로우 생성**:
    - 캔버스에 노드(HTTP Request, PostgreSQL, Google Sheets 등)를 드래그 앤 드롭.
    - 선으로 연결하여 로직 구성.
    - `Execute Workflow` 버튼으로 테스트 실행.

### 6.2 Webhook 활용
- **URL 형식**:
    - Production: `https://n8n.${DEFAULT_URL}/webhook/...`
    - Test: `https://n8n.${DEFAULT_URL}/webhook-test/...`
- **확인**: Webhook 노드 추가 후 테스트 모드를 활성화하면 들어오는 요청 데이터를 실시간으로 볼 수 있습니다.

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `EXECUTIONS_MODE`: `queue` (필수 설정).
- `N8N_ENCRYPTION_KEY`: 자격 증명 암호화 키. **절대 변경하거나 분실하여서는 안 됩니다.**
- `WEBHOOK_URL`: 외부에서 접근 가능한 도메인 주소.
- `DB_TYPE`: `postgresdb` (외부 DB 사용).

### 볼륨 마운트 (Volumes)
- `n8n-data`: `/home/node/.n8n` (사용자 설정 파일 등).

### 네트워크 포트 (Ports)
- **Internal**: 5678 (Main Instance).
- **External**: Traefik을 통해 443 포트로 노출.

## 8. 통합 및 API 가이드 (Integration Guide)
**Public API**:
- **활성화 여부**: `N8N_PUBLIC_API_DISABLED=false`.
- **기능**: 워크플로우 제어, 실행 내역 조회 등.
- **문서**: [n8n API Reference](https://docs.n8n.io/api/).

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- **Main**: `nc -z localhost 5678` (포트 응답 확인).
- **Queue**: `QUEUE_HEALTH_CHECK_ACTIVE=true` 설정을 통해 Redis 연결 상태 감시.

**Monitoring**:
- `N8N_METRICS=true`: `/metrics` 엔드포인트 활성화.
- **주요 지표**: `n8n_workflow_execution_count`, `n8n_workflow_execution_duration_seconds`.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**핵심 백업 대상**:
1.  **PostgreSQL DB**: 모든 워크플로우 데이터가 저장됨.
2.  **Encryption Key**: 이 키가 없으면 DB의 자격 증명을 복호화할 수 없음.
3.  **Volume**: `n8n-data` (Binary Data 저장 시).

## 11. 보안 및 강화 (Security Hardening)
- **Encryption**: 민감한 Credential은 `N8N_ENCRYPTION_KEY`로 암호화되어 DB에 저장됩니다.
- **Isolation**: Worker 컨테이너는 외부로 포트를 노출하지 않고 오직 내부 네트워크와 Redis를 통해서만 통신합니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Workflow Stuck**: Worker 컨테이너가 중단되었거나 Redis 연결이 끊긴 경우 작업이 멈출 수 있습니다. `docker logs n8n-worker`를 확인하세요.
- **Webhook 404**: Traefik 라우팅 문제이거나 `WEBHOOK_URL` 환경변수 설정 오타일 수 있습니다.

---
**공식 문서**: [https://docs.n8n.io/](https://docs.n8n.io/)
