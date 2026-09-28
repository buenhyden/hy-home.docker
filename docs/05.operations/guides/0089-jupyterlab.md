---
title: "JupyterLab Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0089"
parent_ids:
- "POL-0089"
implementation_services:
  infra/11-laboratory/jupyterlab/docker-compose.yml:
  - jupyterlab
created: "2026-09-21"
---

# JupyterLab Usage Guide

## Usage

### Purpose and classification

JupyterLab은 `data-science`만 선택하는 OPTIONAL single-user notebook
server이며, 이 profile은 MLflow도 함께 선택한다. HOME에도, 현재 8개
profile 운용 명령에도 들어 있지 않다.

### Current implementation

- [JupyterLab Compose](../../../infra/11-laboratory/jupyterlab/docker-compose.yml)는
  pinned library를 가진 scipy-notebook image를 빌드하고 Jupyter Server 하나를
  실행한다.
- notebook은 repository 밖의 `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`에
  있다. bind에 `create_host_path: false`를 쓰므로 디렉터리가 없으면
  UID 1000이 쓸 수 없는 root 소유 디렉터리를 만드는 대신 시작에
  실패한다.
- server에는 `jupyter_token` secret이 필요하며 16자 미만의 token이면 시작을
  거부한다.

### Access paths and isolation

| Path | Control | What it does not provide |
| --- | --- | --- |
| 브라우저 route | Gateway SSO, 이후 server token(이후 cookie); REST와 kernel WebSocket도 같은 route를 따름 | Jupyter 내부의 user별 identity; token을 아는 모든 SSO user가 동일한 UID 1000이 됨 |
| port 8888에 대한 직접 `ai_net` access | Server token | Network isolation; peer가 API를 시도할 수 있음 |
| Kernel과 terminal | container 내 UID 1000으로 실행 | 사람 간 isolation, user별 CPU/memory quota |

SSO는 누가 gateway에 도달했는지 증명할 뿐, kernel이나 파일을 격리하지
않는다. 진정한 multi-user isolation에는 spawner와 user별 storage를 가진
JupyterHub가 필요하다. 이는 설계와 dependency를 따로 결정할 일이다. 이
single-user server에 JupyterHub 설정을 붙여넣지 않는다.

### MLflow from notebooks

`MLFLOW_TRACKING_URI`는 `ai_net`의 `http://mlflow:5000`을 가리킨다. 이 경로는
브라우저 SSO route를 우회하며 MLflow 수준의 인증이 없다. notebook에서 기록한
run은 SSO user에게 귀속되지 않는다. artifact는 MLflow proxy를 통해
upload되므로 notebook은 object-storage credential을 보유하지 않는다. 나중에
MLflow 인증을 채택하면 인증되지 않은 API를 다시 열지 말고 notebook에
전용 MLflow identity를 부여한다.

### Normal use and backup

work 디렉터리를 복사하기 전에 server를 멈춘다. notebook과 output은 민감할
수 있는 data로 취급한다. library를 바꾸려면 image를 재빌드하고, MLflow
client version을 server와 맞춘다.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=data-science bash scripts/validation/validate-docker-compose.sh`
- route에 인증 없이 요청하면 401(gateway)을 반환하고, token 없이 `/api/status`에
  요청하면 403(server)을 반환한다.

## Runbook Handoff

token, 시작, kernel, restore 문제에는
[runbook](../runbooks/0089-jupyterlab.md)을 사용한다.

## Traceability

- [Policy](../policies/0089-jupyterlab.md) (`POL-0089`)
- [Runbook](../runbooks/0089-jupyterlab.md) (`RUN-0089`)
- [MLflow guide](0088-mlflow.md) (`GDE-0088`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Image Dockerfile](../../../infra/11-laboratory/jupyterlab/Dockerfile) 및 [derived version projection](../../../infra/tech-stack.versions.json)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
- [Jupyter Docker Stacks common options](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html)
