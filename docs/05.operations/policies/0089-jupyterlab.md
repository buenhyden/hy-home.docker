---
title: "JupyterLab Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0089"
parent_ids:
- "AD-0011"
created: "2026-09-21"
---

# JupyterLab Operations Policy

## Overview

JupyterLab은 임의의 코드를 실행한다. kernel이나 terminal에 도달할 수 있는 사람은 누구든
컨테이너와 그것이 읽을 수 있는 모든 credential을 제어한다.

## Policy Scope

활성화, 인증, 네트워크 노출, work-directory 데이터, 이미지 의존성, MLflow client 접근,
backup, 제거.

## Controls

- `data-science`를 통해서만 선택한다. HOME 밖에 유지한다.
- 빈 토큰이나 비활성화된 인증으로 절대 실행하지 않는다. route에서 gateway SSO를 유지하고
  host 포트를 게시하지 않는다.
- 서버를 single-user로 취급한다. per-user isolation을 제공하는 검토된 JupyterHub 설계가
  나올 때까지 여러 사람에게 접근을 허용하지 않는다.
- secret, Docker socket, 공유 storage credential을 컨테이너에 마운트하지 않는다.
  노트북의 MLflow 접근은 artifact proxy를 통한다.
- work directory는 저장소 밖에 owner UID 1000으로 유지한다. 사용자 데이터로서
  백업한다.
- 라이브러리 버전을 고정한다. 의존성 변경은 다른 이미지 변경처럼 검토한다.

## Exceptions

내부 MLflow SDK 경로는 인증되지 않는다 (`POL-0088` 참고). terminal은 단일 사용자를
위해 활성화 상태로 유지된다. 추가 검토 없이 비활성화하는 것은 허용된다.

## Verification

정적 렌더링 후 런타임 검사: 세션 없이 gateway 401, 토큰 없이 서버 403, route를 통한
kernel 시작과 WebSocket, 토큰을 받지 못한 realm user의 거부.

## Review Cadence

이미지나 라이브러리 변경, 인증 변경, 신규 사용자, JupyterHub 결정 시 검토한다.

## Traceability

- [Guide](../guides/0089-jupyterlab.md) (`GDE-0089`)
- [Runbook](../runbooks/0089-jupyterlab.md) (`RUN-0089`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Image Dockerfile](../../../infra/11-laboratory/jupyterlab/Dockerfile) and [derived version projection](../../../infra/tech-stack.versions.json)
- [JupyterLab Compose source](../../../infra/11-laboratory/jupyterlab/docker-compose.yml)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
</content>
