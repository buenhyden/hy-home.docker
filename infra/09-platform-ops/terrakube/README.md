---
title: "Terrakube IaC Automation Platform"
version: "1.0.4"
type: "common/package-readme"
status: "review"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

<!-- [ID:09-platform-ops:terrakube] -->
# Terrakube IaC Automation Platform

> Terraform 오케스트레이션, 원격 상태, 프라이빗 레지스트리 서비스 스택입니다.

## Overview

`infra/09-platform-ops/terrakube/`는 중앙 집중식 Terraform 워크플로우를 위한 Terrakube 서비스 스택을 정의합니다. 이 스택은 Compose에 선언된 Terrakube 이미지를 사용하는 API, UI, executor 서비스를 포함합니다. 신원 확인은 Keycloak과 통합해 처리하고 메타데이터는 관리용 PostgreSQL 서비스에 저장하며 Terraform 상태에는 SeaweedFS 호환 S3 스토리지를 사용합니다.

이 README는 서비스 수준 진입점입니다. Compose 구성을 요약하고 정식 가이드, 운영 정책, 런북으로 연결합니다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Terrakube API, UI, executor의 Compose 서비스 경계
- 게이트웨이 호스트명과 내부 서비스 관계
- 메타데이터, 상태 저장소, Docker secret 사용에 대한 상위 수준 설명
- 관련 가이드, 운영, 런북 링크

### Out of Scope

- 시크릿 값이나 자격 증명 자료
- Terraform 모듈 작성 표준
- 장문의 IaC 거버넌스 정책
- 클라우드 provider 계정 설정

## Structure

```text
terrakube/
├── docker-compose.yml  # Terrakube API, UI, and executor service definitions
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `09-platform-ops`의 Terrakube IaC Automation Platform 서비스 leaf; 서비스: `terrakube-api`, `terrakube-ui`, `terrakube-executor`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-platform-ops/terrakube/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml` |
| Config values | env 키: `ApiDataSourceType`, `DatasourceHostname`, `DatasourceDatabase`, `DatasourceUser`, `DatasourcePassword_FILE`, `GroupValidationType`, `UserValidationType`, `AuthenticationValidationType` 외 다수; 프로필: `iac` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-platform-ops/terrakube/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | `edge_net`, `mng_data_net`, `object_net`, `terrakube_net` |
| Volumes | `/var/run/docker.sock:/var/run/docker.sock` |
| Ports | 선언되지 않음 |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.terrakube-api.rule`, `traefik.http.routers.terrakube-api.entrypoints`, `traefik.http.routers.terrakube-api.tls`, `traefik.http.routers.terrakube-api.middlewares`, `traefik.http.services.terrakube-api.loadbalancer.server.port`, `traefik.http.routers.terrakube-ui.rule` 외 다수 |
| Secret refs | 이름: `terrakube_db_password`, `seaweedfs_s3_terrakube_secret_key`, `terrakube_valkey_password`, `terrakube_pat_secret`, `terrakube_internal_secret`; 마운트: `/run/secrets/terrakube_db_password`, `/run/secrets/seaweedfs_s3_terrakube_secret_key`, `/run/secrets/terrakube_valkey_password`, `/run/secrets/terrakube_pat_secret`, `/run/secrets/terrakube_internal_secret` |
| Healthcheck | `terrakube-api`, `terrakube-ui`, `terrakube-executor`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide (`docs/05.operations/guides/0069-terrakube.md`), Policy (`docs/05.operations/policies/0069-terrakube.md`), Runbook (`docs/05.operations/runbooks/0069-terrakube.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | hardening 점검으로 시작한 뒤 승인된 런타임 컨텍스트에서 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. Terrakube를 변경하기 전에 상위 [`../README.md`](../README.md)와 이 서비스의 Compose 파일을 읽습니다.
2. 시크릿 자료는 Docker secrets에 유지하고 시크릿 이름과 용도만 문서화합니다.
3. 스택을 변경할 때는 API, UI, executor, PostgreSQL, SeaweedFS, Valkey, Keycloak 가정을 함께 검증합니다.
4. 사용자 접근, 상태 처리, 복구 동작이 바뀌면 관련 가이드, 운영, 런북을 업데이트합니다.

## Tech Stack

| Component | Image / Source | Role |
| --- | --- | --- |
| `terrakube-api` | [declared runtime image](../../tech-stack.versions.json) | API 서버 및 메타데이터 오케스트레이션 |
| `terrakube-ui` | [declared runtime image](../../tech-stack.versions.json) | 웹 관리 UI |
| `terrakube-executor` | [declared runtime image](../../tech-stack.versions.json) | Terraform 작업 실행 |
| Metadata | Management PostgreSQL | Terrakube 데이터베이스 |
| State storage | SeaweedFS S3 버킷 `tfstate` | Terraform 상태와 출력 저장 |
| Identity | Keycloak / DEX 검증 | SSO 통합 |

## Usage Instructions

`iac` 프로필로 스택이 활성화된 이후에는 다음 라우팅된 엔드포인트를 사용합니다.

- API: `https://terrakube-api.${DEFAULT_URL}`
- UI: `https://terrakube-ui.${DEFAULT_URL}`
- API docs: `https://terrakube-api.${DEFAULT_URL}/swagger-ui.html`

## Validation

- Compose나 설정 참조를 변경한 후에는 `bash scripts/hardening/check-all-hardening.sh 09-platform-ops`을 실행합니다.
- 문서를 준비 완료로 표시하기 전에 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.
- Terrakube UI에서 워크스페이스 설정을 검증하고 Terraform 워크스페이스가 올바른 provider 자격 증명으로 등록되어 있는지 확인합니다.
- 설정 변경 후 `terrakube-api`, `terrakube-ui`, `terrakube-executor` 로그에서 API 연결을 확인합니다.
- Keycloak 클라이언트 설정이 Terrakube의 인증 설정과 일치하는지 확인하여 OIDC 인증을 검증합니다.
- API와 UI는 여전히 OAuth2 Proxy 클라이언트 ID를 재사용하며 API 라우트의 ForwardAuth가 Terraform CLI, API 토큰 호출, 공개 URL로 API를 호출하는 `terrakube-executor`를 차단합니다. `iac` 활성화 전에 별도 변경 검토·승인으로 다음을 해결해야 합니다: 전용 공개 클라이언트 `home-terrakube`, API 라우트에서 ForwardAuth 제거(또는 executor용 내부 API URL), executor 라우트의 SSO 여부 결정, 실제 audience/RBAC 확인(GDE-0079).

## Troubleshooting

- Terrakube 네트워크, 데이터베이스, 시크릿 참조가 계속 선언되어 있는지 hardening 점검으로 먼저 확인합니다.
- executor, PAT, 영속화 설정을 변경하기 전에 Terrakube 로그와 연결된 런북을 확인합니다.

## Related Documents

- [Platform Operations tier README](../README.md)
- Terrakube guide (`docs/05.operations/guides/0069-terrakube.md`)
- Terrakube operations policy (`docs/05.operations/policies/0069-terrakube.md`)
- Terrakube recovery runbook (`docs/05.operations/runbooks/0069-terrakube.md`)
- [Root infra README](../../README.md)
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.
