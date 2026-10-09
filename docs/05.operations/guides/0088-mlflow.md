---
title: "MLflow Usage Guide"
version: "1.0.5"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0088"
parent_ids:
- "POL-0088"
implementation_services:
  infra/08-ai/mlflow/docker-compose.yml:
  - mlflow
  - mlflow-db-provision
created: "2026-09-21"
---

# MLflow Usage Guide

## Overview

MLflow는 `mlops` 또는 `data-science`가 선택하는 OPTIONAL experiment tracking
server이다. HOME에도, 현재 8개 profile 운용 명령에도 들어 있지 않다.
추가하려면 별도로 활성화를 결정해야 한다.

## Audience and Goal

MLflow tracking server를 쓰는 MLOps·데이터 과학 운영자를 위한 문서다. 선택 방법, 인증 경계, artifact 처리 방식을 이해하고 정상 사용과 점검 방법을 찾는 것이 목표다.

## Usage

### Current implementation

- [MLflow Compose](../../../infra/08-ai/mlflow/docker-compose.yml)가
  두 service를 관장한다. `mlflow-db-provision`이 feature SQL을 실행한 뒤,
  `seaweedfs-buckets`가 `mlflow-artifacts`를 생성하면 `mlflow`가 시작한다.
  그 SeaweedFS identity `mlflow`는
  [s3-identities.conf](../../../infra/04-data/seaweedfs/config/s3-identities.conf)에
  선언되어 있다.
- tracking store는 `mng-pg`의 `MLFLOW_DB_NAME` database이며 `MLFLOW_DB_USER`가
  소유한다. 다른 login role은 기본 `PUBLIC` connect 권한을 잃는다.
- artifact는 server의 artifact proxy를 통해 `s3://${MLFLOW_ARTIFACT_BUCKET}`로
  간다. SDK client는 MLflow를 통해 upload/download하며 SeaweedFS credential을
  보유하지 않는다. MLflow SeaweedFS identity는 다른 bucket을 읽을 수 없다.
- 공유 `mng-pg-init` job은 더 이상 MLflow object를 생성하지 않고 MLflow
  secret도 읽지 않으므로 `core`/`mng`/`dev`/`local`은 이것들 없이 시작한다.

### Sizing

현재 자원·worker·job 설정의 원본은 Compose다. job 재활성화는 측정한 메모리
예산과 승인이 필요하다. 아래 과거 측정은 현재 이미지의 측정 결과가 아니다.

원본: `docs/05.operations/guides/0088-mlflow.md`, SPEC-0198 이전 Git 기록.

> Historical evidence (not current authority; source: Git history):
>
> 첫 시작 시 측정(2026-09-21): 기본 설정에서 MLflow 3.x는 server-job consumer
> (`huey`, 각각 약 200 MB)와 uvicorn worker를 실행하며 512 MB template
> limit에서는 OOM kill이 반복됐다. Compose 파일은 server-side job을
> 비활성화하고(`MLFLOW_SERVER_ENABLE_JOB_EXECUTION=false`; GenAI scheduled
> scorer와 trace archival은 사용하지 않음), worker 2개를 실행하며
> `mem_limit: 1g`를 설정한다(steady state 약 560 MB). job을 다시 활성화하려면
> 측정한 메모리 예산이 있어야 한다.

### Authentication and identity

| Path | Control | Limitation |
| --- | --- | --- |
| 브라우저 `https://mlflow.${DEFAULT_URL}` | Gateway SSO(`sso-auth`); OAuth2 Proxy의 `/admins` 그룹 제한 | MLflow 수준의 user, experiment 권한, group 권한 없음 |
| `edge_net`, `ai_net`, `mng_data_net`, `object_net`의 직접 SDK (`http://mlflow:5000`) | 없음; Host header가 `--allowed-hosts`와 일치해야 함 | 네트워크 peer에 동등한 MLflow 사용자 인증·experiment별 권한 통제가 선언되지 않음 |
| Artifact storage | server만 보유한 bucket-scoped SeaweedFS identity | run soft-delete는 artifact 자동 삭제가 아니며 별도 보존·정리 승인이 필요함 |

MLflow가 문서화한 OIDC route는 community `mlflow-oidc-auth` plugin
(`--app-name oidc-auth`)이며, 내장 대안은 `basic-auth`이다. 이 plugin은
**채택되지 않았다**. pinned server release와의 호환성, UI, REST API와 SDK
token flow, 유지보수와 보안 검토, session과 authorization을 설계한
Keycloak client 중 어느 것도 확인되지 않았다. owner가 승인한 변경으로 이
조건들을 증명하기 전까지는 브라우저용 gateway SSO를 유지하고 `ai_net`,
`object_net`만이 아니라 `edge_net`·`mng_data_net`까지 직접 접근 경계로 기록한다. SDK가 동작하도록
SSO 없이 route를 열지 않는다.

### Normal use, backup, and upgrade

실행 순서와 실패·복구 판단은 [런북](../runbooks/0088-mlflow.md)의 `Tracking 데이터와 변경 전 검토` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Checks

- `HYHOME_COMPOSE_PROFILES="mlops data-science" bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`
- `docker compose --profile core --profile mlops ps mlflow mlflow-db-provision`

### Runbook Handoff

provisioning 실패, credential 회전, restore, upgrade에는
[runbook](../runbooks/0088-mlflow.md)을 사용한다.

### 사용·신호와 helper 경계

승인된 notebook/job은 `MLFLOW_TRACKING_URI`로 tracking 서버를 선택하고
실험·run과 artifact proxy를 사용한다. bucket 또는 DB 이름 변경은 기존 URI를
깨뜨릴 수 있는 migration이다. `--allowed-hosts`는 사용자 인증이 아니다. 서버
health는 DB 복구·artifact round-trip·사용자 인가를 증명하지 않는다.

`mlflow-db-provision`은 공유 PostgreSQL과 초기화 작업을 기다리는 일회성 SQL
변경 작업으로 HTTP health가 없다. 서버는 helper와 공유 버킷 작업의 성공 후
시작한다. SQL은 다른 소유자의 DB·관리자 role 인수를 거부하지만 이미 커밋된 변경은
자동 복구하지 않는다. 빌드의 직접 라이브러리 pin은 모든 transitive dependency를
고정하지 않으며 서버와 helper의 버전·자원 설정은 각 Compose/build 원본이 소유한다.

### 소스 검토의 한계

여기서 설명한 네트워크는 선언상 연결 가능한 경로다. 실제 peer 연결·인터넷 공개·
사용자 인증·복구 성공을 이번 문서 작업에서 시험하지 않았다. 현재 선언의 제한을
해소하는 구현 변경은 별도 승인·보안 검토·검증이 필요하다.

### Traceability

- [Policy](../policies/0088-mlflow.md) (`POL-0088`)
- [Runbook](../runbooks/0088-mlflow.md) (`RUN-0088`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)
- [Current Task](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0007-optional-capability-restructure.md)

## Related Documents

- [Image Dockerfile](../../../infra/08-ai/mlflow/Dockerfile) 및 [derived version projection](../../../infra/tech-stack.versions.json)
- [MLflow self-hosting network security](https://mlflow.org/docs/latest/self-hosting/security/network)
- [MLflow SSO and the OIDC plugin](https://mlflow.org/docs/latest/self-hosting/security/sso)
- [MLflow tracking server architecture and artifact proxy](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server)
