---
title: Compose Profile Vocabulary Policy
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0078
parent_ids: []
created: 2026-09-04
updated: 2026-09-04
---

# Compose Profile Vocabulary Policy

## Overview

이 문서는 `infra/` 하위 Compose 파일이 선언하는 profile 이름 24개의 canonical
정의를 소유한다. Compose profile은 이 workspace에서 stack 구성원을 선택하는
유일한 runtime 메커니즘이므로, 이름 하나하나가 무엇을 선택하는지 여기에서
확정한다.

`include:`는 파일을 무조건 병합하고 profile이 선택을 담당한다. 따라서 어떤
서비스가 뜨는지는 파일 목록이 아니라 선택한 profile 이름이 결정한다.

## Policy Scope

- 대상: `infra/**/docker-compose*.yml`과 `infra/**/docker-compose*.yaml`이
  선언하는 모든 `profiles:` 값
- 목적: 선언된 이름과 등록된 정의를 1:1로 유지하고, 동시 선택이 불가능한
  이름 쌍을 명시
- 비대상: profile이 선택한 뒤의 서비스 설정 내용, 이미지 버전, secret 값,
  network 주소 체계

- **Systems**: `infra/` 하위 Compose 파일 47개 중 root가 include하는 41개, 서비스 127개
- **Agents**: Infra/DevOps/Operations 역할의 에이전트
- **Environments**: Local, Dev, Stage, Production-like

## Definitions

아래 세 표의 서비스 수는 root가 include하는 41개 파일 기준이며,
`docker compose config --services`가 해당 profile 하나만 선택했을 때 내놓는
수와 일치한다. SPEC-0171이 보류한 6개 파일의 서비스는 세지 않는다.

profile 이름은 세 종류로 나뉜다.

- **Domain selector**: `infra/NN-<domain>` 한 영역을 통째로 선택한다.
- **Topology selector**: 같은 영역의 서로 다른 구성 형태를 고른다.
- **Role selector**: 한 영역 안에서 서비스의 역할을 고른다. 같은 제품을 다른
  용도로 두 번 띄우는 경우가 이에 해당한다.

### Domain selector

| Profile | 선택 대상 | 서비스 |
| --- | --- | ---: |
| `auth` | `02-auth` | 2 |
| `security` | `03-security` | 2 |
| `data` | `04-data` | 58 |
| `messaging` | `05-messaging` | 8 |
| `obs` | `06-observability`와 `04-data`의 exporter | 18 |
| `workflow` | `07-workflow` | 12 |
| `ai` | `08-ai`와 `04-data`의 vector store | 4 |
| `tooling` | `09-tooling` | 10 |
| `communication` | `10-communication` | 2 |
| `admin` | `11-laboratory`의 관리 UI | 6 |

`01-gateway`는 전용 domain selector가 없다. 기본 gateway인 traefik은 `core`가,
대체 gateway인 nginx는 `nginx`가 선택한다.

### Topology selector

| Profile | 선택 대상 | 서비스 |
| --- | --- | ---: |
| `core` | 최소 도달 가능 stack: gateway, auth, security | 5 |
| `dev` | 개발용 구성 변형 | 47 |
| `nginx` | traefik 대신 nginx를 gateway로 사용 | 2 |
| `messaging-option` | messaging 선택 구성 요소 | 1 |
| `ksql` | analytics 선택 구성 요소 | 3 |
| `storage-cluster` | 단일 노드 minio 대신 4노드 minio 클러스터 | 4 |

### Role selector

| Profile | 선택 대상 | 서비스 |
| --- | --- | ---: |
| `service` | 애플리케이션용 데이터 인스턴스 | 19 |
| `mng` | 관리용 데이터 인스턴스 | 5 |
| `storage` | object/lake 역할 | 2 |
| `graph` | graph 데이터 역할 | 1 |
| `iac` | IaC 도구 역할 | 4 |
| `registry` | 컨테이너 registry 역할 | 1 |
| `sast` | 정적 분석 역할 | 1 |
| `sync` | 파일 동기화 역할 | 1 |
| `testing` | 부하 시험 역할 | 2 |

## Controls

- **Required**:
  - `infra/` 하위 모든 서비스는 `profiles:`를 최소 하나 선언한다. 선언이 없는
    서비스는 profile을 고르지 않아도 기동되어 "선택으로만 기동한다"는 전제를
    깨뜨린다.
  - 새 profile 이름을 도입하면 같은 논리 변경에서 이 문서에 행을 추가한다.
  - 상호 배타 쌍을 새로 만들면 아래 표에 근거와 함께 기록한다.
  - `depends_on` 대상은 출발 서비스의 모든 profile을 함께 선언한다. 이 규칙이
    깨지면 해당 profile은 `depends on undefined service`로 렌더링 자체가
    실패한다. 규칙은 전이적이므로 의존 그래프의 폐포까지 닫아야 한다.
- **Allowed**:
  - 한 서비스가 여러 profile을 선언하는 것. 예로 `k6-master`는 `tooling`과
    `testing`을 함께 선언한다.
  - domain selector와 topology selector의 동시 선택.
- **Disallowed**:
  - 등록되지 않은 이름 선언.
  - 아래 상호 배타 쌍의 동시 선택.
  - 한 profile이 선택하는 두 서비스가 같은 host port를 공개하는 구성.

### 상호 배타 쌍

| 쌍 | 충돌 | 근거 |
| --- | --- | --- |
| `nginx` ↔ `core`, `nginx` ↔ `dev` | host port 80, 443 | nginx와 traefik은 같은 역할의 대체재이며 동시에 gateway가 될 수 없다 |
| `storage-cluster` ↔ `storage` | host port 충돌 없음 | 두 minio 토폴로지는 대체재다. 두 파일이 서비스 이름을 공유하지 않아 host port는 부딪히지 않지만, 동시에 띄우면 같은 network에 독립된 object store가 둘 생긴다 |

`testing`은 `k6-master`와 `locust-master`를 함께 선택한다. 두 서비스는 원래
`LOCUST_HOST_PORT` 하나를 공유해 18089에서 충돌했으므로, k6에 `K6_HOST_PORT`
(기본 18189)를 분리 배정했다. 이제 배타 쌍이 아니다.

## Exceptions

- `00-workspace`와 `12-infra-net`은 운영 catalog domain이지만 `infra/` 대응
  디렉터리가 없으므로 domain selector를 갖지 않는다. 결함이 아니다.
- `infra/` 하위 6개 sibling 쌍은 양쪽이 같은 서비스 이름을 선언하여 동시
  include가 불가능하다. 이 쌍의 topology selector는 SPEC-0171이 결정할 때까지
  등록하지 않는다.
- 이미 함께 include된 두 파일 사이의 host port 충돌은 이 정책 이전부터
  존재하는 결함으로, 발견 시 기록하고 별도 변경으로 처리한다.

## Verification

```bash
bash scripts/validation/validate-docker-compose.sh
```

이 명령은 선언된 모든 profile을 렌더링하고, 한 profile이 선택하는 두 서비스가
같은 host port를 공개하면 실패한다.

```bash
bash scripts/operations/generate-compose-profile-service-coverage.sh --check
```

생성된 coverage snapshot이 현재 트리와 일치하는지 확인한다. snapshot의
`Profile Coverage` 표에 나타나는 이름 집합은 이 문서의 세 표를 합친 집합과
같아야 한다.

## Review Cadence

- **Owner**: Infra/DevOps Engineer
- **Cadence**: `infra/` 하위 Compose 파일의 `profiles:` 변경 시
- **Trigger**: 새 서비스 추가, profile 이름 신설, host port 재배정

## Traceability

- **Subject**: [00-workspace](../README.md)
- **Authority**: [SPEC-0156](../../../../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/spec.md)
- **Deferred pairs**: [SPEC-0171](../../../../03.specs/0171-compose-sibling-pair-resolution/spec.md)
- **Generated evidence**: [Compose profile service coverage](../../../../90.references/data/0059-compose-profile-service-coverage/README.md)

## Related Documents

- [Infrastructure optimization governance](../0006-infrastructure-optimization-governance/policy.md)
- [Developer environment](../0002-developer-environment/guide.md)
- [Environment constraints](../../../../00.agent-governance/policies/environment-constraints.md)
