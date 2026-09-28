---
title: "MLflow Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0088"
parent_ids:
- "POL-0088"
implementation_services:
  infra/11-laboratory/mlflow/docker-compose.yml:
  - mlflow
  - mlflow-db-provision
created: "2026-09-21"
---

# MLflow Usage Guide

## Usage

### Purpose and classification

MLflow는 `mlops` 또는 `data-science`가 선택하는 OPTIONAL experiment tracking
server이다. HOME에도, 현재 8개 profile 운용 명령에도 들어 있지 않다.
추가하려면 별도로 활성화를 결정해야 한다.

### Current implementation

- [MLflow Compose](../../../infra/11-laboratory/mlflow/docker-compose.yml)가
  두 service를 관장한다. `mlflow-db-provision`이 feature SQL을 실행한 뒤,
  `seaweedfs-buckets`가 `mlflow-artifacts`를 생성하면 `mlflow`가 시작한다.
  그 SeaweedFS identity `mlflow`는
  [s3-identities.conf](../../../infra/04-data/lake-and-object/seaweedfs/config/s3-identities.conf)에
  선언되어 있다.
- tracking store는 `mng-pg`의 `MLFLOW_DB_NAME` database이며 `MLFLOW_DB_USER`가
  소유한다. 다른 login role은 기본 `PUBLIC` connect 권한을 잃는다.
- artifact는 server의 artifact proxy를 통해 `s3://${MLFLOW_ARTIFACT_BUCKET}`로
  간다. SDK client는 MLflow를 통해 upload/download하며 SeaweedFS credential을
  보유하지 않는다. MLflow SeaweedFS identity는 다른 bucket을 읽을 수 없다.
- 공유 `mng-pg-init` job은 더 이상 MLflow object를 생성하지 않고 MLflow
  secret도 읽지 않으므로 `core`/`mng`/`dev`/`local`은 이것들 없이 시작한다.

### Sizing

첫 시작 시 측정(2026-09-21): 기본 설정에서 MLflow 3.x는 server-job consumer
(`huey`, 각각 약 200 MB)와 uvicorn worker를 실행하며 512 MB template
limit에서는 OOM kill이 반복됐다. Compose 파일은 server-side job을
비활성화하고(`MLFLOW_SERVER_ENABLE_JOB_EXECUTION=false`; GenAI scheduled
scorer와 trace archival은 사용하지 않음), worker 2개를 실행하며
`mem_limit: 1g`를 설정한다(steady state 약 560 MB). job을 다시 활성화하려면
측정한 메모리 예산이 있어야 한다.

### Authentication and identity

| Path | Control | Limitation |
| --- | --- | --- |
| 브라우저 `https://mlflow.${DEFAULT_URL}` | Gateway SSO(`sso-auth`); 임의의 realm user 통과 | MLflow 수준의 user, experiment 권한, group 권한 없음 |
| `ai_net`, `object_net` 내부 SDK (`http://mlflow:5000`) | 없음; Host header가 `--allowed-hosts`와 일치해야 함 | `ai_net`, `object_net`의 모든 container가 모든 experiment를 읽고 쓸 수 있음 |
| Artifact storage | server만 보유한 bucket-scoped SeaweedFS identity | MLflow를 통해 run을 삭제하면 artifact도 삭제됨 |

MLflow가 문서화한 OIDC route는 community `mlflow-oidc-auth` plugin
(`--app-name oidc-auth`)이며, 내장 대안은 `basic-auth`이다. 이 plugin은
**채택되지 않았다**. pinned server release와의 호환성, UI, REST API와 SDK
token flow, 유지보수와 보안 검토, session과 authorization을 설계한
Keycloak client 중 어느 것도 확인되지 않았다. owner가 승인한 변경으로 이
조건들을 증명하기 전까지는 브라우저용 gateway SSO를 유지하고 `ai_net`,
`object_net` 도달 가능성을 SDK trust boundary로 취급한다. SDK가 동작하도록
SSO 없이 route를 열지 않는다.

### Normal use, backup, and upgrade

notebook과 job을 위해 `MLFLOW_TRACKING_URI`를 internal URL로 설정한다. 기존
experiment와 artifact URI는 `MLFLOW_ARTIFACT_BUCKET`과 database 이름이
변경되지 않는 동안만 유효하다. 둘 중 하나라도 rename하면 migration이다.

`MLFLOW_DB_NAME`의 `pg_dump`로 tracking database를 backup하고, run이
artifact path를 참조하므로 bucket도 SeaweedFS backup set으로 함께
가져간다. 먼저 격리된 `mng-pg`와 SeaweedFS로 restore해 run과 artifact
수를 비교한다. upgrade 전에는 release note를 읽는다. server는 시작 시
database migration을 적용하므로 backup을 먼저 수행한다. 이 service에서는
backup도 restore도 아직 실행하지 않았다.

## Common Checks

- `HYHOME_COMPOSE_PROFILES="mlops data-science" bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`
- `docker compose --profile core --profile mlops ps mlflow mlflow-db-provision`

## Runbook Handoff

provisioning 실패, credential 회전, restore, upgrade에는
[runbook](../runbooks/0088-mlflow.md)을 사용한다.

## Traceability

- [Policy](../policies/0088-mlflow.md) (`POL-0088`)
- [Runbook](../runbooks/0088-mlflow.md) (`RUN-0088`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)
- [Current Task](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0007-optional-capability-restructure.md)

## Related Documents

- [Image Dockerfile](../../../infra/11-laboratory/mlflow/Dockerfile) 및 [derived version projection](../../../infra/tech-stack.versions.json)
- [MLflow self-hosting network security](https://mlflow.org/docs/latest/self-hosting/security/network)
- [MLflow SSO and the OIDC plugin](https://mlflow.org/docs/latest/self-hosting/security/sso)
- [MLflow tracking server architecture and artifact proxy](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server)
