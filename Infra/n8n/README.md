# n8n Workflow Automation Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 워크플로우 자동화 도구인 n8n을 정의합니다. 대규모 처리를 위해 Queue 모드로 구성되어 있으며, 메인 서버와 워커 노드로 분리되어 있습니다. 작업 큐 관리를 위해 전용 Redis를 사용합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **n8n** | Main Server (Webhook/Editor) | 워크플로우 편집기 UI를 제공하고 웹훅 요청을 수신하여 큐에 적재합니다. |
| **n8n-worker** | Worker Node | 큐에 쌓인 작업을 실제로 수행하는 워커입니다. |
| **n8n-redis** | Job Queue | n8n의 작업 큐(Queue)로 사용되는 전용 Redis입니다. |
| **n8n-redis-exporter**| Metrics Exporter | n8n Redis의 메트릭을 수집합니다. |

## 3. 구성 및 설정 (Configuration)

### 실행 모드 (Queue Mode)
`EXECUTIONS_MODE=queue` 설정을 통해 메인 서버와 워커가 역할을 분담합니다.
- 메인 서버: Editor, Webhook 수신 -> Redis Queue 적재
- 워커: Redis Queue -> 작업 수행

### 데이터베이스
외부 PostgreSQL(`mng-pg`)과 연결하여 워크플로우 저장 및 실행 이력을 관리합니다.

### 보안
- **암호화 키**: `N8N_ENCRYPTION_KEY`를 사용하여 자격 증명(Credential)을 암호화합니다.
- **SSO 연동**: 별도의 설정이 없으면 n8n 자체 로그인 또는 Basic Auth를 사용하나, Traefik 레벨에서 도메인 라우팅이 설정되어 있습니다.

### 로드밸런싱 (Traefik)
- **URL**: `https://n8n.${DEFAULT_URL}`
- **Websocket**: 편집기와의 실시간 통신을 위해 `N8N_PUSH_BACKEND=websocket` 설정이 되어 있습니다.

### 모니터링
- `N8N_METRICS=true` 설정으로 자체 메트릭을 노출합니다. (`n8n_` prefix)
