# Infrastructure Overview

Hy-Home 인프라는 도커 컴포즈(Docker Compose)를 기반으로 구축된 계층화된 서비스 스택입니다. 각 서비스의 상세 설정 및 기술 정보는 해당 `infra/` 디렉토리 내의 `README.md`에서 확인할 수 있습니다.

## 🏗️ 서비스 카테고리

| 카테고리 | 목적 | 주요 서비스 | 상세 문서 |
| :--- | :--- | :--- | :--- |
| **01-Gateway** | 외부 접속 및 라우팅 | Traefik, Nginx | [README](../../infra/01-gateway/README.md) |
| **02-Auth** | 인증 및 권한 관리 | Keycloak, OAuth2 Proxy | [README](../../infra/02-auth/README.md) |
| **03-Security** | 시크릿 및 보안 정책 | Vault | [README](../../infra/03-security/README.md) |
| **04-Data** | 데이터베이스 및 저장소 | PostgreSQL, MinIO, OpenSearch | [README](../../infra/04-data/README.md) |
| **05-Messaging** | 메시징 및 스트리밍 | Kafka | [README](../../infra/05-messaging/README.md) |
| **06-Observability**| 모니터링 및 로깅 | LGTM 스택 (Grafana, Loki 등) | [README](../../infra/06-observability/README.md) |
| **07-Workflow** | 자동화 및 워크플로우 | n8n, Airflow | [README](../../infra/07-workflow/README.md) |
| **08-AI** | 로컬 LLM 및 RAG | Ollama, Open WebUI | [README](../../infra/08-ai/README.md) |
| **09-Tooling** | 개발 도구 및 코드 관리 | SonarQube | [README](../../infra/09-tooling/README.md) |
| **10-Communication**| 통신 및 메일 인프라 | MailHog | [README](../../infra/10-communication/README.md) |

## 🧭 운영 가이드

- **전체 실행**: 루트 디렉토리의 `docker-compose.yml`을 사용합니다.
- **환경 변수**: `.env` 파일과 `secrets/` 폴더에서 중앙 관리됩니다.
- **운영 명령어**: 자세한 운영 명령어는 루트의 [README.md](../../README.md) 및 [infra/README.md](../../infra/README.md)를 참조하십시오.

---
> **참고**: 이 문서는 마이그레이션된 거대 문서(`infra-migrated-setup.md`)를 대체하며, 상세 기술 스펙은 코드와 인접한 곳(`infra/`)에서 관리하는 것을 원칙으로 합니다.
