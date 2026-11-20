---
title: "Qdrant"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2025-11-12"
---

# Qdrant

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

> 고성능 벡터 유사도 검색 엔진입니다.

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

`qdrant` 서비스는 AI/ML 애플리케이션을 위한 벡터 데이터베이스 계층을 제공하며 고차원 임베딩의 빠른 의미 검색을 가능하게 합니다. `04-data` tier 안에 위치하며 Retrieval-Augmented Generation(RAG) 워크플로의 핵심 구성 요소입니다.

###### Audience
<!-- core-payload-level:4 -->

이 README의 주요 독자:

- AI/ML Engineers(벡터 검색 통합)
- Operators(자원 튜닝과 snapshot)
- Documentation Writers

###### Scope
<!-- core-payload-level:4 -->

###### In Scope
<!-- core-payload-level:5 -->

- Qdrant unprivileged 컨테이너 설정(`docker-compose.yml`)
- REST 6333(SSO 뒤에서 라우팅)과 gRPC 6334(네트워크 내부 전용)
- Snapshot 저장 설정(`/qdrant/storage/snapshots`)
- Telemetry와 서비스 헬스 모니터링

###### Out of Scope
<!-- core-payload-level:5 -->

- 벡터 임베딩 생성(upstream 모델이 담당)
- collection 수준의 스키마 설계(시스템 가이드 `docs/05.operations/01.guides/09.ai-and-search/0034-qdrant.md` 참조)
- 운영 통제(운영 정책 `docs/05.operations/02.policies/09.ai-and-search/0034-qdrant.md` 참조)
- 헬스와 복구 triage(복구 런북 `docs/05.operations/03.runbooks/09.ai-and-search/0034-qdrant.md` 참조)

###### Structure
<!-- core-payload-level:4 -->

```text
qdrant/
├── docker-compose.yml    # 서비스 정의
└── README.md            # 이 파일
```

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| REST `${QDRANT_PORT:-6333}` | `qdrant` | 이 README는 소비자를 기록하지 않는다. | HTTP REST이며 SSO 뒤에서 라우팅되고 `qdrant_api_key` API key가 필요하다. | key가 없으면 health 엔드포인트만 응답하며 `/readyz`와 Compose 헬스체크로 확인하고 RUN-0034를 따른다. |
| gRPC `${QDRANT_GRPC_PORT:-6334}` | `qdrant` | 이 README는 소비자를 기록하지 않는다. | gRPC이며 네트워크 내부 전용이다. | 이 README는 실패 처리를 기록하지 않는다. |
| Prometheus 스크레이프 | `qdrant` | Prometheus | `qdrant_read_only_api_key`의 read-only key로 스크레이프한다. | 이 README는 실패 처리를 기록하지 않는다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

호스트로 게시하는 포트 선언이 없다. 연결 네트워크는 `ai_net`, `edge_net`, `obs_net`이다. (출처: `infra/04-data/qdrant/docker-compose.yml`의 `qdrant` 서비스)

###### Security Boundary
<!-- core-payload-level:4 -->

Compose가 참조하는 secret은 `qdrant_api_key`, `qdrant_read_only_api_key`이며 값은 저장소에 두지 않는다. 호스트로 게시하는 포트 선언은 없다. (출처: `infra/04-data/qdrant/docker-compose.yml`의 `qdrant` 서비스)

#### Usage

##### Prerequisites

###### Tech Stack
<!-- core-payload-level:4 -->

| Category   | Technology   | Notes                          |
| ---------- | ------------ | ------------------------------ |
| Engine     | [선언된 runtime 이미지](../../tech-stack.versions.json) | 단일 unprivileged 서비스 |
| REST API   | HTTP         | 포트 6333                      |
| gRPC API   | gRPC         | 포트 6334                      |
| Persistence | Local Bind  | `${DEFAULT_DATA_DIR}/qdrant/data` |

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

1. RAG 통합 패턴을 위해 시스템 가이드 (`docs/05.operations/01.guides/09.ai-and-search/0034-qdrant.md`)를 검토합니다.
2. 배포 시 `ai`나 `qdrant` profile이 활성화되어 있는지 확인합니다.
3. Snapshot은 persistent volume 안에 설정됩니다. owner 승인 백업 작업 전에 경로 매핑을 확인합니다.
4. `/readyz` 엔드포인트로 헬스를 모니터링합니다.

#### Checks

##### Readiness

###### Validation
<!-- core-payload-level:4 -->

Classification은 `HOME`입니다. Qdrant는 `qdrant_api_key`(AI-008)의 API key가
필요하며 이것이 없으면 health 엔드포인트만 응답합니다. Prometheus는
`qdrant_read_only_api_key`(AI-009)의 read-only key로 스크레이프합니다.
Snapshot 복구는 동일 minor 또는 다음 minor의 새로운 target, 별도로 승인된
force가 아닌 한 존재하지 않는 목적지 collection, snapshot 크기의 약 2배에
해당하는 여유 디스크를 사용합니다. 소유 artifact는 `GDE-0034`, `POL-0034`,
`RUN-0034`입니다.

- Qdrant에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- Qdrant 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

##### Failure Handling

###### Related Documents
<!-- core-payload-level:4 -->

- Specialized 가이드 (`docs/05.operations/01.guides/README.md`)
- Qdrant 시스템 가이드 (`docs/05.operations/01.guides/09.ai-and-search/0034-qdrant.md`)
- Qdrant 운영 정책 (`docs/05.operations/02.policies/09.ai-and-search/0034-qdrant.md`)
- Qdrant 복구 런북 (`docs/05.operations/03.runbooks/09.ai-and-search/0034-qdrant.md`)
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 검증을 제공합니다.

###### Service Readiness
<!-- core-payload-level:4 -->

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 Qdrant 서비스 leaf; services: `qdrant`; [root docker-compose.yml](../../../docker-compose.yml)을 통해 root include 활성화 -> `infra/04-data/qdrant/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | 환경 키는 Compose가 소유함; exact profiles: `ai`, `ai-llm`, `qdrant` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)을 통해 root include 활성화 -> `infra/04-data/qdrant/docker-compose.yml` |
| Networks | `ai_net`, `edge_net`, `obs_net` |
| Volumes | `qdrant-data:/qdrant/storage:rw`, `qdrant-data` |
| Ports | `${QDRANT_PORT:-6333}`, `${QDRANT_GRPC_PORT:-6334}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.qdrant.rule`, `traefik.http.routers.qdrant.entrypoints`, `traefik.http.routers.qdrant.tls`, `traefik.http.routers.qdrant.middlewares`, `traefik.http.services.qdrant.loadbalancer.server.port` |
| Secret refs | `qdrant_api_key`, `qdrant_read_only_api_key` |
| Healthcheck | `qdrant`에 Compose healthcheck 선언됨 |
| Operations | Guide (`docs/05.operations/01.guides/09.ai-and-search/0034-qdrant.md`), Policy (`docs/05.operations/02.policies/09.ai-and-search/0034-qdrant.md`), Runbook (`docs/05.operations/03.runbooks/09.ai-and-search/0034-qdrant.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

###### Troubleshooting
<!-- core-payload-level:4 -->

- `docker compose config --quiet`로 Qdrant volume, 네트워크, label 참조가 정상 렌더링되는지 먼저 확인합니다.
- collection, snapshot, persistence 설정을 변경하기 전에 Qdrant 로그와 연결된 runbook을 확인합니다.

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
