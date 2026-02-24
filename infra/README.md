# Hy-Home Infrastructure (infra/)

이 디렉토리는 `Docker Compose`로 구축된 홈 서버/개발 환경 인프라의 **서비스 정의**를 관리합니다. 각 서비스는 `infra/<번호-카테고리>/<서비스명>/docker-compose.yml`에 분리되어 있으며, **저장소 루트의 `docker-compose.yml`에서 `include`** 기능으로 통합됩니다.

## 🏗️ 전체 구조

```text
infra/
├── 01-gateway/               # Edge/Gateway
│   └── traefik/
├── 02-auth/                  # 인증/SSO
│   └── keycloak/
├── 03-security/              # 시크릿/보안
│   └── vault/
├── 04-data/                  # DB/Storage
│   └── postgresql-cluster/
├── 05-messaging/             # 메시징/스트리밍
│   └── kafka/
├── 06-observability/         # LGTM 스택
│   ├── docker-compose.yml
│   └── prometheus/
├── 07-workflow/              # 워크플로우
│   └── n8n/
├── 08-ai/                    # AI/LLM
│   └── ollama/
├── 09-tooling/               # DevOps/QA/TF
│   └── terrakube/
└── 10-communication/         # Mail
    └── mail/
```

## 🧭 실행 흐름

> **실행 진입점은 저장소 루트의 `docker-compose.yml`입니다.**

```bash
# 저장소 루트에서
cp .env.example .env
docker compose up -d
```

- `.env`와 `secrets/` 값은 루트 기준으로 관리됩니다.

## 🧩 정리 기준 (분류 원칙)

infra 하위 폴더는 실행 방식에 따라 다음 4가지로 분류합니다.

1. **Core (Include)**: 루트 `docker-compose.yml`에 `include`된 기본 스택.
2. **Optional (Profile)**: `include`는 되어 있으나 `profiles`로 켜는 스택.
3. **Standalone**: 루트 `include`에 없으며 폴더 단위로 별도 실행.
4. **Placeholder**: 문서만 존재하며 실행 정의가 아직 없음.

### 분류 요약

- **Core (Include)**: traefik, mng-db, oauth2-proxy, observability, minio, keycloak, n8n, qdrant, postgresql-cluster, kafka, valkey-cluster, opensearch
- **Optional (Profile)**: airflow, influxdb, couchdb, mail, nginx, ollama, open-webui, sonarqube, vault, terrakube, redis-cluster, ksql
- **Standalone**: supabase
- **Placeholder**: rabbitmq

## ➕ 서비스 추가 방법

1. `infra/<번호-카테고리>/<서비스명>/` 디렉토리를 생성하고 `docker-compose.yml`을 작성합니다.
2. 필요 시 `profiles`를 지정해 선택 실행 가능한 스택으로 분리합니다.
3. 루트 `docker-compose.yml`의 `include`에 새 서비스를 추가합니다.
4. 환경 변수가 필요하면 루트 `.env.example`에 추가하고, 민감 값은 `secrets/`에 `*.txt`로 분리합니다.
5. 문서 반영: `infra/README.md`에 서비스 요약을 추가하고 `docs/README.md` 및 `docs/guides/README.md`에 관련 내용을 업데이트합니다.
