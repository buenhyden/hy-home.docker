# 🌟 Project Overview

**Hy-Home Docker**는 가정용 홈 서버 및 AI/데이터 처리를 위한 고성능 로컬 인프라를 Docker 기반으로 손쉽게 구축하고 관리하기 위한 프로젝트입니다.

## 🎯 프로젝트 목적 (Mission)

이 프로젝트는 다음과 같은 문제들을 해결하고 가치를 제공하기 위해 시작되었습니다.

1. **복잡성의 추상화**: 수많은 마이크로서비스(DB, 캐시, 메시징, AI 모듈 등)를 개별적으로 설치하고 관리하는 복잡함을 `docker compose` 설정을 통해 단순화합니다.
2. **AI 로컬 환경 최적화**: 로컬 LLM(Ollama), 벡터 DB(Qdrant), 워크플로우 자동화(n8n)를 사전에 통합하여 즉시 AI 에이전트 개발이 가능한 환경을 제공합니다.
3. **엔터프라이즈급 모니터링**: 개인이 구축하기 힘든 통합 관제 시스템(Grafana, Prometheus, Loki, Tempo)을 기본 탑재하여 시스템 상태를 투명하게 시각화합니다.
4. **보안 우선 설계**: 모든 서비스에 대한 통합 인증(SSO)과 비밀 관리(Vault)를 내재화하여 안전한 홈 랩 환경을 보장합니다.

## 🔑 핵심 철학 (Core Philosophy)

### 1. Everything as Code (EaC)

인프라, 설정, 문서, 심지어 AI 에이전트의 룰까지 모든 것을 코드로 관리하여 버전 관리와 재현성을 보장합니다.

### 2. Modularity & Scalability

각 서비스는 독립적인 모듈로 구성되며(`infra/` 내 하위 폴더), 필요에 따라 `include` 기능을 통해 레고 블록처럼 조합하여 사용할 수 있습니다.

### 3. Developer Experience (DX)

복잡한 설정 없이 `cp .env.example .env` 와 `docker compose up` 만으로 전체 스택을 구동할 수 있도록 개발자 편의성을 최우선으로 합니다.

## 🛠 주요 기능 및 스택

| 영역 | 주요 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **Gateway** | **Traefik** | 동적 라우팅, 로드 밸런싱, 자동 SSL 처리 |
| **Security** | **Keycloak**, **Vault**, **OAuth2 Proxy** | 통합 인증(SSO), 비밀 관리, 제로 트러스트 보안 모델 |
| **Compute & AI** | **Ollama**, **n8n**, **Airflow** | 로컬 LLM 구동, 워크플로우 자동화, 데이터 파이프라인 |
| **Data Store** | **PostgreSQL**, **Redis**, **Minio** | 관계형 데이터, 캐시, 오브젝트 스토리지 (S3 호환) |
| **Messaging** | **Kafka**, **Redpanda** | 고성능 이벤트 스트리밍 및 메시지 큐 |
| **Vector Search** | **Qdrant**, **OpenSearch** | AI 검색 및 RAG(검색 증강 생성) 구현을 위한 벡터 엔진 |
| **Observability** | **Grafana Stack** (LGTM) | 로그(Loki), 그래프(Grafana), 트레이스(Tempo), 메트릭(Prometheus) |

## 📐 아키텍처 조망

이 프로젝트는 논리적으로 **인프라(Infrastructure) 레이어**와 **응용(Application) 레이어**로 구분됩니다.

- **Infrastructure Layer (`infra/`)**: 애플리케이션이 구동되기 위한 토대(DB, Message Queue, AI Engine 등)를 제공합니다.
- **Application Layer (`projects/`)**: 인프라 위에서 실제 비즈니스 로직을 수행하는 서비스나 코드가 위치합니다.

이 두 레이어는 명확히 분리되어 있으며, 인프라의 변경이 애플리케이션 코드에 영향을 최소화하도록 설계되었습니다.
