---
title: "JupyterLab Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "operations"
artifact_id: "GDE-0089"
parent_ids:
- "POL-0089"
implementation_services:
  labs/jupyterlab.yml:
  - jupyterlab
created: "2026-09-21"
---

# JupyterLab Usage Guide

## Overview

JupyterLab은 root Compose에서 분리된 독립 LAB `labs/jupyterlab.yml`의 single-user notebook
server이며 LAB profile `jupyterlab`으로 선택된다(SPEC-0262). root `data-science` profile은 이제
MLflow와 그 provisioner만 선택하고 JupyterLab을 선택하지 않는다.

## Scope

### Audience and Goal

JupyterLab LAB을 쓰는 노트북 사용자와 운영자를 위한 문서다. 접근 경로, 작업 파일 보존, MLflow 연동의 현재 한계를 이해하고 정상 사용과 점검 방법을 찾는 것이 목표다.

## Concepts

### Current implementation

- [JupyterLab LAB Compose](../../../../labs/jupyterlab.yml)는 pinned library를 가진
  scipy-notebook image를 빌드하고 Jupyter Server 하나를 `hy-home-lab-jupyterlab` project의
  `lab_jupyterlab_net`에서 실행한다. HOME network에는 합류하지 않으며 서비스는
  `hy-home.tier: lab`, `traefik.enable: 'false'` label을 가진다.
- notebook은 repository 밖의 `${LAB_DATA_DIR}/jupyterlab/work`에 있다(이전
  `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`). 기존 notebook은 옮기지 않았으며 재배치는
  별도 승인 아래 수동으로 한다. bind volume이므로 디렉터리가 미리 있고 UID 1000 소유여야
  시작된다.
- server에는 `jupyter_token` secret이 필요하며 16자 미만의 token이면 시작을
  거부한다. secret은 LAB 전용이다. 이름은 `lab_jupyterlab_<purpose>`이고 파일은
  `${LAB_SECRET_DIR:-../secrets/labs}/jupyterlab/` 아래에 있으며 원래 `/run/secrets/<name>` target에
  mount되고 group은 `LAB_SECRETS_GID`다. 값은 복사되지 않았으므로 운영자가 token의 LAB 사본을
  별도 승인 아래 준비해야 한다(미결정 항목).

## Usage

### Access paths and isolation

| Path | Control | What it does not provide |
| --- | --- | --- |
| 브라우저 `http://${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_JUPYTERLAB_HOST_PORT:-18888}` | Server token(이후 cookie); REST와 kernel WebSocket도 같은 port를 따름 | gateway SSO·ForwardAuth(더 이상 적용되지 않음); Jupyter 내부의 user별 identity |
| `lab_jupyterlab_net` peer | Server token | Network isolation; 같은 LAB network peer가 API를 시도할 수 있음 |
| Kernel과 terminal | container 내 UID 1000으로 실행 | 사람 간 isolation, user별 CPU/memory quota |

gateway route가 없으므로 접근 통제는 mandatory token과 bind 주소뿐이다. `LAB_HOST_BIND_IP`를
loopback 밖으로 바꾸면 token만으로 노출되므로 별도 보안 검토가 필요하다. 진정한 multi-user
isolation에는 spawner와 user별 storage를 가진 JupyterHub가 필요하다. 이는 설계와 dependency를
따로 결정할 일이다. 이 single-user server에 JupyterHub 설정을 붙여넣지 않는다.

### MLflow from notebooks

`MLFLOW_TRACKING_URI`는 선택 LAB 입력 `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`에서 온다. 비어 있으면
tracking server가 없다. HOME은 MLflow를 LAB network에 기본 게시하지 않으므로 소유자가 도달
가능한 endpoint를 승인하기 전까지 notebook에서 HOME MLflow에 기록할 수 없다(SPEC-0262 미결정
항목, 별도 승인). 승인된 endpoint를 쓰더라도 MLflow 수준의 인증이 없고 run은 사람에게 귀속되지
않는다. 나중에 MLflow 인증을 채택하면 인증되지 않은 API를 다시 열지 말고 notebook에 전용
MLflow identity를 부여한다.

### Normal use and backup

실행 순서와 실패·복구 판단은 [런북](../../runbooks/15-labs/0089-jupyterlab.md)의 `작업 디렉터리와 라이브러리 보존` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Runbook Handoff

token, 시작, kernel, restore 문제에는
[runbook](../../runbooks/15-labs/0089-jupyterlab.md)을 사용한다.

### 정상 사용과 준비 조건

한 명의 승인된 사용자가 notebook·kernel·terminal을 사용한다. 출력과 work 파일에는
민감 정보가 포함될 수 있으므로 공유·삭제 전에 보존 범위를 확인한다. 기동은
`python3 scripts/operations/lab.py check|up|down jupyterlab`의 목적·lease·충돌·예산 규칙을
따르고, `docker compose --env-file labs/.env -f labs/jupyterlab.yml --profile jupyterlab config`
렌더링만 승인 없이 안전하다. 자원 제한은 서비스 전체에 적용되며 사용자별 quota가 아니다.

Dockerfile의 base 날짜와 직접 library pin은 정확한 Lab·Server·Python 실행 버전이나
transitive dependency를 증명하지 않는다. 새 build와 rollback 전에 resolved 이미지·
의존성을 확인한다.

### 소스 검토의 한계

여기서 설명한 네트워크와 port는 선언상 경로다. 실제 peer 연결·인터넷 공개·사용자 인증·
복구 성공을 이번 문서 작업에서 시험하지 않았다. 현재 선언의 제한을 해소하는 구현 변경은
별도 승인·보안 검토·검증이 필요하다.

### Traceability

- [Policy](../../policies/15-labs/0089-jupyterlab.md) (`POL-0089`)
- [Runbook](../../runbooks/15-labs/0089-jupyterlab.md) (`RUN-0089`)
- [MLflow guide](../13-analytics-and-data-quality/0088-mlflow.md) (`GDE-0088`)
- [Laboratory architecture](../../../02.architecture/descriptions/0011-laboratory-architecture.md)
- SPEC-0262 Analytics labs migration

## Troubleshooting

### Common Checks

- `docker compose --env-file labs/.env -f labs/jupyterlab.yml --profile jupyterlab config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`
- 승인된 런타임 검사에서 token 없는 요청과 잘못된 token의 거부를 각각 확인한다. health의
  `/api` 응답은 인증·kernel 증거가 아니다.

## Related Documents

- [Image Dockerfile](../../../../labs/jupyterlab/Dockerfile) 및 [derived version projection](../../../../infra/tech-stack.versions.json)
- [LAB 공개 입력 예시](../../../../labs/.env.example)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
- [Jupyter Docker Stacks common options](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html)
