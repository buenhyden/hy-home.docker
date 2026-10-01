---
title: "Open Notebook"
version: "1.0.2"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-05-09"
---

# Open Notebook

> 로컬 지식 노트북이자 SurrealDB 기반 laboratory 서비스입니다.

## Overview

Open Notebook은 로컬 지식 워크플로우를 위한 admin/laboratory 노트북 인터페이스를 제공합니다. 이 스택은 `open_notebook` 애플리케이션과 영속화 전용 `surrealdb` 데이터베이스 백엔드를 함께 실행하며 둘은 `ai_net`으로 상호 연결됩니다.

Lifecycle: **OPTIONAL**. 루트 Compose가 이 정의를 include하며 명시적 프로필(`notebook`, `surrealdb`)이 활성화를 제어합니다.

## Audience

- **Operators**: 로컬 laboratory 서비스, 데이터 영속화, 자격 증명 관리.
- **Developers**: 노트북 기반 AI 또는 지식 워크플로우 테스트.
- **AI Agents**: 서비스 경계, 시크릿, 검증 경로 파악.

## Scope

### In Scope

- `open_notebook`과 `surrealdb`의 Docker Compose 정의.
- `${DEFAULT_MANAGEMENT_DIR}` 하위의 로컬 영속 볼륨(`open-notebook-data`, `surrealdb-data`).
- Traefik 라우팅, admin IP allowlist, 애플리케이션 비밀번호를 통한 Open Notebook의 게이트웨이 노출.
- 노트북 비밀번호, 암호화 키, 데이터베이스 자격 증명용 Docker Secret 사용.
- 커스텀 SurrealDB 런타임용 다단계 빌드 컨텍스트(`surrealdb/Dockerfile`).

### Out of Scope

- 프로덕션 노트북 승격 정책.
- 노트북 데이터 내부의 사용자 콘텐츠 거버넌스.
- 외부 모델 provider 자격 증명이나 비공개 노트북 내보내기.

## Structure

```text
open-notebook/
├── docker-compose.yml        # Open Notebook and SurrealDB service definitions
├── surrealdb/                # SurrealDB custom build context
│   ├── Dockerfile            # Multi-stage build definition
│   ├── docker-entrypoint.sh  # Secret-aware entrypoint script
│   └── README.md             # SurrealDB package documentation
└── README.md                 # This file
```

- [docker-compose.yml](docker-compose.yml)
- [surrealdb/Dockerfile](surrealdb/Dockerfile)
- [surrealdb/docker-entrypoint.sh](surrealdb/docker-entrypoint.sh)
- [surrealdb/README.md](surrealdb/README.md)

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `08-ai`의 Open Notebook 서비스 leaf; 서비스: `open_notebook`, `surrealdb`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/open-notebook/docker-compose.yml` 경로로 루트 include가 활성화됨 |
| Config files | `docker-compose.yml`, `surrealdb/Dockerfile`, `surrealdb/docker-entrypoint.sh` |
| Config values | 환경 변수 키: `SURREALDB_USERNAME`, `SURREALDB_NAMESPACE`, `SURREALDB_DATABASE`, `OPEN_NOTEBOOK_PASSWORD_FILE`, `OPEN_NOTEBOOK_ENCRYPTION_KEY_FILE`, `API_URL`, `SURREAL_URL`, `SURREAL_USER`, `OLLAMA_API_BASE`; 프로필: `notebook`, `surrealdb` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/open-notebook/docker-compose.yml` 경로로 루트 include가 활성화됨 |
| Networks | `ai_net`, `edge_net` |
| Volumes | `open-notebook-data:/app/data`, `surrealdb-data:/mydata` |
| Ports | Loopback 전용 API 포트 `127.0.0.1:${OPEN_NOTEBOOK_API_URL:-5055}:5055`; Traefik은 `expose`를 통한 내부 web 포트 `${OPEN_NOTEBOOK_WEB_URL:-8502}`을 대상으로 함; SurrealDB 내부 포트 `8000`은 `expose`로 노출 |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.open-notebook.rule`, `traefik.http.routers.open-notebook.entrypoints`, `traefik.http.routers.open-notebook.tls`, `traefik.http.middlewares.open-notebook-admin-ip.ipallowlist.sourcerange`, `traefik.http.routers.open-notebook.middlewares`, `traefik.http.services.open-notebook.loadbalancer.server.port` |
| Secret refs | 이름: `surreal_db_password`, `open_notebook_password`, `open_notebook_encryption_key`; 마운트: `/run/secrets/surreal_db_password`, `/run/secrets/open_notebook_password`, `/run/secrets/open_notebook_encryption_key` |
| Healthcheck | `surrealdb`와 `open_notebook`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide (`docs/05.operations/guides/0073-open-notebook.md`), Policy (`docs/05.operations/policies/0073-open-notebook.md`), Runbook (`docs/05.operations/runbooks/0073-open-notebook.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) `08-ai` tier; [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) 루트 `notebook` 프로필; [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 하드닝 점검부터 시작한 뒤 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. `HYHOME_COMPOSE_PROFILES="notebook" bash scripts/validation/validate-docker-compose.sh`로 루트에서 활성화되는 laboratory 프로필을 검증합니다.
2. `notebook` 프로필이 의도적으로 선택된 경우에만 시작합니다. `admin`은 더 이상 Open Notebook이나 SurrealDB를 선택하지 않습니다.
3. 허용된 CIDR 범위에서 `https://open-notebook.${DEFAULT_URL}`로 Open Notebook UI에 접속해 Open Notebook 비밀번호로 로그인합니다. 이 라우트는 의도적으로 공유 SSO 미들웨어를 사용하지 않습니다. API 호스트 포트는 loopback에서만 응답합니다.
4. floating 이미지 사용은 `infra/image-tag-policy.exceptions.json`을 통해 계속 검토합니다.
5. 자격 증명의 원본은 Docker Secret으로 관리하며 평문 값을 커밋하지 않습니다. 현재 시작 스크립트는 일부 값을 런타임 프로세스 환경으로 내보내므로 환경 덤프를 증거로 수집하지 않습니다.

## Tech Stack

런타임 이미지 고정 값은 [Compose](docker-compose.yml)와 참조된 Dockerfile에 선언되어 있습니다. [버전 레지스트리](../../tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션입니다.

| Component | Image / Source | Purpose |
| --- | --- | --- |
| `open_notebook` | [declared runtime image](../../tech-stack.versions.json) | 노트북 UI 및 API 런타임 |
| `surrealdb` | [Dockerfile](surrealdb/Dockerfile) | 로컬 메타데이터 및 노트북 영속화(Open Notebook 호환을 위해 SurrealDB v2에 고정) |

## Configuration

### Services

| Service | Profiles | Networks | Host ports | Volumes | Secrets |
| --- | --- | --- | --- | --- | --- |
| `open_notebook` | `notebook` | `ai_net`, `edge_net` | `127.0.0.1:${OPEN_NOTEBOOK_API_URL:-5055}:5055` | `open-notebook-data:/app/data` | `surreal_db_password`, `open_notebook_password`, `open_notebook_encryption_key` |
| `surrealdb` | `notebook`, `surrealdb` | `ai_net` | 없음 (`expose: 8000`) | `surrealdb-data:/mydata` | `surreal_db_password` |

### Environment Variables

| Variable | Required | Service | Description |
| --- | :---: | --- | --- |
| `SURREALDB_USERNAME` | Yes | `open_notebook`, `surrealdb` | SurrealDB용 데이터베이스 사용자명 |
| `SURREALDB_NAMESPACE` | Yes | `open_notebook` | Open Notebook이 사용하는 네임스페이스 |
| `SURREALDB_DATABASE` | Yes | `open_notebook` | 네임스페이스 내 데이터베이스명 |
| `DEFAULT_URL` | Yes | `open_notebook` | Traefik 라우팅용 기본 도메인 |
| `DEFAULT_MANAGEMENT_DIR` | Yes | Global | 영속 바인드 마운트용 기본 호스트 디렉터리 |
| `OPEN_NOTEBOOK_API_URL` | No | `open_notebook` | API용 loopback 호스트 포트 (기본값: 5055) |
| `OPEN_NOTEBOOK_WEB_URL` | No | `open_notebook` | Web UI 내부 포트 (기본값: 8502) |
| `LAB_ALLOWED_CIDRS` | No | Traefik | admin 엔드포인트용 IP allowlist |

### Traefik Routing

Open Notebook은 `gateway-standard-chain@file`, `open-notebook-admin-ip@docker`, `large-body@file`을 사용해 `websecure`에서 Traefik으로 라우팅됩니다. 공유 SSO는 의도적으로 없으며(소유자 결정, 커밋 `b90b74837`) 접근은 CIDR allowlist와 Open Notebook 비밀번호로 제어합니다.

### Database Compatibility

이 저장소의 승인된 호환성 경계는 SurrealDB v2입니다. [Dockerfile](surrealdb/Dockerfile)은
변경 가능한 `surrealdb/surrealdb:v2` 태그를 사용하므로 정확한 패치 버전이나 digest를
보장하지 않습니다. 선택된 Open Notebook 이미지와의 호환성·데이터 이전을 검증하고
별도 변경 승인을 받기 전에는 v3 이상으로 업그레이드하지 않습니다.

### Secret Management

- `surreal_db_password`: SurrealDB의 root 인증과 Open Notebook의 데이터베이스 연결 수립에 사용됩니다.
- `open_notebook_password`: 애플리케이션 수준 접근 제어에 사용되는 비밀번호입니다.
- `open_notebook_encryption_key`: Open Notebook이 모델 API 키를 암호화·복호화하는 데 사용합니다. 이 키를 잃으면 저장된 자격 증명을 복구할 수 없습니다.

## Image Tag Review

- `infra/08-ai/open-notebook/docker-compose.yml`은 현재 [declared runtime image](../../tech-stack.versions.json)를 사용합니다. latest에 가까운 태그입니다.
- 이 태그는 `infra/image-tag-policy.exceptions.json`에 등록되어 매월 Laboratory Operator가 검토합니다. 이후 승인된 작업이 안정 태그를 고정하거나 예외를 제거하지 않는 한 그대로 유지합니다.

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/hardening/check-all-hardening.sh 08-ai`를 실행합니다.
- 루트에서 활성화되는 laboratory 프로필을 검증하려면 `HYHOME_COMPOSE_PROFILES="notebook" bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.
- 승인된 실행 환경에서 `docker compose --profile notebook logs --tail=200 open_notebook`으로 상태를 점검합니다. 로그나 `/app/data` 디렉터리 존재만으로 영속화·복구 성공을 입증하지는 못합니다.
- `http://127.0.0.1:8000`은 SurrealDB 컨테이너 내부 헬스체크 대상입니다. 호스트 포트는 게시하지 않으며 이 응답이 애플리케이션 인증·쿼리 성공을 대신하지 않습니다.

## Troubleshooting

- Open Notebook, SurrealDB, 네트워크, 시크릿 참조를 확인하려면 하드닝 점검부터 시작합니다.
- API URL, 암호화, 데이터베이스 설정을 변경하기 전에 Open Notebook과 SurrealDB 로그를 확인합니다.
- **SurrealDB Version Compatibility**: 현재 승인된 경계는 v2이며, 선택된 이미지의 v3 호환성과 데이터 이전은 검증되지 않았습니다. 별도 검증과 승인 전에는 업그레이드하지 않습니다.
- **Encryption Key Loss**: `OPEN_NOTEBOOK_ENCRYPTION_KEY`를 변경하거나 잃으면 기존에 암호화된 provider API 키를 읽을 수 없게 됩니다. 키는 데이터베이스 백업과 별도로 보관합니다.
- **Database Dependency**: Open Notebook은 SurrealDB의 HTTP `is-ready` 헬스체크가 통과할 때까지 대기합니다. 애플리케이션 연결 주소는 별도의 `ws://surrealdb:8000/rpc`입니다. Open Notebook이 시작에 실패하면 SurrealDB 컨테이너 로그를 확인합니다.

## Related Documents

- **Guide**: Open Notebook usage guide (`docs/05.operations/guides/0073-open-notebook.md`)
- **Policy**: Open Notebook operations policy (`docs/05.operations/policies/0073-open-notebook.md`)
- **Runbook**: Open Notebook recovery runbook (`docs/05.operations/runbooks/0073-open-notebook.md`)
- **SurrealDB Guide**: SurrealDB usage guide (`docs/05.operations/guides/0080-surrealdb.md`)
- **SurrealDB Policy**: SurrealDB operations policy (`docs/05.operations/policies/0080-surrealdb.md`)
- **SurrealDB Runbook**: SurrealDB recovery runbook (`docs/05.operations/runbooks/0080-surrealdb.md`)
- [Image tag exceptions](../../image-tag-policy.exceptions.json)
- [Documentation index](../../../docs/README.md)
- [Infrastructure index](../../README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.
