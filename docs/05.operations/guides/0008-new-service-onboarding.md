---
title: "New Service Onboarding Guide"
version: "1.3.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "operations"
artifact_id: "GDE-0008"
parent_ids:
- "RUN-0009"
created: "2026-06-04"
---


# New Service Onboarding Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

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
5. public env/secret schema와 secret-file reference를 추가한다. 민감값은 Docker Secrets/OpenBao 참조로 주입한다. seed의 `env_file`은 비밀이 아닌 설정 예제이며 credential 전달 방식으로 확대하지 않는다.
6. service Guide에 `implementation_services` mapping을 반드시 두어 exact Compose path와 service 이름을 연결하고 Policy/Runbook, service README, 필요 Spec/Task를 함께 갱신한다. operations catalog가 이 binding과 global join을 검증하므로 병렬 registry/checker를 만들지 않는다.
7. 새 bounded change 계약이 필요하면 `docs/99.templates/templates/specs/spec.template.md`에서 시작해 Registry가 허용하는 `docs/03.specs/####-<slug>/spec.md`를 만들고, 같은 package의 `plan.md`와 `tasks/tsk-####-<slug>.md`에 계획과 실행 증거를 둔다. 서비스별 steady-state 구현·운영 계약은 service README와 Stage 05 Guide/Policy/Runbook이 소유하며, 임의의 `service.md`는 만들지 않는다.

복사한 seed는 아직 `infra/` 운영 계약을 충족하지 않는다. 현재 예제에는 infra
공통 template 참조와 profile이 없고, sample network·host port·리소스 필드도
별도 정의다. root 편입 전에 [공통 template](../../../infra/common-optimizations.yml),
[예외 Policy](../policies/0001-common-optimizations-template-exceptions.md),
[network Policy](../policies/0077-ip-address-management.md),
[profile Policy](../policies/0078-compose-profile-vocabulary.md)에 맞게 조정한다.
`deploy.resources`만 보고 공통 검사에서 요구하는 `cpus`/`mem_limit`까지
충족했다고 보지 않는다. 예제의 `service.md`는 sample 전용이며 infra의 운영
권위를 대신하지 않는다. package 위치는 현재 티어 책임으로 정하고, 디렉터리
이동이나 profile 추가를 activation 승인으로 해석하지 않는다.

### Common Pitfalls

- Floating tag(`latest`, `stable`) 사용 — 반드시 태그나 digest를 핀한다.
- root 사용자 실행 또는 불필요한 capability 유지 — 최소 권한 원칙을 지킨다.
- `docker-compose.yml`에 secret 값을 직접 작성 — 참조 메커니즘만 사용한다.

### Common Checks

- [RUN-0086](../runbooks/0086-dependency-version-management.md#static-configuration-validation)의 승인된 공개 입력으로 구성 검증을 수행한다. 전체 private 모델을 출력하지 않는다.
- 승인된 기동 뒤에는 선택한 daemon의 health와 초기화 작업의 종료 결과, 인증된 기능을 구분해 확인한다. `start_period` 경과는 healthy 보장이 아니다.
- 원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix)) — 서비스를 `infra/`에 편입할 때 contract가 동기화 상태를 유지한다.

### Runbook Handoff

release/tag 준비는 [RUN-0009](../runbooks/0009-release-management.md)를 따른다.
실제 배포·중단·rollback·data recovery는 추가한 서비스의 Runbook이 소유한다.
기존 데이터나 승인된 복구 경계가 불명확하면 @buenhyden에게 전달한다.

### Traceability

- 상위 문서: [Release Management Runbook](../runbooks/0009-release-management.md) (`RUN-0009`)
- 과거 구현 근거이며 현재 실행 권한이 아님: [Workspace Revalidation Outcome](../../98.archive/completed/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md) (`SPEC-0097`)
- 같은 번호 `0008`의 Policy/Runbook은 없다.

## Related Documents

- Compose/Dockerfile 선언이 runtime pin을 소유하고 [파생 이미지 projection](../../../infra/tech-stack.versions.json)은 Compose-image drift를 검사한다.

- [Operations index](../README.md)
- [Spec contract template](../../99.templates/templates/specs/spec.template.md)
- [Reference service seed](../../../examples/sample-web-service/README.md)
