# Hy-Home Infrastructure (infra/)

이 디렉토리는 `Docker Compose`로 구축된 홈 서버/개발 환경 인프라의 **서비스 정의**를 관리합니다. 각 서비스는 `infra/<번호-카테고리>/<서비스명>/docker-compose.yml`에 분리되어 있으며, **저장소 루트의 `docker-compose.yml`에서 `include`** 기능으로 통합됩니다.

## 🏗️ 전체 구조

```text
infra/
├── [01-gateway](01-gateway/)         # Edge/Gateway ([Context](../docs/guides/01-gateway/))
│   └── traefik/
│   └── nginx/                 # (Standalone/Optional)
├── [02-auth](02-auth/)               # 인증/SSO ([Context](../docs/guides/02-auth/))
│   ├── keycloak/
│   └── oauth2-proxy/
├── [03-security](03-security/)           # 시크릿/보안 ([Context](../docs/guides/03-security/))
│   └── vault/                 # (Standalone/Optional)
├── [04-data](04-data/)               # DB/Storage ([Context](../docs/guides/04-data/))
│   ├── mng-db/
│   ├── minio/
│   ├── opensearch/
│   ├── postgresql-cluster/
│   ├── qdrant/
│   └── valkey-cluster/
├── [05-messaging](05-messaging/)          # 메시징/스트리밍 ([Context](../docs/guides/05-messaging/))
│   └── kafka/
├── [06-observability](06-observability/)      # LGTM 스택 ([Context](../docs/guides/06-observability/))
│   ├── docker-compose.yml
│   └── prometheus/
├── [07-workflow](07-workflow/)           # 워크플로우 ([Context](../docs/guides/07-workflow/))
│   ├── airflow/
│   └── n8n/                   # (Optional, root include 주석 처리)
├── [08-ai](08-ai/)                 # AI/LLM ([Context](../docs/guides/08-ai/))
│   ├── ollama/
│   └── open-webui/
├── [09-tooling](09-tooling/)            # DevOps/QA/TF ([Context](../docs/guides/09-tooling/))
│   ├── sonarqube/
│   └── terrakube/             # (Optional, root include 주석 처리)
└── [10-communication](10-communication/)      # Mail (Optional) ([Context](../docs/guides/10-communication/))
    └── mail/                  # (Optional, root include 주석 처리)
```

## 🧭 실행 흐름

> **실행 진입점은 저장소 루트의 `docker-compose.yml`입니다.**

```bash
# 저장소 루트에서
cp .env.example .env
docker compose up -d
```

- `.env`와 `secrets/` 값은 루트 기준으로 관리됩니다.

## 🔒 컨테이너 보안 기준

- 모든 infra 서비스는 `security_opt: [no-new-privileges:true]`와 `cap_drop: [ALL]`을 기본 적용합니다.
- 예외(예: `privileged`, `cap_add`, root 필요)는 **compose 파일에 주석으로 사유를 명시**하고, 관련 Spec에 기록합니다.

## 🧩 정리 기준 (분류 원칙)

infra 하위 폴더는 실행 방식에 따라 다음 4가지로 분류합니다.

1. **Core (Include)**: 루트 `docker-compose.yml`에 `include`된 기본 스택.
2. **Optional (Profile)**: `include`는 되어 있으나 `profiles`로 켜는 스택.
3. **Standalone**: 루트 `include`에 없으며 폴더 단위로 별도 실행.
4. **Placeholder**: 문서만 존재하며 실행 정의가 아직 없음.

### 분류 요약

- **Core (Profile: `core`)**: traefik, keycloak, oauth2-proxy
- **Data (Profile: `data`)**: mng-db (valkey, postgres), postgresql-cluster, valkey-cluster, opensearch, minio
- **Observability (Profile: `obs`)**: prometheus, loki, tempo, grafana, alloy, etc.
- **Messaging (Profile: `messaging`)**: kafka, schema-registry, etc.
- **AI (Profile: `ai`)**: ollama, open-webui, qdrant
- **Workflow (Profile: `workflow`)**: airflow (n8n은 기본 비활성/주석 처리)
- **Tooling (Profile: `tooling`)**: sonarqube
- **Standalone**: supabase (manual directory run)
- **Placeholder**: courier, rabbitmq (정의는 있으나 루트 include에 아직 미통합)

## ➕ 서비스 추가 방법

1. `infra/<번호-카테고리>/<서비스명>/` 디렉토리를 생성하고 `docker-compose.yml`을 작성합니다.
2. 필요 시 `profiles`를 지정해 선택 실행 가능한 스택으로 분리합니다.
3. 루트 `docker-compose.yml`의 `include`에 새 서비스를 추가합니다.
4. 환경 변수가 필요하면 루트 `.env.example`에 추가하고, 민감 값은 `secrets/`에 `*.txt`로 분리합니다.
5. 문서 반영: `infra/README.md`에 서비스 요약을 추가하고 `docs/README.md` 및 `docs/guides/README.md`에 관련 내용을 업데이트합니다.
