---
title: "New Service Onboarding Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0008"
parent_ids:
- "RUN-0009"
created: "2026-06-04"
---


# New Service Onboarding Guide

> 새 컨테이너 서비스를 워크스페이스 표준에 맞게 추가하는 방법을 설명한다.

## Usage

### Overview

이 가이드는 새 컨테이너 서비스를 `hy-home.docker`에 추가할 때 참조한다.
복사 가능한 시드(`examples/sample-web-service/`)와 bounded-change Spec 템플릿
(`docs/99.templates/templates/specs/spec.template.md`)을 사용해, 보안 하드닝·이미지 핀·
healthcheck 표준을 처음부터 갖춘 서비스를 만든다.

### Usage Type

`onboarding`

### Target Audience

- Operator
- Developer
- Contributor
- AI Agent

### Purpose

독자가 표준 하드닝과 Compose 규약을 누락 없이 적용한 새 서비스를 정의하고,
구현·운영 계약을 canonical service README와 Stage 05 subject에 연결하며 필요한
bounded change를 유효한 Spec Package로 기록할 수 있게 한다.

### Prerequisites

- Docker Engine과 Docker Compose v2 사용 가능 환경.
- `infra/image-tag-policy.exceptions.json`, Compose/Dockerfile runtime pin source,
  `infra/tech-stack.versions.json` derived Compose image projection의 역할 숙지.

### Step-by-step Instructions

1. `examples/sample-web-service/`를 새 서비스 디렉터리로 복사하고 구현 Compose/Dockerfile source를 확정한다.
2. 이름, base image pin 또는 digest, 포트, 네트워크, 볼륨을 서비스에 맞게 수정한다. Compose/Dockerfile 선언이 runtime pin authority이며 derived projection에는 Compose image만 동기화한다.
3. 하드닝 기본값을 유지한다: non-root 실행, `read_only: true` + `tmpfs`, `cap_drop: [ALL]`, `no-new-privileges:true`, 리소스 제한, healthcheck, 로그 회전.
4. root `docker-compose.yml` include, 각 service `profiles:`, 그리고 POL-0078 canonical profile membership을 함께 갱신한다. HOME 편입은 named profile만으로 정하지 않고 current consumer, persistence, recovery, resource evidence로 판단한다.
5. public env/secret schema와 secret-file reference를 추가한다. secret은 `env_file`/Docker secrets/OpenBao 참조로만 주입하고 plaintext value를 넣지 않는다.
6. service Guide에 optional `implementation_services` mapping으로 exact Compose path와 service 이름을 연결하고 Policy/Runbook, service README, 필요 Spec/Task를 함께 갱신한다. operations catalog가 이 binding과 global join을 검증하므로 병렬 registry/checker를 만들지 않는다.
7. 새 bounded change 계약이 필요하면 `docs/99.templates/templates/specs/spec.template.md`에서 시작해 Registry가 허용하는 `docs/03.specs/####-<slug>/spec.md`를 만들고, 같은 package의 `plan.md`와 `tasks/tsk-####-<slug>.md`에 계획과 실행 증거를 둔다. 서비스별 steady-state 구현·운영 계약은 service README와 Stage 05 Guide/Policy/Runbook이 소유하며, 임의의 `service.md`는 만들지 않는다.

### Common Pitfalls

- Floating tag(`latest`, `stable`) 사용 — 반드시 태그나 digest를 핀한다.
- root 사용자 실행 또는 불필요한 capability 유지 — 최소 권한 원칙을 지킨다.
- `docker-compose.yml`에 secret 값을 직접 작성 — 참조 메커니즘만 사용한다.

## Common Checks

- `docker compose config` — compose 정의가 오류 없이 파싱된다.
- `docker compose ps` — start period 이후 `healthy` 상태가 보고된다.
- `python3 scripts/validation/run-ci-gate.py --profile changed` — 서비스를 `infra/`에 편입할 때 contract가 동기화 상태를 유지한다.

## Runbook Handoff

반복 실행 배포·롤백·장애 대응 절차는 해당 서비스 도메인의
[recovery runbook](../runbooks/0009-release-management.md)을 따른다.

## Traceability

- Declared parent: [Release Management Runbook](../runbooks/0009-release-management.md) (`RUN-0009`)
- Governing authority: [Workspace Revalidation Outcome](../../98.archive/completed/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md) (`SPEC-0097`)
- Subject peers: none — `00-workspace/0008-new-service-onboarding` holds this document alone.

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides Compose-image drift verification.

- [Operations index](../README.md)
- [Spec contract template](../../99.templates/templates/specs/spec.template.md)
- [Reference service seed](../../../examples/sample-web-service/README.md)
