---
title: "JupyterLab Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0089"
parent_ids:
- "POL-0089"
implementation_services:
  infra/12-analytics/jupyterlab/docker-compose.yml:
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

- [JupyterLab Compose](../../../infra/12-analytics/jupyterlab/docker-compose.yml)는
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
| 브라우저 route | Gateway SSO, 이후 server token(이후 cookie); REST와 kernel WebSocket도 같은 route를 따름 | Jupyter 내부의 user별 identity; gateway의 `/admins` 허용 후 token을 아는 사용자가 동일한 UID 1000을 공유함 |
| 직접 `edge_net`·`ai_net` access | Server token | Network isolation; peer가 API를 시도할 수 있음 |
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

실행 순서와 실패·복구 판단은 [런북](../runbooks/0089-jupyterlab.md)의 `작업 디렉터리와 라이브러리 보존` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=data-science bash scripts/validation/validate-docker-compose.sh`
- 승인된 런타임 검사에서 gateway 로그인 redirect와 인가 거부, 서버 token 거부를
  각각 확인한다. `sso-errors`가 인증 실패 401을 302로 바꿀 수 있으므로 외부 route의
  응답을 무조건 401로 기대하지 않는다. health의 `/api` 응답은 인증·kernel 증거가 아니다.

## Runbook Handoff

token, 시작, kernel, restore 문제에는
[runbook](../runbooks/0089-jupyterlab.md)을 사용한다.

### 정상 사용과 준비 조건

한 명의 승인된 사용자가 notebook·kernel·terminal을 사용한다. 출력과 work 파일에는
민감 정보가 포함될 수 있으므로 공유·삭제 전에 보존 범위를 확인한다. MLflow에 대한
의존성은 선택적 health 대기이며 `data-science` 전체 기동은 다른 서버·helper도
선택할 수 있다. 자원 제한은 서비스 전체에 적용되며 사용자별 quota가 아니다.

Dockerfile의 base 날짜와 직접 library pin은 정확한 Lab·Server·Python 실행 버전이나
transitive dependency를 증명하지 않는다. 새 build와 rollback 전에 resolved 이미지·
의존성을 확인한다. 호스트 포트는 게시되지 않지만 두 네트워크 peer가 token 인증
listener에 접근할 수 있으므로 물리적 격리를 주장하지 않는다.

### 소스 검토의 한계

여기서 설명한 네트워크는 선언상 연결 가능한 경로다. 실제 peer 연결·인터넷 공개·
사용자 인증·복구 성공을 이번 문서 작업에서 시험하지 않았다. 현재 선언의 제한을
해소하는 구현 변경은 별도 승인·보안 검토·검증이 필요하다.

## Traceability

- [Policy](../policies/0089-jupyterlab.md) (`POL-0089`)
- [Runbook](../runbooks/0089-jupyterlab.md) (`RUN-0089`)
- [MLflow guide](0088-mlflow.md) (`GDE-0088`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Image Dockerfile](../../../infra/12-analytics/jupyterlab/Dockerfile) 및 [derived version projection](../../../infra/tech-stack.versions.json)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
- [Jupyter Docker Stacks common options](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html)
