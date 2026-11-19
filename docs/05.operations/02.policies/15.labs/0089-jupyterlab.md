---
title: "JupyterLab Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0089"
parent_ids:
- "AD-0011"
created: "2026-09-21"
next_review_at: "2027-05-13"
---

# JupyterLab Operations Policy

## Purpose and Scope

### Objective

JupyterLab은 임의의 코드를 실행한다. kernel이나 terminal에 도달할 수 있는 사람은 누구든
컨테이너와 컨테이너가 읽을 수 있는 모든 credential을 제어한다.

#### Authority

- [Laboratory architecture](../../../02.architecture/01.descriptions/0011-laboratory-architecture.md)
- SPEC-0262 Analytics labs migration
- [Image Dockerfile](../../../../labs/jupyterlab/Dockerfile) and [derived version projection](../../../../infra/tech-stack.versions.json)
- [JupyterLab Compose source](../../../../labs/jupyterlab/docker-compose.yml)

### Applies To

활성화, 인증, 네트워크 노출, work-directory 데이터, 이미지 의존성, MLflow client 접근,
backup, 제거.

#### Exclusions

다중 사용자 JupyterHub 설계와 MLflow 서버 자체 통제(POL-0088)는 이 정책의 대상이 아니다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0089-R1 | 항상 | 필수: 독립 LAB `labs/jupyterlab/docker-compose.yml`의 LAB profile `jupyterlab`으로만 선택한다 | none | none |
| POL-0089-R2 | 항상 | 금지: root include, HOME network 합류, HOME 이름 선택 추가 | none | none |
| POL-0089-R3 | 항상 | 금지: 빈 토큰이나 비활성화된 인증으로 실행 | lease 아래 런타임 검사(토큰 없는 요청/잘못된 토큰 거부) | none |
| POL-0089-R4 | 항상 | 필수: token을 유일한 server 인증으로 쓴다(gateway route와 SSO 없음) | none | none |
| POL-0089-R5 | 항상 | 필수: host 포트는 `LAB_HOST_BIND_IP`(기본 `127.0.0.1`)의 `LAB_JUPYTERLAB_HOST_PORT`에만 게시한다 | lease 아래 런타임 검사(게시 port가 `LAB_HOST_BIND_IP`에만 bind됨) | none |
| POL-0089-R6 | loopback 밖 bind 시 | 금지: 별도 보안 검토 없는 bind | none | none |
| POL-0089-R7 | 항상 | 필수: 서버를 single-user로 취급한다 | none | none |
| POL-0089-R8 | per-user isolation을 제공하는 검토된 JupyterHub 설계가 나오기 전 | 금지: 여러 사람에게 접근 허용 | none | none |
| POL-0089-R9 | 항상 | 필수: 필수 `jupyter_token`만 선언된 secret으로 제공한다 | none | none |
| POL-0089-R10 | 항상 | 금지: 추가 공유 secret, Docker socket, 공유 storage credential을 컨테이너에 마운트 | none | none |
| POL-0089-R11 | 노트북의 MLflow 접근 시 | 필수: 선택 입력 `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`의 승인된 endpoint와 artifact proxy로만 접근한다 | none | none |
| POL-0089-R12 | MLflow endpoint 승인 전 | 필수: `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`를 비워 둔다 | none | none |
| POL-0089-R13 | 항상 | 필수: work directory를 저장소 밖 `${LAB_DATA_DIR}/jupyterlab/work`에 owner UID 1000으로 유지한다 | none | none |
| POL-0089-R14 | backup 시 | 필수: work directory를 사용자 데이터로 백업한다 | 수동 | none |
| POL-0089-R15 | 이전 `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work` 데이터 재배치 시 | 필수: 별도 승인 아래 수동으로만 한다 | 수동 | none |
| POL-0089-R16 | 항상 | 필수: 라이브러리 버전을 고정한다 | 수동 | none |
| POL-0089-R17 | 의존성 변경 시 | 필수: 다른 이미지 변경처럼 검토한다 | 수동 | none |
| POL-0089-R18 | 토큰 회전 시 | 필수: 새 token 성공과 이전 token/cookie 거부 근거를 갖춘다 | none | none |
| POL-0089-R19 | 정확한 base 동작이 확인되지 않을 때 | 금지: 폐기 완료로 기록 | none | none |
| POL-0089-R20 | work 복구 시 | 필수: 복구본과 원본을 격리하고 파일/노트북 출력의 민감성을 유지한다 | none | none |
| POL-0089-R21 | 데이터 삭제 시 | 필수: 컨테이너 제거와 별도로 보존/승인을 확인한다 | 수동 | none |
| POL-0089-R22 | 항상 | 필수: 책임자는 `@buenhyden`이다 | none | none |

- 독립 LAB `labs/jupyterlab/docker-compose.yml`의 LAB profile `jupyterlab`으로만 선택한다(SPEC-0262). root
  include, HOME network 합류, HOME 이름 선택 추가를 금지한다.
- 빈 토큰이나 비활성화된 인증으로 절대 실행하지 않는다. gateway route와 SSO는 더 이상 없으므로
  token이 유일한 server 인증이다. host 포트는 `LAB_HOST_BIND_IP`(기본 `127.0.0.1`)의
  `LAB_JUPYTERLAB_HOST_PORT`에만 게시하며 loopback 밖 bind는 별도 보안 검토 없이 허용하지 않는다.
- 서버를 single-user로 취급한다. per-user isolation을 제공하는 검토된 JupyterHub 설계가
  나올 때까지 여러 사람에게 접근을 허용하지 않는다.
- 필수 `jupyter_token`만 선언된 secret으로 제공한다. 추가 공유 secret, Docker
  socket, 공유 storage credential을 컨테이너에 마운트하지 않는다.
  노트북의 MLflow 접근은 선택 입력 `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`의 승인된 endpoint와
  artifact proxy로만 한다. 승인 전에는 비워 둔다(미결정, 별도 승인).
- work directory는 저장소 밖 `${LAB_DATA_DIR}/jupyterlab/work`에 owner UID 1000으로 유지한다.
  사용자 데이터로 백업한다. 이전 `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`의 데이터 재배치는
  별도 승인 아래 수동으로만 한다.
- 라이브러리 버전을 고정한다. 의존성 변경은 다른 이미지 변경처럼 검토한다.

#### 복구·회전과 책임

책임자는 `@buenhyden`이다. 토큰 회전은 새 token 성공뿐 아니라 이전 token·cookie
거부 근거가 필요하다. 정확한 base 동작이 확인되지 않으면 폐기 완료로 기록하지 않는다.
work 복구본과 원본은 격리하고 파일·노트북 출력의 민감성을 유지한다. 데이터 삭제는
컨테이너 제거와 별도로 보존·승인을 확인한다.

### Exceptions

#### Exception Conditions

내부 MLflow SDK 경로는 인증되지 않는다 (`POL-0088` 참고). terminal은 단일 사용자를
위해 활성화 상태로 유지한다. 추가 검토 없이 비활성화해도 된다.

#### Approval and Review

이미지나 라이브러리 변경, 인증 변경, 신규 사용자, JupyterHub 결정 시 검토한다.

## Enforcement

### Mechanisms

정적 렌더링(`docker compose --env-file labs/.env -f labs/jupyterlab/docker-compose.yml --profile jupyterlab config --quiet`)과
`tests.validation.test_lab_isolation` 후, lease 아래 런타임 검사: 토큰 없는 요청과 잘못된 토큰의
거부, 게시 port가 `LAB_HOST_BIND_IP`에만 bind됨, kernel 시작과 WebSocket.

### Limits

아래 규칙은 이름 붙은 검사가 규칙에 연결되어 있지 않거나 승인/검토에 의존한다(정적 렌더링과 `tests.validation.test_lab_isolation`은 개별 규칙과 연결되지 않음).

- 격리/노출: 강제 수단 없음 `POL-0089-R1`~`R2`, `POL-0089-R6`
- 인증: 강제 수단 없음 `POL-0089-R4`
- 접근/secret: 강제 수단 없음 `POL-0089-R7`~`R12`
- data/의존성: 수동 검토 `POL-0089-R14`~`R17`; 강제 수단 없음 `POL-0089-R13`
- 복구/회전/책임: 수동 검토 `POL-0089-R21`; 강제 수단 없음 `POL-0089-R18`~`R20`, `POL-0089-R22`
- 토큰 거부와 bind 범위, kernel/WebSocket 검사는 lease 아래 runtime 검사이며 실행 기록에 의존한다.
- 토큰 회전의 이전 token/cookie 거부는 정확한 base 동작이 확인되지 않으면 폐기 완료로 기록할 수 없다.
- MLflow endpoint 승인은 미결정이며 내부 MLflow SDK 경로는 인증되지 않는다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [Guide](../../01.guides/15.labs/0089-jupyterlab.md) (`GDE-0089`)
- [Runbook](../../03.runbooks/15.labs/0089-jupyterlab.md) (`RUN-0089`)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
