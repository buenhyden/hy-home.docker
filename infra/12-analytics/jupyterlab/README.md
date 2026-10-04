---
title: "JupyterLab Workspace"
version: "1.0.4"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-09-21"
---

# JupyterLab Workspace

> 데이터 과학 노트북용 단일 사용자 JupyterLab으로, 내부 MLflow 추적 클라이언트를 갖췄습니다.

## Overview

JupyterLab은 한 명의 운영자를 위해 하나의 Jupyter Server를 실행합니다. JupyterHub가
**아니며** 접근하는 사용자마다 별도로 생성되는 프로세스도, 커널 격리도,
파일시스템 격리도 없습니다. 인증된 모든 브라우저 세션과 서버 토큰이 있는
모든 사람은 컨테이너의 UID 1000으로 코드를 실행하고 터미널을 열고 전체
작업 디렉터리를 읽을 수 있습니다. Lifecycle: **OPTIONAL**이며 `data-science`에서만
선택됩니다. HOME이나 현재 8개 프로필 선택에는 포함되지 않습니다.

## Audience

- **Data scientists**: 노트북, DuckDB/Polars, MLflow SDK 사용.
- **Operators**: 토큰, 작업 디렉터리 백업, 이미지 재빌드 관리.
- **AI agents**: 소유 Guide, Policy, Runbook에 따라 이 패키지를 변경.

## Scope

- **Included**: JupyterLab 서버 이미지, Python 의존성 고정, 게이트웨이 라우트, 토큰 처리, 작업 볼륨.
- **Excluded**: MLflow 서버(`08-ai` 패키지), JupyterHub 또는 다중 사용자 격리, GPU 커널.

## Structure

```text
.
├── Dockerfile          # scipy-notebook base + pinned requirements
├── requirements.txt    # Pinned notebook libraries (MLflow client matches the server)
├── docker-compose.yml  # jupyterlab service
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `jupyterlab` | Jupyter Docker Stacks scipy 이미지를 기반으로 한 [Dockerfile](Dockerfile) | 노트북 서버 |
| Libraries | [requirements.txt](requirements.txt) | MLflow client, Polars, DuckDB, PyArrow, psycopg, boto3/s3fs, confluent-kafka, JupySQL, Optuna |

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증에 쓰입니다.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `data-science` (MLflow와 그 의존성 클로저도 함께 선택) |
| Network / port | `ai_net`, `edge_net`; `expose`를 통한 내부 `${JUPYTER_PORT:-8888}`; 호스트 포트 없음 |
| Route | `gateway-standard-chain`, `sso-errors`, `sso-auth`를 사용하는 `https://jupyter.${DEFAULT_URL}`; WebSocket은 Traefik을 통과 |
| Authentication | 브라우저 라우트는 게이트웨이 SSO를 사용**하며** Jupyter Server 토큰도 필요합니다. 이 토큰은 시크릿 `jupyter_token`(AI-007)에서 가져와 `JUPYTER_TOKEN`으로 내보냅니다. 토큰이 16자 미만이면 시작이 실패합니다. 빈 토큰을 허용하면 같은 네트워크의 다른 대상이 커널, 터미널, REST API에 직접 접근할 수 있으므로 빈 토큰은 허용되지 않습니다 |
| Work directory | `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`을 `/home/jovyan/work`로 바인드하며 `create_host_path: false`입니다. 최초 시작 전에 UID 1000 소유로 생성합니다 |
| MLflow client | `MLFLOW_TRACKING_URI=http://mlflow:${MLFLOW_PORT}` — 게이트웨이 SSO 라우트를 거치지 않는 내부 경로입니다 |
| Object storage | 오브젝트 스토리지 자격 증명은 주입되지 않으며 아티팩트는 MLflow 아티팩트 프록시를 통해 업로드됩니다 |
| Health | `GET /api`(인증 불필요한 버전 엔드포인트); 서버가 응답함을 증명할 뿐 커널 상태는 증명하지 않습니다 |

## Validation

- `HYHOME_COMPOSE_PROFILES=data-science bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`
- 이미지 빌드는 저장소 검사 대상이 아니므로, 승인된 환경에서만 빌드합니다.

## Usage

1. 등록된 시크릿 워크플로우를 통해 `secrets/tools/jupyterlab/jupyter_token.txt`를 만들고 작업 디렉터리를
   UID 1000 소유로 생성합니다.
2. 정적으로 검증한 뒤 승인된 대상으로만 시작합니다. 예:
   `docker compose --profile core --profile data-science up -d jupyterlab`.
3. 라우트를 열어 SSO를 통과한 뒤, 브라우저 세션마다 한 번씩 서버 토큰을 입력합니다.
4. 업그레이드 시 라이브러리 고정 값을 MLflow 서버 버전과 맞춥니다.

## Related Documents

- **Guide**: JupyterLab usage guide (`docs/05.operations/guides/0089-jupyterlab.md`)
- **Policy**: JupyterLab operations policy (`docs/05.operations/policies/0089-jupyterlab.md`)
- **Runbook**: JupyterLab recovery runbook (`docs/05.operations/runbooks/0089-jupyterlab.md`)
- [MLflow package](../../08-ai/mlflow/README.md)
- [Documentation index](../../../docs/README.md)
