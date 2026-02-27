# Hy-Home Docker Infrastructure

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

`hy-home.docker`는 로컬/홈랩 환경에서 멀티 서비스 인프라를 일관되게 실행하기 위한 Docker Compose 기반 저장소입니다.
루트 [`docker-compose.yml`](docker-compose.yml)이 [`infra/**/docker-compose*.yml`](infra/)을 `include`하여 스택을 조립합니다.

## 문서 시작점

- 아키텍처 원칙: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- 운영 정책/런북 인덱스: [`OPERATIONS.md`](OPERATIONS.md)
- 기술 블루프린트 허브: [`docs/context/README.md`](docs/context/README.md)
- 실행 런북 허브: [`runbooks/README.md`](runbooks/README.md)
- 인프라 디렉토리 가이드: [`infra/README.md`](infra/README.md)

## 준비 사항

- Docker Engine 또는 Docker Desktop
- Docker Compose v2
- `rg`(ripgrep), `bash` (스크립트 실행용)
- Windows + WSL2 사용 시: 저장소를 `/mnt/c`가 아닌 WSL Linux 파일시스템(예: `/home/<user>`)에 두는 것을 권장

## 빠른 시작

```bash
# 1) 환경 파일 생성
cp .env.example .env

# 2) 로컬 TLS 인증서 생성 (최초 1회)
bash scripts/generate-local-certs.sh

# 3) 시크릿 파일 생성 (최초 1회)
# - root docker-compose.yml의 secrets(file:)를 기준으로 `secrets/**/*.txt`를 생성
# - 외부 연동이 필요한 값(Slack Webhook, SMTP 등)은 CHANGE_ME_* placeholder로 생성됨
bash scripts/bootstrap-secrets.sh --env-file .env.example

# (옵션) placeholder 강제 검증 (CHANGE_ME_*가 남아있으면 실패)
# bash scripts/bootstrap-secrets.sh --strict

# 4) Compose 정적 검증 (Docker 데몬 없이도 가능)
# - `.env.example` 기반으로 `docker compose config`가 0 exit인지 확인
bash scripts/validate-docker-compose.sh

# (옵션) 런타임 사전 점검 (Docker 데몬 필요)
# bash scripts/preflight-compose.sh

# 5) 스택 실행
docker compose up -d

# 또는 프로파일 기반 실행
docker compose --profile core --profile data up -d
```

접속 예시 (`DEFAULT_URL=127.0.0.1.nip.io` 기준):

- Traefik Dashboard: `https://dashboard.127.0.0.1.nip.io`
- Grafana: `https://grafana.127.0.0.1.nip.io`
- Prometheus: `https://prometheus.127.0.0.1.nip.io`

### 인프라 서비스 프로파일 (Profiles)

| Profile | Description | Included Services |
| :--- | :--- | :--- |
| `core` | 핵심 관문 및 인증 | Traefik, Keycloak, OAuth2-Proxy |
| `data` | 공통 데이터 저장소 | mng-db, postgresql-cluster, valkey-cluster, minio, opensearch, qdrant |
| `obs` | 관측성 (LGTM) | Grafana, Loki, Tempo, Prometheus, Alloy, Alertmanager, etc. |
| `messaging` | 메시징 인프라 | Kafka Stack |
| `workflow` | 자동화 엔진 | Airflow (n8n은 기본 비활성/주석 처리) |
| `ai` | 로컬 LLM 환경 | Ollama, Open-webui, Qdrant |
| `tooling` | QA/DevOps 도구 | SonarQube |

```bash
docker compose --profile obs up -d
```

## 운영 명령 요약

```bash
# Compose 설정 검증
bash scripts/validate-docker-compose.sh

# 특정 서비스만 재기동
docker compose up -d --no-deps <service>

# 로그 확인
docker compose logs -f <service>

# 종료
docker compose down
```

## 구성 정책 요약

- **Root-only**: 서비스 폴더의 `docker-compose.yml` 단독 실행은 지원하지 않으며, 루트 `docker-compose.yml`에서만 조립/실행합니다. (Standalone로 명시된 스택은 예외)
- Host 포트는 `.env`/`.env.example`의 `*_HOST_PORT`로 관리
- 컨테이너 기본 포트는 `*_PORT`로 관리하고, Compose에는 `${VAR:-default}` 형태로 기본값 명시
- 비밀번호/토큰은 환경변수 대신 `secrets/**/*.txt` 파일 + Docker secrets로 주입
- 컨테이너 보안 기본값: `no-new-privileges:true`, `cap_drop: [ALL]` (예외 시 파일 내 사유 명시)

## 저장소 구조

| Directory | Purpose | Docs |
| :--- | :--- | :--- |
| [`infra/`](infra/) | 서비스별 Compose 정의 | [`infra/README.md`](infra/README.md) |
| [`docs/`](docs/) | 아키텍처/가이드/블루프린트 | [`docs/README.md`](docs/README.md) |
| [`runbooks/`](runbooks/) | 장애 대응/복구 절차 | [`runbooks/README.md`](runbooks/README.md) |
| [`secrets/`](secrets/) | 런타임 시크릿 파일 | [`secrets/README.md`](secrets/README.md) |
| [`scripts/`](scripts/) | 검증/부트스트랩 스크립트 | [`scripts/README.md`](scripts/README.md) |
| [`specs/`](specs/) | 구현 스펙/계획 문서 | [`specs/`](specs/) |
| [`.github/`](.github/) | CI/CD 워크플로 | [`.github/workflows/`](.github/workflows/) |

## 기여

- 가이드: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- 행동강령: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- 아키텍처 제약: [`ARCHITECTURE.md`](ARCHITECTURE.md)

## License

Apache-2.0. See `LICENSE`.
