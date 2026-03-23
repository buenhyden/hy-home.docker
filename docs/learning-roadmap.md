# 🚀 hy-home.docker 학습 로드맵: 백엔드 개발자 정복 가이드

비전공 6년 차 백엔드 개발자로서 인프라의 기초를 다지고, 실무 기술의 'Why'와 'How'를 연결하는 체계적인 학습 경로입니다.

---

## 🏗️ Phase 1: Basic (기초 - "왜(Why)" 동작하는가?)

가장 먼저 인프라의 기본 도구와 `hy-home.docker`의 독특한 구조를 이해합니다.

### 1️⃣ Docker & Orchestration

- **학습 내용**: 이미지 vs 컨테이너, 볼륨 마운트(Persist), 네트워크 브릿지.
- **프로젝트 실습**: `docker-compose.yml`의 `include`와 `profiles` 기능이 어떻게 여러 서비스를 하나로 묶는지 분석합니다.
- **추천 파일**: [docker-compose.yml](file:///home/hy/projects/hy-home.docker/docker-compose.yml)

### 2️⃣ Linux & Shell Scripting

- **학습 내용**: 권한 설정(chmod, chown), 환경 변수 관리(.env), Bash 제어문.
- **프로젝트 실습**: `scripts/` 폴더의 자동화 스크립트들이 로컬 인증서나 비밀값을 어떻게 생성하는지 분석합니다.
- **추천 파일**: [scripts/bootstrap-secrets.sh](file:///home/hy/projects/hy-home.docker/scripts/bootstrap-secrets.sh)

---

## 🔥 Phase 2: Intermediate (심화 1 - 백엔드 핵심 3요소)

백엔드 개발자에게 가장 중요한 계층입니다. 단순히 사용하는 수준을 넘어 **클러스터링과 보안 아키텍처**를 다룹니다.

### 3️⃣ [Deep Dive] Data (DB & Storage)

- **학습 내용**: RDBMS 클러스터링(Stolon/Patroni), 캐시 전략, Object Storage(S3).
- **프로젝트 실습**:
  - `04-data/postgresql-cluster`: 단순 DB가 아닌, 고가용성(HA)을 고려한 구성을 분석합니다.
  - `MinIO`: 로컬 S3 환경 구축 및 정적 리소스 관리 학습.
- **추천 디렉토리**: [infra/04-data/](file:///home/hy/projects/hy-home.docker/infra/04-data/)

### 4️⃣ [Deep Dive] Auth (인증 & 인가)

- **학습 내용**: OIDC, SAML, JWT, SSO(Single Sign-On), OAuth2 Proxy Flow.
- **프로젝트 실습**:
  - `Keycloak`: 대규모 사용자 관리 및 백엔드 연동(OAuth2/OpenID Connect) 실습.
  - `OAuth2-Proxy`: 애플리케이션 코드 수정 없이 게이트웨이에서 인증을 처리하는 'Proxy-level Auth' 이해.
- **추천 디렉토리**: [infra/02-auth/](file:///home/hy/projects/hy-home.docker/infra/02-auth/)

### 5️⃣ [Deep Dive] Messaging (이벤트 기반 아키텍처)

- **학습 내용**: Pub/Sub vs Queue, 데이터 일관성, Schema Registry.
- **프로젝트 실습**:
  - `Kafka`: 분산 스트리밍 플랫폼의 원리와 멀티 브로커 구성 학습.
  - `ksqlDB`: 스트리밍 데이터를 실시간으로 쿼리하고 처리하는 백엔드 로직 확장성 학습.
- **추천 디렉토리**: [infra/05-messaging/](file:///home/hy/projects/hy-home.docker/infra/05-messaging/)

---

## 🛠️ Phase 3: Advanced (심화 2 - 고도화 및 운영)

시스템을 안정적으로 운영하고 고도화하기 위한 필수 영역입니다.

### 6️⃣ Observability (관측성)

- **학습 내용**: Metrics(Prometheus), Logging(Loki), Tracing(Tempo) - LGTM 스택.
- **프로젝트 실습**: 분산 시스템에서 에러를 추적하고 병목을 찾아내는 방법(Distributed Tracing) 분석.

### 7️⃣ DevSecOps (보안 & AI)

- **학습 내용**: 시크릿 관리(HashiCorp Vault), 컨테이너 보안 가이드라인.
- **프로젝트 실습**:
  - `Vault`: API Key나 DB 암호를 소스코드나 `.env`가 아닌 금고에서 동적으로 가져오는 패턴.
  - `AI Infra`: Ollama와 Qdrant(Vector DB)를 연동한 로컬 RAG 시스템 구축.

---

## 🏁 학습 체크리스트 (Summary)
>
> [!TIP]
>
> 1. `Phase 1`을 통해 `docker compose up`으로 전체 시스템을 한 번 띄워보는 것이 첫 번째 목표입니다.
> 2. `Phase 2`의 각 섹션을 정복할 때마다, 본인이 작성한 기존 백엔드 코드를 이 인프라에 올려보는 연습을 하세요.
> 3. `Phase 3`은 운영 환경으로 넘어가기 위한 관문입니다. Monitoring 대시보드를 직접 꾸며보는 것으로 마무리하세요.
