---
title: "JupyterLab Workspace"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-05"
created: "2026-09-21"
---

# JupyterLab Workspace

> 데이터 과학 노트북용 단일 사용자 JupyterLab LAB으로, 선택적 MLflow 추적 클라이언트를 갖췄습니다.

## Overview

JupyterLab은 한 명의 운영자를 위해 하나의 Jupyter Server를 실행합니다. JupyterHub가
**아니며** 접근하는 사용자마다 별도로 생성되는 프로세스도, 커널 격리도,
파일시스템 격리도 없습니다. 서버 토큰이 있는 모든 사람은 컨테이너의 UID 1000으로
코드를 실행하고 터미널을 열고 전체 작업 디렉터리를 읽을 수 있습니다.
독립 Compose project인 [JupyterLab LAB](docker-compose.yml)(`jupyterlab` profile)이며
root Compose에 포함되지 않고 HOME network에 연결되지 않으며 Traefik route와 SSO도
없습니다.

## Audience

- **Data scientists**: 노트북, DuckDB/Polars, MLflow SDK 사용.
- **Operators**: 토큰, 작업 디렉터리 백업, 이미지 재빌드 관리.

## Scope

- **Included**: JupyterLab 서버 이미지, Python 의존성 고정, 토큰 처리, 작업 볼륨.
- **Excluded**: MLflow 서버(HOME `08-ai` 패키지), 게이트웨이 라우트와 SSO, JupyterHub 또는 다중 사용자 격리, GPU 커널.

## Structure

```text
.
├── docker-compose.yml  # 독립 LAB entrypoint
├── promotion.yaml      # SPEC-0263 승격 manifest
├── Dockerfile          # scipy-notebook base + pinned requirements
├── requirements.txt    # Pinned notebook libraries (MLflow client matches the server)
└── README.md
```

서비스 정의는 [labs/jupyterlab/docker-compose.yml](docker-compose.yml)이 소유합니다.

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `jupyterlab` | Jupyter Docker Stacks scipy 이미지를 기반으로 한 [Dockerfile](Dockerfile) | 노트북 서버 |
| Libraries | [requirements.txt](requirements.txt) | MLflow client, Polars, DuckDB, PyArrow, psycopg, boto3/s3fs, confluent-kafka, JupySQL, Optuna |

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며
[파생된 Compose 이미지 프로젝션](../../infra/tech-stack.versions.json)은 드리프트 검증에 쓰입니다.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `jupyterlab` / `labs/jupyterlab/docker-compose.yml` |
| Network / port | `lab_jupyterlab_net`(`hy-home-lab-jupyterlab`); HOME network 없음; `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_JUPYTERLAB_HOST_PORT:-18888}` -> 8888 |
| Route | 없음(Traefik route·게이트웨이 SSO 없음); labels `hy-home.tier: lab`, `traefik.enable: 'false'` |
| Authentication | Jupyter Server 토큰만 사용합니다. `${LAB_SECRET_DIR}/jupyterlab/token.txt`의 LAB 전용 `lab_jupyterlab_token`을 `/run/secrets/jupyter_token`으로 마운트해 `JUPYTER_TOKEN`으로 내보냅니다. 토큰이 16자 미만이면 시작이 실패합니다. 빈 토큰은 게시 포트의 모든 client에 커널, 터미널, REST API를 열기 때문에 허용되지 않습니다. HOME 값 복사는 별도 승인입니다 |
| Work directory | `${LAB_DATA_DIR}/jupyterlab/work`을 `/home/jovyan/work`로 바인드합니다. 최초 시작 전에 UID 1000 소유로 생성합니다 |
| MLflow client | 선택 입력 `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`; 비어 있으면 추적 서버 없음. HOME은 MLflow를 LAB network에 게시하지 않으므로 endpoint는 owner 승인 대상(미결정)입니다 |
| Object storage | 오브젝트 스토리지 자격 증명은 주입되지 않습니다 |
| Health | `GET /api`(인증 불필요한 버전 엔드포인트); 서버가 응답함을 증명할 뿐 커널 상태는 증명하지 않습니다 |

## Validation

- `docker compose --env-file labs/.env -f labs/jupyterlab/docker-compose.yml --profile jupyterlab config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`
- 이미지 빌드는 저장소 검사 대상이 아니므로, 승인된 환경에서만 빌드합니다.

## Usage

명령은 저장소 루트에서
`docker compose --env-file labs/.env -f labs/jupyterlab/docker-compose.yml --profile jupyterlab` 접두사로 실행합니다.
`config`는 render만 하며, 컨테이너를 시작하는 명령은
`python3 scripts/operations/lab.py check|up|down jupyterlab`의 lease 규칙
([LAB 안내](../README.md#usage))을 따릅니다.

1. 별도 승인 아래 `${LAB_SECRET_DIR}/jupyterlab/token.txt`를 만들고 작업 디렉터리를
   UID 1000 소유로 생성합니다.
2. render로 정적 검증한 뒤 활성 lease 안에서만 `... up -d jupyterlab`으로 시작합니다.
3. `http://${LAB_HOST_BIND_IP}:${LAB_JUPYTERLAB_HOST_PORT}`를 열고 브라우저 세션마다 한 번씩 서버 토큰을 입력합니다.
4. 업그레이드 시 라이브러리 고정 값을 MLflow 서버 버전과 맞춥니다.

## Related Documents

- **Guide**: JupyterLab usage guide (`docs/05.operations/guides/15-labs/0089-jupyterlab.md`)
- **Policy**: JupyterLab operations policy (`docs/05.operations/policies/15-labs/0089-jupyterlab.md`)
- **Runbook**: JupyterLab recovery runbook (`docs/05.operations/runbooks/15-labs/0089-jupyterlab.md`)
- [MLflow package](../../infra/08-ai/mlflow/README.md)
- [LAB 탐색](../README.md)
- [Documentation index](../../docs/README.md)
