---
title: "JupyterLab Operations Policy"
version: "1.1.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "POL-0089"
parent_ids:
- "AD-0011"
created: "2026-09-21"
---

# JupyterLab Operations Policy

## Purpose

### Objective

JupyterLab은 임의의 코드를 실행한다. kernel이나 terminal에 도달할 수 있는 사람은 누구든
컨테이너와 컨테이너가 읽을 수 있는 모든 credential을 제어한다.

### Authority

- [Laboratory architecture](../../../02.architecture/descriptions/0011-laboratory-architecture.md)
- SPEC-0262 Analytics labs migration
- [Image Dockerfile](../../../../labs/jupyterlab/Dockerfile) and [derived version projection](../../../../infra/tech-stack.versions.json)
- [JupyterLab Compose source](../../../../labs/jupyterlab/docker-compose.yml)

## Scope

### Applies To

활성화, 인증, 네트워크 노출, work-directory 데이터, 이미지 의존성, MLflow client 접근,
backup, 제거.

### Exclusions

다중 사용자 JupyterHub 설계와 MLflow 서버 자체 통제(POL-0088)는 이 정책의 대상이 아니다.

## Rules

### Requirements

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

### Enforcement

정적 렌더링(`docker compose --env-file labs/.env -f labs/jupyterlab/docker-compose.yml --profile jupyterlab config --quiet`)과
`tests.validation.test_lab_isolation` 후, lease 아래 런타임 검사: 토큰 없는 요청과 잘못된 토큰의
거부, 게시 port가 `LAB_HOST_BIND_IP`에만 bind됨, kernel 시작과 WebSocket.

## Exceptions

### Exception Conditions

내부 MLflow SDK 경로는 인증되지 않는다 (`POL-0088` 참고). terminal은 단일 사용자를
위해 활성화 상태로 유지한다. 추가 검토 없이 비활성화해도 된다.

### Approval and Review

이미지나 라이브러리 변경, 인증 변경, 신규 사용자, JupyterHub 결정 시 검토한다.

## Ownership

### Responsibilities

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Change and Adoption

- [Guide](../../guides/15-labs/0089-jupyterlab.md) (`GDE-0089`)
- [Runbook](../../runbooks/15-labs/0089-jupyterlab.md) (`RUN-0089`)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
