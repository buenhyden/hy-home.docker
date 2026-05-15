# Secrets Management

> Docker Secrets 포맷의 민감 정보 파일 경로와 운영 규칙을 관리하는 보안 진입 문서

## Overview

`secrets/`는 `hy-home.docker` 인프라에서 사용하는 비밀번호, 키, 토큰, 인증서 관련 파일 경로를 Docker Secrets 포맷으로 배치하는 공간입니다. 이 README는 secret 값 자체가 아니라 디렉터리 구조, registry, 생성/검증 절차, 안전한 운영 원칙을 설명합니다.

이 작업 범위에서는 `secrets/**/*.txt` 값 파일을 열람하지 않습니다. 분석과 문서화는 파일명, 디렉터리 구조, `SENSITIVE_ENV_VARS.md.example`, 관련 README와 스크립트 설명만 기준으로 수행합니다.

## Audience

이 README의 주요 독자:

- Operators
- Security Maintainers
- Developers
- AI Agents

## Scope

### In Scope

- Docker secret 파일의 경로 체계와 책임 범위
- secret registry와 example 파일의 사용 방식
- secret 생성/동기화 스크립트 안내
- 문서 작성 시 민감값을 노출하지 않는 기준

### Out of Scope

- secret 값, token, private key, 인증서 원문
- 운영 승인 없는 secret 교체 또는 재생성
- 외부 secret manager 마이그레이션
- Docker Compose runtime 동작 변경

## Structure

```text
secrets/
├── auth/                 # Traefik, Keycloak, proxy 관련 인증 secret
├── automation/           # Airflow, n8n 등 자동화 서비스 secret
├── certs/                # 로컬 TLS 인증서 파일 경로
├── common/               # SMTP, webhook 등 공통 secret
├── data/                 # OpenSearch, Supabase, AI 도구 관련 secret
├── db/                   # PostgreSQL, Valkey, NoSQL 등 DB secret
├── observability/        # Grafana와 monitoring stack secret
├── security/             # Vault 등 보안 계층 secret
├── storage/              # MinIO 등 object storage secret
├── tools/                # SonarQube, Syncthing 등 도구 secret
├── SENSITIVE_ENV_VARS.md.example  # registry 예시
└── README.md             # This file
```

## How to Work in This Area

1. secret 값 파일을 열지 말고, 먼저 이 README와 `SENSITIVE_ENV_VARS.md.example`를 확인합니다.
2. 새 secret 경로가 필요하면 대응 서비스의 `infra/` Compose 정의와 registry mapping을 함께 확인합니다.
3. secret 생성 또는 누락 파일 보강은 `./scripts/operations/gen-secrets.sh` 같은 승인된 스크립트를 우선 사용합니다.
4. 인증서 파일은 `./scripts/operations/generate-local-certs.sh` 절차와 관련 runbook을 따릅니다.
5. 문서, 로그, commit, PR 설명에는 secret 값 원문을 쓰지 않습니다.

## Navigation / Inventory

| Component | Path | Purpose |
| --- | --- | --- |
| Registry example | `SENSITIVE_ENV_VARS.md.example` | secret mapping과 metadata 예시 |
| Auth | `auth/` | Traefik, Keycloak, proxy credentials |
| Automation | `automation/` | Airflow, n8n 등 workflow secret |
| Certs | `certs/` | local TLS certificate file paths |
| Common | `common/` | SMTP, Slack webhook 등 공통 secret |
| Data | `data/` | OpenSearch, Supabase, AI service secret |
| DB | `db/` | PostgreSQL, Valkey, Cassandra, CouchDB, MongoDB 등 DB secret |
| Observability | `observability/` | Grafana and monitoring credentials |
| Security | `security/` | Vault and security-layer secret |
| Storage | `storage/` | MinIO and object storage credentials |
| Tools | `tools/` | SonarQube, Syncthing, utility service secret |

## Inventory Classification

현재 인벤토리는 secret 값이나 인증서 원문을 열람하지 않고 파일명, 디렉터리, 루트 Compose 선언, registry 예시만 기준으로 분류합니다.

| Classification | Current Evidence | Handling Rule |
| --- | --- | --- |
| `compose-declared` | 루트 `docker-compose.yml`의 `secrets:` 선언 69개, 누락 파일 0개 | Docker Secret mount 계약으로 관리 |
| `bind-mounted-cert` | `certs/cert.pem`, `certs/key.pem`, `certs/rootCA.pem`, `certs/rootCA-key.pem` | canonical certificate path는 `secrets/certs/`; 값/원문은 문서화하지 않음 |
| `registry/local-only` | `security/unseal_keys.txt`, `auth/traefik_admin_password.txt`, `tools/terrakube_minio_secret_key.txt` | root Compose secret 선언과 별개로 registry 또는 운영 절차에서 분류 |
| `private-registry` | `SENSITIVE_ENV_VARS.md` | 개인 gitignored registry로 취급하고 내용은 열람하지 않음 |
| `example-registry` | `SENSITIVE_ENV_VARS.md.example` | 새 환경과 문서 검토용 예시 mapping |

`infra/secrets/certs/` 같은 비표준 local-only 경로가 보이더라도 문서 진입점이나 인증서 절차의 기준으로 사용하지 않습니다. 인증서 기준 경로는 항상 `secrets/certs/`입니다.

## Secret Management System

### Registry

- `SENSITIVE_ENV_VARS.md`가 존재하는 환경에서는 secret mapping의 source of truth로 사용합니다.
- 새 환경이나 문서 검토에서는 `SENSITIVE_ENV_VARS.md.example`을 사용합니다.
- registry는 파일 경로, 대응 `.env` 변수, 자동화 상태, 갱신 이력을 추적해야 합니다.

### Automation

```bash
# Generate or sync missing secrets using the approved script
./scripts/operations/gen-secrets.sh

# Generate local TLS certificates when certificate material is required
./scripts/operations/generate-local-certs.sh
```

특정 secret을 교체해야 할 때는 값을 문서에 쓰지 말고, 승인된 운영 절차에 따라 secure input 또는 스크립트 기반 생성 방식으로 처리합니다. 교체 후에는 해당 서비스의 runbook에 따라 재시작과 검증을 수행합니다.

## Security Policy

- `.txt` secret 값 파일은 Git에 커밋하지 않습니다.
- secret 값 파일, private key, token, 인증서 원문을 응답이나 문서에 노출하지 않습니다.
- host filesystem encryption과 Docker secret mount 정책을 운영 환경 기준에 맞게 유지합니다.
- registry와 실제 파일 경로가 달라지면 문서와 검증 절차를 함께 갱신합니다.
- AI Agent는 secret 값 파일 열람이 필요해 보이는 상황에서도 먼저 사용자 승인과 안전한 대체 절차를 요청해야 합니다.

## Related References

- [../README.md](../README.md)
- [../AGENTS.md](../AGENTS.md)
- [../docs/03.specs/infra-secrets-docs-refresh/spec.md](../docs/03.specs/infra-secrets-docs-refresh/spec.md)
- [../docs/05.operations/README.md](../docs/05.operations/README.md)
- [../docs/05.operations/README.md](../docs/05.operations/README.md)
- [../docs/99.templates/readme.template.md](../docs/99.templates/readme.template.md)
- [SENSITIVE_ENV_VARS.md.example](./SENSITIVE_ENV_VARS.md.example)
