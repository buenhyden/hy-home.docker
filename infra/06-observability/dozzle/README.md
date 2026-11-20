---
title: "Dozzle"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-03-27"
---

# Dozzle

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

> Docker 컨테이너 로그를 실시간으로 확인하는 뷰어입니다.

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

Dozzle은 작고 가벼운 애플리케이션으로, 웹 기반 인터페이스에서 Docker 컨테이너 로그를 실시간으로 확인할 수 있습니다. `06-observability` 티어의 일부로, 인프라 내 서비스의 모니터링과 디버깅에 사용됩니다.

###### Audience
<!-- core-payload-level:4 -->

이 README의 주요 독자:

- Operators (로그 모니터링 및 디버깅)
- Developers (서비스 상태 확인)

###### Scope
<!-- core-payload-level:4 -->

###### In Scope
<!-- core-payload-level:5 -->

- Dozzle 서비스 설정 (`docker-compose.yml`)
- 로컬 Docker 컨테이너의 로그 수집 및 표시
- Dozzle native OIDC와 Traefik CIDR 제한을 통한 접근 제어; 공유 cookie ForwardAuth 경로와 구별

###### Out of Scope
<!-- core-payload-level:5 -->

- 중앙 집중식 로그 저장소 (예: Elasticsearch, Loki)
- 로그 로테이션 정책 (Docker 데몬에서 관리)
- 외부 로그 전송

###### Structure
<!-- core-payload-level:4 -->

```text
dozzle/
├── docker-compose.yml    # Service definition
└── README.md             # This file
```

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Traefik 라우터 `dozzle` -> Web UI `${DOZZLE_PORT:-8080}` | `dozzle` | 이 README는 소비자를 기록하지 않는다. | Dozzle native OIDC와 `dozzle-admin-ip` CIDR allowlist로 보호되며 호스트 게시는 없다. | 컨테이너가 안 보이면 필터와 Docker 호스트 공유를 확인하고 Dozzle 런북을 따른다. |
| Docker 소켓 `/var/run/docker.sock:ro` | Docker 데몬 | `dozzle` | 소켓으로 로그를 실시간 스트리밍하며 `:ro`는 Docker API 권한을 읽기 전용으로 제한하지 않는다. | 소켓 경로가 올바르게 마운트되고 Dozzle에 읽기 권한이 있는지 확인한다. |

###### Configuration
<!-- core-payload-level:4 -->

###### Environment Variables
<!-- core-payload-level:5 -->

| Variable               | Required | Description                        |
| ---------------------- | -------: | ---------------------------------- |
| `DOZZLE_PORT`          |       No | Web UI 포트 (기본값: 8080)        |
| `DEFAULT_URL`          |      Yes | Traefik 라우팅을 위한 기본 URL       |
| `DEFAULT_MANAGEMENT_DIR`|      Yes | 영속 데이터 저장 경로   |

###### Security Boundary
<!-- core-payload-level:4 -->

Compose가 참조하는 secret은 `dozzle_client_secret`이며 값은 저장소에 두지 않는다. 호스트로 게시하는 포트 선언은 없다. (출처: `infra/06-observability/dozzle/docker-compose.yml`의 `dozzle` 서비스)

#### Usage

##### Prerequisites

###### Tech Stack
<!-- core-payload-level:4 -->

런타임 이미지 고정 값은 [Compose](docker-compose.yml)에 선언되어 있습니다. [버전 레지스트리](../../tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션입니다.

| Category   | Technology   | Notes                     |
| ---------- | ------------ | ------------------------- |
| Image      | amir20/dozzle | Compose에 선언됨                 |
| Interface  | Web UI       | 실시간 스트리밍       |
| Monitoring | Docker Logs  | `/var/run/docker.sock`를 통해|

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

1. [docker-compose.yml](./docker-compose.yml)을 통해 서비스 구성을 확인한다.
2. 가이드 문서는 Dozzle guide (`docs/05.operations/01.guides/07.observability/0072-dozzle.md`)를 참조한다.
3. 운영 정책은 Dozzle policy (`docs/05.operations/02.policies/07.observability/0072-dozzle.md`)를 확인한다.
4. 장애 조치 지침은 Dozzle runbook (`docs/05.operations/03.runbooks/07.observability/0072-dozzle.md`)를 따른다.

#### Checks

##### Readiness

###### Validation
<!-- core-payload-level:4 -->

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/hardening/check-all-hardening.sh 06-observability`를 실행합니다.
- 루트에서 활성화되는 `admin` 프로필을 검증하려면 `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- `docker logs dozzle`을 확인하고 Docker 소켓 마운트에 접근 가능한지 확인하여 로그 스트리밍을 검증합니다.
- 시작 후 대상 컨테이너가 Dozzle UI에 나타나는지 확인하여 서비스 가시성을 검증합니다.

Docker 소켓의 `:ro` 마운트는 Docker API 호출 권한을 읽기 전용으로 제한하지
않습니다. 로그에 포함된 비밀 정보와 소켓 접근 권한은 운영 정책에 따라 보호합니다.

##### Failure Handling

###### Related Documents
<!-- core-payload-level:4 -->

- **Guide**: `docs/05.operations/01.guides/07.observability/0072-dozzle.md`
- **Policy**: `docs/05.operations/02.policies/07.observability/0072-dozzle.md`
- **Runbook**: `docs/05.operations/03.runbooks/07.observability/0072-dozzle.md`
- [Documentation index](../../../docs/README.md)

###### Service Readiness
<!-- core-payload-level:4 -->

| Field | Evidence |
| --- | --- |
| Purpose | `06-observability`의 Dozzle 서비스 leaf; 서비스: `dozzle`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/06-observability/dozzle/docker-compose.yml` 경로로 루트 include가 활성화됨 |
| Config files | `docker-compose.yml` |
| Config values | 프로필: `admin`, `admin-logs` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/06-observability/dozzle/docker-compose.yml` 경로로 루트 include가 활성화됨 |
| Networks | `edge_net` |
| Volumes | `/var/run/docker.sock:/var/run/docker.sock:ro`, `dozzle-data:/data`, `dozzle-data` |
| Ports | `${DOZZLE_PORT:-8080}` 내부 expose만 선언; 호스트 게시 없음 |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.dozzle.rule`, `traefik.http.routers.dozzle.entrypoints`, `traefik.http.routers.dozzle.tls`, `traefik.http.middlewares.dozzle-admin-ip.ipallowlist.sourcerange`, `traefik.http.routers.dozzle.middlewares`, `traefik.http.services.dozzle.loadbalancer.server.port` |
| Secret refs | `dozzle_client_secret`; OIDC client secret 파일 참조 |
| Healthcheck | `dozzle`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide (`docs/05.operations/01.guides/07.observability/0072-dozzle.md`), Policy (`docs/05.operations/02.policies/07.observability/0072-dozzle.md`), Runbook (`docs/05.operations/03.runbooks/07.observability/0072-dozzle.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) `06-observability` tier; [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) 루트 `admin` 프로필; [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 하드닝 점검부터 시작한 뒤 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

###### Troubleshooting
<!-- core-payload-level:4 -->

- 네트워크, 볼륨, 소켓, 레이블 참조가 올바른지 하드닝 점검으로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- Docker 소켓 오류 시: 소켓 경로(`/var/run/docker.sock`)가 올바르게 마운트되어 있고 Dozzle에 읽기 권한이 있는지 확인합니다.
- 컨테이너가 보이지 않을 때: Dozzle의 필터 설정과 대상 컨테이너가 동일한 Docker 호스트를 공유하는지 확인합니다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
