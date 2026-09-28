---
title: "11-laboratory - Management & Laboratory Tier"
version: "1.1.4"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-03-26"
---

# 11-laboratory - Management & Laboratory Tier

## Overview

이 티어는 선택적 관리 도구를 담고 있습니다. 루트 프로젝트는 다섯 개의
leaf를 모두 include하며 프로필이 실제 서비스를 선택합니다.

| Service | Profiles | Authority and risk |
| --- | --- | --- |
| `dozzle` | `admin`, `admin-logs` | Docker 로그; 읽기 전용 소켓이더라도 강력한 Docker API 가시성을 부여함 |
| `redisinsight` | `admin`, `admin-data` | 로컬 연결/설정 데이터베이스; 대상 Redis/Valkey 데이터는 외부에 남음 |
| `open_notebook` | `notebook` | 애플리케이션 데이터/provider 자격 증명과 암호화 키 보관; 앱 비밀번호와 admin CIDR을 사용하며 공유 SSO 없음 |
| `surrealdb` | `notebook`, `surrealdb` | `open-notebook/surrealdb/` 하위에 함께 위치한 Open Notebook 데이터베이스 |
| `mlflow`, `mlflow-db-provision` | `mlops`, `data-science` | `mng-pg`의 추적 데이터베이스와 버킷 범위 SeaweedFS 아티팩트; `ai_net`의 SDK 경로는 인증 없음 |
| `jupyterlab` | `data-science` | 필수 서버 토큰을 사용하는 단일 사용자 코드 실행; JupyterHub 아님 |

이 서비스들에는 `dev` 프로필이 없습니다. Dozzle과 RedisInsight는 Open
Notebook 없이도 실행할 수 있습니다. `notebook`을 선택하면 루트 프로젝트를
통해 Open Notebook과 그 SurrealDB 의존성이 함께 활성화됩니다.

## Audience

인프라 관리자, laboratory 사용자, 보안 검토자, 선택적 admin 도구 경계를
담당하는 문서화 agent.

## Scope

이 티어는 Dozzle, RedisInsight, Open Notebook(함께 위치한 SurrealDB 포함),
MLflow, JupyterLab의 선언과 그 접근/영속화 계약을 소유합니다. `admin`은
Dozzle과 RedisInsight만 선택합니다.
대상 Redis/Valkey 데이터, 복사된 Docker 로그, provider 계정, 프로덕션
노트북 워크로드, Metabase는 소유하지 않습니다.

## Structure

```text
11-laboratory/
├── dozzle/
├── jupyterlab/
├── mlflow/
├── open-notebook/
├── redisinsight/
└── README.md
```

## Configuration

세 UI 모두 추적 중인 gateway/allowlist/ForwardAuth 통제가 적용된 Traefik
라우트를 사용합니다. Dozzle에는 네이티브 OIDC 설정도 있으며 그 Docker
소켓은 여전히 호스트 보안 경계입니다. Dozzle의 `/data`는 설정을 저장할 뿐
복사된 컨테이너 로그를 저장하지 않습니다. RedisInsight의 `/data`는 민감한
연결 메타데이터를 저장하며 현재 추적되는 `RI_ENCRYPTION_KEY`가 없습니다.
Open Notebook `/app/data`, SurrealDB `/mydata`, Open Notebook 암호화 키는
하나의 복구 세트를 이루며 키를 잃으면 저장된 provider 시크릿을 읽을 수
없게 될 수 있습니다. 대상 Redis/Valkey 백업은 대상 데이터 서비스가
소유합니다.

## How to Work in This Area

[documentation index](../../docs/README.md)를 사용한 뒤,
`docs/05.operations/README.md` 아래의 정확한 Stage 05 대상
`0072-dozzle`, `0073-open-notebook`, `0076-redisinsight`를 확인합니다.
저장소 루트에서 실행합니다.

```bash
HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 11-laboratory
```

정적 검증은 런타임 접근, Docker API 안전성, provider egress, 복구 근거가
되지 않습니다. Compose/Dockerfile 선언이 런타임 고정 값을 소유하며
[tech-stack.versions.json](../tech-stack.versions.json)은 파생된 이미지
프로젝션입니다.

## Related Documents

- [Documentation index](../../docs/README.md)
- [Infrastructure index](../README.md)
- Stage 05 laboratory package: `docs/05.operations/README.md`
